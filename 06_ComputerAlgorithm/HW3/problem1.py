N = int(input())

result = [(1,0)]
past = set()
possible = 0

while(result):
    a, b = result.pop(0)
    if a == N:
        print(b)
        possible = 1
        break
    if a*2 not in past and a*2 < 100000:
        result.append((a*2, b+1))
        past.add(a*2)
    if a//3 !=0 and a//3 not in past:
        result.append((a//3, b+1))
        past.add(a//3)
    r = int(str(a)[::-1])
    if  r not in past and r < 100000:
        result.append((r, b+1))
        past.add(r)

if possible == 0:
    print(-1)