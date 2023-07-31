import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from lgs import lead_generation_skills

sentence = lead_generation_skills
tokens = word_tokenize(sentence)
num_tokens = len(tokens)

print("Речення:", sentence)
print("Токени:", tokens)
print("Кількість токенів:", num_tokens)
