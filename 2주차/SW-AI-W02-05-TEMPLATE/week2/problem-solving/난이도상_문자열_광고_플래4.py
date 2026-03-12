# 문자열 - 광고 (백준 플래4)
# 문제 링크: https://www.acmicpc.net/problem/1305
import sys


def build_pi(pattern):
    pi = [0] * len(pattern)
    matched = 0

    for i in range(1, len(pattern)):
        while matched > 0 and pattern[i] != pattern[matched]:
            matched = pi[matched - 1]

        if pattern[i] == pattern[matched]:
            matched += 1
            pi[i] = matched

    return pi


def main():
    length = int(sys.stdin.readline())
    slogan = sys.stdin.readline().strip()

    pi = build_pi(slogan)
    print(length - pi[-1])


if __name__ == "__main__":
    main()
