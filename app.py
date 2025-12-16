
st.set_page_config(page_title="Calculator", page_icon="🧮")

import streamlit as st

st.title("Calculator App")
st.write("My first Streamlit calculator 🚀")
import streamlit as st

st.title("Simple Calculator")

a = st.number_input("Enter first number", value=0.0)
b = st.number_input("Enter second number", value=0.0)

operation = st.selectbox(
    "Choose operation",
    ["Add", "Subtract", "Multiply", "Divide"]
)
import streamlit as st

st.title("Simple Calculator")

a = st.number_input("Enter first number", value=0.0)
b = st.number_input("Enter second number", value=0.0)

operation = st.selectbox(
    "Choose operation",
    ["Add", "Subtract", "Multiply", "Divide"]
)

if st.button("Calculate"):
    if operation == "Add":
        result = a + b
    elif operation == "Subtract":
        result = a - b
    elif operation == "Multiply":
        result = a * b
    elif operation == "Divide":
        if b == 0:
            st.error("Cannot divide by zero")
            result = None
        else:
            result = a / b

    if result is not None:
        st.success(f"Result: {result}")
      st.markdown("---")
st.caption("Made by Shadow using Streamlit")

