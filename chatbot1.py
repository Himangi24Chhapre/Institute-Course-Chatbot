from openaikey import open_ai_key
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# --- Course Information Dictionary ---
course_data = {
    
    "M.Tech CAD/CAM": {"intake": "12", "fees": "₹62,500"},
    "M.Tech Computer Science & Engineering": {"intake": "30", "fees": "₹62,500"},
    "M.Tech Artificial Intelligence & Data Science": {"intake": "30", "fees": "₹62,500"},
    "M.Tech Automation & Robotics Engineering": {"intake": "30", "fees": "₹1,01,000"},
    "M.Tech Civil Engineering": {"intake": "30", "fees": "₹1,01,000"},
    "B.Tech Civil Engineering with Computer Application": {"intake": "60", "fees": "₹80,000"},
    "B.Tech Computer Science & Engineering": {"intake": "180", "fees": "₹80,000"},
    "B.Tech CSE (AI Specialization)": {"intake": "60", "fees": "₹80,000"},
    "B.Tech CSE (Blockchain Specialization)": {"intake": "60", "fees": "₹80,000"},
    "B.Tech Information Technology": {"intake": "60", "fees": "₹80,000"},
    "B.Tech Electrical and Power Engineering": {"intake": "60", "fees": "₹80,000"},
    "B.Tech Electronics & Communication Engineering": {"intake": "60", "fees": "₹80,000"},
    "B.Tech Logistics": {"intake": "60", "fees": "₹80,000"},
    "B.Tech Mechanical Engineering": {"intake": "60", "fees": "₹80,000"},
    "B.Tech (Lateral Entry)": {
        "intake": "60",
        "fees": "₹80,000",
        "branches": "Civil, CSE, CS-AI, ECE, EEE, IT, ME, Logistics"
    }
}

# --- Format Course Info for Chatbot ---
def format_course_info(data):
    formatted = ""
    for course, details in data.items():
        formatted += f"\n\n**{course}**\n"
        for key, value in details.items():
            formatted += f"- {key.capitalize()}: {value}\n"
    return formatted

course_info_text = format_course_info(course_data)

# --- LangChain Chat Model ---
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=open_ai_key)

# --- Streamlit UI ---
st.set_page_config(page_title="Institute Course Chatbot")
st.image('https://d3md8ar2i5icyz.cloudfront.net/wp-content/uploads/2022/11/logo_updated.svg')
st.title("🎓 Course Inquiry Chatbot")
st.info("Ask anything about our available computer and engineering courses!")

# --- Initialize Session State ---
if "messages" not in st.session_state:
    system_prompt = (
        "You are a helpful assistant for a computer training and engineering institute."
        "Here is the list of available courses with their details:\n"
        f"{course_info_text}\n"
        "Answer student questions based on this information only. Be concise and informative."
        "If the user asks to compare two courses, show a side-by-side comparison of intake, fees, and other available details."
    )
    st.session_state.messages = [SystemMessage(content=system_prompt)]

# --- Chat Input ---
user_input = st.text_input("Your Question", key="user_input")

# --- Course Comparison Logic ---
def compare_courses(course1, course2):
    if course1 not in course_data or course2 not in course_data:
        return "One or both courses not found. Please check the names."
    
    details1 = course_data[course1]
    details2 = course_data[course2]
    
    comparison = f"Comparison: {course1} vs {course2}\n"
    keys = set(details1.keys()).union(set(details2.keys()))
    
    for key in keys:
        val1 = details1.get(key, "N/A")
        val2 = details2.get(key, "N/A")
        comparison += f"- **{key.capitalize()}**: {course1} → {val1} | {course2} → {val2}\n"
    
    return comparison

# --- On User Submit ---
if user_input:
    # Check for comparison request
    if "compare" in user_input.lower():
        parts = user_input.lower().replace("compare", "").strip().split(" and ")
        if len(parts) == 2:
            course1 = parts[0].strip().title()
            course2 = parts[1].strip().title()
            comparison_result = compare_courses(course1, course2)
            st.markdown(comparison_result)
        else:
            st.warning("Please use format: Compare [Course 1] and [Course 2]")
    else:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Thinking..."):
            response = llm(st.session_state.messages)
        st.session_state.messages.append(response)

# --- Display Chat History ---
for msg in st.session_state.messages[1:]:
    if isinstance(msg, HumanMessage):
        st.markdown(f"**You:** {msg.content}")
    else:
        st.markdown(f"**Bot:** {msg.content}")
