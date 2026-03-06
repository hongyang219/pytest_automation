import os
from openai import OpenAI
from dotenv import load_dotenv

# Online Model
deepseek_url = "https://api.deepseek.com"
DEEPSEEK = "deepseek-reasoner"

# Local Model
ollama_url = "http://localhost:11434/v1"
QWEN = "qwen2.5-coder:7b"
DEEPSEEK_CODER = "deepseek-coder"
DEEPSEEK_R1 = "deepseek-r1:7b"


# API Key
load_dotenv(override=True)
API_KEY = os.getenv('DEEPSEEK_API_KEY')

ONLINE_MODEL = DEEPSEEK
LOCAL_MODEL = QWEN


def initialize_client(llm_type :str = "local"):
    if llm_type == "online":
        client = OpenAI(
            api_key=API_KEY,
            base_url=deepseek_url,
        )
        model = ONLINE_MODEL
    elif llm_type == "local":
        client = OpenAI(
            api_key="ollama",  # 本地部署不需要真实 Key，随便填一个字符串即可
            base_url=ollama_url  # Ollama 的默认本地地址
        )
        model = LOCAL_MODEL
    else:
        print("Please enter either online or local")
        exit()
    return client, model