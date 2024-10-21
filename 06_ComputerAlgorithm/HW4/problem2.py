import sys

sys.setrecursionlimit(10 ** 6)
sys.set_int_max_str_digits(10000000)

def bfs(pos, target, disturb, path):
    queue = [[pos[0], pos[1], 0]]
    visited = [[False] * 51 for _ in range(51)]
    dx = [-1, 1, 0, 0]
    dy = [0, 0, 1, -1]
    visited[pos[0]][pos[1]] = True
    while queue:
        x, y, m = queue.pop(0)
        if ((x, y) in target):
            path.append([m, (x, y), pos])
        for i in range(4):
            if x + dx[i] >= 0 and x + dx[i] <= 50 and y + dy[i] >= 0 and y + dy[i] <= 50 and (
                    x + dx[i], y + dy[i]) not in disturb:
                if visited[x + dx[i]][y + dy[i]] == False:
                    queue.append([x + dx[i], y + dy[i], m + 1])
                    visited[x + dx[i]][y + dy[i]] = True


def solve():
    target = set()
    disturb = set()
    dist = 0
    b, c = map(int, sys.stdin.readline().split())
    x, y = map(int, sys.stdin.readline().split())
    agent = [(x, y) for _ in range(b)]
    to_path = []
    for _ in range(b):
        h_x, h_y = map(int, sys.stdin.readline().split())
        target.add((h_x, h_y))
    for _ in range(c):
        h_x, h_y = map(int, sys.stdin.readline().split())
        disturb.add((h_x, h_y))
    bfs((x, y), target, disturb, to_path)

    while target:

        to_path.sort()

        while to_path:
            if (to_path[0][1] in target and to_path[0][2] in agent):
                dist += to_path[0][0]
                target.remove(to_path[0][1])
                agent.append(to_path[0][1])
                bfs(to_path[0][1], target, disturb, to_path)
                #agent.remove(to_path[0][2])
                to_path.pop(0)
                break
            else:
                to_path.pop(0)

    return dist


print(solve())