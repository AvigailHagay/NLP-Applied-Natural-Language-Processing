import re
import math
import pandas as pd


def edit_word(word):

    word = re.sub(r'[^\w\s]', '', word)  # remove punctuation marks
    word = word.lower()  # lowercase the words

    if re.match(r"^[0-9]+$", word):  # replace digit
        return "<!DIGIT!>"
    if not word.isascii():  # replace any non-english names
        return "<UNK>"

    return word


def edit_data(f):

    data = f.readlines()

    for i in range(len(data)):

        lst = data[i].split()  # split to words
        lst = lst[1:len(lst)]  # remove the indexes

        body = ""
        for word in lst:
            body += edit_word(word)+" "

        data[i] = str(i+1) + "<S>" + body + "</S>\n"
    return data


def read_columns():

    columns = []
    with open('eng_wikipedia_2016_1M-words.txt', 'r', encoding="utf8") as col_words:
        wikipediaWords = col_words.readlines()
        for i in range(50, 20051):
            columns.append(wikipediaWords[i].split('\t')[1])
    columns[:0] = ['-']
    return columns


def read_simlex():

    simlex = []

    with open('EN-SIMLEX-999.txt', 'r', encoding="utf8") as row_words:
        rows = row_words.readlines()

        for line in rows:
            line = line.split('\t')
            simlex.extend([line[0], line[1]])
        simlex = list(set(simlex))
    return simlex


def create_matrix():

    columns = read_columns()
    simlex = read_simlex()
    matrix = []

    columns = ["I go to school every day by bus .",
            "i go to theatre every night by bus"]
    simlex = ["I go to school every day by bus .",
            "i go to theatre every night by bus"]
    matrix.append(columns)
    for i in simlex:
        matrix.append([i]+[0] * (len(columns)-1))
    return matrix


def create_hash_table():

    hash_table = {}
    with open('eng_wikipedia_2016_10K-sentences.txt', 'r', encoding="utf8") as editFile:
        data = editFile.readlines()
        for i, line in enumerate(data):
            line = line[line.index("<S>")+len("<S>"):line.index("</S>")-1].split()
            for j, word in enumerate(line):
                if word in hash_table:
                    hash_table[word].append([i, j])
                else:
                    hash_table[word] = [[i, j]]
    return hash_table


def count(smlxWord, wikWord, content, size):

    counter = 0
    if smlxWord in content and wikWord in content:
        for posSmlx in content[smlxWord]:
            for posWik in content[wikWord]:
                if posSmlx[0] == posWik[0] and abs(posSmlx[1] - posWik[1]) <= size:
                    counter += 1
    return counter


def frequency_counts(matrix, content, size):

    for row in range(1, len(matrix)):
        for col in range(1, len(matrix[0])):
            matrix[row][col] = count(matrix[0][col], matrix[row][0], content, size)
    return matrix


def count_val(content):

    counter = 0
    for i in content:
        counter += len(content[i])
    return counter


def PPMI(mat, content):
    ppmiMat = mat
    allWords = count_val(content)
    for row in range(1,len(ppmiMat)):
        for col in range(1, len(ppmiMat[0])):
            if ppmiMat[row][col] !=0:
                ppmiMat[row][col] = math.log2((ppmiMat[row][col]/allWords)/
                                          ((len(content[ppmiMat[row][0]])/allWords)*(len(content[ppmiMat[0][col]])/allWords)))
    return ppmiMat


with open('eng_wikipedia_2016_10K-sentences.txt', 'r', encoding="utf8") as file:
    content = edit_data(file)

with open('eng_wikipedia_2016_10K-sentences.txt', 'w') as f:
    f.writelines(content)

matrix = create_matrix()
content = create_hash_table()


frequencyCountMat2 = frequency_counts(matrix, content, 2)
df = pd.DataFrame(frequencyCountMat2)
print(df)
frequencyCountMax5 = frequency_counts(matrix, content, 5)
ppmiMat2 = PPMI(frequencyCountMat2, content)
ppmiMat5 = PPMI(frequencyCountMax5, content)



