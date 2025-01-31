import re
from datetime import datetime

def logs_parser(file: str) -> list:
    log_data = []

    with open(file, 'r', encoding='utf-8') as log:

        regex = r'(\d{4} \w{3} \d{2} \d{2}:\d{2}:\d{2}) (\w+)\s?(\w*): (\S+) (.*)'

        for line in log:
            match = re.match(regex, line)

            if match:
                date = datetime.strptime(match.group(1), "%Y %b %d %H:%M:%S")
                event = match.group(2)
                source = match.group(3) if match.group(3) else "Unknown"
                code = match.group(4)
                content = match.group(5)
            else:
                print(f'No match found for: {line}')
            
            log_data.append({
                    'date' : date,
                    'event' : event,
                    'source' : source,
                    'code' : code,
                    'content' : content
                    })

    return log_data


def logs_sorter(logs: list) -> list:
    sorted_log = sorted(logs, key=lambda item: item['date'])

    with open('sorted_logs.txt', 'w', encoding='utf-8') as sl:
        for line in sorted_log:
            sl.write(f'{line['date']} {line['event']} {line['source']} : {line['code']} {line['content']}\n')
        
    return sorted_log    


def unique_parameters_set(logs: list, parameter: str) -> list:
    unique_parameters = list(set(line[parameter] for line in logs))
    return unique_parameters


def logs_counter(logs: list, parameters: list, parameter: str) -> dict:
    uniq_params_counter = {}
    for param in parameters:
        cntr = 0
        for line in logs:
            if line[parameter] == param:
                cntr += 1
                uniq_params_counter[param] = cntr

    return uniq_params_counter


def split_logs_by_event(logs: list, events: list):
    for event in events:
        with open(f'{event}.txt', 'a', encoding='utf-8') as evnt:
            for line in logs:
                if line['event'] == event:
                    evnt.write(f'{line['date']} {line['event']} {line['source']} : {line['code']} {line['content']}\n')
    

try:

    file = 'messages_SYS.log'
    log_data = logs_parser(file)
    sorted_log = logs_sorter(log_data)
    unique_events = unique_parameters_set(sorted_log, 'event')
    uniq_events_counter = logs_counter(sorted_log, unique_events, 'event')
    split_logs_by_event(sorted_log, unique_events)
    print(f"Earliest record: {sorted_log[0]['date']};\nLatest record: {sorted_log[-1]['date']};\n{uniq_events_counter}\nList of unique events: {unique_parameters_set(sorted_log, 'content')}")

except FileNotFoundError:
    print('No such file or directory')
