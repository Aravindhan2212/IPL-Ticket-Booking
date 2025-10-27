import streamlit as st
import pandas as pd
import os
from fpdf import FPDF

# ================================
#  IPL Ticket Booking System
# ================================
st.set_page_config(page_title="🏏 IPL Ticket Booking", layout="wide")

# Load Matches Data
matches_df = pd.read_csv("matches.csv")

st.title("🏏 IPL Ticket Booking System")

match_option = st.selectbox(
    "🏟️ Select Match",
    matches_df.apply(
        lambda x: f"{x['Team1']} vs {x['Team2']} — {x['Venue']} ({x['Date']} {x['Time']})", axis=1
    )
)

selected_match = matches_df.iloc[
    matches_df.apply(
        lambda x: f"{x['Team1']} vs {x['Team2']} — {x['Venue']} ({x['Date']} {x['Time']})", axis=1
    ).tolist().index(match_option)
]

# ================================
#  Display Team Logos and Info
# ================================
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    team1_logo = os.path.join("logos", f"{selected_match['Team1'].capitalize()}.png")
    if os.path.exists(team1_logo):
        st.image(team1_logo, width=150)
    else:
        st.write(selected_match['Team1'])

with col2:
    st.markdown(f"""
    <h2 style='text-align:center; color:#FF4B4B;'>{selected_match['Team1']} 🆚 {selected_match['Team2']}</h2>
    <p style='text-align:center; font-size:18px;'>📍 {selected_match['Venue']}</p>
    <p style='text-align:center; font-size:16px;'>📅 {selected_match['Date']} | ⏰ {selected_match['Time']}</p>
    """, unsafe_allow_html=True)

with col3:
    team2_logo = os.path.join("logos", f"{selected_match['Team2'].capitalize()}.png")
    if os.path.exists(team2_logo):
        st.image(team2_logo, width=150)
    else:
        st.write(selected_match['Team2'])

st.divider()

# ================================
#  Ticket Booking + Parking
# ================================
st.subheader("🎟️ Ticket & Parking Booking")

num_tickets = st.number_input("Select Number of Tickets", 1, 10, 1)
ticket_price = 500
parking_price = 150
ticket_total = num_tickets * (ticket_price + parking_price)

st.write(f"🎫 Ticket Price: ₹{ticket_price} | 🚗 Parking: ₹{parking_price}")
st.success(f"💰 Total Ticket + Parking Cost: ₹{ticket_total}")

st.divider()

# ================================
#  Food, Snacks, and Drinks
# ================================
st.subheader("🍔 Foods, 🍟 Snacks & 🥤 Drinks (Add to Cart)")

col_food, col_snack, col_drink = st.columns(3)

# ---- FOODS ----
with col_food:
    st.markdown("### 🍛 Foods")
    foods = {"Veg Biryani": 120, "Chicken Burger": 150, "Paneer Roll": 100, "Pizza": 180}
    food_total = 0
    for item, price in foods.items():
        qty = st.number_input(f"{item} (₹{price})", 0, 10, 0, key=f"food_{item}")
        food_total += qty * price

# ---- SNACKS ----
with col_snack:
    st.markdown("### 🍿 Snacks")
    snacks = {"French Fries": 80, "Popcorn": 100, "Samosa": 50, "Puffs": 60}
    snack_total = 0
    for item, price in snacks.items():
        qty = st.number_input(f"{item} (₹{price})", 0, 10, 0, key=f"snack_{item}")
        snack_total += qty * price

# ---- DRINKS ----
with col_drink:
    st.markdown("### 🥤 Drinks")
    drinks = {"Cold Coffee": 120, "Milkshake": 150, "Water Bottle": 30, "Fresh Juice": 100}
    drink_total = 0
    for item, price in drinks.items():
        qty = st.number_input(f"{item} (₹{price})", 0, 10, 0, key=f"drink_{item}")
        drink_total += qty * price

# Total
food_snack_drink_total = food_total + snack_total + drink_total
st.info(f"🧾 Food & Drinks Total: ₹{food_snack_drink_total}")

st.divider()

# ================================
#  Customer Details
# ================================
st.subheader("👤 Customer Details")
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")

st.divider()

# ================================
#  Payment Section
# ================================
st.subheader("💳 Payment Section")

total_payment = ticket_total + food_snack_drink_total
st.write(f"💰 **Grand Total: ₹{total_payment}**")

payment_method = st.selectbox("Select Payment Method", ["UPI", "Credit Card", "Debit Card", "Net Banking"])

if st.button("✅ Confirm Booking"):
    if not name or not email or not phone:
        st.error("⚠️ Please fill all customer details before proceeding!")
    else:
        st.success("🎉 Booking Successful! Enjoy the Match 🏏")
        st.balloons()

        # Create PDF Ticket
        pdf = FPDF()
        pdf.add_page()

        # Font Fix (Cross OS)
        font_path = None
        for path in [
            "fonts/DejaVuSans.ttf",
            r"C:\Windows\Fonts\Arial.ttf",
            r"C:\Windows\Fonts\arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ]:
            if os.path.exists(path):
                font_path = path
                break

        if font_path:
            pdf.add_font("UnicodeFont", "", font_path, uni=True)
            pdf.set_font("UnicodeFont", "", 14)
        else:
            pdf.set_font("Helvetica", "B", 14)

        pdf.cell(200, 10, txt="🏏 IPL Ticket Booking Confirmation", ln=True, align="C")
        pdf.cell(200, 10, txt=f"{selected_match['Team1']} vs {selected_match['Team2']}", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Venue: {selected_match['Venue']}", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Date: {selected_match['Date']} | Time: {selected_match['Time']}", ln=True, align="C")

        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Tickets: {num_tickets} (₹{ticket_total})", ln=True)
        pdf.cell(200, 10, txt=f"Food & Snacks Total: ₹{food_snack_drink_total}", ln=True)
        pdf.cell(200, 10, txt=f"Grand Total Paid: ₹{total_payment}", ln=True)
        pdf.cell(200, 10, txt=f"Payment Method: {payment_method}", ln=True)

        pdf.ln(10)
        pdf.cell(200, 10, txt="✅ Booking Successful! Enjoy the Match 🏏", ln=True, align="C")

        # Save PDF
        pdf_path = "ticket_confirmation.pdf"
        pdf.output(pdf_path)

        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download Your Ticket (PDF)", f, file_name="ticket_confirmation.pdf")

