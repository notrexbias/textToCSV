import csv
import re

# open the text file
file = open('gre_vocab_text.txt', 'r')

# number followed by period pattern e.g. 1. or 233.
subjectpattern = re.compile(r'^(\d)+(\.)')

mydict = {}
# mydict = { subjectnumber : [ subject, synonym, meaning, example] }
# e.g. mydict = { 1 : [ 'angry', 'fume',
# 'feel or express great anger.', 'She sat in the car, silently Fuming at the traffic jam.'] }

# create and open a new csv file
with open('gre_vocab_csv.csv', 'w') as csvfile:
    wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    wr.writerow(['SUBJECT', 'SYNONYM', 'MEANING', 'EXAMPLE'])
    for line in file:  # loop over each line in the text file
        strippedline = line.rstrip().lstrip()  # strip spaces and new line characters from line
        match = subjectpattern.search(strippedline)  # search for our pattern
        # the idea is to match the pattern above, then take the line with the pattern, split it by the period(.),
        # take the word i.e. 1. Angry, when split, becomes ['1', 'angry'], the subject is the second element of the
        # split and subjectnumber is the first element of the split. For lines with '=', we split by the '=' and take
        # the first element as the synonym and the second as the meaning For lines with ':', we split by the ':' and
        # take the second as the example. It turns out there are lines where the subject is in a new line, so for that
        # we pick those words that do not fit our other conditions and check if we have a subject in the current list,
        # if not, we push the word
        if match:
            subject = strippedline.split('.')
            word = subject[1].rstrip().lstrip()
            mydict[subject[0]] = [word]
        elif '=' in strippedline:
            synonym = strippedline.split('=')
            mydict[subject[0]].append(synonym[0].rstrip().lstrip())
            mydict[subject[0]].append(synonym[1].rstrip().lstrip())
        elif ':' in strippedline:
            example = strippedline.split(':')
            mydict[subject[0]].append(example[1].rstrip().lstrip())
            wr.writerow(mydict[subject[0]])
            del mydict[subject[0]][1:len(mydict[subject[0]])]
        elif strippedline != '' and mydict[subject[0]][0] == '':
            mydict[subject[0]][0] = strippedline
file.close()
csvfile.close()

# todo there are some examples that are broken into two by a newline character, find a way of appending it to the end
#  of the example.
