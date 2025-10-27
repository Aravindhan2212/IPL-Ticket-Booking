# admin.py
import streamlit as st
import pandas as pd
from pathlib import Path
import uuid
import os

BASE = Path(__file__).parent
MATCHES_CSV = BASE / "matches.csv"
LOGOS_DIR = BASE / "logos"
LOGOS_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="IPL Admin", page_icon="⚙️", layout="centered")
st.title("⚙️ IPL Admin Panel — Add / Edit Matches & Upload Logos")

def ensure_csv():
    if not MATCHES_CSV.exists():
        df = pd.DataFrame(columns=["team1","team2","venue","date","time","seats_available","parking_available","logo1","logo2","ticket_price"])
        df.to_csv(MATCHES_CSV, index=False)

ensure_csv()
df = pd.read_csv(MATCHES_CSV)

mode = st.sidebar.selectbox("Mode", ["View Matches","Add Match","Edit / Delete Match","Upload Logo"])

if mode == "View Matches":
    st.subheader("📋 Current Matches")
    st.dataframe(df)

elif mode == "Add Match":
    st.subheader("➕ Add Match")
    with st.form("add", clear_on_submit=True):
        team1 = st.text_input("Team 1 (short code, e.g. MI)")
        team2 = st.text_input("Team 2 (short code, e.g. CSK)")
        venue = st.text_input("Venue")
        date = st.date_input("Date")
        time = st.time_input("Time")
        seats = st.number_input("Seats available", min_value=0, value=200)
        parking = st.number_input("Parking available", min_value=0, value=50)
        logo1 = st.text_input("Logo1 filename (e.g. mi.png)")
        logo2 = st.text_input("Logo2 filename (e.g. csk.png)")
        ticket_price = st.number_input("Ticket price (per seat)", min_value=0, value=1000)
        submit = st.form_submit_button("Save Match")
    if submit:
        new = {"team1":team1.strip(),"team2":team2.strip(),"venue":venue.strip(),
               "date":str(date),"time":str(time),"seats_available":int(seats),
               "parking_available":int(parking),
               "logo1":logo1.strip(),"logo2":logo2.strip(),"ticket_price":int(ticket_price)}
        df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
        df.to_csv(MATCHES_CSV, index=False)
        st.success("Match added ✅")

elif mode == "Edit / Delete Match":
    st.subheader("✏️ Edit or Delete")
    if df.empty:
        st.info("No matches to edit")
    else:
        idx = st.selectbox("Choose match to edit (index)", df.index.tolist())
        row = df.loc[idx]
        with st.form("edit", clear_on_submit=False):
            team1 = st.text_input("Team 1", value=row['team1'])
            team2 = st.text_input("Team 2", value=row['team2'])
            venue = st.text_input("Venue", value=row['venue'])
            date = st.text_input("Date", value=row['date'])
            time = st.text_input("Time", value=row['time'])
            seats = st.number_input("Seats available", min_value=0, value=int(row['seats_available']))
            parking = st.number_input("Parking available", min_value=0, value=int(row['parking_available']))
            logo1 = st.text_input("Logo1 filename", value=row.get('logo1',''))
            logo2 = st.text_input("Logo2 filename", value=row.get('logo2',''))
            ticket_price = st.number_input("Ticket price", min_value=0, value=int(row.get('ticket_price',1000)))
            save = st.form_submit_button("Save changes")
        if save:
            df.at[idx,"team1"]=team1.strip()
            df.at[idx,"team2"]=team2.strip()
            df.at[idx,"venue"]=venue.strip()
            df.at[idx,"date"]=date
            df.at[idx,"time"]=time
            df.at[idx,"seats_available"]=int(seats)
            df.at[idx,"parking_available"]=int(parking)
            df.at[idx,"logo1"]=logo1.strip()
            df.at[idx,"logo2"]=logo2.strip()
            df.at[idx,"ticket_price"]=int(ticket_price)
            df.to_csv(MATCHES_CSV, index=False)
            st.success("Updated ✅")
        if st.button("Delete this match"):
            df = df.drop(index=idx).reset_index(drop=True)
            df.to_csv(MATCHES_CSV, index=False)
            st.success("Deleted ✅")

elif mode == "Upload Logo":
    st.subheader("📁 Upload Team Logo (PNG/JPG)")
    uploaded = st.file_uploader("Choose logo image", type=["png","jpg","jpeg"])
    filename = st.text_input("Save as filename (example: mi.png)")
    if st.button("Upload"):
        if uploaded and filename:
            safe = "".join(c for c in filename if c.isalnum() or c in "._-")
            path = LOGOS_DIR / safe
            with open(path, "wb") as f:
                f.write(uploaded.getbuffer())
            st.success(f"Saved logo to logos/{safe}")
        else:
            st.error("Please choose a file and provide filename.")
