import streamlit as st
import bridge

st.title("ZKTeco Bridge Control")

    st.write("Bridge started...")
    try:
        bridge.main()
        st.success("Bridge executed successfully!")
    except Exception as e:
        st.error(f"Error: {e}")

