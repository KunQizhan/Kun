import numpy as np
import random
from maze_env import FLMPEnv, generate_flmp
MOVES = {0: (0, -1), 2: (0, 1), 1: (1, 0), 3: (-1, 0)}
# 90 degrees clockwise
PERP = {0: 1, 1: 2, 2: 3, 3: 0}

class StochasticFLMPEnv(FLMPEnv):
    def __init__(self, desc, portals=None, render_mode="ansi", p=0.9):
        super().__init__(desc, portals, render_mode)
        # the possibility of successful movement
        self.p = p

    # input is the origin thought action, and outpout is actual action
    def step(self, action):
        if random.random() < self.p:
            actual_action = action
        else:
            actual_action = PERP[action]
        
        # record the movement direction
        dr, dc = MOVES[actual_action]

        # get the on-time status and store the new expet position
        row, col = self.to_row_col(self.s)
        new_row, new_col = row + dr, col + dc

        # no wall and no exceeding boundage for both of row and column
        if (0 <= new_row < self.nrow and 0 <= new_col < self.ncol and self.desc[new_row, new_col] != "W"):
            row, col = new_row, new_col
        # move to that position
        next_state = self.to_s(row, col)

        # wormhole
        if next_state in self._portal_states:
            next_state = self._portal_states[next_state]

        # get the updated status of position, and know what type for this position
        r, c = self.to_row_col(next_state)
        cell = self.desc[r, c]

        # Touch the goal and stop
        if cell == "G":
            reward = 1.0
            terminated = True
        else:
            reward = 0.0
            terminated = False
        # update on-time status
        self.s = next_state
        # return the position status, and if I touch the goal, and if we should terminate
        return next_state, reward, terminated, False, {}

# Markov Descision Process
class MazeMDP:
    def __init__(self, env, gamma=0.99):
        self.env = env
        # Focus on long-term goals, but don't completely ignore the future.
        self.gamma = gamma
        # number of rows
        self.nrow = env.nrow
        # number of columns
        self.ncol = env.ncol
        self.n_states = self.nrow * self.ncol
        self.n_actions = 4

        # how likely are you to succeed
        self.V = np.zeros(self.n_states, dtype=float)
        # direction for each location
        self.policy = np.zeros(self.n_states, dtype=int)

        # make a dic and estimate every postion with different direction' result
        self.transitions = {}
        self._build_transition_model()
    # estimate all posibility for all position
    def _build_transition_model(self):
        for state in range(self.n_states):
            row, col = self.env.to_row_col(state)
            cell = self.env.desc[row, col]
            # touch the goal and stay
            if cell == "G":
                for action in range(self.n_actions):
                    self.transitions[(state, action)] = [(state, 1.0, 0.0)]
                continue

            # for the other position, think about intended postion, but there is a p, so also cosinder about the vertical situation
            for action in range(self.n_actions):
                # intended
                intended_dr, intended_dc = MOVES[action]
                # vertical
                perp_action = PERP[action]
                perp_dr, perp_dc = MOVES[perp_action]
                # rocord separetely
                candidates = [(intended_dr, intended_dc, self.env.p), (perp_dr, perp_dc, 1.0 - self.env.p)]
                # maybe the actual movement is the same direction, since there maybe a wall or both direction is wall
                stats = {}
                for dr, dc, prob in candidates:
                    next_state, reward = self._one_step(state, dr, dc)
                    if next_state not in stats:
                        stats[next_state] = [0.0, reward]
                    stats[next_state][0] += prob
                # use list comprehension and save
                self.transitions[(state, action)] = [(s_next, prob, rew) for s_next, (prob, rew) in stats.items()]

    # calculate the every step's result
    def _one_step(self, state, dr, dc):
        # save the current position and get the next position
        row, col = self.env.to_row_col(state)
        new_row, new_col = row + dr, col + dc

        # wall or exceeding the boundary, stay origin position, otherwise get into the next position
        if (0 <= new_row < self.nrow and 0 <= new_col < self.ncol and self.env.desc[new_row, new_col] != "W"):
            row, col = new_row, new_col
            next_state = self.env.to_s(row, col)
        else:
            next_state = state

        # wormhole
        if next_state in self.env._portal_states:
            next_state = self.env._portal_states[next_state]
            row, col = self.env.to_row_col(next_state)

        # get the type of that position, and get reward seperately
        cell = self.env.desc[row, col]
        # goal
        if cell == "G":
            reward = 100.0
        # drop into the hole, and give a larger punishment than common point
        elif cell == "H":
            reward = -5.0
        else:
            reward = -1.0
        return next_state, reward

    def value_iteration(self, theta=0.01, max_iterations=1000, verbose=False):
        for it in range(max_iterations):
            # reocrd the chage of coverngence
            delta = 0.0
            # go thourgh every position, and get the cordinates and type
            for state in range(self.n_states):
                row, col = self.env.to_row_col(state)
                cell = self.env.desc[row, col]
                # jump if goal
                if cell == "G":
                    continue
                # save the old value, to compare with the new value to see the change
                old_v = self.V[state]
                # to store every reward for each direction at a point
                q_values = []
                # calculate every reward for each direction at a point
                for action in range(self.n_actions):
                    q = 0.0
                    # consider about two possible direction for a position
                    for next_state, prob, reward in self.transitions[(state, action)]:
                        # calculate the expected reward
                        q += prob * (reward + self.gamma * self.V[next_state])
                    q_values.append(q)

                # use the best Q and record what direction 
                best_q = max(q_values)
                best_a = int(np.argmax(q_values))
                self.V[state] = best_q
                self.policy[state] = best_a
                # to get know about if finish estimating all reward and position and direction
                delta = max(delta, abs(old_v - best_q))
            # print the status for each 50 times
            if verbose and (it + 1) % 50 == 0:
                print(f"iter {it+1}, delta = {delta:.6f}")
            # let user know which time convergence
            if delta < theta:
                if verbose:
                    print(f"value iteration converged in {it+1} iterations")
                return it + 1
        # if interation bigger than 1000 times, stop
        if verbose:
            print("reached max_iterations without full convergence")
        return max_iterations

    def execute_policy(self, max_steps=2000, verbose=False):
        # inital the environment and prepare for the step and dropped holes
        state, _ = self.env.reset()
        steps = 0
        holes = 0
        # run and until 2000 steps
        while steps < max_steps:
            # search for the strattegy for that position
            action = self.policy[state]
            # we only want to know the next position to get, and if we touch the goal
            next_state, reward, terminated, stop, extraInfo = self.env.step(action)
            r, c = self.env.to_row_col(next_state)
            cell = self.env.desc[r, c]
            # drop into the hole
            if cell == "H":
                holes += 1

            steps += 1
            state = next_state
            # print what steps, which direction, coordinates, type
            if verbose:
                print(f"step {steps}: action={action}, pos=({r},{c}), cell={cell}")
            # only possible if touch goal
            if terminated:
                break
        performance = steps * holes
        return {"steps": steps, "holes_fallen": holes, "performance": performance}

# 50*50 maze, posibility for generation a wall is 0.15, hole is 0.15, portal  number is 15, seed to make sure the same situation for task2-4
def run_experiment(size=50, wall_prob=0.15, hole_prob=0.15, n_portals=15, p=0.9, seed=None, gamma=0.99, max_steps=2000, verbose=False):
    # genertae a maze
    desc, portals = generate_flmp(size=size, wall_prob=wall_prob, hole_prob=hole_prob, n_portals=n_portals, seed=seed)
    # create a stochastic environment
    env = StochasticFLMPEnv(desc=desc, portals=portals, p=p)
    # create a MDP  model
    mdp = MazeMDP(env, gamma=gamma)
    # get the best strategy
    mdp.value_iteration(verbose=verbose)
    # execute the policy
    result = mdp.execute_policy(max_steps=max_steps, verbose=verbose)
    # release the resources
    env.close()
    return result

if __name__ == "__main__":
    # Task 1
    result = run_experiment(size=50, wall_prob=0.15, hole_prob=0.15, n_portals=15, p=0.9, seed=42, verbose=True)
    print("=" * 60)
    print(f"Steps={result['steps']}, Holes={result['holes_fallen']}, P={result['performance']}")

    # TASK 2
    for n_portals in [5, 10, 15, 20, 25, 30]:
        result = run_experiment(size=50, wall_prob=0.15, hole_prob=0.15, n_portals=n_portals, p=0.9, seed=42)
        print(f"Portals={n_portals:2d}: Steps={result['steps']:4d}, Holes={result['holes_fallen']:3d}, P={result['performance']:6d}")
    print("=" * 60)
    print()
    
    # TASK 3
    for hole_prob in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]:
        result = run_experiment(size=50, wall_prob=0.15, hole_prob=hole_prob, n_portals=15, p=0.9, seed=42)
        print(f"Hole_prob={hole_prob:.2f}: Steps={result['steps']:4d}, Holes={result['holes_fallen']:3d}, P={result['performance']:6d}")
    print("=" * 60)
    print()
    
    # TASK 4
    for p_value in [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]:
        result = run_experiment(size=50, wall_prob=0.15, hole_prob=0.15, n_portals=15, p=p_value, seed=42)
        print(f"p={p_value:.1f}: Steps={result['steps']:4d}, Holes={result['holes_fallen']:3d}, P={result['performance']:6d}")
    print("=" * 60)
    print()
