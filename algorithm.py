import math

def fcfs_schedule(procs):
    procs = sorted(procs, key=lambda p: (p.arrival, p.pid))
    time = 0.0
    gantt = []
    for p in procs:
        if time < p.arrival:
            gantt.append(("idle", time, p.arrival))
            time = p.arrival
        p.start = time
        p.finish = time + p.burst
        p.waiting = p.start - p.arrival
        p.turnaround = p.finish - p.arrival
        gantt.append((p.pid, p.start, p.finish))
        time = p.finish
    return gantt


def sjf_nonpreemptive(procs):
    procs = sorted(procs, key=lambda p: (p.arrival, p.burst, p.pid))
    time = 0.0
    gantt = []
    remaining = procs[:]
    done = []
    while remaining:
        available = [p for p in remaining if p.arrival <= time]
        if not available:
            next_arr = min(remaining, key=lambda p: p.arrival)
            gantt.append(("idle", time, next_arr.arrival))
            time = next_arr.arrival
            continue
        p = min(available, key=lambda x: (x.burst, x.arrival, x.pid))
        p.start = time
        p.finish = time + p.burst
        p.waiting = p.start - p.arrival
        p.turnaround = p.finish - p.arrival
        gantt.append((p.pid, p.start, p.finish))
        time = p.finish
        remaining.remove(p)
        done.append(p)
    return gantt


def srtf_preemptive(procs):
    time = 0.0
    gantt = []
    procs = sorted(procs, key=lambda p: (p.arrival, p.pid))
    n = len(procs)
    remaining = {p.pid: p for p in procs}
    last_pid = None
    finished_count = 0

    while finished_count < n:
        available = [p for p in remaining.values() if p.arrival <= time and p.remaining > 0]
        if not available:
            future = [p for p in remaining.values() if p.remaining > 0 and p.arrival > time]
            if not future:
                break
            nxt = min(future, key=lambda p: p.arrival)
            if last_pid != "idle":
                last_pid = "idle"
                gantt.append(("idle", time, nxt.arrival))
            time = nxt.arrival
            continue

        current = min(available, key=lambda x: (x.remaining, x.arrival, x.pid))
        if last_pid != current.pid:
            gantt.append((current.pid, time, time))
            last_pid = current.pid

        next_arrival_time = min([p.arrival for p in remaining.values() if p.arrival > time] + [math.inf])
        time_slice = min(current.remaining, next_arrival_time - time if next_arrival_time != math.inf else current.remaining)
        if time_slice <= 0:
            time += 1e-6
            continue

        current.remaining -= time_slice
        pid, gstart, gend = gantt[-1]
        gantt[-1] = (pid, gstart, gend + time_slice)

        if current.remaining <= 1e-9:
            current.finish = time + time_slice
            current.start = current.start if current.start is not None else gstart
            current.waiting = (current.finish - current.arrival - current.burst)
            current.turnaround = current.finish - current.arrival
            finished_count += 1
        time += time_slice

    merged = []
    for pid, s, e in gantt:
        if merged and merged[-1][0] == pid and abs(merged[-1][2] - s) < 1e-6:
            merged[-1] = (pid, merged[-1][1], e)
        else:
            merged.append((pid, s, e))
    return merged


def priority_nonpreemptive(procs):
    procs = sorted(procs, key=lambda p: (p.arrival, p.priority, p.pid))
    time = 0.0
    gantt = []
    remaining = procs[:]
    while remaining:
        available = [p for p in remaining if p.arrival <= time]
        if not available:
            nxt = min(remaining, key=lambda p: p.arrival)
            gantt.append(("idle", time, nxt.arrival))
            time = nxt.arrival
            continue
        p = min(available, key=lambda x: (x.priority, x.arrival, x.pid))
        p.start = time
        p.finish = time + p.burst
        p.waiting = p.start - p.arrival
        p.turnaround = p.finish - p.arrival
        gantt.append((p.pid, p.start, p.finish))
        time = p.finish
        remaining.remove(p)
    return gantt


def round_robin(procs, quantum):
    procs = sorted(procs, key=lambda p: (p.arrival, p.pid))
    time = 0.0
    q = []
    gantt = []
    arriving = procs[:]
    while arriving or q:
        while arriving and arriving[0].arrival <= time:
            q.append(arriving.pop(0))
        if not q:
            if arriving:
                nxt = arriving[0]
                gantt.append(("idle", time, nxt.arrival))
                time = nxt.arrival
                continue
            break
        p = q.pop(0)
        if p.start is None:
            p.start = time
        run = min(quantum, p.remaining)
        gantt.append((p.pid, time, time + run))
        p.remaining -= run
        time += run
        while arriving and arriving[0].arrival <= time:
            q.append(arriving.pop(0))
        if p.remaining > 1e-9:
            q.append(p)
        else:
            p.finish = time
            p.waiting = p.finish - p.arrival - p.burst
            p.turnaround = p.finish - p.arrival
    return gantt
