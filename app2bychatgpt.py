import streamlit as st

# Streamlit app configuration
st.set_page_config(page_icon="💬", layout="wide", page_title="LLM Quiz Chat")

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'previous_conversations' not in st.session_state:
    st.session_state['previous_conversations'] = {}
if 'conversation_counter' not in st.session_state:
    st.session_state['conversation_counter'] = 1

# Function to display the chat messages
def display_chat():
    for message in st.session_state['messages']:
        avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# Function to start a new conversation
def new_conversation():
    conv_name = f"Conversation {st.session_state['conversation_counter']}"
    st.session_state['previous_conversations'][conv_name] = st.session_state['messages']
    st.session_state['messages'] = []
    st.session_state['conversation_counter'] += 1

# Sidebar for previous conversations
with st.sidebar:
    st.header("Previous Conversations")
    for conv_name, conv_msgs in st.session_state['previous_conversations'].items():
        if st.button(conv_name):
            st.session_state['messages'] = conv_msgs
            st.experimental_rerun()

    if st.button("New Conversation"):
        new_conversation()
        st.experimental_rerun()

# Main chat interface
st.title("ChatGPT UI with Streamlit")
st.write("Chat with the bot below:")

display_chat()

# Suggested prompts
st.write("Suggested Prompts:")
if st.button("Hello!"):
    prompt = "Hello!"
    st.session_state['messages'].append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    response = "Hi there! How can I help you today?"
    st.session_state['messages'].append({"role": "assistant", "content": response})

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response)

    st.experimental_rerun()
