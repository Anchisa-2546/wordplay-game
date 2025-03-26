import streamlit as st
import time
import random

# คำศัพท์แต่ละหมวดหมู่
word_categories = {
    "🌍 ประเทศ": {
        "คำศัพท์": ["Thailand", "Japan", "France", "Brazil", "Germany", "Canada", "Australia", "China", "Italy", "India"],
        "คำใบ้": [
            "ประเทศในเอเชียตะวันออกเฉียงใต้", "ประเทศที่มีอนิเมะดัง", "เมืองหลวงคือปารีส", "ประเทศในอเมริกาใต้",
            "ประเทศที่มีเบียร์ดัง", "ประเทศที่มีน้ำตกไนแองการา", "ประเทศที่มีจิงโจ้", "ประเทศที่มีประชากรมากที่สุด",
            "ประเทศที่มีพิซซ่า", "ประเทศที่มีทัชมาฮาล"
        ],
        "background": "https://example.com/world_background.jpg"
    },
    "🍎 ผลไม้": {
        "คำศัพท์": ["Apple", "Banana", "Mango", "Orange", "Durian", "Rambutan", "Longan", "Strawberry", "Pineapple", "Watermelon"],
        "คำใบ้": [
            "ผลไม้สีเขียว-แดง", "ผลไม้สีเหลืองงอได้", "ผลไม้เมืองร้อนสีเหลือง", "ผลไม้ที่เป็นชื่อสี",
            "ราชาผลไม้ มีกลิ่นแรง", "ผลไม้มีขน เปลือกสีแดง", "ผลไม้ลูกเล็ก เปลือกบาง", "ผลไม้สีแดง มีกลิ่นหอม",
            "ผลไม้สีเหลือง เปลือกแข็ง", "ผลไม้สีเขียว-แดง ฉ่ำน้ำ"
        ],
        "background": "https://example.com/fruit_background.jpg"
    },
    "🐅 สัตว์": {
        "คำศัพท์": ["Tiger", "Elephant", "Rabbit", "Penguin", "Sloth", "Capybara", "Kangaroo", "Hamster", "Giraffe", "Dolphin"],
        "คำใบ้": [
            "เสือที่อยู่ในป่า", "สัตว์บกที่ตัวใหญ่ที่สุด", "สัตว์ที่กระโดดได้", "นกที่ว่ายน้ำเก่ง",
            "สัตว์เคลื่อนไหวช้าที่สุด", "สัตว์ฟันแทะขนาดใหญ่ในอเมริกาใต้", "สัตว์ที่มีกระเป๋าหน้าท้อง",
            "สัตว์เลี้ยงขนาดเล็กที่ชอบวิ่งในวงล้อ", "สัตว์คอยาวกินใบไม้", "สัตว์เลี้ยงลูกด้วยนมที่ว่ายน้ำเก่ง"
        ],
        "background": "https://example.com/animal_background.jpg"
    },
    "👩‍🔬 อาชีพ": {
        "คำศัพท์": ["Doctor", "Engineer", "Teacher", "Artist", "Scientist", "Chef", "Musician", "Writer", "Nurse", "Actor"],
        "คำใบ้": [
            "ผู้เชี่ยวชาญด้านการรักษา", "ผู้เชี่ยวชาญด้านวิศวกรรม", "ผู้สอนนักเรียน", "ผู้สร้างงานศิลปะ",
            "ผู้วิจัยในห้องปฏิบัติการ", "ผู้ทำอาหาร", "ผู้เล่นดนตรี", "ผู้เขียนหนังสือ", "ผู้ดูแลผู้ป่วย",
            "ผู้แสดงในภาพยนตร์"
        ],
        "background": "https://example.com/job_background.jpg"
    },
    "⚽ กีฬา": {
        "คำศัพท์": ["Football", "Basketball", "Tennis", "Baseball", "Cricket", "Rugby", "Hockey", "Golf", "Volleyball", "Badminton"],
        "คำใบ้": [
            "กีฬาใช้ลูกบอลกลม", "กีฬาใช้ลูกบอลยัดใส่ตะกร้า", "กีฬาเล่นด้วยไม้และลูก", "กีฬาเล่นบนสนามหญ้า",
            "กีฬาใช้ไม้ตีลูกกลม", "กีฬาที่เล่นในสนามหิมะ", "กีฬาใช้ไม้ไม้เล็กๆ และลูกเล็ก", "กีฬาเล่นในสนามทราย",
            "กีฬาเล่นในสนามหญ้า", "กีฬาเล่นในสนามไม้"
        ],
        "background": "https://example.com/sport_background.jpg"
    }
}

# ตั้งค่าค่าเริ่มต้นใน session_state
if "last_score" not in st.session_state:
    st.session_state.last_score = 0
if "last_time" not in st.session_state:
    st.session_state.last_time = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "total_time" not in st.session_state:
    st.session_state.total_time = 0
if "incorrect_attempts" not in st.session_state:
    st.session_state.incorrect_attempts = 0
if "game_running" not in st.session_state:
    st.session_state.game_running = False

# UI เกม
st.title("🎮 WordPlay: ทายคำศัพท์")
st.subheader(f"📊 คะแนน: {st.session_state.score} | ⏳ เวลารวม: {st.session_state.total_time}s")
st.subheader(f"💡 ครั้งที่แล้ว - คะแนน: {st.session_state.last_score} | เวลา: {st.session_state.last_time}s")

# เลือกหมวดหมู่
category = st.selectbox("\U0001f4c2 เลือกหมวดหมู่", list(word_categories.keys()))
st.markdown(f"""
    <style>
        body {{
            background-image: url('{word_categories[category]["background"]}');
            background-size: cover;
        }}
    </style>
    """, unsafe_allow_html=True)

# ปุ่มเริ่มเกม
if st.button("🚀 เริ่มเกม"):
    st.session_state.game_running = True
    st.session_state.score = 0
    st.session_state.total_time = 0
    st.session_state.incorrect_attempts = 0

if st.session_state.game_running:
    # แสดงคำใบ้
    word_index = random.randint(0, len(word_categories[category]["คำศัพท์"]) - 1)
    correct_word = word_categories[category]["คำศัพท์"][word_index]
    hint = word_categories[category]["คำใบ้"][word_index]
    st.write(f"💡 คำใบ้: {hint}")
    
    # แสดงจำนวนครั้งที่ตอบผิด
    st.write(f"❌ ตอบผิดไปแล้ว: {st.session_state.incorrect_attempts}/3")
    
    user_answer = st.text_input("📝 ใส่คำตอบที่นี่")
    if user_answer and user_answer.lower().strip() == correct_word.lower():
        st.success("✅ คำตอบถูกต้อง!")
        st.session_state.score += 10
    else:
        st.session_state.incorrect_attempts += 1
        if st.session_state.incorrect_attempts >= 3:
            st.session_state.game_running = False
            st.session_state.last_score = st.session_state.score
            st.session_state.last_time = st.session_state.total_time