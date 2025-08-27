from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()

def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"

# ✅ FIXED: now accepts 4 arguments
def generate_post(length, language, tag, tone="Professional"):
    length_str = get_length_str(length)

    prompt = f'''
You're a LinkedIn post expert. Based on the details below, generate:

1. A high-quality LinkedIn post.
2. A catchy title (like a post headline).
3. A one-line summary (not just the first line).

Respond using this exact format:
<post>
[Generated Post]
</post>
<title>
[Catchy Title]
</title>
<summary>
[One-line Summary]
</summary>

DETAILS:
Topic: {tag}
Length: {length_str}
Language: {language}
Tone: {tone}

If Language is Hinglish, use English script with Hindi-English mix.
'''

    examples = few_shot.get_filtered_posts(length, language, tag)
    if len(examples) > 0:
        prompt += "\n\nUse style inspired by examples:"
        for i, post in enumerate(examples[:2]):
            prompt += f"\n\nExample {i+1}:\n{post['text']}"

    response = llm.invoke(prompt)
    full_output = response.content.strip()

    if "</think>" in full_output:
        full_output = full_output.split("</think>", 1)[-1].strip()

    # Parse output
    post = full_output.split("<post>")[1].split("</post>")[0].strip()
    title = full_output.split("<title>")[1].split("</title>")[0].strip()
    summary = full_output.split("<summary>")[1].split("</summary>")[0].strip()

    return post, title, summary
