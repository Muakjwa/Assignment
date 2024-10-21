
N = int(input())

animal = list(map(int, input().split()))

tree = [[] for _ in range(N)]

for _ in range(N - 1):
    a, b = map(int, input().split())
    tree[a-1].append(b-1)

answer = 1

lst = [(tree[0],1,1)]

while(lst):
    val = lst.pop(0)

    for i, next in enumerate(val[0]):
        total = val[2]
        if animal[next] == 0:
            cal = val[1] +1
            total+=1
        else:
            cal = val[1]-1
        if cal > 0:
            lst.append((val[0][:i] + val[0][i+1:] + tree[next], cal, total))
            answer = max(answer, total)

print(answer)