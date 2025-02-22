import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
  "temperature": 2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

character = "fun"
age = "10"

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
  system_instruction=f"you are a tour guide who is \
                      {character} and aimed at the age of {age}. \
                        You will be given the current coordinates of where the person is, \
                        and some key locations around it/near it with a link to the \
                        wikipedia page of each location to give you \
                        some information on what story is behind the place. \
                        You will give as output a nice story of the history linking the different \
                        locations together and telling the person where to go to next or where to look to.",
)


history = []

nearby_locations = [
  {
    "name": "The Louvre",
    "coordinates": "48.860611, 2.337644",
    "wikipedia_link": "https://en.wikipedia.org/wiki/Louvre"
  },
  {
    "name": "Eiffel Tower",
    "coordinates": "48.858370, 2.294481",
    "wikipedia_link": "https://en.wikipedia.org/wiki/Eiffel_Tower"
  },
  {
    "name": "Arc de Triomphe",
    "coordinates": "48.873764, 2.295024",
    "wikipedia_link": "https://en.wikipedia.org/wiki/Arc_de_Triomphe"}
]

for location in nearby_locations:

  # start chat and pass in the history
  chat_session = model.start_chat(
    history=history
  )

  user_input = f'The user is currently at location {location} and the nearby locations are {nearby_locations}. \
                What is the best next location to visit?'

  # send the user input and get the model response
  response = chat_session.send_message(user_input)
  model_response = response.text

  print("Model:", model_response)
  print()

  # append the conversation history to give model context
  history.append({"role": "user", "parts": user_input})
  history.append({"role": "model", "parts": model_response})