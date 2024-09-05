import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from google.generativeai.types import content_types
from collections.abc import Iterable
genai.configure(api_key="YOUR_APIKEY")
calculator=genai.protos.Tool({"function_declarations": [
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
def tool_config_from_mode(mode: str, fns: Iterable[str] = ()):
    """Create a tool config with the specified function calling mode."""
    return content_types.to_tool_config(
        {"function_calling_config": {"mode": mode, "allowed_function_names": fns}}
    )
# Choose a model that's appropriate for your use case.
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  tools=calculator,
  generation_config=generation_config,
  safety_settings =safety_settings,
)
chat = model.start_chat()

response = chat.send_message(
    f"can you increase the humour level"
)
print(response)
