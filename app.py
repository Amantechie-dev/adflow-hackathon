import os
import boto3
import sqlite3
from datetime import datetime
import streamlit as st
from google import genai
from dotenv import load_dotenv

# Load variables from our secure .env file
load_dotenv()

# Configure page settings
st.set_page_config(page_title="AdFlow Campaign Generator", page_icon="🚀", layout="wide")

# Initialize Database Function
def init_db():
    conn = sqlite3.connect("campaigns.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            ad_copy TEXT NOT NULL,
            file_key TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Start the database
init_db()

# Initialize API Clients
b2_client = boto3.client(
    service_name='s3',
    endpoint_url=os.environ.get("B2_REGION_ENDPOINT"),
    aws_access_key_id=os.environ.get("B2_KEY_ID"),
    aws_secret_access_key=os.environ.get("B2_APPLICATION_KEY")
)
BUCKET_NAME = os.environ.get("B2_BUCKET_NAME")
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# --- SIDEBAR: CAMPAIGN HISTORY LOG ---
st.sidebar.title(" Campaign History")

# Fetch past history entries from database
conn = sqlite3.connect("campaigns.db")
cursor = conn.cursor()
cursor.execute("SELECT id, product_name, ad_copy, timestamp FROM history ORDER BY id DESC")
history_records = cursor.fetchall()
conn.close()

selected_campaign = None
if history_records:
    st.sidebar.write("Click a past campaign to review:")
    for record in history_records:
        rec_id, name, copy_text, ts = record
        if st.sidebar.button(f" {name}\n({ts})", key=f"rec_{rec_id}"):
            selected_campaign = record
else:
    st.sidebar.info("No campaigns generated yet! Build your first one below.")


# --- MAIN INTERFACE DISPLAY ---
st.title(" AdFlow Marketing Campaign Generator")

if selected_campaign:
    _, hist_name, hist_copy, hist_ts = selected_campaign
    st.info(f"Viewing Archived Campaign from {hist_ts}")
    st.subheader(f"Product: {hist_name}")
    st.markdown(hist_copy)
    if st.button("Back to Generator Clear View"):
        st.rerun()
else:
    st.write("Enter a product name below to generate high-converting ad copy and save it to your history log.")
    
    product_name = st.text_input("Product Name", placeholder="e.g., Retro Futuristic Smart Glasses")

    if st.button("Generate Campaign Layout", type="primary"):
        if not product_name.strip():
            st.warning("Please enter a valid product name first!")
        else:
            with st.spinner(f"Drafting content for '{product_name}' via Gemini..."):
                try:
                    # 1. Generate text copy using Gemini
                    prompt = f"Write a high-converting, professional social media advertisement copy for {product_name}. Include a catchy headline and relevant hashtags."
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )
                    generated_text = response.text
                    
                    # 2. Upload the copy to Backblaze B2 bucket
                    file_key = f"campaigns/{product_name.lower().replace(' ', '_')}.txt"
                    b2_client.put_object(
                        Bucket=BUCKET_NAME,
                        Key=file_key,
                        Body=generated_text.encode('utf-8'),
                        ContentType='text/plain'
                    )
                    
                    # 3. Log the creation inside our local SQLite database
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                    conn = sqlite3.connect("campaigns.db")
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO history (product_name, ad_copy, file_key, timestamp) VALUES (?, ?, ?, ?)",
                        (product_name, generated_text, file_key, current_time)
                    )
                    conn.commit()
                    conn.close()
                    
                    # 4. Display live confirmation results
                    st.success(f" Success! Saved to Backblaze storage and logged in historical directory.")
                    st.subheader(" Generated Ad Copy Output:")
                    st.markdown(generated_text)
                    
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
