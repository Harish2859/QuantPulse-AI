import traceback
from dotenv import load_dotenv
from app.agents.researcher import run_research

load_dotenv()

try:
    print(run_research('AAPL'))
except Exception as exc:
    traceback.print_exc()
