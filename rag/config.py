import os


TOP_K = 3

embedding_model = 'intfloat/multilingual-e5-base'

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://127.0.0.1:11434",
)

OLLAMA_MODEL = os.getenv(
    'OLLAMA_MODEL',
    'qwen3.5:9b-q4_K_M',
)