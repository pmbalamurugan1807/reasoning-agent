import streamlit as st
import json
from openai import OpenAI

st.set_page_config(page_title="Reasoning Agent", layout="centered")
st.title("Reasoning Agent (GPT-4o-mini)")

# ---------------- Sidebar: Test Suite ---------------- #

st.sidebar.header("Test Suite")

easy_questions = [
    "What is the sum of 12 and 8?",
    "If one pen costs 10 and I buy 3, what is the total cost?",
    "What is 45 minus 17?",
    "A train travels for 2 hours at 30 km per hour. How far does it go?",
    "If a movie starts at 3:00 PM and lasts 90 minutes, when does it end?"
]

tricky_questions = [
    "John has 3 boxes with 5 apples each and eats 4 apples. How many apples remain?",
    "A shop gives a 10% discount on a 500 item and then adds 18% tax. What is the final price?",
    "A train departs at 11:50 PM and travels for 30 minutes. What time does it arrive?"
]

easy_choice = st.sidebar.selectbox(
    "Easy Questions",
    ["-- Select an easy question --"] + easy_questions
)

tricky_choice = st.sidebar.selectbox(
    "Tricky Questions",
    ["-- Select a tricky question --"] + tricky_questions
)

if easy_choice != "-- Select an easy question --":
    question_value = easy_choice
elif tricky_choice != "-- Select a tricky question --":
    question_value = tricky_choice
else:
    question_value = ""

# ---------------- Main UI ---------------- #

api_key = st.text_input("Enter your OpenAI API Key", type="password")

question = st.text_area(
    "Enter a question (or select from test suite)",
    value=question_value,
    height=100
)

run = st.button("Solve")

# ---------------- Reasoning Agent ---------------- #

def reasoning_agent(client, question, max_retries=2):
    retries = 0
    checks = []
    plan = "Understand → reason internally → compute answer → validate"

    system_prompt = """
You are a reasoning agent.

Rules:
- Reason internally.
- DO NOT reveal chain-of-thought.
- Provide only a short explanation.
- Output ONLY a valid JSON object in the exact schema below.

Schema:
{
  "answer": "<final short answer>",
  "status": "success" | "failed",
  "reasoning_visible_to_user": "<brief explanation>",
  "metadata": {
    "plan": "<short plan>",
    "checks": [],
    "retries": 0
  }
}
"""

    while retries <= max_retries:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0
            )

            raw_output = response.choices[0].message.content
            result = json.loads(raw_output)

            passed = bool(result.get("answer"))
            checks.append({
                "check_name": "non_empty_answer",
                "passed": passed,
                "details": "Answer present" if passed else "Answer missing"
            })

            if passed:
                result["metadata"]["plan"] = plan
                result["metadata"]["checks"] = checks
                result["metadata"]["retries"] = retries
                return result

            retries += 1

        except Exception as e:
            retries += 1
            last_error = str(e)

    return {
        "answer": "",
        "status": "failed",
        "reasoning_visible_to_user": "Unable to solve the problem reliably",
        "metadata": {
            "plan": plan,
            "checks": checks,
            "retries": retries,
            "error": last_error
        }
    }

# ---------------- Run ---------------- #

if run:
    if not api_key:
        st.error("Please enter your API key")
    elif not question.strip():
        st.error("Please enter or select a question")
    else:
        client = OpenAI(api_key=api_key)
        with st.spinner("Reasoning..."):
            result = reasoning_agent(client, question)

        st.subheader("Output")

        st.json(result)
