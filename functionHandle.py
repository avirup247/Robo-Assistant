import speech
import json
file_path="settings.json"
def get_persona(key):
    try:
        with open(file_path, 'r') as file:
            settings = json.load(file)
            return settings.get(key)
    except FileNotFoundError:
        print("Settings file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding the settings file.")
        return None
    

def set_persona(param1,param2):
    if isinstance(param1, str) and isinstance(param2, float):
        key, value = param1, param2
    elif isinstance(param1, float) and isinstance(param2, str):
        key, value = param2, param1
    try:
        with open(file_path, 'r') as file:
            settings = json.load(file)
            settings[key] = value
            try:
                with open(file_path, 'w') as file:
                    json.dump(settings, file, indent=4)
            except Exception as e:
                print(f"Error saving settings file: {e}")
    except FileNotFoundError:
        print("Settings file not found.")
    except json.JSONDecodeError:
        print("Error decoding the settings file.")


def walk_forward():
    print("walking forward")
    return "walking forward"
def walk_backward():
    print("walking backward")
    return "walking backward"
def capture_image():
    print(f"image captured in s")
    return "image captured"
def shutdown():
    print("shutdown successfull")
    return "shutdown successfull"

function_handlers={
  "walk_forward":walk_forward,
  "walk_backward":walk_backward,
  "capture_image":capture_image,
  "shutdown":shutdown,
  "set_persona":set_persona,
  "get_persona":get_persona,

  }
def execute_function(function_name,argument):
    if function_name in function_handlers:
        if function_name == 'set_persona':  # Handle 'set_persona' differently
            key = list(argument.values())[0]  # Extract key and value
            value = list(argument.values())[1]
            function_response = set_persona(key,value)  # Pass as positional args
        else:
            args={key: value for key, value in argument.items()}
            print(args)
            if args: # Check if args is not empty
                function_response=function_handlers[function_name](args['key']) 
            else:
                function_response = function_handlers[function_name]()
        return function_response
    else:
        return -1

print(get_persona("humour"))
