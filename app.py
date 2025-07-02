import streamlit as st
import requests

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
        st.error("Please enter your OpenAI API key in the sidebar.")
    else:
        # Generate assistant response
        with st.chat_message("assistant"):
            try:
                # Prepare the API request
                headers = {
                    "Authorization": f"Bearer {openai_api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": "gpt-3.5-turbo",
                    "messages": st.session_state.messages
                }
                
                # Make the API call using requests
                with st.spinner("Thinking..."):
                    response = requests.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers=headers,
                        json=data,
                        timeout=30
                    )
                
                if response.status_code == 200:
                    # Extract and display response
                    response_data = response.json()
                    reply = response_data["choices"][0]["message"]["content"]
                    st.markdown(reply)
                    
                    # Add assistant response to session state
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                else:
                    # Handle API errors
                    try:
                        error_data = response.json()
                        error_message = error_data.get("error", {}).get("message", f"HTTP {response.status_code}")
                    except:
                        error_message = f"HTTP {response.status_code}"
                    st.error(f"API Error: {error_message}")
                
            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")
            except requests.exceptions.RequestException as e:
                st.error(f"Network error: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.error("Make sure your OpenAI API key is valid and you have sufficient credits.")
