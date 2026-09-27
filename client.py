 
from openai import OpenAI
import os
# client = OpenAI()
client=OpenAI(
api_key=os.getenv("OPEN_API_KEY"),
)
completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "what is coding?"},
  ]
)
print(completion.choices[0].message.content)