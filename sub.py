import streamlit as st
import random
import time

st.set_page_config(page_title="Mini Subway Surf", page_icon="🏃")

# --- Initialize state ---
if "player_lane" not in st.session_state:
    st.session_state.player_lane = 1   # 0 = left, 1 = middle, 2 = right
if "obstacles" not in st.session_state:
    st.session_state.obstacles = []    # list of lanes where obstacle is present
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

st.title("Mini Subway Surf (Streamlit)")
st.write("Use buttons to move between 3 lanes and avoid obstacles.")

# --- Controls ---
colL, colM, colR = st.columns(3)
with colL:
    if st.button("⬅ Left"):
        st.session_state.player_lane = max(0, st.session_state.player_lane - 1)
with colM:
    st.write("Lane:", st.session_state.player_lane + 1)
with colR:
    if st.button("Right ➡"):
        st.session_state.player_lane = min(2, st.session_state.player_lane + 1)

# Restart button
if st.button("Restart game"):
    st.session_state.player_lane = 1
    st.session_state.obstacles = []
    st.session_state.score = 0
    st.session_state.game_over = False

# --- Game tick function ---
def game_step():
    if st.session_state.game_over:
        return

    # Randomly spawn obstacle in a lane (0,1,2) or no obstacle
    if random.random() < 0.7:
        st.session_state.obstacles = [random.randint(0, 2)]
    else:
        st.session_state.obstacles = []

    # Check collision
    if st.session_state.player_lane in st.session_state.obstacles:
        st.session_state.game_over = True
    else:
        st.session_state.score += 1

# Run one step each page run
game_step()

# --- Display lanes ---
lane_symbols = []
for lane in range(3):
    if lane == st.session_state.player_lane and lane in st.session_state.obstacles:
        cell = "💥"   # collision
    elif lane == st.session_state.player_lane:
        cell = "🧍"
    elif lane in st.session_state.obstacles:
        cell = "🚧"
    else:
        cell = "▫️"
    lane_symbols.append(cell)

st.markdown(f"**Lanes:**  {lane_symbols[0]}   {lane_symbols[1]}   {lane_symbols[2]}")
st.write("Score:", st.session_state.score)

if st.session_state.game_over:
    st.error("Game Over! Press **Restart game** to play again.")
else:
    # Auto-refresh every 0.7s to simulate motion
    time.sleep(0.7)
    st.experimental_rerun()
