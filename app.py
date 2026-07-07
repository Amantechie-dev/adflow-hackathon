import os
import boto3
import streamlit as st
from google import genai
from dotenv import load_dotenv

# Load variables from our secure .env file
load_dotenv()

# Configure page settings
st.set_page_config(page_title="AdFlow Campaign Generator", page_icon="", layout="centered")

# Initialize Clients
b2_client = boto3.client(
    service_name='s3',
    endpoint_url=os.environ.get("B2_REGION_ENDPOINT"),
    aws_access_key_id=os.environ.get("B2_KEY_ID"),
    aws_secret_access_key=os.environ.get("B2_APPLICATION_KEY")
)
BUCKET_NAME = os.environ.get("B2_BUCKET_NAME")
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# UI Elements
st.title(" AdFlow Marketing Campaign Generator")
st.write("Enter a product name below to generate high-converting ad copy and automatically back it up to your cloud storage.")

# Input Box
product_name = st.text_input("Product Name", placeholder="e.g., Retro Futuristic Smart Glasses")

if st.button("Generate Campaign Layout", type="primary"):
    if not product_name.strip():
        st.warning("Please enter a valid product name first!")
    else:
        with st.spinner(f"Drafting content for '{product_name}' via Gemini..."):
            try:
                # 1. Generate text copy using the live active Gemini model
                prompt = f"Write a high-converting, professional social media advertisement copy for {product_name}. Include a catchy headline and relevant hashtags."
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                generated_text = response.text
                
                # 2. Upload the copy directly to your Backblaze B2 bucket
                file_key = f"campaigns/{product_name.lower().replace(' ', '_')}.txt"
                b2_client.put_object(
                    Bucket=BUCKET_NAME,
                    Key=file_key,
                    Body=generated_text.encode('utf-8'),
                    ContentType='text/plain'
                )
                
                # 3. Display results on the web page
                st.success(f"✅ Campaign successfully backed up to Backblaze B2 bucket at path: {file_key}")
                
                st.subheader("📋 Generated Ad Copy Output:")
                st.markdown(generated_text)
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")