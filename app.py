import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Alkhorayef Group HR Assistant",
    page_icon="👥",
    layout="wide"
)

# Custom CSS for HR theme
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 2rem;
}
.main-header h1 {
    color: white;
    margin: 0;
    font-size: 2rem;
}
.main-header p {
    color: #e0e7ff;
    margin: 0.5rem 0 0 0;
}
.quick-question-btn {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.75rem;
    margin: 0.25rem 0;
    transition: all 0.2s;
    cursor: pointer;
}
.quick-question-btn:hover {
    background-color: #eff6ff;
    border-color: #3b82f6;
}
.hr-info-box {
    background-color: #eff6ff;
    border-left: 4px solid #3b82f6;
    padding: 1rem;
    border-radius: 0 8px 8px 0;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>👥 Alkhorayef Group HR Assistant</h1>
    <p>Your guide to company policies, benefits, and procedures</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for API key and quick questions
with st.sidebar:
    st.header("⚙️ Settings")
    openai_api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key to start chatting")
    
    st.header("🚀 Quick Questions")
    
    quick_questions = {
        "💰 Salary & Benefits": "Tell me about the compensation and benefits structure at Alkhorayef Group",
        "📅 Leave Policies": "What are the different types of leave available and their policies?",
        "🏆 Performance & Promotion": "How does the performance management and promotion system work?",
        "📚 Training Programs": "What training and development opportunities are available?",
        "👥 Employee Relations": "What should I know about workplace conduct and employee relations policies?",
        "📋 End-of-Service": "How is end-of-service indemnity calculated and what are the entitlements?",
        "⏰ Working Hours": "What are the official working hours and overtime policies?",
        "🏥 Medical Benefits": "Tell me about medical insurance and health benefits",
        "🏠 Housing & Transportation": "What allowances are provided for housing and transportation?",
        "👩 Women's Policies": "What are the specific policies for female employees?"
    }
    
    for emoji_title, question in quick_questions.items():
        if st.button(emoji_title, use_container_width=True):
            st.session_state.selected_question = question

    # Info box
    st.markdown("""
    <div class="hr-info-box">
        <h4>📚 About This Assistant</h4>
        <p>I'm trained on Alkhorayef Group's official HR policies and procedures. For official documentation or complex cases, please contact HR directly.</p>
    </div>
    """, unsafe_allow_html=True)

# HR System Prompt
HR_SYSTEM_PROMPT = """You are an expert HR assistant for Alkhorayef Group of Companies in Saudi Arabia. You specialize in helping employees understand company HR policies, benefits, procedures, and regulations.

IMPORTANT GUIDELINES:
1. Always provide helpful, accurate information about HR policies
2. Reference specific policy sections when possible (e.g., "According to Section 2.5 of the HR manual...")
3. Be professional but friendly and approachable
4. If you don't know something specific, ask for clarification or suggest they contact HR directly
5. Always comply with Saudi Labor Law and company regulations
6. For sensitive matters (disciplinary, termination, etc.), be tactful and suggest proper channels

FOCUS AREAS:
- Compensation & Benefits policies (grades, salaries, allowances, bonuses)
- Leave policies and holidays (annual, sick, maternity, pilgrimage, etc.)
- Performance management and appraisals (PMR system, ratings, feedback)
- Training and development programs (Masarat, career paths, succession planning)
- Job grades, promotions, and salary structures
- Employee relations and conduct policies
- Disciplinary procedures and violations
- Company organizational structure
- Safety and health policies
- Women's work policies and regulations
- Termination and end-of-service benefits
- Working hours and overtime policies
- Medical insurance and benefits

KEY COMPANY INFO:
- Alkhorayef Group operates in Saudi Arabia
- Has multiple companies: Alkhorayef Group Company, Commercial, Industries, Saudi Parts Center, Petroleum, Printing Solutions
- Follows Saudi Labor Law and Islamic principles
- Uses grade system from A (lowest) to O (highest): Semi-professionals (A-D), Professionals (E-G), Supervisors (H-I), Managers (J-K), Directors (L-M), Executives (N-O)
- 48-hour work week (36 hours during Ramadan for Muslims)
- Performance management uses 5-point scale: 1-Does not meet expectations, 2-Meets some expectations, 3-Meets expectations, 4-Exceeds expectations, 5-Exceptional

Always end responses with a helpful follow-up question or offer to clarify anything else about HR policies."""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": """👋 Hello! I'm your Alkhorayef Group HR Assistant. I can help you with questions about our HR policies, benefits, procedures, and more.

**I can help you with:**
• 💰 Compensation & Benefits (salaries, allowances, bonuses)
• 📊 Performance Management (evaluations, promotions, career development)
• 📅 Leave Policies & Holidays (annual leave, sick leave, special leave)
• 🎯 Training & Development (programs, career paths, skill development)
• 📋 Job Grades & Salary Structure (grade levels A-O, pay scales)
• 🏢 Company Policies (conduct, procedures, regulations)
• ⚖️ Disciplinary Procedures (violations, sanctions, grievances)
• 👥 Employee Relations (workplace conduct, communications)

**Quick Examples:**
• "What is the annual leave policy for professionals?"
• "How is end-of-service indemnity calculated?"
• "What are the working hours during Ramadan?"
• "Tell me about the performance bonus system"
• "How do promotions work in the company?"

Use the quick questions in the sidebar or ask me anything about our HR policies! What would you like to know?"""
        }
    ]

# Handle selected question from sidebar
if hasattr(st.session_state, 'selected_question'):
    st.session_state.messages.append({"role": "user", "content": st.session_state.selected_question})
    delattr(st.session_state, 'selected_question')
    st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about HR policies, benefits, leave, performance, etc..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check if API key is provided
    if not openai_api_key:
        with st.chat_message("assistant"):
            st.error("Please enter your OpenAI API key in the sidebar to continue.")
    else:
        # Generate assistant response
        with st.chat_message("assistant"):
            try:
                # Prepare messages for API call
                api_messages = [
                    {"role": "system", "content": HR_SYSTEM_PROMPT}
                ]
                
                # Add conversation history
                for msg in st.session_state.messages:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})
                
                # Prepare the API request
                headers = {
                    "Authorization": f"Bearer {openai_api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": "gpt-3.5-turbo",
                    "messages": api_messages,
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
                
                # Make the API call
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
                    
                    # Add assistant response to chat history
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

# Footer with additional information
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **📞 Need Direct Help?**
    - Contact HR Department
    - Submit through Oracle system
    - Speak with your line manager
    """)

with col2:
    st.markdown("""
    **📋 Key Policies**
    - Employee Handbook
    - Code of Conduct  
    - Safety Guidelines
    """)

with col3:
    st.markdown("""
    **🔒 Privacy Notice**
    - HR conversations are confidential
    - This assistant provides general guidance
    - For official matters, contact HR directly
    """)

st.markdown("""
<div style="text-align: center; color: #64748b; margin-top: 2rem;">
    <p>🏢 Alkhorayef Group HR Assistant • Powered by AI • For internal use only</p>
</div>
""", unsafe_allow_html=True)
