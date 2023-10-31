import os

from django.core.cache import cache
from dotenv import load_dotenv

from .enums import ExportDataFileType

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


def cache_quiz_result(instance):
    cache_key = f'quiz_result_{instance.id}'

    cache_value = {
        'id': instance.id,
        'user': instance.user.username,
        'company': instance.company.name,
        'quiz': instance.quiz.title,
        'score': instance.score,
        'date_passed': instance.updated_at,
    }

    cache.set(cache_key, cache_value, REDIS_TIMEOUT)


def get_redis_data_by_key(search_key, 
                          username=None, 
                          company_name=None, 
                          file_type=ExportDataFileType.CSV.value):
    keys = cache.keys(search_key)
    data = []

    # If username is passed
    if username:
        if company_name: # If username and company_name are passed
            for key in keys:
                value = cache.get(key)
                if value['user'] == username and value['company'] == company_name:
                    if file_type == ExportDataFileType.CSV.value:
                        data.append((*value.values(), ))
                    else:
                        data.append(value)
        else:
            for key in keys:
                value = cache.get(key)
                if value['user'] == username:
                    if file_type == ExportDataFileType.CSV.value:
                        data.append((*value.values(), ))
                    else:
                        data.append(value)
    # If username is not passed
    else:
        if company_name:
            for key in keys:
                value = cache.get(key)
                if value['company'] == company_name:
                    if file_type == ExportDataFileType.CSV.value:
                        data.append((*value.values(), ))
                    else:
                        data.append(value)
    
    return data
