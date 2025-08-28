def compute_metrics_from_gantt(gantt, procs):
    info = {p.pid: p for p in procs}
    for block in gantt:
        pid, s, e = block
        if pid == "idle":
            continue
        p = info[pid]
        if p.start is None:
            p.start = s
        p.finish = e
    for p in procs:
        p.waiting = max(0.0, (p.finish - p.arrival - p.burst)) if p.finish is not None else 0.0
        p.turnaround = max(0.0, (p.finish - p.arrival)) if p.finish is not None else 0.0
