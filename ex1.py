import re


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


def frequency_counts():
    with open('eng_wikipedia_2016_1M-words.txt', 'r', encoding="utf8") as col_words:
        columns = col_words.readlines()
        for i in range(50, 20051):
            columns[i] = columns[i].split('\t')[1]

    simlex = []
    with open('EN-SIMLEX-999.txt', 'r', encoding="utf8") as row_words:
        rows = row_words.readlines()
        for line in rows:
            line = line.split('\t')
            simlex.extend([line[0], line[1]])
        simlex = list(set(simlex))





with open('eng_wikipedia_2016_10K-sentences.txt', 'r', encoding="utf8") as file:
    content = edit_data(file)

with open('eng_wikipedia_2016_10K-sentences.txt', 'w') as f:
    f.writelines(content)

frequency_counts()


