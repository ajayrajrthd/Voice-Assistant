from flask import Flask, request, jsonify, render_template
import asyncio
from src.agents.agent import Agent
from src.tools.calendar.calendar_tool import CalendarTool
from src.tools.contacts import AddContactTool, FetchContactTool
from src.tools.emails.emailing_tool import EmailingTool
from src.tools.search import SearchWebTool, KnowledgeSearchTool
from src.speech_processing.conversation_manager import ConversationManager
from src.prompts.prompts import assistant_prompt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

model = "groq/llama3-70b-8192"

tools_list = [
    CalendarTool,
    AddContactTool,
    FetchContactTool,
    EmailingTool,
    SearchWebTool,
    KnowledgeSearchTool
]

agent = Agent("Assistant Agent", model, tools_list, system_prompt=assistant_prompt)
manager = ConversationManager(agent)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json['message']
    response = asyncio.run(manager.ask(user_input))
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
