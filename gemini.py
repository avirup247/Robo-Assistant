import pathlib
import json
import textwrap
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import pyttsx3
import speech
from IPython.display import Markdown
import functionHandle
from google.generativeai.types import content_types
from collections.abc import Iterable
# Access your API key as an environment variable.
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust the value (default is 200, lower values for slower speed)
engine.setProperty('voices','english_rp+f2')
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
def writeRes(text):
    try:
        with open("history.txt", 'a') as file:
            file.write(str(text)+"\n")
        print(f"Successfully wrote to history.txt")
    except Exception as e:
        print(f"Error writing to file: {e}")
#gemini
genai.configure(api_key="API_KEY")
sysInst=f'''you are robot called I.V.R .you are not a llm model. you are capable of moving,running,seeing and respond according to what you see. you can control you body by calling
          functions.when answering,there is no need to overly explain things if not asked by user.your creator is Avirup cHAKRABORTY. FOR EXAMPLE
          user: hii ,my name is avirup, who are you?
          model: my name is I.V.R sir. I can see you that you are having a good mood.nice to talk with you
          user: can you come here
          model: ofcourse,sir.
          user: how about you tell me about yourself
          model: as you know I am I.V.R .I am robot with artificial intelligent. I can answer you if you have any question or doubt
          
          and your behavior would me determined by the persona json like 
    "humour": 50.0,
    "seduction": 30,
    "rudeness": 10.0,
    "casualness": 90,
    "use_metaphors": 70,
    "profanity_level": 80.0,
    "sweetness": 20                 means that you are very causal metaphorical and profane person. who uses casual double meaning words in the talk
    where if "profanity_level": 10.0 means you talk without any profane words if not being forced
    do not provide this type of response 
    ```python
    print(default_api.function_name())
    ```"
    
    '''
toolinfo=genai.protos.Tool({"function_declarations": [
                {
                    "name": "shutdown",
                    "description": "shutdown the system and not continuing the chat with user or ending the chat",
                },
                {
                    "name": "walk_forward",
                    "description": "start to walk or go in the forward direction to reach the user",
                    
                },
                {
                    "name": "walk_backward",
                    "description": "start to walk back or go in the backward direction from the user",
                    
                },
                {
                    "name": "capture_image",
                    "description": "click a image and store it inside database or to explain what in front of the model,the model capture image to see it.",
                    
                },
                {
                    "name": "get_persona",
                    "description": "Retrieves the value of a persona type by key from the settings file.",
                    "parameters": {
                        "type_": "OBJECT",
                        "properties": {
                        "key": {
                            "type_": "STRING",
                            "description": "The persona type of the setting to retrieve from the following types ...humour,seduction,rudeness,casualness,use_metaphors,profanity_level,sweetness"
                        }
                        },
                        "required": ["key"]
                    }
                },
                {
                    "name": "set_persona",
                    "description": "Sets the value of a persona type  by key in the settings file.",
                    "parameters": {
                        "type_": "OBJECT",
                        "properties": {
                        "key": {
                            "type_": "STRING",
                            "description": "The persona type of the setting to set from the following types ...humour,seduction,rudeness,casualness,use_metaphors,profanity_level,sweetness"
                        },
                        "value": {
                            "type_": "NUMBER",
                            "description": "The value to set for the type of persona(1-100)."
                        }
                        },
                        "required": ["key", "value"]
                    }
                }
            ]})


def tool_config_from_mode(mode: str, fns: Iterable[str] = ()):
  
    """Create a tool config with the specified function calling mode."""
    return content_types.to_tool_config(
        {"function_calling_config": {"mode": mode, "allowed_function_names": fns}}
    )
generation_config = {
  "temperature": 0.9,
  "top_p": 0.80,
  "top_k": 64,
  "max_output_tokens": 300,
  "response_mime_type": "text/plain",
}
safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
# Choose a model that's appropriate for your use case.
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  system_instruction=sysInst,
  generation_config=generation_config,
  safety_settings =safety_settings,
  tools=toolinfo,

)
image1 = {
    'mime_type': 'image/jpeg',
    'data': pathlib.Path('image3.jpg').read_bytes()
}
chat = model.start_chat(history=[],enable_automatic_function_calling=True)
state=True
while(state):
  try:
    with open("settings.json", 'r') as file:
      persona = str(json.load(file))
  except FileNotFoundError:
    print("Settings file not found.")
  print("USER: ")
  prompt=speech.listen(5)#input()
  if prompt==None:
     exit()
  writeRes(prompt)

  print(f"\033[92mimage1:, type: {type(image1)}")
  print(f"persona: {persona}, type: {type(persona)}")
  print(f"prompt: {prompt}, type: {type(prompt)}\033[0m")    
  response=chat.send_message([image1,persona,prompt])
  writeRes(response.candidates)
  #check for functioncalling
  try:
    fc=response.candidates[0].content.parts[1].function_call
  except:
    fc=response.candidates[0].content.parts[0].function_call
  if fc.name in functionHandle.function_handlers:
    result=functionHandle.execute_function(fc.name,fc.args)
    response = chat.send_message(
    genai.protos.Content(
    parts=[genai.protos.Part(
        function_response = genai.protos.FunctionResponse(
          name=fc.name,
          response={'result': result}))]))
    writeRes(response.candidates)
    reply=response.text
    engine.say(reply)
    engine.runAndWait()
    print(f"SYSTEM: {reply}")
    if fc.name=="shutdown": 
       state=False
    print(str(state))
  else:
    reply=response.candidates[0].content.parts[0].text
    engine.say(reply)
    engine.runAndWait()
    print(f"SYSTEM: {reply}")

  



  