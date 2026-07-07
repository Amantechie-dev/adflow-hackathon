import os
import boto3
from google import genai

# 1. Connect to Backblaze B2 using the official S3 Client protocol
b2_client = boto3.client(
    service_name='s3',
    endpoint_url='https://s3.eu-central-003.backblazeb2.com',  # Matches your eu-central-003 region
    aws_access_key_id="003ebf5aca537d90000000001",
    aws_secret_access_key="K003ACLajqOCVs2PQXTGadGGdviODa4"
)

BUCKET_NAME = "aman-adflow"

# 2. Configure the new modern Google GenAI client directly
client = genai.Client(api_key="AQ.Ab8RN6KSlGQWZTaXtIVp8vNeDRYc3JkhdOvGls7VRrjHcWmQVQ")

def generate_ad_campaign(product_name):
    print(f"🚀 Starting AI content generation for: {product_name}...")
    
    prompt = f"Write a high-converting, professional social media advertisement copy for {product_name}. Include a catchy headline and relevant hashtags."
    
    # 3. Generate text copy using the updated official client syntax
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    generated_text = response.text
    
    print("\n--- Generated Copy ---")
    print(generated_text)
    
    # 4. Upload the copy directly to your Backblaze B2 bucket
    file_key = f"campaigns/{product_name.lower().replace(' ', '_')}.txt"
    
    b2_client.put_object(
        Bucket=BUCKET_NAME,
        Key=file_key,
        Body=generated_text.encode('utf-8'),
        ContentType='text/plain'
    )
    
    print(f"\n✅ Success! Ad content saved directly to Backblaze B2 bucket '{BUCKET_NAME}' at path '{file_key}'.")

if __name__ == "__main__":
    generate_ad_campaign("Neon Cyberpunk Running Sneakers")