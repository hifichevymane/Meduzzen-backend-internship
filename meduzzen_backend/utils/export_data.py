import csv
import datetime
import json

from .enums import ExportDataFileType


def export_quiz_result(data, file_type=ExportDataFileType.CSV.value):
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
