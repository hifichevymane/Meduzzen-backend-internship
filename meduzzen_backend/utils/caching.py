import os

from django.core.cache import cache
from dotenv import load_dotenv

load_dotenv()

REDIS_TIMEOUT = int(os.environ.get('REDIS_TIMEOUT', 48)) * 3600

def cache_user_answer(data, quiz_company_id):
    cache_key = f'user_answer_{data["id"]}'
    cache_value = {
        'user': data['user'],
        'company': quiz_company_id,
        'quiz': data['quiz'],
        'question': data['question'],
        'answer': data['answer'],
        'is_correct': data['is_correct']
    }
    cache.set(cache_key, cache_value, REDIS_TIMEOUT)
