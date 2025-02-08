import ollama

model="deepseek-r1:8b"
qn="who is iron man in 10 words"

response=ollama.chat(model=model, messages=[
    {
        'role': 'user',
        'content': qn
    }
])

o_response=response["message"]['content']
print(o_response)
