import openai

openai.api_key = "YOUR_API_KEY"
messages = [{"role": "system", "content": "You are a helpful assistant."},]

while (request := input("\nUSER: ")) != 'quit':
    messages.append({"role": "user", "content": request})

    try:
        response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages, stream=True)
        content = '' 
        print("CHATGPT: ", end='')
        
        for chunk in response:  
            message = chunk['choices'][0]['delta'].get('content', '')
            content += message
            print(message, end='', flush=True)

        messages.append({"role": "assistant", "content": content})

    except Exception as e:
        print(f"An error occurred: {e}")
        break