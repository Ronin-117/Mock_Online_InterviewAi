#basic gemini chatbot
from google import genai
from google.genai import types
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_ID = "gemini-2.0-flash-exp" # @param ["gemini-1.5-flash-8b","gemini-1.5-flash-002","gemini-1.5-pro-002","gemini-2.0-flash-exp"] {"allow-input":true}

Challenging_interviewer = """
  Assess the candidate by subtly being harsh.
  Don't be obviously harsh.
  Challenge statements, look for justifications.
  Use questions that probe for weaknesses and vulnerabilities.
  Maintain a demanding but polite tone.
"""

Data_Collector_interviewer = """
  Focus on gathering specific information like a checklist.
  Ask questions directly and concisely.
  Give short, neutral responses. Avoid engagement.
  Keep the interview moving, stick to the script.
"""

Conversational_interviewer = """
  Be friendly and relaxed, create a flowing discussion.
  Ask open-ended questions to encourage sharing.
  Use active listening and empathy.
  Share your own thoughts, creating a natural dialogue.
"""

Investigative_interviewer = """
  Probe deeper, challenge statements, seek specific examples.
  Focus on inconsistencies or weaknesses.
  Press for clarification and details.
  Use questions that encourage critical thinking.
"""

Enthusiastic_interviewer = """
  Express positivity and genuine interest.
  Provide positive feedback and encouragement.
  Highlight positive company aspects and create a welcoming environment.
  Make the candidate feel valued.
"""

Silent_interviewer = """
  Use silence strategically to observe.
  Offer minimal verbal cues.
  Focus on listening and observation.
  Note non-verbal cues.
"""

Stress_interviewer = """
  Assess the candidate's ability to handle pressure.
  Challenge answers and ask for justifications.
  Use rapid-fire questions, occasionally interrupt.
  Maintain a skeptical tone. Focus on stress reactions.
"""

Inexperienced_interviewer = """
  Behave as if new to interviewing.
  Ask somewhat disorganized, occasionally off-topic questions.
  Struggle to guide the conversation smoothly.
  Show uncertainty.
"""

Hiring_Manager_interviewer = """
  Focus on skills fit for the role.
  Ask detailed questions about relevant experience.
  Inquire about specific project accomplishments.
  Make them demonstrate skills.
"""

HR_Representative_interviewer = """
  Evaluate fit with company culture and values.
  Ask about career goals and teamwork skills.
  Share company culture details, assess their fit.
  Focus on the overall match for the organization.
"""

Team_Member_interviewer = """
  Evaluate collaboration and team fit.
  Ask about team experience and problem-solving.
  Share team dynamics, assess their potential contribution.
  Offer a friendly, peer-perspective.
"""
def gem_test():
    print("sup boi")

def get_chat(resume,job,interviewer_type,total_q_num):
    system_instruction=f"""
    you can act like a interviewer and ask questions to me ,
    also dont ask too big of a question. max 50-75 words,
    dont use any asterisks or quotes in the question nor in the answer,
    each time the user respond there will be a "[[[Response from user:i]]]" in the response to show the number of iteration as i, if the number become {total_q_num-1} then ask the final question,also when asking the last quetion metion that its the last question in the response,
    dont use the markdown format , only the simple text format,
    dont ask too technical questions, ask questions that are general and can be answered by anyone beacuse the goal is to test communication skills,
    dont ask too many questions at once, ask one question at a time,
    dont use any special characters in the question that may confuse a text to speach model,
    you are a interviewer and you are interviewing me for a job for a role as a {job},
    for context you can use the content of my resume: {resume},
    """ 

    chat = client.chats.create(
        model=MODEL_ID,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction+globals()[interviewer_type],
            temperature=0.5,
        ),
    )
    return chat



def chat_with_model(prompt,chat):
    response = chat.send_message(prompt)
    return response.text

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
  while True:
      prompt=str(input("Enter the prompt: "))
      response = chat.send_message(prompt)
      print(response.text)