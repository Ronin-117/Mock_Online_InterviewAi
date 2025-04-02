import os
import tempfile
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import Literal
import json
from config import GEMINI_API_KEY

class Language_data(BaseModel):
    Vocabulary: Literal["high","mid","low"]
    Grammar: Literal["high","mid","low"]
    description: str

conversion={
    "high":10,
    "mid":6,
    "low":3
}

def filler_score(filler_words_count):
    if filler_words_count < 3:
        return 10
    elif filler_words_count < 10:
        return 6
    else:
        return 3
    
def eye_contact_score(non_verbal_results):
    eye_contact_diff=int(non_verbal_results["good_eye_contact"])- int(non_verbal_results["no_eye_contact"])
    if eye_contact_diff > int(non_verbal_results["good_eye_contact"])/2:
        return 10
    elif eye_contact_diff > 0:
        return 6
    else:
        return 3

def posture_score(non_verbal_results):
    posture_diff=int(non_verbal_results["good_posture"])- int(non_verbal_results["unclear_posture"])
    if posture_diff > int(non_verbal_results["good_posture"])/2:
        return 10
    elif posture_diff > 0:
        return 6
    else:
        return 3

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-2.0-flash-exp" 

def evaluation_score(interview_data):
    filler_words_count = interview_data["filler_words_count"]
    user_responses = interview_data["user_responses"]
    gemini_responses = interview_data["gemini_responses"]
    non_verbal_results = interview_data["non_verbal_results"]
    meta_data = interview_data["metadata"]

    conversation=""
    for i in range(len(user_responses)):
        conversation+=f"Gemini: {gemini_responses[i]} \nUser: {user_responses[i]}"
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=f"this is the a conversation between user and gemini: {conversation} \nbased on the above information give a score on the user's response for vocabulary and grammar in high, mid and low.",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Language_data,
        ),
    )
    vocabulary, grammar = None, None
    try:
        parsed_data = response.candidates[0].content.parts[0].text
        # Convert the string to a dictionary
        parsed_data_dict = json.loads(parsed_data)
        vocabulary = conversion[parsed_data_dict["Vocabulary"]]
        grammar = conversion[parsed_data_dict["Grammar"]]
        #print(f"{vocabulary=},{grammar=},{type(vocabulary)=},{type(grammar)=}")
    except (IndexError, KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing Gemini response: {e}")
        vocabulary = "low"  # Default value in case of error
        grammar = "low"  # Default value in case of error

    filler = filler_score(filler_words_count)


    eye_contact = eye_contact_score(non_verbal_results)
    posture = posture_score(non_verbal_results)


    # Calculate the score based on the verbal and non-verbal results
    verbal_score = (vocabulary + grammar+ filler) / 3
    non_verbal_score = (eye_contact + posture) / 2
    overall_score= (verbal_score + non_verbal_score) / 2

    score = {
        "overall_score": round(overall_score,1),
        "verbal_score": round(verbal_score,1),
        "non_verbal_score": round(non_verbal_score,1),
        "filler": round(filler,1),
        "eye_contact": round(eye_contact,1),
        "posture": round(posture,1),
        "vocabulary": round(vocabulary,1),
        "grammar": round(grammar,1),
    }
    return score

if __name__ == "__main__":
    interview_data={'gemini_responses': ['Good morning NeilJoseph. Thanks for being here today.To start, can you tell me about a time you worked as part of a team to solve a challenging problem?What was your role, and how did the team overcome the obstacles you faced?', 'Of course. Can you describe a situation where you collaborated with a team to tackle a difficult problem?Please explain your specific role in the team and how the team managed to overcome the challenges encountered.', 'Okay,okay, this is the last question.Considering your experience with AI and software engineering, what do you believe is the most important quality for a team member to possess in order to foster a collaborative and innovative environment?'], 
                    'metadata': {'Interview Timestamp': '20250329_202427', 'Job': 'Ai software engineer', 'Interviewer Type': 'Team_Member_interviewer'}, 
                    'non_verbal_results': {'good_posture': 0, 'unclear_posture': 0, 'good_eye_contact': 0, 'no_eye_contact': 0}, 
                    'user_audio_files': ['C:\\Users\\njne2\\Desktop\\Cuda_PWR\\CREATIVE\\Mini_project\\app2\\backend\\myapp\\interviews\\interview_20250329_202427\\user_audio\\user_response_0.wav', 'C:\\Users\\njne2\\Desktop\\Cuda_PWR\\CREATIVE\\Mini_project\\app2\\backend\\myapp\\interviews\\interview_20250329_202427\\user_audio\\user_response_1.wav', 'C:\\Users\\njne2\\Desktop\\Cuda_PWR\\CREATIVE\\Mini_project\\app2\\backend\\myapp\\interviews\\interview_20250329_202427\\user_audio\\user_response_2.wav'], 
                    'interview_folder': 'C:\\Users\\njne2\\Desktop\\Cuda_PWR\\CREATIVE\\Mini_project\\app2\\backend\\myapp\\interviews\\interview_20250329_202427', 
                    'user_responses': [" I don't understand the question Can you please repeat that?", " I don't like to answer that because most of my teammates were Rautalmulji."], 
                    'filler_words_count': 3}
    score=evaluation_score(interview_data)
    print(score)
