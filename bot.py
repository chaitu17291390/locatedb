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

# Add background image to the entire page
add_background_image = """
    <style>
    .stApp {
        background-image: url('https://adaptive-cards.s3.us-east-1.amazonaws.com/samsara1.png');  /* URL of your background image */
        background-size: cover;  /* Cover the entire screen */
        background-position: center;  /* Center the image */
        height: 100vh;  /* Ensure the image covers the entire viewport height */
        display: flex;
        flex-direction: column;
    }

    /* Make the background of the container with class 'st-emotion-cache-uhkwx6 ea3mdgi6' transparent */
    .st-emotion-cache-uhkwx6.ea3mdgi6 {
        background: transparent !important;  /* Set background to transparent */
        padding: 10px;  /* Optional: Adjust padding if needed */
        border-radius: 10px;  /* Optional: Add rounded corners */
        margin-top:40px;
    }

    /* Fixed height for the container with class 'st-emotion-cache-16i25t9 e1f1d6gn2' with a vertical scrollbar */
    .st-emotion-cache-16i25t9.e1f1d6gn2 {
        height: 50px;  /* Set a fixed height */
        /* Ensure the height does not increase */
        overflow-y: auto;  /* Add vertical scrollbar */
        padding: 10px;  /* Optional: Adjust padding if needed */
        border-radius: 10px;  /* Optional: Add rounded corners */
    }

    /* Decrease width of the container with class 'st-emotion-cache-1vxmjmh e1f1d6gn4' */

"""
st.markdown(add_background_image, unsafe_allow_html=True)

# Add border to the chat container
add_border_style = """
    <style>
    .st-emotion-cache-1n76uvr.e1f1d6gn2 {
        margin-top:60px;
        border: 2px solid #3498db;  /* Change the color and style of the border */
        border-radius: 10px;  /* Optional: Add rounded corners */
        padding: 15px;  /* Optional: Adjust padding if needed */
        background-color:white;
        width:50vw;
    }
    /* Remove the container with the class 'st-emotion-cache-qcqlej ea3mdgi1' */
    .st-emotion-cache-qcqlej.ea3mdgi1 {
        display: none !important;
    }
    </style>
"""
st.markdown(add_border_style, unsafe_allow_html=True)

# Set up Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm the Locates Chatbot!  How can I help you?"},
    ]


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


# Display messages in Session State
for message in st.session_state.messages:
    write_message(message['role'], message['content'], save=False)

# Handle any user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    write_message('user', prompt)

    # Generate a response
    handle_submit(prompt)
