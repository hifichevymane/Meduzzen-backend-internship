import csv
import datetime
import json

from .caching import get_redis_data_by_key
from .enums import ExportDataFileType


def export_quiz_result(file_type=ExportDataFileType.CSV.value, 
                       user_instance=None, company_instance=None):
    data = []

    if user_instance:
        if company_instance: # Search all quiz results for particular user and company
            data = get_redis_data_by_key('quiz_result_*', 
                                         username=user_instance.username, 
                                         company_name=company_instance.name,
                                         file_type=file_type)
        else: # Search all quiz results for particular user
            data = get_redis_data_by_key('quiz_result_*', 
                                         username=user_instance.username,
                                         file_type=file_type)
    else:
        if company_instance: # Search all quiz results for particular company
            data = get_redis_data_by_key('quiz_result_*', 
                                         company_name=company_instance.name,
                                         file_type=file_type)
    
    filepath = f'exported_data/quiz_result_{datetime.datetime.now()}.csv'

    if file_type == ExportDataFileType.JSON.value:
        data = json.dumps(data, indent=4, default=str)
        filepath = f'exported_data/quiz_result_{datetime.datetime.now()}.json'

    with open(filepath, 'w', newline='') as file:
        if file_type == ExportDataFileType.JSON.value:
            file.write(data)
        else:
            writer = csv.writer(file)
            writer.writerow(['id', 'user', 'company', 'quiz', 'score', 'date passed'])
            for item in data:
                writer.writerow(item)
    
    return filepath
