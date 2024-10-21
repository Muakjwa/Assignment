import sys

sys.setrecursionlimit(10 ** 6)
sys.set_int_max_str_digits(10000000)

n, m = map(int, sys.stdin.readline().split())

flow = [[0] * (n + 1) for _ in range(n + 1)]

for _ in range(m):
    a, b, c = map(int, sys.stdin.readline().split())
    flow[a][b] = c


def bfs(start, flow, bus):
    queue = [start]

    visited = [-1] * n
    visited[start] = start

    while queue:
        idx = queue.pop(0)
        for i in range(n):
            if visited[i] == -1 and flow[idx][i] - bus[idx][i] > 0:
                queue.append(i)
                visited[i] = idx
    return visited

def main():
    start = 0
    end = n - 1
    bus = [[0] * (n + 1) for _ in range(n + 1)]
    result = 0

    while True:
        parent = bfs(start, flow, bus)
        if parent[end] == -1:
            break

        min_val = 1e9

        idx = end
        while idx!= start:
            min_val = min(min_val, flow[parent[idx]][idx] - bus[parent[idx]][idx])
            idx = parent[idx]

        idx = end
        while idx!=start:
            bus[parent[idx]][idx] += min_val
            bus[idx][parent[idx]] -= min_val
            idx = parent[idx]

        result += min_val

    print(result)

main()