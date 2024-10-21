case = [[0] * 3 for _ in range(100005)]

N = int(input())

for i in range(N):
    if i == 0:
        case[i + 1][0] = 1
        case[i + 3][1] = 1
        case[i + 5][2] = 1
    else:
        for j, num in enumerate(case[i]):
            if j == 0 and num != 0:
                case[i + 3][1] += num
                case[i + 5][2] += num
            elif j == 1 and num != 0:
                case[i + 1][0] += num
                case[i + 5][2] += num
            elif j == 2 and num != 0:
                case[i + 1][0] += num
                case[i + 3][1] += num

output = sum(case[N])
if output == 0:
    print(-1)
else:
    print(output)