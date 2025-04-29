import time, sys, os, datetime, csv, json

def is_last_line_blank(csv_filepath):
    with open(csv_filepath, 'r') as file:
        file.seek(0, 2)
        end_position = file.tell()

        if end_position == 0:
            return True

        while end_position > 0:
            end_position -= 1
            file.seek(end_position)
            char = file.read(1)
            if char == '\n':
                last_line = file.readline()
                return not last_line.strip()
        
        file.seek(0)
        last_line = file.read()
        return not last_line.strip()

def reg_log(path, content):
    input = ([str(content['date']), str(content['time']), str(content['username']), str(content['operation']), str(content['first_number']), str(content['second_number']), str(content['result']), str(content['comment'])]) 
    file = ''
    json_content = {
        'date': content['date'],
        'time': content['time'],
        'user': content['username'],
        'operation': content['operation'],
        'first number': content['first_number'],
        'second number': content['second_number'],
        'result': content['result'],
        'comment': content['comment']
    }

    if not os.path.exists(path.replace(".csv", ".json")):
        json_input = {'logs': [json_content]}
        with open(path.replace(".csv", ".json"), mode="w", encoding="utf-8") as write_file:
            json.dump(json_input, write_file, indent=3)
            write_file.close()
    else:
        json_input = json.loads(open(path.replace(".csv", ".json"), "r").read())
        json_input["logs"].append(json_content)
        with open(path.replace(".csv", ".json"), mode="w", encoding="utf-8") as write_file:
            json.dump(json_input, write_file, indent=3)
            write_file.close()

    if os.path.exists(path):
        with open(path, "r+") as file:
            file.seek(0)
            first_line = file.readline()
            if first_line.strip() != 'date,time,username,operation,first_number,second_number,result,id,comment' or first_line.strip() == '':
                
                file.seek(0)
                temp_cont = file.read()
                temp_cont += '\n' if not is_last_line_blank(path) else ''
                file.close()
                open(path, "w").close()
                file = open(path, "r+")
                file.write('date,time,username,operation,first_number,second_number,result,id,comment\n' + temp_cont) if first_line.strip() != '' else file.write('date,time,username,operation,first_number,second_number,result,id,comment' + temp_cont + '\n')
                file.seek(0, 2)
                
            if (not is_last_line_blank(path)):
                file.write('\n')
            writer = csv.writer(file)
            writer.writerow(input)
    else:
        with open(path, "w") as file:
            writer = csv.writer(file)
            writer.writerow(('date', 'time', 'username', 'operation', 'first_number', 'second_number', 'result', 'id', 'comment'))
            writer.writerow(input)

    

def print_log(path):
    print("\n---------- LOG INIT ----------\n")
    log_row = open(path, "r").read().split('\n')
    del log_row[0]
    log_row.pop()
    for row in log_row:
        try:
            cols = row.split(',')
            print(cols)
            comment = ''
            for col in cols[7:len(cols)]:
                comment += col
            print('Date: ' + cols[0] + ' ' + cols[1] + ' | User: ' + cols[2] + ' | Operation: ' + cols[3] + ' | Numbers: ' + cols[4] + ' e ' + cols[5] + ' | Result: ' + cols[6] + ' | Comment: ' + comment)
        except:
            print('Invalid row: ' + row)
    print("\n---------- LOG END ----------\n")

def init_calc(user):
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month) if now.month > 10 else "0" + str(now.month)
    day = str(now.day)
    date = year + "-" + month + "-" + day
    time_now = str(now.hour) + ":" + (str(now.minute) if len(str(now.minute)) > 1 else "0" + str(now.minute)) + ":" + str(now.second)
    
    print('Choos one of the options below:\n 1 - Sum\n 2 - Subtract\n 3 - Multiply\n 4 - Divide\n 5 - See logs\n 0 - End program\n')
    option = str(input('\nType the number (1/2/3/4/5/0) to select one option: '))
    if option in ['1', '2', '3', '4', '5', '0']:
        if option != '0' and option != '5':
            nums = get_numbers()
            os.system('clear')
            res = do_the_math(option, nums)
            comment = get_comment_q()
            operation = [
                "Sum",
                "Subtract",
                "Multiply",
                "Divide"
            ]
            content = {
                "date": date,
                "time": time_now,
                "username": user,
                "operation": operation[int(option) - 1],
                "first_number": nums[0],
                "second_number": nums[1],
                "result": res,
                "comment": comment
            }
            reg_log("./calc/calc_log.csv", content)
            print("\n---------- CALCULATION MADE ----------\n")
            return init_calc(user)
        elif option == '5':
            os.system('clear')
            print_log("./calc/calc_log.csv")
            return init_calc(user)
        elif option == '0':
            os.system('clear')
            print("\n---------- PROGRAMM CLOSED ----------\n")
            return -1
    else:
        print('\nInvalid option, please try again')
        sys.stdout.flush()
        time.sleep(1)
        os.system('clear')
        sys.stdout.flush()
        return init_calc(user)

def get_number():
    try:
        num = float(input('\nAdd a number: '))
        return num
    except:
        print('\nPlease, add a valid number', end='\r')
        sys.stdout.flush()
        time.sleep(1)
        print(" " * 80, end='\r') # Clear the line
        sys.stdout.flush()
        return get_number()    

def get_numbers():
    num_1 = get_number()
    num_2 = get_number()
    return [num_1, num_2]

def get_comment_q():
    print('\n')
    add_comment = input('Would you like to add a comment? [y/n] ')
    if add_comment.lower() == 'n':
        return ''
    elif add_comment.lower() == 'y':
        comment = input('Comment: ')
        print('\n')
        return comment
    else:
        print('Invalid option, please use "y" (yes) or "n" (no)\n')
        return get_comment_q()
        

def do_the_math(opt, nums):
    print('\nDoing the math...')
    res = ''
    if opt == '1':
        print('\Result: ', nums[0], ' + ', nums[1], ' = ', nums[0] + nums[1], '\n')
        res = nums[0] + nums[1]
    elif opt == '2':
        print('\nResult: ', nums[0], ' - ', nums[1], ' = ', nums[0] - nums[1], '\n')
        res = nums[0] - nums[1]
    elif opt == '3':
        print('\nResult: ', nums[0], ' * ', nums[1], ' = ', nums[0] * nums[1], '\n')
        res = nums[0] * nums[1]
    else:
        print('\nResult: ', nums[0], ' / ', nums[1], ' = ', nums[0] / nums[1], '\n')
        res = nums[0] / nums[1]

    return res

print('\n---------- INITIATING PYTHON CALCULATOR ----------\n')
user = input("Username: ")
print('\n')

option = init_calc(user)
