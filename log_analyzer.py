
try:
    lst = []
    code_dict = {}
    error_lines = []
    with open('log.txt', 'r', encoding='utf-8') as log:
        data = list(log)

        for i in data:
            key_value = [' '.join(i.split(" ")[:2]), ' '.join(i.split(" ")[2:])]
            
            if code_dict.get(key_value[1].split(" ")[0]) == None:
                code_dict[key_value[1].split(" ")[0]] = 1
            else:
                code_dict[key_value[1].split(" ")[0]] += 1
            
            if key_value[1].split(" ")[0] == "ERROR":
                error_lines.append(i)

            lst.append(key_value)
    
    with open('error.txt', 'w', encoding='utf-8') as error:
        error.writelines(error_lines)

    
    print(code_dict)

    lst = sorted(lst, key=lambda value: value[0])

    with open('log.txt', 'w', encoding='utf-8') as log:
        for i in lst:
            log.write(' '.join(i))


except FileNotFoundError:
    print("No such file or directory")
