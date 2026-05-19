from openai import OpenAI
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os

# Colors for to be used in print
GREEN = "\033[32m"
REGULAR = "\033[0m"

# Initialize the OpenAI client with your API key
client = OpenAI()

# Function to clean and organize notes using the OpenAI API
def clean_notes(raw_notes):
    prompt = f"""
        Clean and organize these notes into categories, bullet points, and concise summaries of those categories.
        Also if there is any information on the topics in my notes that is missing or incorrect please add it and mark it in a way that is clear to me that the new information is yours and not from my notes
        Try to group things into categories and subcategories clearly if possible and make notes easy to read and digestible.

        Notes:
        {raw_notes}
        """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
# End of clean_notes function

# Function to send email
def send_email(content):
    from_email = "mark.nguyen@g.austincc.edu"
    to_email = "mark.nguyen@g.austincc.edu"
    password = os.getenv("EMAIL_APP_PASSWORD")

    msg = MIMEText(content)
    msg["Subject"] = "Cleaned Notes"
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, password)
        server.send_message(msg)


# Gets user input for notes
lines=[]
print("Paste your notes below (Type 'END INPUT' when done):")
while True:
    try:
        line=input()
        if line.strip().upper() == "END INPUT":
            break
        lines.append(line)
    except EOFError:
        break

# Join the lines into a single string to be processed
user_input = "\n".join(lines) 

# Inform the user to wait for the delay from chatGPT
print(f"{GREEN}\nProcessing your notes, please wait...\n{REGULAR}")

# Call the function to clean the notes
result = clean_notes(user_input)

# # Optionally, save the cleaned notes to a text file with a timestamped filename
# filename = f"cleaned_notes_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
# with open(f"/Users/marknguyen/Code Stuff/Text Files/{filename}", "w", encoding="utf-8") as f:
#     f.write(result)

# Print the cleaned notes to the console and sends an email version
# So that Zapier turns the email into a Google Doc
print("\n--- CLEANED NOTES ---\n")
print(f"{GREEN}{result}{REGULAR}")
send_email(result)
