import requests
from bs4 import BeautifulSoup
import os
import string
import sys


def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
Uses a whitelist approach: any characters not present in valid_chars are
removed. Also spaces are replaced with underscores.
 
Note: this method may produce invalid filenames such as ``, `.` or `..`
When I use this method I prepend a date string like '2009_01_15_19_46_32_'
and append a file extension like '.txt', so I avoid the potential of using
an invalid filename.
 
"""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename

def parse_page(url):
    # clue_J_column_row
    
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    links = soup.find_all('a', href=True)

    next_game = ''

    for link in links:
        if link.get_text() == '[next game >>]':
            next_game = link['href']

    categories = soup.find_all('td', {'class' : 'category_name'})
    comments = soup.find_all('td', {'class' : 'category_comments'})

    # singles
    for column in range(1, 7):

        clues = []
        responses = []

        for row in range(1, 6):

            # get the clue
            id = "clue_J_{}_{}".format(column, row)
            s = soup.find('td', {'id': id})

            if s.find('a') != None:
                break

            clues.append("clue: " + s.get_text() + '\n')

            # get the correct response
            id = "clue_J_{}_{}_r".format(column, row)
            s = soup.find('td', {'id': id}).find('em', {'class': 'correct_response'})
            responses.append("response: " + s.get_text() + '\n')

        if len(clues) == 5:
            with open('singles/' + format_filename(categories[column - 1].get_text()), 'w+', encoding="utf-8") as file:
                file.write('category: ' + categories[column - 1].get_text() + '\n')
                file.write('category comment: ' + comments[column - 1].get_text() + '\n\n')
                for n in range(0, 5):
                    file.write(clues[n] + '\n')
                    file.write(responses[n] + '\n')

    # doubles
    for column in range(1, 7):
        clues = []
        responses = []

        for row in range(1, 6):

            # get the clue
            id = "clue_DJ_{}_{}".format(column, row)
            
            s = soup.find('td', {'id': id})

            if s == None or s.find('a') != None:
                break

            clues.append("clue: " + s.get_text() + '\n')

            # get the correct response
            id = "clue_DJ_{}_{}_r".format(column, row)
            s = soup.find('td', {'id': id}).find('em', {'class': 'correct_response'})
            responses.append("response: " + s.get_text() + '\n')

        if len(clues) == 5:
            with open('doubles/' + format_filename(categories[column + 5].get_text()), 'w+', encoding="utf-8") as file:
                file.write('category: ' + categories[column + 5].get_text() + '\n')
                file.write('category comment: ' + comments[column + 5].get_text() + '\n\n')
                for n in range(0, 5):
                    file.write(clues[n] + '\n')
                    file.write(responses[n] + '\n')

    # finals
    final_clue = soup.find('td', {'id': 'clue_FJ'})
    final_response = soup.find('td', {'id': 'clue_FJ_r'}).find('em', {'class': 'correct_response'})

    with open('finals/' + format_filename(categories[12].get_text()), 'w+', encoding="utf-8") as file:
        file.write('category: ' + categories[12].get_text() + '\n')
        file.write('clue: ' + final_clue.get_text() + '\n')
        file.write('response: ' + final_response.get_text() + '\n')

    return 'https://j-archive.com/' + next_game
