# NLP - Applied Natural Language Processing
This project is an exercise in text processing and distributional semantics, where you will implement a model that defines a distributional similarity measure between words. The script takes in a Simlex-999 dataset of word similarity scores, a corpus of Wikipedia sentences, and a list of the 20,000 most common words in the corpus as input. It then builds 4 word-context matrices with the following combinations:

window of +/-2 words, frequency counts
window of +/-5 words, frequency counts
window of +/-2 words, PPMI (Positive Point-wise Mutual Information)
window of +/-5 words, PPMI

The script calculates the cosine similarity measure for each pair of words in the Simlex dataset for each of the 4 matrices. The results are saved in files named freq_window2, freq_window5, ppmi_window2, ppmi_window5. The script then calculates the similarity between the files it created and the Simlex file, using the Spearman correlation coefficient, and saves the results in a file named correlation.txt.
