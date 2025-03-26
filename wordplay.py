import streamlit as st
import random
import time

# Initialize session state variables
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "score" not in st.session_state:
    st.session_state.score = 0
if "total_time" not in st.session_state:
    st.session_state.total_time = 0
if "last_score" not in st.session_state:
    st.session_state.last_score = 0
if "last_time" not in st.session_state:
    st.session_state.last_time = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "incorrect_answers" not in st.session_state:
    st.session_state.incorrect_answers = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# Word categories
word_categories = {
    "🌍 ประเทศ": {
        "words": ["Thailand", "Japan", "France", "Brazil", "Germany", "Canada", "Australia", "China", "Italy", "India", "Russia", "Mexico", "Spain", "Egypt", "Sweden"],
        "hints": ["ประเทศในเอเชีย", "มีอะนิเมะดัง", "เมืองหลวงคือปารีส", "อยู่ในอเมริกาใต้", "มีเบียร์ดัง", "มีน้ำตกไนแองการา", "มีจิงโจ้", "ประชากรเยอะสุด", "มีพิซซ่า", "มีทัชมาฮาล",
                  "มีหมีขาว", "ประเทศในอเมริกากลาง", "ใช้ภาษาสเปน", "มีพีระมิด", "ประเทศในสแกนดิเนเวีย"],
        "background": "https://example.com/world_background.jpg"
    },
    "🍎 ผลไม้": {
        "words": ["Apple", "Banana", "Mango", "Orange", "Durian", "Rambutan", "Longan", "Strawberry", "Pineapple", "Watermelon", "Papaya", "Coconut", "Cherry", "Grapes", "Guava"],
        "hints": ["สีเขียว-แดง", "สีเหลืองโค้ง", "ผลไม้เมืองร้อน", "ชื่อเป็นสี", "ราชาผลไม้", "ผลไม้เปลือกแดง", "ผลไม้ลูกเล็ก", "สีแดงหวาน", "เปลือกแข็ง", "ผลไม้ฉ่ำน้ำ",
                  "ผลไม้สุกสีส้ม", "มีน้ำมะพร้าว", "ผลไม้ลูกเล็กสีแดง", "เป็นพวง", "เปลือกเขียวเนื้อขาว"],
        "background": "https://example.com/fruit_background.jpg"
    },
    "🐅 สัตว์": {
        "words": ["Tiger", "Elephant", "Rabbit", "Penguin", "Sloth", "Capybara", "Kangaroo", "Hamster", "Giraffe", "Dolphin", "Zebra", "Panda", "Wolf", "Parrot", "Turtle"],
        "hints": ["เสือในป่า", "สัตว์บกตัวใหญ่", "กระต่ายน่ารัก", "นกว่ายน้ำได้", "เคลื่อนที่ช้า", "สัตว์ฟันแทะใหญ่", "มีกระเป๋าหน้าท้อง", "วิ่งในวงล้อ", "คอยาว", "ว่ายน้ำเก่ง",
                  "มีลายขาวดำ", "หมีขาวดำ", "สัตว์ป่าดุร้าย", "นกพูดได้", "สัตว์เปลือกแข็ง"],
        "background": "https://example.com/animal_background.jpg"
    },
    "👩‍🔬 อาชีพ": {
        "words": ["Doctor", "Engineer", "Teacher", "Artist", "Scientist", "Chef", "Musician", "Writer", "Nurse", "Actor", "Pilot", "Firefighter", "Police", "Judge", "Dancer"],
        "hints": ["รักษาคนไข้", "สร้างสะพาน", "สอนหนังสือ", "วาดภาพ", "ทำวิจัย", "ทำอาหาร", "เล่นดนตรี", "เขียนหนังสือ", "ดูแลผู้ป่วย", "แสดงภาพยนตร์",
                  "ขับเครื่องบิน", "ดับเพลิง", "จับโจร", "ตัดสินคดี", "เต้นรำ"],
        "background": "https://example.com/job_background.jpg"
    },
    "⚽ กีฬา": {
        "words": ["Football", "Basketball", "Tennis", "Baseball", "Cricket", "Rugby", "Hockey", "Golf", "Volleyball", "Badminton", "Swimming", "Cycling", "Skiing", "Boxing", "Chess"],
        "hints": ["กีฬายอดนิยม", "ใช้ลูกบอลใหญ่", "ใช้ไม้ตีลูก", "กีฬาอเมริกา", "กีฬาค้างคาว", "กีฬาสัมผัสตัว", "กีฬาน้ำแข็ง", "ใช้ไม้ตีลูกเล็ก", "เล่นเป็นทีม", "ใช้ไม้ขนไก่",
                  "ว่ายน้ำ", "ปั่นจักรยาน", "เล่นบนหิมะ", "ชกมวย", "เกมกระดาน"],
        "background": "https://example.com/sport_background.jpg"
    }
}

# UI
st.title("🎮 WordPlay: ทายคำศัพท์")

# Player name input
st.session_state.player_name = st.text_input("👤 ชื่อผู้เล่น:", st.session_state.player_name)

st.subheader(f"📊 คะแนน: {st.session_state.score} | ⏳ เวลารวม: {st.session_state.total_time}s")

# Convert last_time to minutes and seconds
last_minutes, last_seconds = divmod(st.session_state.last_time, 60)
st.subheader(f"💡 ครั้งที่แล้ว - คะแนน: {st.session_state.last_score} | เวลา: {int(last_minutes)} นาที {int(last_seconds)} วินาที")

category = st.selectbox("📂 เลือกหมวดหมู่", list(word_categories.keys()))

# Display background
if category:
    st.markdown(f"""
        <style>
            body {{
                background-image: url('{word_categories[category]["background"]}');
                background-size: cover;
            }}
        </style>
        """, unsafe_allow_html=True)

# Start new game
if st.button("🚀 เริ่มเกมใหม่"):
    if st.session_state.player_name == "":
        st.error("กรุณาใส่ชื่อผู้เล่นก่อนเริ่มเกม!")
    else:
        st.session_state.score = 0
        st.session_state.total_time = 0
        st.session_state.current_question = 0
        st.session_state.incorrect_answers = 0
        st.session_state.game_over = False
        st.session_state.start_time = time.time()

if not st.session_state.game_over and category:
    word = word_categories[category]["words"][st.session_state.current_question]
    hint = word_categories[category]["hints"][st.session_state.current_question]
    st.write(f"💡 คำใบ้: {hint} ({len(word)} ตัวอักษร)")

    # Ensure start_time is not None
    if st.session_state.start_time is not None:
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = 30 - elapsed_time
        st.write(f"⏳ เวลาที่เหลือ: {int(remaining_time)} วินาที")

        if remaining_time <= 0:
            st.error("⏰ หมดเวลา! เริ่มเกมใหม่.")
            st.session_state.game_over = True
            st.session_state.last_score = st.session_state.score
            st.session_state.last_time = time.time() - st.session_state.start_time
            st.experimental_rerun()

    answer = st.text_input("✍️ พิมพ์คำตอบ:")

    if st.button("✅ ส่งคำตอบ"):
        if answer.lower().strip() == word.lower():
            st.success("✅ ถูกต้อง! +10 คะแนน")
            st.session_state.score += 10
        else:
            st.error(f"❌ ผิด! คำตอบที่ถูกคือ: {word}")
            st.session_state.incorrect_answers += 1

        # Update total time
        st.session_state.total_time += time.time() - st.session_state.start_time
        st.session_state.current_question += 1
        st.session_state.start_time = time.time()  # Reset timer for next question

        # Check if the game is over
        if st.session_state.incorrect_answers >= 3 or st.session_state.current_question >= len(word_categories[category]["words"]):
            st.session_state.game_over = True
            st.session_state.last_score = st.session_state.score
            st.session_state.last_time = st.session_state.total_time

            # Record player data
            st.session_state.leaderboard.append({
                "name": st.session_state.player_name,
                "score": st.session_state.score,
                "time": st.session_state.last_time
            })

            # Sort leaderboard by score and time
            st.session_state.leaderboard.sort(key=lambda x: (-x["score"], x["time"]))

            st.write("🎉 เกมจบแล้ว! คุณทำได้ดีมาก!")

# Display leaderboard
st.write("🏆 Leaderboard:")
for idx, player in enumerate(st.session_state.leaderboard):
    minutes, seconds = divmod(player["time"], 60)
    st.write(f"{idx + 1}. {player['name']} - คะแนน: {player['score']}, เวลา: {int(minutes)} นาที {int(seconds)} วินาที")
