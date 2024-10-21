INF = 10e9

n, e, k = map(int, input().split())

D_map = [[] for _ in range(n + 1)]
visited = [False] * (n + 1)
distance = [INF] * (n + 1)
police_list = set()

h = [(0, 1)]

for _ in range(e):
    a, b, w = map(int, input().split())
    D_map[a].append((w, b))

for _ in range(k):
    police = int(input())
    police_list.add(police)

while h:
    dis, node = h.pop(h.index(min(h)))
    if visited[node] == True:
        continue
    visited[node] = True
    distance[node] = min(dis, distance[node])
    for w, b in D_map[node]:
        if b not in police_list and w + dis < distance[b]:
            distance[b] = w + dis
            h.append((w + dis, b))

if distance[n] == INF:
    print(-1)
else:
    print(distance[n])