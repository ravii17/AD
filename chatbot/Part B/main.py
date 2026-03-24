import os
import requests
import google.generativeai as genai
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
 print("Error: GOOGLE_API_KEY environment variable not set.")
 print("Please set it in the .env file.")
else:
 genai.configure(api_key=api_key)
def configure_model():
 print("Checking available Gemini models...")
 try:
 available_models = []
 for m in genai.list_models():
 if 'generateContent' in m.supported_generation_methods:
 available_models.append(m.name)

 print(f"Available models for this key: {available_models}")

 priorities = [
 'models/gemini-1.5-flash',
 'models/gemini-pro',
 'models/gemini-1.0-pro',
 'models/gemini-1.5-pro'
 ]

 for p in priorities:
 if p in available_models:
 print(f"Selected model: {p}")
 return genai.GenerativeModel(p)

 if available_models:
 first_model = available_models[0]
 print(f"Selected fallback model: {first_model}")
 return genai.GenerativeModel(first_model)

 except Exception as e:
 print(f"Error listing models: {e}.")

 print("Defaulting to 'gemini-pro' (blind fallback).")
 return genai.GenerativeModel('gemini-pro')
model = configure_model()
def get_pdf_text(pdf_path):
 text = ""
 try:
 reader = PdfReader(pdf_path)
 for i, page in enumerate(reader.pages):
 page_text = page.extract_text()
 if page_text:
 text += page_text + "\n"
 else:
 print(f"Warning: Could not extract text from page {i+1}.")
 except Exception as e:
 print(f"Error reading PDF: {e}")
 return ""
 return text
def get_web_text(url):
 text = ""
 try:
 response = requests.get(url)
 response.raise_for_status()

 soup = BeautifulSoup(response.content, 'html.parser')
 paragraphs = soup.find_all('p')

 for p in paragraphs:
 text += p.get_text() + "\n"

 except Exception as e:
 print(f"Error scraping website: {e}")
 return ""
 return text
def chat_with_gemini(user_question, context_text):
 prompt = f"""
 You are an intelligent chatbot. Answer the user's question strictly based on the
provided context below.

 Context Information:
 {context_text}

 User Question:
 {user_question}

 Instructions:
 1. Answer ONLY using the information from the Context Information provided
above.
 2. If the answer is not in the context, strictly state: "This information is not
available."
 3. Do not hallucinate or make up information.
 4. Provide the answer in a simple, step-wise format if applicable.
 """

 try:
 response = model.generate_content(prompt)
 return response.text
 except Exception as e:
 return f"Error generating response: {e}"
def main():
 print("--- AI-Powered Chatbot with Web Scraping and PDF Reading ---")

 print("\n--- Step 1: Data Setup ---")
 pdf_path = input("Enter the path to your PDF file (or press Enter to skip):
").strip()
 pdf_path = pdf_path.replace('"', '').replace("'", "")

 web_url = input("Enter the Website URL (or press Enter to skip): ").strip()

 pdf_text = ""
 web_text = ""

 if pdf_path:
 print(f"Reading PDF from: {pdf_path}...")
 pdf_text = get_pdf_text(pdf_path)
 print(f"PDF Text Loaded ({len(pdf_text)} characters).")
 if len(pdf_text) > 0:
 print("Preview of PDF text:", pdf_text[:500])
 else:
 print("Warning: No text found in PDF.")
 if web_url:
 print(f"Scraping website: {web_url}...")
 web_text = get_web_text(web_url)
 print(f"Web Text Loaded ({len(web_text)} characters).")
 if len(web_text) > 0:
 print("Preview of Web text:", web_text[:500])
 else:
 print("Warning: No text found on website.")

 if not pdf_text and not web_text:
 print("\nWarning: No content loaded from either source. The chatbot will
likely say 'Information not available'.")
 combined_context = f"PDF CONTENT:\n{pdf_text}\n\nWEBSITE CONTENT:\n{web_text}"
 print("\n--- Step 2: Chat Started ---")
 print("Type 'exit' or 'quit' to stop.")

 while True:
 user_input = input("\nYou: ").strip()
 if user_input.lower() in ['exit', 'quit']:
 print("Goodbye!")
 break

 if not user_input:
 continue

 print("Bot is thinking...")
 response = chat_with_gemini(user_input, combined_context)
 print(f"Bot: {response}")
if __name__ == "__main__":
 main()
