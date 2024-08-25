import json
from openai import OpenAI
import os

choice_base_desc = "这是一个选择题，请严格按照以下格式回答：芝麻开门#你的答案#芝麻开门\n"


def get_gpt_response(content):
    client = OpenAI(
        api_key=os.getenv("QIANWEN"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-turbo",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': choice_base_desc + content}],
        temperature=0.8,
        top_p=0.8
    )
    content = completion.model_dump_json()
    data = json.loads(content)
    extracted_content = data['choices'][0]['message']['content']

    return extract_answer(extracted_content)


def extract_answer(content):
    parts = content.split('#')
    if len(parts) >= 3:
        return parts[1]
    else:
        return ""
