from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

def parse_response(query):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_format={ "type": "json_object" },
    messages=[
      {"role": "system", "content": "You are a helpful assistant designed to output JSON for the given text, the keys shouls be Orgainsation, Company Number, Registered Address, Other Adresss, Contact, Website, Social Media, Answer. The answer should be the exact text inputted. If any of the information is not available then leave that blank."},
      {"role": "user", "content": query}
    ]
  )
  return response.choices[0].message.content
#print(response.choices[0].message.content)