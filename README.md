# reasoning-agent

Entire project is done in 1 python file ( reasoningagent.py )

Problem:

Build a small “reasoning agent” that can solve structured problems in multiple
steps, check its own work, and only show the final answer to the user. You may
use any LLM API you like (OpenAI, Anthropic, Gemini etc.) and any
programming language.
The input is a plain text question.
The output should be a JSON object with this schema:
{
"answer": "<final short answer, user-facing>",
"status": "success" | "failed",
"reasoning_visible_to_user": "<short explanation, but no raw chain-of-thought
logs>",
"metadata": {
"plan": "<model's internal plan, can be abbreviated>",
"checks": [
{
"check_name": "<string>",
"passed": true,
"details": "<string>"
}
],
"retries": <integer>
}
}

Prerequisites:
pip install streamlit
pip install openai

The project is a streamlit program as seen below, input API key first to be able to proceed further

<img width="500" height="280" alt="Screenshot (123)" src="https://github.com/user-attachments/assets/eaf7b3fc-3f17-43c3-9cb7-da4b9a992297" />

After inputting API key, enter the question you want the reasoning for(or select from the given testsuite)

<img width="500" height="280" alt="Screenshot (124)" src="https://github.com/user-attachments/assets/7acd75db-ca74-4ef8-b2fd-a184cb39628f" />

Now the GPT-4o-mini will give the answer and also give the reasoning in the schema as asked by the problem

<img width="500" height="280" alt="Screenshot (125)" src="https://github.com/user-attachments/assets/988b28fe-ce40-4755-a9b7-22f830fc9a9e" />

