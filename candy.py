import random

ROWS = 7
COLS = 7
CANDIES = ["A", "B", "C", "D", "E"]

def create_board():
    return [[random.choice(CANDIES) for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    for row in board:
        print(" ".join(cell if cell is not None else "." for cell in row))
    print()

def find_matches(board):
    matched = [[False] * COLS for _ in range(ROWS)]

    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 2):
            if board[r][c] is not None and \
               board[r][c] == board[r][c+1] == board[r][c+2]:
                matched[r][c] = matched[r][c+1] = matched[r][c+2] = True

    # vertical
    for c in range(COLS):
        for r in range(ROWS - 2):
            if board[r][c] is not None and \
               board[r][c] == board[r+1][c] == board[r+2][c]:
                matched[r][c] = matched[r+1][c] = matched[r+2][c] = True

    return matched

def crush_candies(board, matched):
    crushed = 0
    for r in range(ROWS):
        for c in range(COLS):
            if matched[r][c]:
                board[r][c] = None
                crushed += 1
    return crushed

def apply_gravity(board):
    for c in range(COLS):
        write_row = ROWS - 1
        # move candies down
        for r in range(ROWS - 1, -1, -1):
            if board[r][c] is not None:
                board[write_row][c] = board[r][c]
                write_row -= 1
        # fill empty cells at top
        for r in range(write_row, -1, -1):
            board[r][c] = random.choice(CANDIES)

def swap(board, r1, c1, r2, c2):
    board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]

def has_any_match(board):
    matched = find_matches(board)
    return any(any(row) for row in matched)

def make_move(board, r1, c1, r2, c2):
    # bounds + adjacency check
    if not (0 <= r1 < ROWS and 0 <= c1 < COLS and
            0 <= r2 < ROWS and 0 <= c2 < COLS):
        return 0
    if abs(r1 - r2) + abs(c1 - c2) != 1:
        return 0

    swap(board, r1, c1, r2, c2)

    matched = find_matches(board)
    if not any(any(row) for row in matched):
        # no match formed, revert
        swap(board, r1, c1, r2, c2)
        return 0

    total_crushed = 0
    while True:
        crushed = crush_candies(board, matched)
        if crushed == 0:
            break
        total_crushed += crushed
        apply_gravity(board)
        matched = find_matches(board)
    return total_crushed

def main():
    board = create_board()
    # optional: ensure starting board has at least one match
    if not has_any_match(board):
        board = create_board()

    print("Simple Candy Crush–style game")
    print("Board indices are 0 to 6 for rows and columns.")
    print("Enter move as: r1 c1 r2 c2 (adjacent cells). Type -1 to quit.\n")
    print_board(board)

    while True:
        s = input("Move (r1 c1 r2 c2) or -1: ").strip()
        if s.startswith("-1"):
            print("Bye!")
            break
        parts = s.split()
        if len(parts) != 4:
            print("Please enter exactly 4 numbers.")
            continue
        try:
            r1, c1, r2, c2 = map(int, parts)
        except ValueError:
            print("Invalid numbers, try again.")
            continue

        score = make_move(board, r1, c1, r2, c2)
        if score == 0:
            print("Invalid move (no match or not adjacent). Try again.\n")
        else:
            print(f"You crushed {score} candies!\n")
        print_board(board)

if __name__ == "__main__":
    main()
