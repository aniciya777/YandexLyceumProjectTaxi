filename = '1.txt'
BUILDINGS = '#'
BACKS = '.'
PARKING = '*'

with open(filename, 'r', encoding='utf-8') as f_in:
    arr = [list(s.strip()) for s in f_in.readlines()]
h = len(arr)
w = max(len(row) for row in arr)
for row in range(h):
    arr[row] += '.' * (w - len(arr[row]))
for row in range(h):
    for col in range(w):
        if arr[row][col] in BUILDINGS:
            if arr[row - 1][col] in BACKS:
                arr[row - 1][col] = PARKING
            elif arr[row + 1][col] in BACKS:
                arr[row + 1][col] = PARKING
            elif arr[row - 1][col - 1] in BACKS:
                arr[row - 1][col - 1] = PARKING
            elif arr[row + 1][col + 1] in BACKS:
                arr[row + 1][col + 1] = PARKING
with open(filename, 'w', encoding='utf-8') as f_out:
    f_out.write('\n'.join(''.join(row) for row in arr))
