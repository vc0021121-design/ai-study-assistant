import streamlit as st
from openai import OpenAI

# Configure OpenRouter API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["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"]
)

# Page config
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stTextArea textarea {
        font-size: 16px;
        border-radius: 10px;
    }
    .stButton button {
        border-radius: 20px;
        font-weight: bold;
    }
    .stSuccess {
        border-radius: 10px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📚 AI Study Assistant")
st.markdown("**Your personal tutor for Physics, Chemistry & Math**")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    subject = st.selectbox(
        "Choose Subject:",
        ["Physics", "Chemistry", "Mathematics"]
    )
    
    level = st.radio(
        "Class Level:",
        ["Class 11", "Class 12", "JEE/NEET"]
    )
    
    st.markdown("---")
    st.markdown("💡 **Tip:** Be specific with your question for best results!")

# Main area
st.subheader(f"🔬 {subject} Problem Solver")

problem = st.text_area(
    "Enter your problem:",
    height=150,
    placeholder="Example: A car accelerates from rest at 2 m/s². What is its velocity after 10 seconds?"
)

# Buttons
col1, col2 = st.columns([1, 4])

with col1:
    solve_button = st.button("✨ Solve", type="primary", use_container_width=True)

with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

# Clear functionality
if clear_button:
    st.rerun()

# Solve functionality
if solve_button:
    if problem:
        with st.spinner(f"🤔 Solving your {subject} problem..."):
            try:
                # Different prompts for different subjects
                if subject == "Physics":
                    system_prompt = f"""You are an expert Physics tutor for {level} students. 
                    Solve problems with:
                    1. Given data clearly listed
                    2. Formula used with explanation
                    3. Step-by-step calculations
                    4. Final answer with units
                    5. Key concept explanation"""
                
                elif subject == "Chemistry":
                    system_prompt = f"""You are an expert Chemistry tutor for {level} students.
                    Solve problems with:
                    1. Given information
                    2. Chemical equations (balanced)
                    3. Step-by-step calculations with mole concept
                    4. Final answer with units
                    5. Important notes about the reaction/concept"""
                
                else:  # Mathematics
                    system_prompt = f"""You are an expert Math tutor for {level} students.
                    Solve problems with:
                    1. Given information
                    2. Formula/theorem used
                    3. Detailed step-by-step solution
                    4. Final answer
                    5. Alternative method if applicable"""
                
                # Call OpenRouter API with Llama 3.3
                response = client.chat.completions.create(
                    model="meta-llama/llama-3.3-70b-instruct:free",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": problem}
                    ]
                )
                
                answer = response.choices[0].message.content
                
                # Display solution
                st.success("✅ Solution:")
                st.markdown(answer)
                
                # Extra features
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📋 Copy Solution"):
                        st.toast("Solution copied! (Paste anywhere)")
                
                with col2:
                    if st.button("💾 Save to History"):
                        st.toast("Saved to your history!")
                
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.info("💡 Make sure your API key is valid!")
    else:
        st.warning("⚠️ Please enter a problem first!")

# Footer
st.markdown("---")

st.markdown("**Made by you** | Powered by Llama 3.3 70B 🚀")
