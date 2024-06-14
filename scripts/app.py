import streamlit as st
from llm_chat_client import LLMChatClient

# Streamlit app configuration
st.set_page_config(page_icon="💬", layout="wide", page_title="LLM Quiz Chat")

# Model details
models = {
    "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google"},
    "llama2-70b-4096": {"name": "LLaMA2-70b-chat", "tokens": 4096, "developer": "Meta"},
    "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
}

# Initialize the LLMChatClient with the provided API key and model details
client = LLMChatClient(api_key=st.secrets["GROQ_API_KEY"], models=models)

# Initialize chat history and selected model in session state if not already set
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize previous conversations in session state if not already set
if 'previous_conversations' not in st.session_state:
    st.session_state['previous_conversations'] = {}

# Define the display_chat function to show chat messages
if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

# Layout for model selection and max_tokens slider
col1, col2 = st.columns(2)

# Model selection dropdown
with col1:
    model_option = st.selectbox(
        "Choose a model:",
        options=list(models.keys()),
        format_func=lambda x: client.get_model_details(x)["name"],
        index=4  # Default to mixtral
    )

# Detect model change and clear chat history if the model has changed
if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

# Get the maximum tokens allowed for the selected model
max_tokens_range = client.get_model_details(model_option)["tokens"]

# Slider to adjust max tokens dynamically based on the selected model
with col2:
    max_tokens = st.slider(
        "Max Tokens:",
        min_value=512,  # Minimum value to allow some flexibility
        max_value=max_tokens_range,
        # Default value or max allowed if less
        value=min(32768, max_tokens_range),
        step=512,
        help=f"Adjust the maximum number of tokens (words) for the model's response. Max for selected model: {max_tokens_range}"
    )

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Input field for user prompt
if prompt := st.chat_input("Enter your prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    # Fetch response from Groq API
    try:
        chat_completion = client.create_chat_completion(
            model=model_option,
            messages=[
                {
                    "role": m["role"],
                    "content": m["content"]
                }
                for m in st.session_state.messages
            ],
            max_tokens=max_tokens
        )

        # Use the generator function with st.write_stream
        with st.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = client.generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)
    except Exception as e:
        st.error(e, icon="🚨")

    # Append the full response to session_state.messages
    if isinstance(full_response, str):
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})
    else:
        # Handle the case where full_response is not a string
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": combined_response})
