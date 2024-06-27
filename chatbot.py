import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

st.title("HugChat")
st.write("HugChat is a chatbot that can help you with your mental health.")

# Create a new instance of the HugChat class
with st.sidebar:
    st.title("Login Hugchat")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            sign = Login(email, password)
            cookies = sign.login()
            st.write("Logging in...")
            st.session_state.chatbot = hugchat.ChatBot(
                cookies=cookies.get_dict())
            st.success("Login successful!")
        except Exception as e:

            st.error("Invalid credentials. Please try again.")

# Initialize session state for messages if not already done
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def generate_response(prompt_input, chatbot):
    # Generate response from chatbot
    return chatbot.chat(prompt_input)

# User-provided prompt


chatbot_initialized = "chatbot" in st.session_state

prompt = st.chat_input(disabled=not chatbot_initialized)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt, st.session_state.chatbot)
                st.write(response)

                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message)
