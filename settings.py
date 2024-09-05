import json

def get_setting(key):
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
    

def set_setting(key, value):
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

# Example usage
file_path = 'settings.json'
print(get_setting('persona'))

