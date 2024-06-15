import openai
from keys import KEY_OPENAI

openai.api_key = KEY_OPENAI

print(KEY_OPENAI)

model_engine = "text-davinci-003"
prompt = str(input())

completion = openai.completion.create(
 engine=model_engine,
 prompt=prompt,
 max_tokens=1024,
 n=1,
 stop=None,
 temperature=0.5,
)

response = completion.choices[0].text
print(response)