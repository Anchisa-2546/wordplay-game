import streamlit as st
import time
import random

# คำศัพท์แต่ละหมวดหมู่
word_categories = {
    "ประเทศ": {
        "คำศัพท์": ["Thailand", "Japan", "France", "Brazil"],
        "คำใบ้": ["ประเทศในเอเชียตะวันออกเฉียงใต้", "ประเทศที่มีอนิเมะดัง", "เมืองหลวงคือปารีส", "ประเทศในอเมริกาใต้"]
    },
    "ผลไม้": {
        "คำศัพท์": ["Apple", "Banana", "Mango", "Orange"],
        "คำใบ้": ["ผลไม้สีเขียว-แดง", "ผลไม้สีเหลืองงอได้", "ผลไม้เมืองร้อนสีเหลือง", "ผลไม้ที่เป็นชื่อสี"]
    },
    "สัตว์": {
        "คำศัพท์": ["Tiger", "Elephant", "Rabbit", "Penguin"],
        "คำใบ้": ["เสือที่อยู่ในป่า", "สัตว์บกที่ตัวใหญ่ที่สุด", "สัตว์ที่กระโดดได้", "นกที่ว่ายน้ำเก่ง"]
    }
}

# ตั้งค่าค่าเริ่มต้น
if "score" not in st.session_state:
    st.session_state.score = 0
if "time_left" not in st.session_state:
    st.session_state.time_left = 60
if "game_running" not in st.session_state:
    st.session_state.game_running = False
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "ประเทศ"
if "word_to_guess" not in st.session_state:
    st.session_state.word_to_guess = ""
if "hint" not in st.session_state:
    st.session_state.hint = ""
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""
if "message" not in st.session_state:
    st.session_state.message = ""

# ฟังก์ชันเลือกคำใหม่
def select_new_word():
    category = st.session_state.selected_category
    index = random.randint(0, len(word_categories[category]["คำศัพท์"]) - 1)
    st.session_state.word_to_guess = word_categories[category]["คำศัพท์"][index]
    st.session_state.hint = word_categories[category]["คำใบ้"][index]
    st.session_state.start_time = time.time()
    st.session_state.user_answer = ""
    st.session_state.message = ""

# ฟังก์ชันเริ่มเกม
def start_game():
    st.session_state.score = 0
    st.session_state.game_running = True
    st.session_state.time_left = 60
    select_new_word()

# ฟังก์ชันรีเซตเกม
def reset_game():
    st.session_state.score = 0
    st.session_state.game_running = False
    st.session_state.message = ""
    st.session_state.word_to_guess = ""
    st.session_state.hint = ""
    st.session_state.time_left = 60
    st.session_state.user_answer = ""

# UI เกม
st.title("🎮 WordPlay: ทายคำศัพท์")
st.subheader(f"📊 คะแนน: {st.session_state.score}")

# เลือกหมวดหมู่
st.session_state.selected_category = st.selectbox("📂 เลือกหมวดหมู่", ["ประเทศ", "ผลไม้", "สัตว์"])

# ปุ่มเริ่มเกม
if st.button("🚀 เริ่มเกม"):
    start_game()

# ปุ่มรีเซตเกม
if st.button("🔄 รีเซตเกม"):
    reset_game()

# ถ้าเกมกำลังทำงาน
if st.session_state.game_running:
    # นับถอยหลังเวลา
    elapsed_time = time.time() - st.session_state.start_time
    st.session_state.time_left = max(0, 60 - int(elapsed_time))

    # แสดงเวลา
    st.write(f"⏳ เวลาที่เหลือ: {st.session_state.time_left} วินาที")

    # ถ้าเวลาหมด
    if st.session_state.time_left <= 0:
        st.error(f"⏰ หมดเวลา! คำตอบคือ: {st.session_state.word_to_guess}")
        time.sleep(1)  # หน่วงเวลาก่อนเปลี่ยนคำใหม่
        select_new_word()

    # แสดงคำใบ้และจำนวนตัวอักษร
    word_length = len(st.session_state.word_to_guess.replace(" ", ""))  # นับตัวอักษรไม่นับช่องว่าง
    st.write(f"💡 คำใบ้: {st.session_state.hint}")
    st.write(f"🔢 คำศัพท์มีทั้งหมด {word_length} ตัวอักษร")

    # กล่องให้กรอกคำตอบ
    user_input = st.text_input("🔤 พิมพ์คำตอบของคุณ", value=st.session_state.user_answer, key="answer_input")

    # ปุ่มส่งคำตอบ
    if st.button("✅ ส่งคำตอบ"):
        if user_input.lower().strip() == st.session_state.word_to_guess.lower().strip():
            st.session_state.score += 10
            st.success(f"🎉 คำตอบถูกต้อง! +10 คะแนน\n👉 คำตอบ: {st.session_state.word_to_guess}")
        else:
            st.session_state.score -= 10
            st.error(f"❌ คำตอบผิด! -10 คะแนน\n👉 คำตอบที่ถูกต้องคือ: {st.session_state.word_to_guess}")

        time.sleep(1)  # หน่วงเวลาก่อนเปลี่ยนคำใหม่
        select_new_word()