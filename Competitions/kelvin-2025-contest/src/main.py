#!/usr/bin/env python3
import sys
import math
from typing import List, Optional

# ==========================================
# 1. Data Structure Definitions
# ==========================================

class Config:
    def __init__(self):
        self.T: int = 0  # Total duration (minutes)
        self.N: int = 0  # Number of states
        self.M: int = 0  # Number of sound effects (actions)
        self.L: int = 0  # Wandering cycle period (0 = Static)
        self.Type: int = 0  # 0 = No Penalty, 1 = Matrix Penalty


class ProblemData:
    def __init__(self):
        self.cfg = Config()

        # Initial base rewards R_initial(s)
        self.initial_rewards: List[int] = []

        # System average reward centroid (mu), calculated during input
        self.mu: float = 0.0

        # Switching Penalty Matrix C_{i,j}
        # Dimensions: [N][N] - Cost of switching from state i to j
        self.penalty_matrix: List[List[int]] = []

        # Transition Matrices P^(a)
        # Dimensions: [M][N][N] - P(from_state -> to_state) given Action
        self.transition_matrices: List[List[List[float]]] = []

        # --- Precomputed helpers for fast greedy ---
        # reward_static[a][i] = sum_j P^a[i][j] * R_initial[j]
        self.reward_static: List[List[float]] = []
        # reward_delta[a][i] = sum_j P^a[i][j] * (R_initial[j] - mu)
        self.reward_delta: List[List[float]] = []
        # precomputed_penalty[a][i] = sum_j P^a[i][j] * C[i][j]
        self.precomputed_penalty: List[List[float]] = []


# ==========================================
# 2. Logic Helpers (Handles Basic/Ult. Cases)
# ==========================================

def get_reward(data: ProblemData, state: int, t: int) -> float:
    """
    Basic helper for DP / debugging.
    R(s,t) according to the Time-Variant Reward System.
    """
    if data.cfg.L == 0:
        return float(data.initial_rewards[state])

    r_init = data.initial_rewards[state]
    cosine_term = math.cos((2 * math.pi * t) / data.cfg.L)
    return data.mu + (r_init - data.mu) * cosine_term


def get_penalty(data: ProblemData, prev_state: int, curr_state: int,
                prev_action: int, curr_action: int) -> int:
    """
    Switching penalty when we *know* states.
    Not used in the fast greedy (we work in expectation there),
    but kept for completeness / potential debugging.
    """
    if prev_action == curr_action:
        return 0
    if data.cfg.Type == 0:
        return 0
    return data.penalty_matrix[prev_state][curr_state]


def propagate(data: ProblemData, dist: List[float], action: int) -> List[float]:
    """
    Propagate state distribution using P^a:
    next_dist[j] = sum_i dist[i] * P^a[i][j]
    """
    N = data.cfg.N
    P = data.transition_matrices[action]
    next_dist = [0.0] * N
    for i in range(N):
        d_i = dist[i]
        if d_i == 0.0:
            continue
        row_P = P[i]
        for j in range(N):
            next_dist[j] += d_i * row_P[j]
    return next_dist


# ==========================================
# 3. Input Parsing + Precomputation
# ==========================================

def precompute_helpers(data: ProblemData) -> None:
    """
    Precompute per-action contributions so that during solving
    we only do O(M*N) work per step, plus one propagate (O(N^2)).
    """
    N = data.cfg.N
    M = data.cfg.M

    R = data.initial_rewards
    mu = data.mu
    C = data.penalty_matrix
    P_all = data.transition_matrices

    # Prepare output arrays
    reward_static: List[List[float]] = [[0.0] * N for _ in range(M)]
    reward_delta: List[List[float]] = [[0.0] * N for _ in range(M)]
    pre_penalty: List[List[float]] = [[0.0] * N for _ in range(M)]

    # delta[s] = R_initial[s] - mu
    delta = [r - mu for r in R]

    for a in range(M):
        P = P_all[a]
        rs_a = reward_static[a]
        rd_a = reward_delta[a]
        pp_a = pre_penalty[a]
        for i in range(N):
            row_P = P[i]
            row_C = C[i]
            rs = 0.0
            rd = 0.0
            pc = 0.0
            # Inner loop over "to" state j
            for j in range(N):
                pij = row_P[j]
                if pij == 0.0:
                    continue
                rs += pij * R[j]
                rd += pij * delta[j]
                pc += pij * row_C[j]
            rs_a[i] = rs
            rd_a[i] = rd
            pp_a[i] = pc

    data.reward_static = reward_static
    data.reward_delta = reward_delta
    data.precomputed_penalty = pre_penalty


def read_input() -> Optional[ProblemData]:
    """
    Reads all data from stdin adhering to the competition Input Format.
    """
    try:
        tokens = sys.stdin.read().split()
        if not tokens:
            return None

        it = iter(tokens)
        data = ProblemData()

        # Header
        data.cfg.T = int(next(it))
        data.cfg.N = int(next(it))
        data.cfg.M = int(next(it))
        data.cfg.L = int(next(it))
        data.cfg.Type = int(next(it))

        N = data.cfg.N
        M = data.cfg.M

        # Base rewards
        data.initial_rewards = [int(next(it)) for _ in range(N)]
        data.mu = sum(data.initial_rewards) / float(N) if N > 0 else 0.0

        # Penalty matrix (always present, may be all zeros if Type=0)
        penalty_matrix: List[List[int]] = []
        for _ in range(N):
            row = [int(next(it)) for _ in range(N)]
            penalty_matrix.append(row)
        data.penalty_matrix = penalty_matrix

        # Transition matrices: M blocks of N x N doubles
        transition_matrices: List[List[List[float]]] = []
        for _a in range(M):
            mat: List[List[float]] = []
            for _i in range(N):
                row = [float(next(it)) for _ in range(N)]
                mat.append(row)
            transition_matrices.append(mat)
        data.transition_matrices = transition_matrices

        # Precompute fast helpers (only if we actually have data)
        if data.cfg.T > 0 and N > 0 and M > 0:
            precompute_helpers(data)

        return data

    except StopIteration:
        return None


# ==========================================
# 4. Optional: Sequence Scorer (for local testing)
# ==========================================

def score_sequence(data: ProblemData, actions: List[int]) -> float:
    """
    Compute expected score J(A) exactly for a fixed action sequence.
    Useful when you test locally, not used by grader.
    """
    T = data.cfg.T
    N = data.cfg.N

    dist = [0.0] * N
    dist[0] = 1.0
    total = 0.0
    prev_action = 0

    for t in range(1, T + 1):
        a = actions[t - 1]

        # Next distribution
        next_dist = propagate(data, dist, a)

        # Expected reward at time t
        if data.cfg.L == 0:
            # Static rewards
            r_exp = 0.0
            for s in range(N):
                if next_dist[s] != 0.0:
                    r_exp += next_dist[s] * data.initial_rewards[s]
        else:
            r_exp = 0.0
            c = math.cos((2 * math.pi * t) / data.cfg.L)
            for s in range(N):
                if next_dist[s] != 0.0:
                    r_s = data.initial_rewards[s]
                    r_exp += next_dist[s] * (data.mu + (r_s - data.mu) * c)

        # Expected penalty
        p_exp = 0.0
        if data.cfg.Type == 1 and a != prev_action:
            C = data.penalty_matrix
            P = data.transition_matrices[a]
            for i in range(N):
                di = dist[i]
                if di == 0.0:
                    continue
                row_P = P[i]
                row_C = C[i]
                for j in range(N):
                    pij = row_P[j]
                    if pij == 0.0:
                        continue
                    p_exp += di * pij * row_C[j]

        total += r_exp - p_exp
        dist = next_dist
        prev_action = a

    return total


# ==========================================
# 5. Core Algorithms
# ==========================================

def solve_basic_dp(data: ProblemData) -> List[int]:
    """
    Exact DP for very small basic cases:
      - Type = 0 (no penalty)
      - L = 0 (static reward)
      - T <= 50, N <= 10, M <= 20
    This branch is just to squeeze a bit more score on small tests.
    """
    T = data.cfg.T
    N = data.cfg.N
    M = data.cfg.M

    # V_next[j] = value from time t+1 if we are in state j
    V_next = [0.0] * N
    V_curr = [0.0] * N
    best_action = [[0] * N for _ in range(T + 1)]

    for t in range(T, 0, -1):
        for i in range(N):
            best_val = -1e100
            best_a = 0
            for a in range(M):
                P_row = data.transition_matrices[a][i]
                val = 0.0
                for j in range(N):
                    pj = P_row[j]
                    if pj == 0.0:
                        continue
                    rj = data.initial_rewards[j]
                    val += pj * (rj + V_next[j])
                if val > best_val:
                    best_val = val
                    best_a = a
            V_curr[i] = best_val
            best_action[t][i] = best_a
        V_next, V_curr = V_curr, V_next

    # Use approximate belief-tracking to convert state-based policy
    # into a pure open-loop sequence.
    actions = [0] * T
    dist = [0.0] * N
    dist[0] = 1.0

    for t in range(1, T + 1):
        # choose state with highest probability
        best_state = 0
        max_p = dist[0]
        for i in range(1, N):
            if dist[i] > max_p:
                max_p = dist[i]
                best_state = i
        a = best_action[t][best_state]
        actions[t - 1] = a
        dist = propagate(data, dist, a)

    return actions


def solve_fast_greedy(data: ProblemData) -> List[int]:
    """
    Main workhorse: O(T * (M*N + N^2)) greedy in expectation.
    Uses precomputed reward / penalty contributions.
    """
    T = data.cfg.T
    N = data.cfg.N
    M = data.cfg.M
    L = data.cfg.L
    Type = data.cfg.Type

    actions = [0] * T

    # initial distribution: S0 = 0
    dist = [0.0] * N
    dist[0] = 1.0
    prev_action = 0

    reward_static = data.reward_static
    reward_delta = data.reward_delta
    pre_penalty = data.precomputed_penalty

    # Precompute cos table for time-variant rewards if needed
    cos_table = None
    if L > 0:
        cos_table = [0.0] * (T + 1)
        for t in range(1, T + 1):
            cos_table[t] = math.cos((2 * math.pi * t) / L)

    for t in range(1, T + 1):
        best_val = -1e100
        best_a = 0

        if L == 0:
            # Static rewards: use reward_static
            for a in range(M):
                rs_a = reward_static[a]
                # expected reward
                r_exp = 0.0
                for i in range(N):
                    di = dist[i]
                    if di != 0.0:
                        r_exp += di * rs_a[i]

                # expected penalty
                if Type == 1 and a != prev_action:
                    pp_a = pre_penalty[a]
                    p_exp = 0.0
                    for i in range(N):
                        di = dist[i]
                        if di != 0.0:
                            p_exp += di * pp_a[i]
                else:
                    p_exp = 0.0

                val = r_exp - p_exp
                if val > best_val:
                    best_val = val
                    best_a = a
        else:
            # Time-variant rewards
            c = cos_table[t]
            for a in range(M):
                rd_a = reward_delta[a]
                tmp = 0.0
                for i in range(N):
                    di = dist[i]
                    if di != 0.0:
                        tmp += di * rd_a[i]
                r_exp = data.mu + c * tmp

                if Type == 1 and a != prev_action:
                    pp_a = pre_penalty[a]
                    p_exp = 0.0
                    for i in range(N):
                        di = dist[i]
                        if di != 0.0:
                            p_exp += di * pp_a[i]
                else:
                    p_exp = 0.0

                val = r_exp - p_exp
                if val > best_val:
                    best_val = val
                    best_a = a

        actions[t - 1] = best_a
        # update distribution only for the chosen action
        dist = propagate(data, dist, best_a)
        prev_action = best_a

    return actions


def solve(data: ProblemData) -> List[int]:
    """
    High-level solver entry.
    Chooses algorithm based on problem size and mode.
    """
    T = data.cfg.T
    N = data.cfg.N
    M = data.cfg.M
    Type = data.cfg.Type
    L = data.cfg.L

    # Small basic case: exact DP for a tiny extra gain.
    if Type == 0 and L == 0 and T <= 50 and N <= 10 and M <= 20:
        return solve_basic_dp(data)

    # Otherwise: fast greedy with precomputation.
    return solve_fast_greedy(data)


# ==========================================
# 6. Output Formatting
# ==========================================

def print_output(actions: List[int]) -> None:
    """
    Formats the output strictly as [a1, a2, ..., aT].
    """
    sys.stdout.write("[" + ", ".join(map(str, actions)) + "]\n")


# ==========================================
# Main Entry Point
# ==========================================

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    data = read_input()
    if data is not None and data.cfg.T > 0:
        ans = solve(data)
        print_output(ans)
