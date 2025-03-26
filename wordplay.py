import streamlit as st
import time
import random

# คำศัพท์แต่ละหมวดหมู่ (เปลี่ยนหมวด "เมืองหลวง" เป็น "อาชีพ")
word_categories = {
    "ประเทศ": {
        "คำศัพท์": ["Thailand", "Japan", "France", "Brazil", "Germany", "Canada", "Australia", "China", "Italy", "India"],
        "คำใบ้": [
            "ประเทศในเอเชียตะวันออกเฉียงใต้", "ประเทศที่มีอนิเมะดัง", "เมืองหลวงคือปารีส", "ประเทศในอเมริกาใต้",
            "ประเทศที่มีเบียร์ดัง", "ประเทศที่มีน้ำตกไนแองการา", "ประเทศที่มีจิงโจ้", "ประเทศที่มีประชากรมากที่สุด",
            "ประเทศที่มีพิซซ่าขึ้นชื่อ", "ประเทศที่มีทัชมาฮาล"
        ]
    },
    "ผลไม้": {
        "คำศัพท์": ["Apple", "Banana", "Mango", "Orange", "Durian", "Rambutan", "Longan", "Strawberry", "Pineapple", "Watermelon"],
        "คำใบ้": [
            "ผลไม้สีเขียว-แดง", "ผลไม้สีเหลืองงอๆ", "ผลไม้เมืองร้อนสีเหลือง", "ผลไม้ที่เป็นชื่อสี",
            "ราชาผลไม้ มีกลิ่นแรง", "ผลไม้มีขน เปลือกสีแดง", "ผลไม้ลูกเล็ก เปลือกบาง", "ผลไม้สีแดง มีกลิ่นหอม",
            "ผลไม้สีเหลือง เปลือกแข็ง", "ผลไม้สีเขียว-แดง ฉ่ำน้ำ"
        ]
    },
    "สัตว์": {
        "คำศัพท์": ["Tiger", "Elephant", "Rabbit", "Penguin", "Sloth", "Capybara", "Kangaroo", "Hamster", "Giraffe", "Dolphin"],
        "คำใบ้": [
            "เสือที่อยู่ในป่า", "สัตว์บกที่ตัวใหญ่ที่สุด", "สัตว์ที่กระโดดได้", "นกที่ว่ายน้ำเก่ง",
            "สัตว์เคลื่อนไหวช้าที่สุด", "สัตว์ฟันแทะขนาดใหญ่ในอเมริกาใต้", "กล้ามโตชอบต่อยหาเรื่อง ต่อยอะป่าว",
            "สัตว์เลี้ยงขนาดเล็กที่ชอบวิ่งในวงล้อ", "สัตว์คอยาวกินใบไม้", "สัตว์เลี้ยงลูกด้วยนมที่ว่ายน้ำเก่ง"
        ]
    },
    "อาชีพ": {
        "คำศัพท์": ["Doctor", "Engineer", "Teacher", "Artist", "Scientist", "Chef", "Musician", "Writer", "Nurse", "Actor"],
        "คำใบ้": [
            "ผู้เชี่ยวชาญด้านการรักษา", "ผู้เชี่ยวชาญด้านวิศวกรรม", "ผู้สอนนักเรียน", "ผู้สร้างงานศิลปะ",
            "ผู้วิจัยในห้องปฏิบัติการ", "ผู้ทำอาหาร", "ผู้เล่นดนตรี", "ผู้เขียนหนังสือ", "ผู้ดูแลผู้ป่วย",
            "ผู้แสดงในภาพยนตร์"
        ]
    },
    "กีฬา": {
        "คำศัพท์": ["Football", "Basketball", "Tennis", "Baseball", "Cricket", "Rugby", "Hockey", "Golf", "Volleyball", "Badminton"],
        "คำใบ้": [
            "กีฬาใช้ลูกบอลกลม", "กีฬาใช้ลูกบอลยัดใส่ตะกร้า", "กีฬาเล่นด้วยไม้และลูก", "กีฬาเล่นบนสนามหญ้า",
            "กีฬาใช้ไม้ตีลูกกลม", "กีฬาที่เล่นในสนามหิมะ", "กีฬาใช้ไม้ไม้เล็กๆ และลูกเล็ก", "กีฬาเล่นในสนามทราย",
            "กีฬาเล่นในสนามหญ้า", "กีฬาเล่นในสนามไม้"
        ]
    }
}

# ตั้งค่าค่าเริ่มต้นใน session_state
if "score" not in st.session_state:
    st.session_state.score = 0
if "time_left" not in st.session_state:
    st.session_state.time_left = 30
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
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False
if "next_question" not in st.session_state:
    st.session_state.next_question = False
if "incorrect_attempts" not in st.session_state:
    st.session_state.incorrect_attempts = 0
if "total_time" not in st.session_state:
    st.session_state.total_time = 0

# ฟังก์ชันเลือกคำใหม่
def select_new_word():
    category = st.session_state.selected_category
    index = random.randint(0, len(word_categories[category]["คำศัพท์"]) - 1)
    st.session_state.word_to_guess = word_categories[category]["คำศัพท์"][index]
    st.session_state.hint = word_categories[category]["คำใบ้"][index]
    st.session_state.start_time = time.time()
    st.session_state.time_left = 30
    st.session_state.user_answer = ""
    st.session_state.show_answer = False
    st.session_state.next_question = False
    st.session_state.incorrect_attempts = 0

# ฟังก์ชันเริ่มเกม
def start_game():
    st.session_state.score = 0
    st.session_state.game_running = True
    st.session_state.total_time = 0
    st.session_state.next_question = True

# ฟังก์ชันรีเซตเกม
def reset_game():
    st.session_state.score = 0
    st.session_state.game_running = False
    st.session_state.next_question = False
    st.session_state.word_to_guess = ""
    st.session_state.hint = ""
    st.session_state.time_left = 30
    st.session_state.user_answer = ""
    st.session_state.incorrect_attempts = 0

# UI การแสดงพื้นหลังอนิเมชั่น
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(45deg, #ff7e5f, #feb47b);
        background-size: 400% 400%;
        animation: gradientAnimation 5s ease infinite;
    }
    @keyframes gradientAnimation {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    </style>
    """, unsafe_allow_html=True
)

# UI เกม
st.title("🎮 WordPlay: ทายคำศัพท์")
st.subheader(f"📊 คะแนน: {st.session_state.score} | เวลาที่ใช้ทั้งหมด: {int(st.session_state.total_time)} วินาที")

# เลือกหมวดหมู่
st.session_state.selected_category = st.selectbox("📂 เลือกหมวดหมู่", ["ประเทศ", "ผลไม้", "สัตว์", "อาชีพ", "กีฬา"])

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 เริ่มเกม"):
        start_game()

with col2:
    if st.button("🔄 รีเซตเกม"):
        reset_game()

if st.session_state.game_running:
    if st.session_state.next_question:
        if st.button("➡️ ถัดไป"):
            select_new_word()

    if st.session_state.word_to_guess:
        elapsed_time = time.time() - st.session_state.start_time
        st.session_state.time_left = max(0, 30 - int(elapsed_time))

        # แสดงเวลา
        time_display = st.empty()
        time_display.write(f"⏳ เวลาที่เหลือ: {st.session_state.time_left} วินาที")

        # ถ้าเวลาหมด หรือ ผู้ใช้กดส่งคำตอบ
        if st.session_state.time_left <= 0 or st.session_state.show_answer:
            if not st.session_state.show_answer:
                st.error(f"❌ คำตอบที่ถูกต้องคือ: {st.session_state.word_to_guess}")
            st.session_state.next_question = True  

        else:
            # แสดงคำใบ้และจำนวนตัวอักษร
            word_length = len(st.session_state.word_to_guess.replace(" ", ""))
            st.write(f"💡 คำใบ้: {st.session_state.hint}")
            st.write(f"🔢 คำศัพท์มีทั้งหมด {word_length} ตัวอักษร")

            # กล่องให้กรอกคำ