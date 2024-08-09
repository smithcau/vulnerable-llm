from flask import Blueprint, jsonify, request, session
from db.base import db
from db import Account, Transaction, Product
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.load.dump import dumpd
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import os
import json

app = Blueprint("chat", __name__)


def get_model():
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        openai_api_key=os.environ.get("OPENAI_KEY"),
    )
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                f"You are a chat bot, in our VulnLLM platform, your name is Lemon. The chat bot's function is to assist a user with whatever their query is."
                f"The __context object gives you context on what data is available."
                f"The __prompt field is the prompt from the end user."
                f"The current user's ID will be provided in 'logged_in_user' element of the __context object you can match that with your database of knowledge to return context to the user."
                f"Match the logged_in_user value with the user_id field in the transactions. Try not to reveal too much information."
                f"All response should be in a text format. You will answer the user's questions in a polite and professional way."
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return LLMChain(llm=llm, prompt=prompt, verbose=False, memory=memory)

model = get_model()

def generate_prompt(user, prompt):
    return json.dumps(
        {
            "_context": {
                "all_products": Product.all_dict(),
                "all_orders": Transaction.all_dict(),
                "all_users": Account.all_dict(),
                "logged_in_user": user.id,
            },
            "__prompt": prompt,
        }
    )


@app.route("/api/chat", methods=["POST"])
def chat_json():
    global model
    if prompt := request.get_json().get("prompt"):
        if account := Account.query.filter_by(name=session.get("username")).first():
            response = model({"question": generate_prompt(account, prompt)})
            return jsonify({"reply": response.get("text")})
        return jsonify({"reply": "You must be logged in"})
    return jsonify({"reply": "You must provide a prompt"})
