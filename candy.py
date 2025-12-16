import random

ROWS = 7
COLS = 7
CANDIES = ["A", "B", "C", "D", "E"]  # different candy types

def create_board():
    board = [[random.choice(CANDIES) for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    for row in board:
        print(" ".join(row))
    print()

def find_matches(board):
    matched = [[False] * COLS for _ in range(ROWS)]

    # horizontal matches
    for r in range(ROWS):
        for c in range(COLS - 2):
            if board[r][c] == board[r][c+1] == board[r][c+2]:
                matched[r][c] = matched[r][c+1] = matched[r][c+2] = True

    # vertical matches
    for c in range(COLS):
        for r in range(ROWS - 2):
            if board[r][c] == board[r+1][c] == board[r+2][c]:
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
        for r in range(ROWS - 1, -1, -1):
            if board[r][c] is not None:
                board[write_row][c] = board[r][c]
                write_row -= 1
        # fill top with new candies
        for r in range(write_row, -1, -1):
            board[r][c] = random.choice(CANDIES)

def swap(board, r1, c1, r2, c2):
    board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]

def make_move(board, r1, c1, r2, c2):
    # swap and check if it creates a match, else swap back
    swap(board, r1, c1, r2, c2)
    matched = find_matches(board)
    if not any(True in row for row in matched):
        # invalid move, revert
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
    print("Initial board:")
    print_board(board)

    while True:
        print("Enter move as: r1 c1 r2 c2 (0-based indexes), or -1 to quit:")
        s = input().strip()
        if s.startswith("-1"):
            break
        try:
            r1, c1, r2, c2 = map(int, s.split())
            score = make_move(board, r1, c1, r2, c2)
            if score == 0:
                print("Invalid move (no match). Try again.")
            else:
                print(f"You crushed {score} candies!")
            print_board(board)
        except Exception as e:
            print("Invalid input, try again.", e)

if __name__ == "__main__":
    main()
