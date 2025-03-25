import streamlit as st
import time
import random

# หมวดหมู่คำศัพท์
word_categories = {
    "ประเทศ 🌍": [
        {"word": "ประเทศไทย", "hint": "🔑 ประเทศในเอเชียตะวันออกเฉียงใต้"},
        {"word": "ญี่ปุ่น", "hint": "🔑 ประเทศที่มีภูเขาไฟฟูจิ"},
        {"word": "ฝรั่งเศส", "hint": "🔑 ประเทศที่มีหอไอเฟล"},
        {"word": "อเมริกา", "hint": "🔑 ประเทศที่มีเทพีเสรีภาพ"}
    ],
    "ผลไม้ 🍎": [
        {"word": "มะม่วง", "hint": "🔑 ผลไม้สีเหลือง ยอดฮิตในไทย"},
        {"word": "สตรอว์เบอร์รี่", "hint": "🔑 ผลไม้สีแดง มีเมล็ดรอบๆ"},
        {"word": "แตงโม", "hint": "🔑 ผลไม้สีเขียว ภายในสีแดง มีเมล็ดสีดำ"},
        {"word": "กล้วย", "hint": "🔑 ผลไม้สีเหลือง ยาวและโค้ง"}
    ],
    "สัตว์ 🐾": [
        {"word": "สิงโต", "hint": "🔑 ราชาแห่งป่า"},
        {"word": "ช้าง", "hint": "🔑 สัตว์บกที่ใหญ่ที่สุด"},
        {"word": "เพนกวิน", "hint": "🔑 นกที่ว่ายน้ำได้ แต่บินไม่ได้"},
        {"word": "จระเข้", "hint": "🔑 สัตว์เลื้อยคลานที่อยู่ทั้งบนบกและในน้ำ"}
    ]
}

# ฟังก์ชันรีเซ็ตเกม
def reset_game():
    selected_category = st.session_state.get("selected_category", "ประเทศ 🌍")  
    word_data = random.choice(word_categories[selected_category])  
    st.session_state.word = word_data["word"]
    st.session_state.hint = word_data["hint"]
    st.session_state.time_left = 60  
    st.session_state.user_input = ""
    st.session_state.correct = None  
    st.session_state.running = True  

    # ถ้ายังไม่มีคะแนนให้ตั้งค่าเป็น 0
    if "score" not in st.session_state:
        st.session_state.score = 0  

    st.rerun()  # รีเฟรชหน้า

# ตรวจสอบค่า session_state
if "word" not in st.session_state:
    reset_game()

# UI เกม
st.title("🎮 WordPlay: ทายคำศัพท์")

# แสดงคะแนน
st.write(f"🏆 คะแนน: {st.session_state.get('score', 0)}/100")

# เลือกหมวดหมู่
category = st.selectbox("📂 เลือกหมวดหมู่", list(word_categories.keys()), key="selected_category")

# ปุ่มเริ่มเกม
if st.button("🚀 เริ่มเกม"):
    reset_game()

# แสดงคำใบ้
st.write(f"💡 คำใบ้: {st.session_state.hint}")

# ระบบนับเวลาถอยหลัง
if st.session_state.running:
    if st.session_state.time_left > 0:
        st.session_state.time_left -= 1
        time.sleep(1)
        st.rerun()  
    else:
        st.session_state.running = False  

# แสดงเวลา
st.write(f"⏳ เวลาที่เหลือ: {st.session_state.time_left} วินาที")

# ช่องป้อนคำตอบ
user_input = st.text_input("🎭 พิมพ์คำศัพท์ที่ต้องการทาย", key="user_input")

# ปุ่มส่งคำตอบ
if st.button("✅ ส่งคำตอบ") and st.session_state.running:
    if user_input.strip() == st.session_state.word:
        st.session_state.correct = True
        st.session_state.score += 10  # เพิ่มคะแนนทีละ 10
        if st.session_state.score > 100:
            st.session_state.score = 100  # จำกัดคะแนนที่ 100
    else:
        st.session_state.correct = False
    st.session_state.running = False  
    st.rerun()

# แสดงผลลัพธ์
if st.session_state.correct is not None:
    if st.session_state.correct:
        st.success(f"🎉 คำตอบถูกต้อง! +10 คะแนน (คะแนนรวม: {st.session_state.score}/100)")
    else:
        st.error("❌ คำตอบผิด ลองใหม่!")

# แสดงข้อความเมื่อหมดเวลา
if not st.session_state.running and st.session_state.time_left == 0:
    st.warning("⏳ หมดเวลา! ลองใหม่")

# ปุ่มรีเซ็ตเกม
if st.button("🔄 รีเซ็ตเกม"):
    st.session_state.score = 0  # รีเซ็ตคะแนนเป็น 0
    reset_game()