import openai
import config
import datetime
import os
from colorama import Fore, Style, init

def main():
    PATH = os.path.dirname(os.path.abspath(__file__))
    print(PATH)
    # colored text headers
    init()
    user_header = Style.BRIGHT + "\x1b[38;2;65;66;250m" + "user: " + Style.RESET_ALL
    GPT_header = Style.BRIGHT + "\x1b[38;2;32;32;122m" + "GPT: " + Style.RESET_ALL
    
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    openai.api_key = config.OPENAI_API_KEY
    
    while True:
        user_input = input(user_header)
        # exit condition
        if user_input == "!Q":
            return
        # promp save
        if user_input == "!SAVE":
            parsed_messages = []
            for i in messages:
                parsed_messages.append(f"{i['role']}: {i['content']}\n")
            
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
            try:
                # save raw messages
                with open(file=f'{PATH}\log\{timestamp}.txt', mode='w', encoding='utf-8') as f:
                    f.write(str(messages))
                #save formatted messages
                with open(file=f'{PATH}\log\\f-{timestamp}.txt', mode='w', encoding='utf-8') as f:
                    for i in parsed_messages:
                        f.write(i)
            except IOError:
                print("Error: Could not create file.")
            print(GPT_header + 'Your file has been saved! Let me know if you need any further assistance.')
            continue
            
        
        messages.append({"role": "user", "content": user_input})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        print(GPT_header + response['choices'][0]['message']['content'])
        
        messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
            
            
def split_string(string):
    substr = "}, {'"
    result = []
    start = 0
    while True:
        idx = string.find(substr, start)
        if idx == -1:
            result.append(string[start:].strip())
            break
        else:
            result.append(string[start:idx+2].strip())
            start = idx + 2 + string[idx+2:].find(' ') + 1
    return result


if __name__ == '__main__':
    main()

