from google import genai
from google.genai import types
from IPython.display import Markdown

# Replace with your actual API key
GOOGLE_API_KEY = "AIzaSyAU6gNgL4-8DIBy2pybFo-tluRHOQErmh4"

# Initialize SDK client
client = genai.Client(api_key=GOOGLE_API_KEY)

MODEL_ID = "gemini-2.0-flash-exp" # or "gemini-1.5-pro-002", "gemini-1.5-flash-8b", etc.


async def generate_custom_response(input_text, instruction, model_id = MODEL_ID):
  """
  Generates a response based on the input text and provided instruction.

  Args:
    input_text: The text to process.
    instruction: The instructions for the model.
    model_id: the gemini model to be used for inference.
  
  Returns:
    str: the output from the model
  """
  prompt = f"""
  {instruction}
  Input Text: {input_text}
  """

  response = await client.aio.models.generate_content(
      model=model_id,
      contents=prompt,
      
  )

  return response.text
    

async def main():

    input_text = "The quick brown fox jumps over the lazy dog. "
    instruction = "Please generate an output that makes the text shorter, and more professional."
    output = await generate_custom_response(input_text, instruction)
    print("Output 1:")
    print(Markdown(output))
    
    input_text = "I am coming from kochi, and my name is neil"
    instruction = "Please reverse the sentence while keeping it in the same format."
    output = await generate_custom_response(input_text, instruction)
    print("Output 2:")
    print(Markdown(output))

    input_text = "This is a list of names\n- john\n- bob\n- sam"
    instruction = "Please convert the list into a comma seperated format."
    output = await generate_custom_response(input_text, instruction)
    print("Output 3:")
    print(Markdown(output))

    input_text = "the dog jumped over the fox"
    instruction = "Please give the above text in different languages, including spanish, german and french"
    output = await generate_custom_response(input_text, instruction, "gemini-1.5-pro-002")
    print("Output 4:")
    print(Markdown(output))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())