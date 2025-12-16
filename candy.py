import random
import streamlit as st

ROWS = 7
COLS = 7
CANDIES = ["🍒", "🍋", "🍇", "🍎", "🍬"]

st.set_page_config(page_title="Candy Crash Mini", page_icon="🍬")

# ---------- STATE ----------
if "board" not in st.session_state:
    st.session_state.board = [
        [random.choice(CANDIES) for _ in range(COLS)] for _ in range(ROWS)
    ]
if "first_click" not in st.session_state:
    st.session_state.first_click = None
if "score" not in st.session_state:
    st.session_state.score = 0

board = st.session_state.board

st.title("Candy Crash Mini (Match‑3 Demo)")
st.write("Click two **adjacent** candies to swap them. If they form a match, they will be crushed.")

st.write(f"**Score:** {st.session_state.score}")

# ---------- HELPERS ----------
def find_matches(b):
    matched = [[False] * COLS for _ in range(ROWS)]
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 2):
            if b[r][c] == b[r][c+1] == b[r][c+2]:
                matched[r][c] = matched[r][c+1] = matched[r][c+2] = True
    # vertical
    for c in range(COLS):
        for r in range(ROWS - 2):
            if b[r][c] == b[r+1][c] == b[r+2][c]:
                matched[r][c] = matched[r+1][c] = matched[r+2][c] = True
    return matched

def crush_and_fall():
    b = st.session_state.board
    matched = find_matches(b)
    crushed = 0
    changed = True
    while changed:
        changed = False
        # crush
        for r in range(ROWS):
            for c in range(COLS):
                if matched[r][c]:
                    b[r][c] = None
                    crushed += 1
                    changed = True
        # gravity
        for c in range(COLS):
            write_row = ROWS - 1
            for r in range(ROWS - 1, -1, -1):
                if b[r][c] is not None:
                    b[write_row][c] = b[r][c]
                    write_row -= 1
            for r in range(write_row, -1, -1):
                b[r][c] = random.choice(CANDIES)
        matched = find_matches(b)
    st.session_state.score += crushed

def handle_click(r, c):
    if st.session_state.first_click is None:
        st.session_state.first_click = (r, c)
    else:
        r1, c1 = st.session_state.first_click
        r2, c2 = r, c
        st.session_state.first_click = None

        # must be adjacent
        if abs(r1 - r2) + abs(c1 - c2) != 1:
            return

        b = st.session_state.board
        # swap
        b[r1][c1], b[r2][c2] = b[r2][c2], b[r1][c1]
        # check if any match formed
        if any(any(row) for row in find_matches(b)):
            crush_and_fall()
        else:
            # swap back if no match
            b[r1][c1], b[r2][c2] = b[r2][c2], b[r1][c1]

# ---------- DRAW GRID ----------
for r in range(ROWS):
    cols = st.columns(COLS)
    for c in range(COLS):
        label = board[r][c]
        if st.session_state.first_click == (r, c):
            label = "✅" + label
        if cols[c].button(label, key=f"{r}-{c}"):
            handle_click(r, c)

if st.button("🔁 Restart"):
    st.session_state.board = [
        [random.choice(CANDIES) for _ in range(COLS)] for _ in range(ROWS)
    ]
    st.session_state.score = 0
    st.session_state.first_click = None
