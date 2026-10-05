import json, sys
R = r"C:\Users\TimLane\unfayr-ref"
ev = {e["id"]: e for e in json.load(open(R + r"\evals\evals.json", encoding="utf-8"))["evals"]}
g = json.load(open(R + r"\evals\benchmarks\2026-10-ref-v1.grades.json", encoding="utf-8"))["runs"]

for it in g:
    for k, v in g[it].items():
        sid = int(k.split("-")[0])
        assert len(v) == len(ev[sid]["assertions"]), (it, k)

def tally(runs):
    t = {"all": [0, 0], "beh": [0, 0], "file": [0, 0]}
    for sid, grades in runs:
        for a, (r, _) in zip(ev[sid]["assertions"], grades):
            kind = "file" if a.startswith("[file]") else "beh"
            for key in ("all", kind):
                t[key][1] += 1
                t[key][0] += r == "P"
    return t

def fmt(t):
    return {k: f"{p}/{n} ({100*p/n:.1f}%)" for k, (p, n) in t.items()}

out = {}
for arm in ("skill", "baseline"):
    it1 = [(s, g["iter1"][f"{s}-{arm}"]) for s in range(1, 8)]
    final = [(s, g["iter2"].get(f"{s}-{arm}", g["iter1"][f"{s}-{arm}"])) for s in range(1, 8)]
    out[arm] = {"iter1": fmt(tally(it1)), "final (iter1 S1-S5 + iter2 S6-S7)": fmt(tally(final))}
    out[arm]["iter2 only (S6,S7)"] = fmt(tally([(s, g["iter2"][f"{s}-{arm}"]) for s in (6, 7)]))
    out[arm]["iter1 S6,S7 only"] = fmt(tally([(s, g["iter1"][f"{s}-{arm}"]) for s in (6, 7)]))
print(json.dumps(out, indent=1))

# per scenario table
for it in ("iter1", "iter2"):
    for s in range(1, 8):
        row = []
        for arm in ("skill", "baseline"):
            k = f"{s}-{arm}"
            if k not in g[it]:
                continue
            t = tally([(s, g[it][k])])
            row.append(f"{arm}: all {t['all'][0]}/{t['all'][1]} beh {t['beh'][0]}/{t['beh'][1]} file {t['file'][0]}/{t['file'][1]}")
        if row:
            print(it, s, ev[s]["name"], " | ".join(row))

if len(sys.argv) > 1:  # emit per-assertion markdown
    lines = []
    for it in ("iter1", "iter2"):
        for s in range(1, 8):
            if f"{s}-skill" not in g[it]:
                continue
            lines.append(f"\n#### {it} · S{s} {ev[s]['name']}\n")
            lines.append("| # | Assertion | Ref | Evidence (Ref) | Baseline | Evidence (baseline) |")
            lines.append("|---|---|---|---|---|---|")
            for i, a in enumerate(ev[s]["assertions"]):
                sk = g[it][f"{s}-skill"][i]; bl = g[it][f"{s}-baseline"][i]
                esc = lambda x: x.replace("|", "\\|")
                lines.append(f"| {i+1} | {esc(a)} | {sk[0]} | {esc(sk[1])} | {bl[0]} | {esc(bl[1])} |")
    open(sys.argv[1], "w", encoding="utf-8").write("\n".join(lines) + "\n")
