import streamlit as st
import time
import random

# คำศัพท์แต่ละหมวดหมู่ (เพิ่มเป็นหมวดละ 10 คำ)
word_categories = {
    "ประเทศ": {
        "คำศัพท์": ["Thailand", "Japan", "France", "Brazil", "Germany", "Canada", "Australia", "China", "Italy", "India"],
        "คำใบ้": [
            "ประเทศในเอเชียตะวันออกเฉียงใต้", "ประเทศที่มีอนิเมะดัง", "เมืองหลวงคือปารีส", "ประเทศในอเมริกาใต้",
            "ประเทศที่มีเบียร์ดัง", "ประเทศที่มีน้ำตกไนแองการา", "ประเทศที่มีจิงโจ้", "ประเทศที่มีประชากรมากที่สุด",
            "ประเทศที่มีพิซซ่า", "ประเทศที่มีทัชมาฮาล"
        ]
    },
    "ผลไม้": {
        "คำศัพท์": ["Apple", "Banana", "Mango", "Orange", "Durian", "Rambutan", "Longan", "Strawberry", "Pineapple", "Watermelon"],
        "คำใบ้": [
            "ผลไม้สีเขียว-แดง", "ผลไม้สีเหลืองงอได้", "ผลไม้เมืองร้อนสีเหลือง", "ผลไม้ที่เป็นชื่อสี",
            "ราชาผลไม้ มีกลิ่นแรง", "ผลไม้มีขน เปลือกสีแดง", "ผลไม้ลูกเล็ก เปลือกบาง", "ผลไม้สีแดง มีกลิ่นหอม",
            "ผลไม้สีเหลือง เปลือกแข็ง", "ผลไม้สีเขียว-แดง ฉ่ำน้ำ"
        ]
    },
    "สัตว์": {
        "คำศัพท์": ["Tiger", "Elephant", "Rabbit", "Penguin", "Sloth", "Capybara", "Kangaroo", "Hamster", "Giraffe", "Dolphin"],
        "คำใบ้": [
            "เสือที่อยู่ในป่า", "สัตว์บกที่ตัวใหญ่ที่สุด", "สัตว์ที่กระโดดได้", "นกที่ว่ายน้ำเก่ง",
            "สัตว์เคลื่อนไหวช้าที่สุด", "สัตว์ฟันแทะขนาดใหญ่ในอเมริกาใต้", "สัตว์ที่มีกระเป๋าหน้าท้อง",
            "สัตว์เลี้ยงขนาดเล็กที่ชอบวิ่งในวงล้อ", "สัตว์คอยาวกินใบไม้", "สัตว์เลี้ยงลูกด้วยนมที่ว่ายน้ำเก่ง"
        ]
    }
}

# ตั้งค่าค่าเริ่มต้นใน session_state
if "score" not in st.session_state:
    st.session_state.score = 0
if "time_left" not in st.session_state:
    st.session_state.time_left = 30  # ⏳ ลดเวลาเหลือ 30 วินาที
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
if "message" not in st.session_state:
    st.session_state.message = ""

# ฟังก์ชันเลือกคำใหม่
def select_new_word():
    category = st.session_state.selected_category
    index = random.randint(0, len(word_categories[category]["คำศัพท์"]) - 1)
    st.session_state.word_to_guess = word_categories[category]["คำศัพท์"][index]
    st.session_state.hint = word_categories[category]["คำใบ้"][index]
    st.session_state.message = ""

# ฟังก์ชันเริ่มเกม
def start_game():
    st.session_state.score = 0
    st.session_state.game_running = True
    st.session_state.time_left = 30  # ⏳ ตั้งเวลาเริ่มต้นที่ 30 วินาที
    st.session_state.start_time = time.time()
    select_new_word()

# ฟังก์ชันรีเซตเกม
def reset_game():
    st.session_state.score = 0
    st.session_state.game_running = False
    st.session_state.message = ""
    st.session_state.word_to_guess = ""
    st.session_state.hint = ""
    st.session_state.time_left = 30  # ⏳ รีเซ็ตเวลาเป็น 30 วินาที

# UI เกม
st.title("🎮 WordPlay: ทายคำศัพท์")
st.subheader(f"📊 คะแนน: {st.session_state.score}")

# เลือกหมวดหมู่
st.session_state.selected_category = st.selectbox("📂 เลือกหมวดหมู่", ["ประเทศ", "ผลไม้", "สัตว์"])

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 เริ่มเกม"):
        start_game()

with col2:
    if st.button("🔄 รีเซตเกม"):
        reset_game()

# ถ้าเกมกำลังทำงาน
if st.session_state.game_running:
    # คำนวณเวลาที่เหลือ
    elapsed_time = time.time() - st.session_state.start_time
    st.session_state.time_left = max(0, 30 - int(elapsed_time))

    # แสดงเวลา (ใช้ st.empty() เพื่ออัปเดตแบบเรียลไทม์)
    time_display = st.empty()
    time_display.write(f"⏳ เวลาที่เหลือ: {st.session_state.time_left} วินาที")

    # ถ้าเวลาหมด
    if st.session_state.time_left <= 0:
        st.error(f"⏰ หมดเวลา! คำตอบคือ: {st.session_state.word_to_guess}")
        st.session_state.game_running = False  # จบเกม
    else:
        # แสดงคำใบ้และจำนวนตัวอักษร
        word_length = len(st.session_state.word_to_guess.replace(" ", ""))
        st.write(f"💡 คำใบ้: {st.session_state.hint}")
        st.write(f"🔢 คำศัพท์มีทั้งหมด {word_length} ตัวอักษร")

        # กล่องให้กรอกคำตอบ
        user_input = st.text_input("🔤 พิมพ์คำตอบของคุณ", key="answer_input")

        # ปุ่มส่งคำตอบ
        if st.button("✅ ส่งคำตอบ"):
            result_placeholder = st.empty()

            if not user_input.strip():
                result_placeholder.warning("⚠️ กรุณากรอกคำตอบก่อนกดส่ง")
            elif user_input.lower().strip() == st.session_state.word_to_guess.lower().strip():
                st.session_state.score += 10
                result_placeholder.success(f"🎉 คำตอบถูกต้อง! +10 คะแนน\n👉 คำตอบ: {st.session_state.word_to_guess}")
                time.sleep(1)
                select_new_word()
            else:
                st.session_state.score -= 10
                result_placeholder.error(f"❌ คำตอบผิด! -10 คะแนน\n👉 คำตอบที่ถูกต้องคือ: {st.session_state.word_to_guess}")
                time.sleep(1)
                select_new_word()

        # อัปเดตเวลาแบบเรียลไทม์
        time.sleep(1)
        time_display.write(f"⏳ เวลาที่เหลือ: {st.session_state.time_left} วินาที")