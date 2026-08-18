import os
import boto3
from google import genai
from dotenv import load_dotenv

# Load variables from our secure .env file
load_dotenv()

# 1. Connect to Backblaze B2 using environment values
b2_client = boto3.client(
    service_name='s3',
    endpoint_url=os.environ.get("B2_REGION_ENDPOINT"),
    aws_access_key_id=os.environ.get("B2_KEY_ID"),
    aws_secret_access_key=os.environ.get("B2_APPLICATION_KEY")
)

BUCKET_NAME = os.environ.get("B2_BUCKET_NAME")

# 2. Configure the Google GenAI client securely
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_ad_campaign(product_name):
    print(f" Starting AI content generation for: {product_name}...")
    
    prompt = f"Write a high-converting, professional social media advertisement copy for {product_name}. Include a catchy headline and relevant hashtags."
    
    # 3. Generate text copy using the live active Gemini model
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
    
    print(f"\n Success! Ad content saved directly to Backblaze B2 bucket '{BUCKET_NAME}' at path '{file_key}'.")

if __name__ == "__main__":
    # The clean, dynamic batch list loops perfectly through your entries
    campaign_catalog = [
        "Neon Cyberpunk Running Sneakers",
        "Retro Futuristic Smart Glasses",
        "Minimalist Matte Black Wireless Earbuds"
    ]
    
    print(f" Found {len(campaign_catalog)} products in queue. Beginning batch generation...\n")
    
    for product in campaign_catalog:
        try:
            generate_ad_campaign(product)
            print("-" * 50)
        except Exception as e:
            print(f" Failed to generate campaign for {product}. Error: {e}")
            
    print("\n🏁 All operations completed successfully!")
