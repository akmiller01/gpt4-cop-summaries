import os
from openai import OpenAI
from dotenv import load_dotenv
import io
import tiktoken
import math
import click
import time


load_dotenv()
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

MODEL = "gpt-4-1106-preview"


def warn_user_about_tokens(tokenizer, text):
    token_cost = 0.01
    token_count = len(tokenizer.encode(text))
    return click.confirm(
        "This will use at least {} tokens and cost at least ${} to run. Do you want to continue?".format(
        token_count, round((token_count / 1000) * token_cost, 2)
    )
    , default=False)

if __name__ == '__main__':
    tokenizer = tiktoken.encoding_for_model(MODEL)
    with open("cop26_glasgow_climate_pact.txt", "r") as cop26_file:
        cop26_full_text = cop26_file.read()

    with open("cop27_sharm_el-Sheikh_implementation_plan.txt", "r") as cop27_file:
        cop27_full_text = cop27_file.read()

    with open("cop28_draft.txt", "r") as cop28_file:
        cop28_full_text = cop28_file.read()

    cop26_question = """
        Below is the text of the Glasgow Climate Pact, the result of COP26.
        In a paragraph or two, and without using bullets, please summarize the most important points:
        {}
    """.format(cop26_full_text)

    cop27_question = """
        Below is the text of the Sharm el-Sheikh Implementation Plan, the result of COP27.
        In a paragraph or two, and without using bullets, please summarize the most important points:
        {}
    """.format(cop27_full_text)

    cop28_question = """
        Below is the draft text of the proposal for COP28 by the President of the summit, Dr. Sultan Ahmed Al Jaber.
        In a paragraph or two, and without using bullets, please summarize the most important points:
        {}
    """.format(cop28_full_text)

    meta_question = """
        Below are three summaries you wrote earlier for COP26, COP27, and COP28.
        In a paragraph or two, and without using bullets, please compare and contrast the COP summit outcomes.
        COP26:
        {}
        COP27:
        {}
        COP28:
        {}
    """

    all_input_tokens = cop26_question + cop27_question + cop28_question + meta_question

    if warn_user_about_tokens(tokenizer, all_input_tokens) == True:
        if(os.path.exists("cop26_summary.txt")):
            with open("cop26_summary.txt", "r") as cop26_summary_file:
                cop26_summary = cop26_summary_file.read()
        else:
            cop26_response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "user", "content": cop26_question}
                ]
            )
            cop26_summary = cop26_response.choices[0].message.content
            with open("cop26_summary.txt", "w") as cop26_summary_file:
                cop26_summary_file.write(cop26_summary)
            time.sleep(60)

        if(os.path.exists("cop27_summary.txt")):
            with open("cop27_summary.txt", "r") as cop27_summary_file:
                cop27_summary = cop27_summary_file.read()
        else:
            cop27_response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "user", "content": cop27_question}
                ]
            )
            cop27_summary = cop27_response.choices[0].message.content
            with open("cop27_summary.txt", "w") as cop27_summary_file:
                cop27_summary_file.write(cop27_summary)
            time.sleep(60)

        if(os.path.exists("cop28_summary.txt")):
            with open("cop28_summary.txt", "r") as cop28_summary_file:
                cop28_summary = cop28_summary_file.read()
        else:
            cop28_response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "user", "content": cop28_question}
                ]
            )
            cop28_summary =  cop28_response.choices[0].message.content
            with open("cop28_summary.txt", "w") as cop28_summary_file:
                cop28_summary_file.write(cop28_summary)
            time.sleep(60)

        meta_question_filled = meta_question.format(
            cop26_summary,
            cop27_summary,
            cop28_summary
        )
        if(os.path.exists("meta_answer.txt")):
            with open("meta_answer.txt", "r") as meta_answer_file:
                meta_answer = meta_answer_file.read()
        else:
            meta_response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "user", "content": meta_question_filled}
                ]
            )
            meta_answer = meta_response.choices[0].message.content
            with open("meta_answer.txt", "w") as meta_answer_file:
                meta_answer_file.write(meta_answer)

        print("Q: {}".format(meta_question_filled))
        print("A: {}".format(meta_answer))