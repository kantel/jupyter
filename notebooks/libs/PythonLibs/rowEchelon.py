def rowMod (M, i, j, x):
    M[i] = [a + x * b for a, b in zip(M[i], M[j])]

def rowEchelon (M):
    row, col = 0, 0
    rows, cols = len(M), len(M[0])
    while row < rows and col < cols:
        # try to find pivot element
        if M[row][col] == 0:
            for r in range(row + 1, rows):
                if M[r][col] != 0:
                    rowMod(M, row, r, 1)
                    break
        # no pivot element, skip column
        if M[row][col] == 0:
            col += 1
            continue
        # pivot element found, create zeros
        pivot = M[row][col]
        for r in range(row + 1, rows):
            if M[r][col] != 0:
                rowMod(M, r, row, -M[r][col] / pivot)
        # next row, next column
        row += 1
        col += 1
