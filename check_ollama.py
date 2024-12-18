import ollama
prompt1 = 'What is the capital of France?'
response = ollama.chat(model='mistral', messages=[
            {'role': 'user','content': prompt1,},])
r1 = response['message']['content']
print(r1)
