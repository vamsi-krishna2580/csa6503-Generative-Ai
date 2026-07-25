from nltk.tokenize import sent_tokenize
import nltk


text = "Hello! My name is Vamsi. I am learning Gen-AI"

sentences = sent_tokenize(text)

for val in sentences:
    print(val)

print(sentences)