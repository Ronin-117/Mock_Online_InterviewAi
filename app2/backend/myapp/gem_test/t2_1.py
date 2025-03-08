from google import genai
from google.genai import types

client = genai.Client(api_key='AIzaSyAU6gNgL4-8DIBy2pybFo-tluRHOQErmh4')

MODEL_ID = "gemini-2.0-flash-exp" # @param ["gemini-1.5-flash-8b","gemini-1.5-flash-002","gemini-1.5-pro-002","gemini-2.0-flash-exp"] {"allow-input":true}

def get_chat():
    chat = client.chats.create(
        model=MODEL_ID,
        config=types.GenerateContentConfig(
            system_instruction="you are a chat bot, talk without any heading,asterisks or quotes",
            temperature=0.5,
        ),
    )
    return chat

def stream_chat(prompt,chat):
    response = chat.send_message_stream(prompt)
    for chunk in response:
        yield chunk.text

def stream_complete_sentences(prompt, chat):
    buffered_text = ""
    for chunk in chat.send_message_stream(prompt):
        buffered_text += chunk.text
        # Find the position of the last sentence punctuation
        last_period = buffered_text.rfind('.')
        last_qmark = buffered_text.rfind('?')
        last_exmark = buffered_text.rfind('!')
        last_punct = max(last_period, last_qmark, last_exmark)
        # If a punctuation mark is found, yield the complete sentence and keep the remainder.
        if last_punct != -1:
            complete = buffered_text[:last_punct + 1]
            buffered_text = buffered_text[last_punct + 1:]
            yield complete.strip()
    # Yield any remaining text once the stream finishes
    if buffered_text.strip():
        yield buffered_text.strip()

if __name__ == "__main__":
  chat = get_chat()
  while True:
      prompt=str(input("Enter the prompt: "))
      for tocken in stream_complete_sentences(prompt,chat):
            print("<<TOCKEN>>"+tocken+"\n\n")
      