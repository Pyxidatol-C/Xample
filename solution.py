# Prologin
# https://prologin.org/train/2018/qualification/crepes_parfaites
from cmath import exp
from math import log2, pi


def fft(X):
    N = len(X)
    if N == 1:
        return X
    even = fft(X[::2])
    odd = fft(X[1::2])
    T = [exp(-2j * pi * k / N) * odd[k] for k in range(N // 2)]
    return [even[k] + T[k] for k in range(N // 2)] + [even[k] - T[k] for k in range(N // 2)]


def ifft(X):
    N = len(X)
    if N == 1:
        return X
    even = ifft(X[::2])
    odd = ifft(X[1::2])
    T = [exp(2j * pi * k / N) * odd[k] for k in range(N // 2)]
    return [even[k] + T[k] for k in range(N // 2)] + [even[k] - T[k] for k in range(N // 2)]


L, n = map(int, input().split())
dirs = [tuple(map(int, input().split())) for _ in range(n)]
cur = 0
path = []
for t in range(L):
    cur = dirs[cur][bin(t).count('1') % 2]
    path.append(int(cur == 0))
path += [0] * L
path += [0] * (2 ** (int(log2(len(path))) + 1) - len(path))
prod = [round(abs(i) / len(path)) for i in ifft([x * x for x in fft(path)])]  # a * c
cnt = 0
for i, b in enumerate(path):
    if b:
        cnt += prod[2 * i] // 2
print(cnt)
