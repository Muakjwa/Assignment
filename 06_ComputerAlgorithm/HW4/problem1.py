import sys

sys.setrecursionlimit(10 ** 6)
sys.set_int_max_str_digits(10000000)

m = int(sys.stdin.readline())

blocks = list(map(int,sys.stdin.readline().split()))

blocks.sort()
result = 0
for i in range(2,m):
    result = max(result, abs(blocks[i]-blocks[i-2]))
print(result)