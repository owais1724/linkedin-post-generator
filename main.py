import streamlit as st
import time
from few_shot import FewShotPosts
from post_generator import generate_post

# ----- PAGE CONFIG -----
st.set_page_config(page_title="LinkedIn Post Generator", page_icon="💼", layout="centered")

# ----- INIT SESSION STATE -----
if "history" not in st.session_state:
    st.session_state["history"] = []

if "show_history" not in st.session_state:
    st.session_state["show_history"] = False

# ----- OPTIONS -----
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]
tone_options = ["Professional", "Friendly", "Inspirational", "Funny"]

# ----- CUSTOM CSS -----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #0e0e1a;
        color: #f1f5f9;
        scroll-behavior: smooth;
    }

    /* Titles */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        color: #60a5fa;
        margin-bottom: 0.5rem;
        animation: fadeInDown 1s ease;
    }

    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #94a3b8;
        margin-bottom: 2rem;
        animation: fadeIn 1.4s ease;
    }

    /* Main Generate Button */
    .stButton > button {
        background: linear-gradient(to right, #6366f1, #3b82f6);
        color: white;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.6rem 2rem;
        border-radius: 12px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }

    .stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(to right, #3b82f6, #6366f1);
        box-shadow: 0 6px 18px rgba(99, 102, 241, 0.5);
        cursor: pointer;
    }

    /* Selectboxes */
    .stSelectbox > div:hover,
    .stSelectbox:hover {
        border-color: #60a5fa !important;
        background-color: rgba(96, 165, 250, 0.05) !important;
        transition: 0.3s ease;
    }

    /* Radio buttons */
    div[role="radiogroup"] > label:hover {
        background-color: rgba(96, 165, 250, 0.1);
        border-radius: 8px;
        transition: 0.2s ease;
    }

    /* Expanders (History / Others) */
    .streamlit-expanderHeader:hover {
        color: #60a5fa;
        background-color: rgba(96, 165, 250, 0.08);
        border-radius: 6px;
        transition: 0.2s ease;
    }

    /* Post Card */
    .post-card {
        background: rgba(255, 255, 255, 0.06);
        padding: 1.8rem;
        border-radius: 18px;
        margin-top: 1.5rem;
        margin-bottom: 1.2rem;
        backdrop-filter: blur(16px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: transform 0.2s ease;
    }

    .post-card:hover {
        transform: scale(1.01);
    }

    .post-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #e0e7ff;
        margin-bottom: 0.4rem;
    }

    .post-summary {
        font-size: 1.05rem;
        font-weight: 500;
        color: #cbd5e1;
        margin-bottom: 1rem;
    }

    .toggle-history {
        background: transparent;
        border: none;
        color: #60a5fa;
        font-weight: 500;
        margin-bottom: 1rem;
    }

    .toggle-history:hover {
        text-decoration: underline;
        color: #3b82f6;
    }

    /* Animations */
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }

    @keyframes fadeInDown {
        from {opacity: 0; transform: translateY(-20px);}
        to {opacity: 1; transform: translateY(0);}
    }
    </style>


""", unsafe_allow_html=True)

# ----- MAIN FUNCTION -----
def main():
    st.markdown("<div class='main-title'>📘 LinkedIn Post Generator</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Craft scroll-stopping, AI-written LinkedIn posts in seconds.</div>", unsafe_allow_html=True)

    fs = FewShotPosts()

    # --- INPUTS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_tag = st.selectbox("📌 Topic", options=fs.get_tags())
    with col2:
        selected_length = st.selectbox("📏 Length", options=length_options)
    with col3:
        selected_language = st.selectbox("🌐 Language", options=language_options)

    tone = st.radio("🎨 Tone of the Post", tone_options, horizontal=True)

    if st.button("🚀 Generate Post"):
        with st.spinner("✨ Thinking of something powerful..."):
            post, title, summary = generate_post(selected_length, selected_language, selected_tag, tone)
            time.sleep(1)

        st.session_state["history"].append({
            "tag": selected_tag,
            "length": selected_length,
            "language": selected_language,
            "tone": tone,
            "content": post,
            "title": title,
            "summary": summary
        })

        st.markdown("### ✅ Your Post Preview:")

        st.markdown(f"""
            <div class='post-card'>
                <div class='post-title'>{title}</div>
                <div class='post-summary'>{summary}</div>
                <div style="font-size: 1rem; line-height: 1.7; color: #f1f5f9;">{post}</div>
            </div>
        """, unsafe_allow_html=True)

        st.code(post, language='markdown')

    # --- TOGGLE HISTORY ---
    with st.sidebar:
        if st.button("📂 Show / Hide Post History", key="toggle"):
            st.session_state["show_history"] = not st.session_state["show_history"]

        if st.session_state["show_history"]:
            st.markdown("### 🕘 Post History")
            if len(st.session_state["history"]) == 0:
                st.info("No posts generated yet.")
            else:
                for i, entry in enumerate(reversed(st.session_state["history"][-5:])):
                    with st.expander(f"📌 {entry['tag']} ({entry['tone']})"):
                        st.markdown(f"**Title:** {entry['title']}")
                        st.markdown(f"**Summary:** {entry['summary']}")
                        st.markdown(entry['content'])

# ----- MAIN CALL -----
if __name__ == "__main__":
    main()






