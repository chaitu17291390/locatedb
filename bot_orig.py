import streamlit as st
from final_agent import run_agent


def write_message(role, content, save=True):
    """
    This is a helper function that saves a message to the
    session state and then writes a message to the UI
    """
    # Append to session state
    if save:
        st.session_state.messages.append({"role": role, "content": content})

    # Write to UI
    with st.chat_message(role):
        st.markdown(content)

st.set_page_config("Ebert", page_icon=":movie_camera:")

# Hide the Main Menu in the Streamlit Community Cloud app
hide_main_menu = """
    <style>
    #MainMenu {visibility: hidden;}
    </style>
    """
st.markdown(hide_main_menu, unsafe_allow_html=True)
# end::setup[]

# tag::session[]
# Set up Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm the Locates Chatbot!  How can I help you?"},
    ]
# end::session[]

# tag::submit[]
# Submit handler


def handle_submit(message):
    # Prepare chat history from session state
    chat_history = [(msg["role"], msg["content"]) for msg in st.session_state.messages if
                    msg["role"] == "user" or msg["role"] == "assistant"]

    # Handle the response
    with st.spinner('Thinking...'):
        response, updated_chat_history = run_agent(message, chat_history)

        # Update the session state with the new response
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Write the response to the chat
        write_message('assistant', response)


# end::submit[]


# tag::chat[]
# Display messages in Session State
for message in st.session_state.messages:
    write_message(message['role'], message['content'], save=False)

# Handle any user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    write_message('user', prompt)

    # Generate a response
    handle_submit(prompt)
# end::chat[]
