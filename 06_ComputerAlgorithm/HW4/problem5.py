import sys

sys.setrecursionlimit(10 ** 6)
sys.set_int_max_str_digits(10000000)

def solve():
    n, m = map(int, sys.stdin.readline().split())

    flow = [[0] * 2 * n for _ in range(2 * n)]
    capacity = [[0] * 2 * n for _ in range(2 * n)]
    mapping = [[] for _ in range(2 * n)]

    for i in range(n):
        mapping[i].append(i + n)
        mapping[i + n].append(i)
        capacity[i][i + n] = 1

    for _ in range(m):
        a, b = map(int, sys.stdin.readline().split())

        mapping[a + n].append(b)
        mapping[b].append(a + n)
        capacity[a + n][b] = 1

        mapping[b + n].append(a)
        mapping[a].append(b + n)
        capacity[b + n][a] = 1

    start = n
    end = n - 1
    answer = 0
    while True:
        prev = [-1] * (2 * n)
        queue = [start]
        while queue:
            here = queue.pop(0)
            if here == end:
                break
            for there in mapping[here]:
                if capacity[here][there] - flow[here][there] > 0 and prev[there] == -1:
                    prev[there] = here
                    queue.append(there)
        if prev[end] == -1:
            break

        here = end
        while here != start:
            flow[prev[here]][here] += 1
            flow[here][prev[here]] -= 1
            here = prev[here]
        answer += 1
    print(answer)


solve()