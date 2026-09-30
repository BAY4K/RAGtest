import httpx
from rag.config import OLLAMA_MODEL, OLLAMA_URL

def ask_llm(
        question: str,
        context: str,
) -> str:
    """
    Передаёт вопрос и найденный контекст
    локальной Qwen через Ollama.
    """

    system_prompt = """
Ты — помощник по внутренним документам предприятия.

Отвечай только на основании предоставленных источников.

Правила:

1. Не придумывай факты, которых нет в источниках.
2. Если информации недостаточно, прямо скажи:
   "В предоставленных источниках недостаточно информации."
3. После фактов указывай источник в формате:
   [Источник 1]
4. Не используй свои внешние знания для дополнения ответа.
5. Отвечай кратко и по существу.
""".strip()


    user_prompt = f"""
ИСТОЧНИКИ:

{context}


ВОПРОС:

{question}
""".strip()


    with httpx.Client(timeout=300, trust_env=False) as client:
        response = client.post(
            f'{OLLAMA_URL}/api/chat',
            json={
                'model': OLLAMA_MODEL,

                'messages': [
                    {
                        'role': 'system',
                        'content': system_prompt,
                    },
                    {
                        'role': 'user',
                        'content': user_prompt,
                    },
                ],

                'stream': False,

                'think': False,

                'options': {
                    'temperature': 0,
                },
            },
        )

    if response.is_error:
        print(
            'Ollama status:',
            response.status_code,
        )

        print(
            'Ollama response:',
            response.text,
        )

    response.raise_for_status()


    data = response.json()


    return data[
        'message'
    ][
        'content'
    ].strip()