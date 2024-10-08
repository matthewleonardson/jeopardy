import os
import random
import re
import csv

directory = "singles"
round = 'jeopardy'
files = random.choices(os.listdir(directory), k=10)
selection_string = ""
chosen_categories = ["", "", "", "", "", "", "", "", "", ""]
chosen_index = 0


def generate_dd_location():
    first = random.randint(1, 10)
    second = random.randint(0, 5)

    if(first == 1):
        first = 1
    elif(first <= 4):
        first = 2
    elif(first <= 7):
        first = 3
    elif(first <= 10):
        first = 4

    return (first, second)

dd1 = generate_dd_location()
dd2 = generate_dd_location()
dd3 = generate_dd_location()

while (dd3 == dd2):
    dd3 = generate_dd_location()

csv_file = open('game.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)

def clear(s):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(s)

def preview(files, index):
    #clear("")
    #with open('singles/' + files[index], 'r') as f:
        #print(f.read())

    os.system("notepad.exe " + os.path.abspath(directory + '/' + files[index]))

def generate_selection_string():
    selection_string = "{0:<35} {1:<35}\n\n".format("POTENTIAL CATEGORIES", "CHOSEN CATEGORIES")
    for n in range(0, 10):
        selection_string += "{0}: {1:<35} {2:<35}\n".format(n, files[n], chosen_categories[n])
    return selection_string

def push_thing():
    if round != 'final':        
        for category in range(0, 6):
            with open(directory + '/' + chosen_categories[category], 'r', encoding='utf-8', newline='') as cat:
                lines = cat.readlines()
                category_name = " ".join(lines[0].split()[1:])
                for n in range(0, 5):

                    boolean = 'False'
                    if (n, category) == dd1 and round == 'jeopardy':
                        boolean = 'TRUE'

                    if ((n, category) == dd2 or (n, category) == dd3) and round == 'double':
                        boolean = 'TRUE'
                    
                    if round == 'double':
                        is_double = 2
                    else:
                        is_double = 1

                    writer.writerow([round, '"{}"'.format(category_name), str(200 * is_double * (n + 1)), '"{}"'.format(" ".join(lines[3 + 4 * n].split()[1:])), '"{}"'.format(" ".join(lines[5 + 4 *  n].split()[1:])), boolean, "", "", ""])
    else:
        with open(directory + '/' + chosen_categories[0], 'r', newline='') as cat:
            lines = cat.readlines()
            category_name = " ".join(lines[0].split()[1:])
            writer.writerow([round, '"{}"'.format(category_name), str(0), '"{}"'.format(" ".join(lines[1].split()[1:])), '"{}"'.format(" ".join(lines[2].split()[1:])), 'False', "", "", ""])

    for category in chosen_categories:
        if category != "":
            os.renames(directory + "/" + category, directory + "_used/" + category)             

selection_string = generate_selection_string()
writer.writerow(['round', 'cat', 'val', 'q', 'a', 'dd', 'type', 'topCaption', 'bottomCaption'])

while(True):

    clear(selection_string)

    i = input('JepOS: ')

    # preview a file
    if re.search(r"preview \d", i.lower()):
        preview(files, int(i.lower()[-1]))
        
    # select a file    
    elif re.search(r"select \d", i.lower()):
        chosen_categories[chosen_index] = files[int(i.lower()[-1])]
        chosen_index += 1
        selection_string = generate_selection_string()

    # refresh choices
    elif i.lower() == 'refresh':
        files = random.choices(os.listdir(directory), k = 10)
        selection_string = generate_selection_string()

    # delete a choice
    elif re.search(r"delete \d", i.lower()):
        del chosen_categories[int(i.lower()[-1])]
        chosen_categories.append("")
        chosen_index -= 1
        selection_string = generate_selection_string()

    elif i.lower() == 'confirm':
        push_thing()
        if directory == 'singles':
            round = 'double'
            directory = 'doubles'
        elif directory == 'doubles':
            round = 'final'
            directory = 'finals'
        else:
            csv_file.close()

            with open('game.csv', 'r', encoding='utf-8') as finished_file:
                filedata = finished_file.read()

            filedata.replace('"""', '"')

            with open('game.csv', 'w', encoding='utf-8') as finished_file:
                finished_file.write(filedata)

            exit(0)
        chosen_categories = ["", "", "", "", "", "", "", "", "", ""]
        chosen_index = 0
        files = random.choices(os.listdir(directory), k = 10)
        selection_string = generate_selection_string()
        
    # exit terminal
    elif i.lower() == 'exit':
        clear("")
        exit(1)
