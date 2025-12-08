# include <bits/stdc++.h>
using namespace std;

int T, N, M, L, Type;
double mu;
vector<int> R;
vector<vector<int>> C;
vector<vector<vector<double>>> P;
vector<vector<double>> rs, rd, pp;
vector<double> costab;
vector<vector<double>> V;

inline void prop(const vector<double>& d, int a, vector<double>& nd) {
    fill(nd.begin(), nd.end(), 0.0);
    for (int i = 0; i < N; ++i) {
        double di = d[i];
        if (di <= 1e-15) continue;
        const auto& row = P[a][i];
        for (int j = 0; j < N; ++j) {
            nd[j] += di * row[j];
        }
    }
}

void precompute() {
    rs.assign(M, vector<double>(N));
    rd.assign(M, vector<double>(N));
    pp.assign(M, vector<double>(N));

    vector<double> delta(N);
    for (int s = 0; s < N; ++s) delta[s] = R[s] - mu;

    for (int a = 0; a < M; ++a) {
        for (int i = 0; i < N; ++i) {
            double s1 = 0.0, s2 = 0.0, s3 = 0.0;
            const auto& rowP = P[a][i];
            const auto& rowC = C[i];
            for (int j = 0; j < N; ++j) {
                double p = rowP[j];
                s1 += p * R[j];
                s2 += p * delta[j];
                s3 += p * rowC[j];
            }
            rs[a][i] = s1;
            rd[a][i] = s2;
            pp[a][i] = s3;
        }
    }

    if (L > 0) {
        costab.resize(T + 1);
        double f = 2.0 * M_PI / L;
        for (int t = 1; t <= T; ++t) costab[t] = cos(f * t);
    }
}

void compute_value_function() {
    V.assign(T + 2, vector<double>(N, 0.0));
    for (int t = T; t >= 1; --t) {
        for (int s = 0; s < N; ++s) {
            double best = -1e100;
            for (int a = 0; a < M; ++a) {
                double v = 0.0;
                const auto& rowP = P[a][s];
                for (int j = 0; j < N; ++j) {
                    v += rowP[j] * (R[j] + V[t + 1][j]);
                }
                if (v > best) best = v;
            }
            V[t][s] = best;
        }
    }
}

void read_input() {
    cin >> T >> N >> M >> L >> Type;
    R.resize(N);
    long long sum = 0;
    for (int i = 0; i < N; ++i) {
        cin >> R[i];
        sum += R[i];
    }
    mu = (double)sum / N;

    C.assign(N, vector<int>(N));
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j)
            cin >> C[i][j];

    P.assign(M, vector<vector<double>>(N, vector<double>(N)));
    for (int a = 0; a < M; ++a)
        for (int i = 0; i < N; ++i)
            for (int j = 0; j < N; ++j)
                cin >> P[a][i][j];

    precompute();
}

double score(const vector<int>& A) {
    vector<double> d(N, 0.0), nd(N, 0.0);
    d[0] = 1.0;
    double tot = 0.0;
    int pa = 0;

    for (int t = 1; t <= T; ++t) {
        int a = A[t - 1];

        double r = 0.0;
        if (L == 0) {
            const auto& ra = rs[a];
            for (int i = 0; i < N; ++i)
                if (d[i] > 0.0) r += d[i] * ra[i];
        } else {
            double c = costab[t], tmp = 0.0;
            const auto& rda = rd[a];
            for (int i = 0; i < N; ++i)
                if (d[i] > 0.0) tmp += d[i] * rda[i];
            r = mu + c * tmp;
        }

        double p = 0.0;
        if (Type == 1 && a != pa) {
            const auto& ppa = pp[a];
            for (int i = 0; i < N; ++i)
                if (d[i] > 0.0) p += d[i] * ppa[i];
        }

        tot += r - p;
        prop(d, a, nd);
        d.swap(nd);
        pa = a;
    }
    return tot;
}

vector<int> local_search(vector<int> A, int max_iter) {
    double bs = score(A);
    for (int iter = 0; iter < max_iter; ++iter) {
        bool improved = false;
        for (int t = 0; t < T && !improved; ++t) {
            int old_a = A[t];
            for (int a = 0; a < M; ++a) {
                if (a == old_a) continue;
                A[t] = a;
                double ns = score(A);
                if (ns > bs + 1e-9) {
                    bs = ns;
                    improved = true;
                    break;
                }
            }
            if (!improved) A[t] = old_a;
        }
        if (!improved) break;
    }
    return A;
}

vector<int> solve_greedy() {
    vector<int> ans(T);
    vector<double> d(N, 0.0), nd(N, 0.0);
    d[0] = 1.0;
    int pa = 0;

    for (int t = 1; t <= T; ++t) {
        double best = -1e100;
        int ba = 0;

        if (L == 0) {
            for (int a = 0; a < M; ++a) {
                double r = 0.0;
                const auto& ra = rs[a];
                for (int i = 0; i < N; ++i)
                    if (d[i] > 0.0) r += d[i] * ra[i];

                double p = 0.0;
                if (Type == 1 && a != pa) {
                    const auto& ppa = pp[a];
                    for (int i = 0; i < N; ++i)
                        if (d[i] > 0.0) p += d[i] * ppa[i];
                }
                double v = r - p;
                if (v > best) {
                    best = v;
                    ba = a;
                }
            }
        } else {
            double c = costab[t];
            for (int a = 0; a < M; ++a) {
                double tmp = 0.0;
                const auto& rda = rd[a];
                for (int i = 0; i < N; ++i)
                    if (d[i] > 0.0) tmp += d[i] * rda[i];
                double r = mu + c * tmp;

                double p = 0.0;
                if (Type == 1 && a != pa) {
                    const auto& ppa = pp[a];
                    for (int i = 0; i < N; ++i)
                        if (d[i] > 0.0) p += d[i] * ppa[i];
                }
                double v = r - p;
                if (v > best) {
                    best = v;
                    ba = a;
                }
            }
        }

        ans[t - 1] = ba;
        prop(d, ba, nd);
        d.swap(nd);
        pa = ba;
    }
    return ans;
}

vector<int> solve_value_greedy() {
    compute_value_function();
    vector<int> ans(T);
    vector<double> d(N, 0.0), nd(N, 0.0);
    d[0] = 1.0;

    for (int t = 1; t <= T; ++t) {
        double best = -1e100;
        int ba = 0;

        for (int a = 0; a < M; ++a) {
            double v = 0.0;
            for (int i = 0; i < N; ++i) {
                double di = d[i];
                if (di <= 0.0) continue;
                const auto& rowP = P[a][i];
                for (int j = 0; j < N; ++j) {
                    v += di * rowP[j] * (R[j] + V[t + 1][j]);
                }
            }
            if (v > best) {
                best = v;
                ba = a;
            }
        }

        ans[t - 1] = ba;
        prop(d, ba, nd);
        d.swap(nd);
    }
    return ans;
}

vector<int> beam_search_vf(int bw) {
    compute_value_function();
    vector<pair<double, pair<vector<double>, vector<int>>>> beam;

    vector<double> init_d(N, 0.0);
    init_d[0] = 1.0;
    beam.push_back({0.0, {init_d, {}}});

    vector<double> nd(N);

    for (int t = 1; t <= T; ++t) {
        vector<tuple<double, int, int>> cand;

        for (int bi = 0; bi < (int)beam.size(); ++bi) {
            auto& b = beam[bi];
            double bsc = b.first;
            auto& bd = b.second.first;

            for (int a = 0; a < M; ++a) {
                double r = 0.0;
                const auto& ra = rs[a];
                for (int i = 0; i < N; ++i)
                    if (bd[i] > 0.0) r += bd[i] * ra[i];

                prop(bd, a, nd);

                double future = 0.0;
                for (int j = 0; j < N; ++j)
                    future += nd[j] * V[t + 1][j];

                cand.push_back({bsc + r + future, bi, a});
            }
        }

        int keep = min((int)cand.size(), bw);
        partial_sort(
            cand.begin(),
            cand.begin() + keep,
            cand.end(),
            [](const auto& x, const auto& y) { return get<0>(x) > get<0>(y); }
        );

        vector<pair<double, pair<vector<double>, vector<int>>>> nbeam;
        nbeam.reserve(keep);

        for (int i = 0; i < keep; ++i) {
            double sc;
            int bi, a;
            tie(sc, bi, a) = cand[i];

            auto& b = beam[bi];
            auto& bd = b.second.first;
            auto& bact = b.second.second;

            double r = 0.0;
            const auto& ra = rs[a];
            for (int j = 0; j < N; ++j)
                if (bd[j] > 0.0) r += bd[j] * ra[j];

            vector<double> new_d(N);
            prop(bd, a, new_d);

            vector<int> new_act = bact;
            new_act.push_back(a);

            nbeam.push_back({b.first + r, {new_d, move(new_act)}});
        }

        beam.swap(nbeam);
    }

    double bs = -1e100;
    vector<int> best;
    for (auto& b : beam) {
        double s = score(b.second.second);
        if (s > bs) {
            bs = s;
            best = b.second.second;
        }
    }
    return best;
}

vector<int> solve_basic() {
    vector<int> best;
    double bs = -1e100;

    auto try_sol = [&](vector<int> r) {
        double s = score(r);
        if (s > bs) {
            bs = s;
            best = move(r);
        }
    };

    try_sol(solve_greedy());
    try_sol(solve_value_greedy());
    try_sol(beam_search_vf(2000));

    for (int a = 0; a < M; ++a) {
        vector<int> r(T, a);
        try_sol(r);
    }

    srand(42);
    for (int i = 0; i < 30; ++i) {
        vector<int> r(T);
        for (int t = 0; t < T; ++t) r[t] = rand() % M;
        r = local_search(r, 5);
        try_sol(r);
    }

    best = local_search(best, 20);
    return best;
}

struct Sol {
    vector<int> a;
    double s;
};

Sol greedy_softmax(double temp, unsigned int seed) {
    vector<int> ans(T);
    vector<double> d(N, 0.0), nd(N, 0.0);
    d[0] = 1.0;
    int pa = 0;
    double total = 0.0;

    srand(seed);
    vector<double> val(M), rarr(M), parr(M);

    for (int t = 1; t <= T; ++t) {
        double c = (L > 0 ? costab[t] : 0.0);
        double maxv = -1e100;

        for (int a = 0; a < M; ++a) {
            double r = 0.0;
            if (L == 0) {
                const auto& ra = rs[a];
                for (int i = 0; i < N; ++i)
                    if (d[i] > 0.0) r += d[i] * ra[i];
            } else {
                double tmp = 0.0;
                const auto& rda = rd[a];
                for (int i = 0; i < N; ++i)
                    if (d[i] > 0.0) tmp += d[i] * rda[i];
                r = mu + c * tmp;
            }

            double p = 0.0;
            if (Type == 1 && a != pa) {
                const auto& ppa = pp[a];
                for (int i = 0; i < N; ++i)
                    if (d[i] > 0.0) p += d[i] * ppa[i];
            }

            rarr[a] = r;
            parr[a] = p;
            double v = r - p;
            val[a] = v;
            if (v > maxv) maxv = v;
        }

        int chosen = 0;
        if (temp <= 0.0) {
            double best = maxv;
            for (int a = 0; a < M; ++a) {
                if (val[a] == best) {
                    chosen = a;
                    break;
                }
            }
        } else {
            double sumw = 0.0;
            for (int a = 0; a < M; ++a) {
                double w = exp((val[a] - maxv) / temp);
                val[a] = w;
                sumw += w;
            }
            double r = (double)rand() / RAND_MAX * sumw;
            double acc = 0.0;
            for (int a = 0; a < M; ++a) {
                acc += val[a];
                if (r <= acc) {
                    chosen = a;
                    break;
                }
            }
        }

        ans[t - 1] = chosen;
        total += rarr[chosen] - parr[chosen];
        prop(d, chosen, nd);
        d.swap(nd);
        pa = chosen;
    }
    return {move(ans), total};
}

vector<int> solve() {
    if (Type == 0 && L == 0 && T <= 50 && N <= 10 && M <= 20)
        return solve_basic();

    Sol best = greedy_softmax(0.0, 123456u);
    double temps[] = {3.0, 7.0, 15.0, 30.0};
    unsigned int seed = 1u;
    for (double tp : temps) {
        Sol cur = greedy_softmax(tp, seed++);
        if (cur.s > best.s) best = move(cur);
    }
    return best.a;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    if (T > 0) {
        auto ans = solve();
        cout << "[";
        for (int i = 0; i < T; ++i) {
            cout << ans[i];
            if (i + 1 < T) cout << ", ";
        }
        cout << "]\n";
    }
    return 0;
}
