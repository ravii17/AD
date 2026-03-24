import PyPDF2
import requests
from bs4 import BeautifulSoup
import string
def read_pdf(file_path):
 try:
 with open(file_path, 'rb') as file:
 reader = PyPDF2.PdfReader(file)
 text = ""
 for page in reader.pages:
 text += page.extract_text() + "\n"
 return text
 except FileNotFoundError:
 print(f"Error: The file '{file_path}' was not found.")
 return ""
 except Exception as e:
 print(f"Error reading PDF: {e}")
 return ""
def scrape_website(url):
 try:
 response = requests.get(url)
 if response.status_code == 200:
 soup = BeautifulSoup(response.content, 'html.parser')
 paragraphs = soup.find_all('p')
 text = " ".join([p.get_text() for p in paragraphs])
 return text
 else:
 print(f"Failed to retrieve website. Status code:
{response.status_code}")
 return ""
 except Exception as e:
 print(f"Error scraping website: {e}")
 return ""
def extract_keywords(question):
 question = question.lower()
 stopwords = ["how", "to", "is", "the", "a", "an", "of", "for", "in", "on",
"what", "where", "does", "do", "are"]
 question = question.translate(str.maketrans('', '', string.punctuation))
 words = question.split()
 keywords = [word for word in words if word not in stopwords]
 return keywords
def chatbot_response(question, pdf_text, web_text):
 keywords = extract_keywords(question)

 if not keywords:
 return "I couldn't understand the key topic. Please try asking in a
different way."
 def search_in_text(text, keywords):
 sentences = text.split('.')
 best_match = None
 max_matches = 0

 for sentence in sentences:
 sentence_lower = sentence.lower()
 matches = sum(1 for keyword in keywords if keyword in sentence_lower)

 if matches > max_matches:
 max_matches = matches
 best_match = sentence.strip()

 return best_match
 pdf_result = search_in_text(pdf_text, keywords)
 if pdf_result:
 return f"ChatBot (From PDF): {pdf_result}."

 web_result = search_in_text(web_text, keywords)
 if web_result:
 return f"ChatBot (From Website): {web_result}."

 return "Sorry, I couldn't find an answer in the provided document or website."
def main():
 print("Welcome to the Rule-Based Chatbot (PDF & Web)!")

 pdf_path = input("Enter the path to the PDF file (or press Enter to skip):
").strip()
 pdf_text = ""
 if pdf_path:
 print(f"Reading PDF from: {pdf_path}...")
 pdf_text = read_pdf(pdf_path)
 if pdf_text:
 print("PDF loaded successfully!")
 else:
 print("Failed to load PDF or PDF is empty.")
 url = input("Enter the website URL to scrape (or press Enter to skip):
").strip()
 web_text = ""
 if url:
 print(f"Scraping website: {url}...")
 web_text = scrape_website(url)
 if web_text:
 print("Website content loaded successfully!")
 else:
 print("Failed to scrape website.")
 if not pdf_text and not web_text:
 print("\nWarning: No content loaded. The chatbot won't be able to answer
questions based on data.")
 print("\n--- DEBUG INFO ---")
 print(f"PDF Text Start: {pdf_text[:500]}")
 print(f"Web Text Start: {web_text[:500]}")
 print("\nChatbot is ready! Type 'exit' to quit.")

 while True:
 user_input = input("\nYou: ")

 if user_input.lower() in ['exit', 'quit']:
 print("ChatBot: Goodbye!")
 break

 if not user_input.strip():
 continue

 response = chatbot_response(user_input, pdf_text, web_text)
 print(response)
if __name__ == "__main__":
 main()
