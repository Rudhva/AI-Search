"""Terminal table comparing the search algorithms (not a required project file)."""
import argparse, json, os, statistics, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from uninformed import bfs, dfs, ucs, ids
from informed import greedy_best_first_search, a_star_search

with open(os.path.join(HERE, "map_data.json")) as f:
    DATA = json.load(f)
GRAPH, LOC = DATA["graph"], DATA["locations"]

ALGS = {
    "BFS": lambda s, t: bfs(GRAPH, s, t),
    "DFS": lambda s, t: dfs(GRAPH, s, t),
    "UCS": lambda s, t: ucs(GRAPH, s, t),
    "IDS": lambda s, t: ids(GRAPH, s, t),
    "Greedy": lambda s, t: greedy_best_first_search(GRAPH, s, t, LOC),
    "A*": lambda s, t: a_star_search(GRAPH, s, t, LOC),
}

def count(e):
    return e if isinstance(e, int) else len(e)

def table(headers, rows):
    w = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]
    line = "+" + "+".join("-" * (n + 2) for n in w) + "+"
    fmt = lambda r: "| " + " | ".join(str(x).rjust(n) if i else str(x).ljust(n)
                                      for i, (x, n) in enumerate(zip(r, w))) + " |"
    print("\n".join([line, fmt(headers), line, *map(fmt, rows), line]))

def one_pair(s, t, runs):
    rows = []
    for name, f in ALGS.items():
        t0 = time.perf_counter()
        for _ in range(runs):
            path, cost, ex = f(s, t)
        ms = (time.perf_counter() - t0) / runs * 1000
        rows.append([name, count(ex), f"{ms:.3f}", f"{cost:.2f}", len(path) - 1])
    print(f"\n{s}  ->  {t}   (runtime averaged over {runs} runs)")
    table(["Algorithm", "Nodes expanded", "Time (ms)", "Path cost", "Hops"], rows)

def all_pairs():
    pairs = [(a, b) for a in GRAPH for b in GRAPH if a != b]
    rows = []
    for name, f in ALGS.items():
        ex, costs = [], []
        t0 = time.perf_counter()
        for s, t in pairs:
            _, c, e = f(s, t)
            ex.append(count(e)); costs.append(c)
        ms = (time.perf_counter() - t0) / len(pairs) * 1000
        rows.append([name, f"{statistics.mean(ex):.1f}", max(ex), f"{ms:.3f}", f"{statistics.mean(costs):.1f}"])
    print(f"\nAveraged over all {len(pairs)} source/destination pairs")
    table(["Algorithm", "Avg expanded", "Max expanded", "Avg time (ms)", "Avg cost"], rows)

def pick(name):
    hits = [c for c in GRAPH if name.lower() in c.lower()]
    exact = [c for c in hits if c.lower() == name.lower()]
    if len(exact) == 1 or len(hits) == 1:
        return (exact or hits)[0]
    sys.exit(f"'{name}' matches {hits or 'nothing'}. Use --list to see city names.")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", nargs="?"); p.add_argument("dest", nargs="?")
    p.add_argument("--all", action="store_true", help="average over every city pair")
    p.add_argument("--list", action="store_true", help="list city names")
    p.add_argument("--runs", type=int, default=200, help="repeats for timing one pair")
    a = p.parse_args()
    if a.list:
        print("\n".join(sorted(GRAPH)))
    elif a.all:
        all_pairs()
    elif a.source and a.dest:
        one_pair(pick(a.source), pick(a.dest), a.runs)
    else:
        p.print_help()
