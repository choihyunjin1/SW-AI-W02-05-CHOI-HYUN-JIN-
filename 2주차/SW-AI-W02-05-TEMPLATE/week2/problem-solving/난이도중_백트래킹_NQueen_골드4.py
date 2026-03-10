n = int(input())
count = 0

col_used = [False] * n
diag1_used = [False] * (2 * n - 1)
diag2_used = [False] * (2 * n - 1)

def dfs(row):
    global count

    if row == n:
        count += 1
        return

    for col in range(n):
        d1 = row + col
        d2 = row - col + n - 1

        if col_used[col] or diag1_used[d1] or diag2_used[d2]:
            continue

        col_used[col] = True
        diag1_used[d1] = True
        diag2_used[d2] = True

        dfs(row + 1)

        col_used[col] = False
        diag1_used[d1] = False
        diag2_used[d2] = False

dfs(0)
print(count)