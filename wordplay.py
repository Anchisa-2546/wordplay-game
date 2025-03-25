import streamlit as st
import random
import time

# คำศัพท์ตัวอย่าง
word_list = {
    "PYTHON": "A popular programming language",
    "STREAMLIT": "A Python library for web apps",
    "COMPUTER": "An electronic device for processing data",
    "DEVELOPER": "A person who writes and maintains code",
    "ARTIFICIAL": "Relating to intelligence created by humans"
}

# ตั้งค่า session_state เพื่อเก็บค่าต่าง ๆ ในเกม
if "word" not in st.session_state:
    st.session_state.word, st.session_state.hint = random.choice(list(word_list.items()))
    st.session_state.shown_word = "_" * len(st.session_state.word)
    st.session_state.score = 0
    st.session_state.time_left = 60  # เวลาทาย 60 วินาที
    st.session_state.start_time = time.time()

# แสดงอินเทอร์เฟซเกม
st.title("🎯 WordPlay: เกมทายคำ")
st.write(f"**Hint:** {st.session_state.hint}")

# แสดงคำที่ต้องทาย
st.write(f"**Word:** {' '.join(st.session_state.shown_word)}")

# แสดงเวลาและคะแนน
elapsed_time = int(time.time() - st.session_state.start_time)
st.session_state.time_left = max(0, 60 - elapsed_time)
st.write(f"⏳ Time Left: {st.session_state.time_left} sec | 🏆 Score: {st.session_state.score}")

# รับคำตอบจากผู้ใช้
user_guess = st.text_input("Enter your guess:", "").upper()

if user_guess:
    if user_guess == st.session_state.word:
        st.success("✅ Correct! You earned 10 points!")
        st.session_state.score += 10
        st.session_state.word, st.session_state.hint = random.choice(list(word_list.items()))
        st.session_state.shown_word = "_" * len(st.session_state.word)
        st.session_state.start_time = time.time()
    else:
        st.error("❌ Incorrect! Try again.")

# เมื่อหมดเวลา
if st.session_state.time_left == 0:
    st.error("⏰ Time's up! Game Over.")
    st.write(f"**Your final score: {st.session_state.score} points**")
    st.stop()