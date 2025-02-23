
import streamlit as st
import random
import pandas as pd
from io import BytesIO

# Define a dictionary of JavaScript, Python, HTML, and CSS questions, answers, and options
questions_data = [
    {"question": "Which keyword is used to declare a variable in JavaScript?", "A": "var", "B": "int", "C": "let", "D": "Both A and C", "answer": "D"},
    {"question": "What does CSS stand for?", "A": "Cascading Style Sheets", "B": "Creative Style Sheets", "C": "Computer Style Sheets", "D": "Colorful Style Sheets", "answer": "A"},
    {"question": "Which of the following is a valid way to create a function in Python?", "A": "def myFunction():", "B": "function myFunction()", "C": "create myFunction()", "D": "fn myFunction()", "answer": "A"},
    {"question": "What does HTML stand for?", "A": "Hyper Text Markup Language", "B": "Hyperlinks and Text Markup Language", "C": "Home Tool Markup Language", "D": "Hyperlinking Text Management Language", "answer": "A"},
    {"question": "Which of the following is a valid way to apply CSS styles?", "A": "Inline", "B": "Internal", "C": "External", "D": "All of the above", "answer": "D"},
    {"question": "Which of the following is a JavaScript framework?", "A": "Django", "B": "Flask", "C": "React", "D": "Laravel", "answer": "C"},
    {"question": "Which symbol is used for comments in Python?", "A": "//", "B": "<!-- -->", "C": "#", "D": "/* */", "answer": "C"},
    {"question": "Which HTML tag is used to create a hyperlink?", "A": "<link>", "B": "<a>", "C": "<href>", "D": "<hyper>", "answer": "B"},
    {"question": "What is the correct way to reference an external JavaScript file?", "A": "<script href='script.js'>", "B": "<script src='script.js'>", "C": "<js src='script.js'>", "D": "<javascript src='script.js'>", "answer": "B"},
    {"question": "Which CSS property is used to change text color?", "A": "text-style", "B": "color", "C": "font-color", "D": "text-color", "answer": "B"}
]

# Convert questions to a pandas DataFrame
questions_df = pd.DataFrame(questions_data)

# Initialize session state
if 'shuffled_questions' not in st.session_state:
    st.session_state.shuffled_questions = questions_df.sample(frac=1).reset_index(drop=True)  # Shuffle questions
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'selected_answer' not in st.session_state:
    st.session_state.selected_answer = None  # Track selected answer

# Get the current question **only if it exists**
if st.session_state.current_question < len(questions_df):
    current_row = st.session_state.shuffled_questions.iloc[st.session_state.current_question]
    
    # Display the current question and options
    st.write(f"**Question {st.session_state.current_question + 1} of {len(questions_df)}:**")
    st.write(current_row['question'])
    
    # Show answer choices as a radio button
    options = {key: current_row[key] for key in ['A', 'B', 'C', 'D']}
    user_answer = st.radio("Select an answer:", list(options.keys()), index=None, format_func=lambda x: f"{x}: {options[x]}")
    
    # Check the user's answer and update the score
    if st.button("Submit"):
        if user_answer:  # Ensure an option is selected
            if user_answer == current_row['answer']:
                st.session_state.score += 1
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. The correct answer is {current_row['answer']}.")
            
            # Move to the next question
            st.session_state.current_question += 1
            st.session_state.selected_answer = None  # Reset selection
            st.rerun()  # Refresh UI
        else:
            st.warning("⚠️ Please select an answer before submitting.")

# When all questions are answered
else:
    st.write("🎉 **Quiz Complete!**")
    st.write(f"Your final score: **{st.session_state.score} / {len(questions_df)}**")
    
    # Convert results to a CSV file
    result_df = pd.DataFrame({
        "Score": [st.session_state.score],
        "Total Questions": [len(questions_df)],
        "Percentage": [f"{(st.session_state.score / len(questions_df)) * 100:.2f}%"]
    })
    csv_buffer = BytesIO()
    result_df.to_csv(csv_buffer, index=False)
    st.download_button("Download Results", data=csv_buffer.getvalue(), file_name="quiz_results.csv", mime="text/csv")
    
    # Restart option
    if st.button("Restart Quiz"):
        st.session_state.shuffled_questions = questions_df.sample(frac=1).reset_index(drop=True)  # Reshuffle for new game
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.selected_answer = None
        st.rerun()
