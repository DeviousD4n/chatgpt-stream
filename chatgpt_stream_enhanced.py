import sys
import openai

openai.api_key = "YOUR_API_KEY"
messages = [{"role": "system", "content": "You are a command line tool running on " + str(dict(line.strip().split('=') for line in open('/etc/os-release', 'r')).get('PRETTY_NAME', '')) + ". Succinct replies are better than long-winded explanations."}]

BOLD = "\033[1m"
ITALIC = "\033[3m"
RESET = "\033[0m"
GPTCOLOR = "\033[38;5;57m"
BLOCKCOLOR = "\033[38;5;200m"
USERCOLOR = "\033[38;5;75m"

def send_request(content):
    messages.append({"role": "user", "content": content})
    try:
        response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages, stream=True)
        print(f"{RESET + GPTCOLOR}GPT: ", end='')
        return handle_stream(response)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def handle_stream(response):
    code_block = False
    buffer = ''
    content = ''

    for chunk in response:
        message = chunk['choices'][0]['delta'].get('content', '')
        content += message

        for c in message:
            buffer += c

            if buffer.endswith('```'):
                code_block = not code_block
                buffer = ''

            elif len(buffer) > 3:
                print(f"{ITALIC + BLOCKCOLOR if code_block else RESET + GPTCOLOR}{buffer[0]}", end='', flush=True)
                buffer = buffer[1:]

    print(f"{BLOCKCOLOR if code_block else GPTCOLOR}{buffer}")
    return content 

if len(sys.argv) > 1:
    send_request(sys.argv[1])
else:
    while (request := input(f"\n{BOLD + USERCOLOR}USER: ")) not in ('quit', 'exit'):
        content = send_request(request)
        messages.append({"role": "assistant", "content": content})