INF = 10e9

N, M = map(int, input().split())

FW_map = [[INF] * (N + 1) for _ in range(N + 1)]

for i in range(1, N + 1):
    FW_map[i][i] = 0

for i in range(M):
    a, b, t = map(int, input().split())
    FW_map[a][b] = t
    FW_map[b][a] = t

K = int(input())
disease = set(map(int, input().split()))
safe = int(input())

for i in range(N + 1):
    for j in range(N + 1):
        for k in range(N + 1):
            if k not in disease:
                FW_map[i][j] = min(FW_map[i][j], FW_map[i][k] + FW_map[k][j])

need_time = 0

for i in range(N + 1):
    if i not in disease and FW_map[i][safe] != INF:
        need_time += FW_map[i][safe]

print(need_time)