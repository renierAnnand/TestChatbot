import streamlit as st
import openai

st.title("💬 Chatbot")

# Sidebar for API key
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Say something"):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check if API key is provided
    if not openai_api_key:
        st.error("Please enter your OpenAI API key.")
    else:
        # Generate assistant response
        with st.chat_message("assistant"):
            try:
                # Set the API key (correct way for old OpenAI version)
                openai.api_key = openai_api_key
                
                # Create response
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages
                )
                
                # Extract and display response
                reply = response.choices[0].message.content
                st.markdown(reply)
                
                # Add assistant response to session state
                st.session_state.messages.append({"role": "assistant", "content": reply})
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.error("Make sure your OpenAI API key is valid and you have sufficient credits.")
