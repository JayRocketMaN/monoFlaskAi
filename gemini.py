import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv()

def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    chat = client.chats.create(
    model="gemini-3.1-pro-preview",
    config=types.GenerateContentConfig(
      #system_instruction='you are a story teller for kids under 5 years old',
      max_output_tokens= 8192,
      top_k= 40,
      top_p= 0.95,
      temperature= 1.0,
      #response_mime_type= 'application/json',
      #stop_sequences= ['\n'],
      #seed=42,
  ),
)
    response = chat.send_message(
    message='Tell me a story in 100 words')
    response = chat.send_message(
    message='What happened after that?') 
    return(response.text)

    # response = chat.send_message(
    # message='Tell me a story in 100 words')
    # response = chat.send_message(
    # message='What happened after that?') 

# #--------------------------------------------------
#     model = "gemini-3.1-pro-preview"
#     contents = [
#         types.Content(
#             role="user",
#             parts=[
#                 types.Part.from_text(text= 'message'),
#             ],
#         ),
#     ]
#     # tools = [
#     #     types.Tool(googleSearch=types.GoogleSearch(
#     #     )),
#     # ]
#     # generate_content_config = types.GenerateContentConfig(
#     #     thinking_config=types.ThinkingConfig(
#     #         thinking_level="HIGH",
#     #     ),
#     #     tools=tools,
#     # )
#     response = client.models.generate_content(
#     contents='Tell me a story in 300 words.'
# )
#     print(response.text)

#     print(response.model_dump_json(
#     exclude_none=True, indent=4))

#     # for chunk in client.models.generate_content_stream(
#     #     model=model,
#     #     contents=contents,
#     #     config=generate_content_config,
#     # ):
#        # print(chunk.text, end="")

if __name__ == "__main__":
    generate()

# #generate content
# from google import genai
# client = genai.Client()

# response = client.models.generate_content(
#     model='gemini-2.0-flash',
#     contents='Tell me a story in 300 words.'
# )
# print(response.text)

# print(response.model_dump_json(
#     exclude_none=True, indent=4))
# #-------------------------------------------
# #config
# #----------------------------------------
# from google import genai
# from google.genai import types

# client = genai.Client()

# response = client.models.generate_content(
#   model='gemini-2.0-flash',
#   contents='Tell me a story in 100 words.',
#   config=types.GenerateContentConfig(
#       system_instruction='you are a story teller for kids under 5 years old',
#       max_output_tokens= 400,
#       top_k= 2,
#       top_p= 0.5,
#       temperature= 0.5,
#       response_mime_type= 'application/json',
#       stop_sequences= ['\n'],
#       seed=42,
#   ),
# )
# #----------
# # start a chat
# #----------
# from google import genai

# client = genai.Client()

# # chat = client.chats.create(model='gemini-2.0-flash')

# # response = chat.send_message(
# #     message='Tell me a story in 100 words')
# # response = chat.send_message(
# #     message='What happened after that?')