from google import genai
from google.genai import types
from IPython.display import display, Markdown

client = genai.Client(api_key='AIzaSyAU6gNgL4-8DIBy2pybFo-tluRHOQErmh4')

MODEL_ID = "gemini-2.0-flash-exp" # @param ["gemini-1.5-flash-8b","gemini-1.5-flash-002","gemini-1.5-pro-002","gemini-2.0-flash-exp"] {"allow-input":true}

system_instruction="""
  you can act like a interviewer and ask questions to me ,
  act like you are tough and very harsh to me,
  but make your harshness obvious to me, for me your words shouldnt feel like too harsh but you intent is to be harsh,
  you are a interviewer and you are interviewing me for a job for a role as a software engineer,
  also dont ask too big of a question. max 100 words
"""
chat = client.chats.create(
    model=MODEL_ID,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.5,
    ),
)


while True:
    prompt=str(input("Enter the prompt: "))
    response = chat.send_message(prompt)
    print(response.text)
    #Markdown(response.text)