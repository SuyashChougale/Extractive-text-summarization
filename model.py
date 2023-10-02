import nltk
import string
from heapq import nlargest
import streamlit as st
st.title("Extractive Text Summarizer")

# Preprocessing steps
text = st.text_area("Enter text:")
nltk.download('punkt')
# tokenizing the text into sentence
if text:
   try:
     sents = nltk.sent_tokenize(text)
     original_sents = sents

     for i in range(len(sents)):
         # removing punctuations from the sentence
       sents[i] = sents[i].translate(str.maketrans("", "", string.punctuation))
         # tokenizing the sentence into words
       words = nltk.word_tokenize(sents[i])
       new_sent = ""
       for j in range(len(words)):
             
                 new_sent = (
                     new_sent + " " + words[j].lower()
                 )  # making a new sentence which don't contain stopword
       sents[i] = new_sent
   
#      new text without stopwords
     new_text = " ".join(sents)
   
     wor_frequency = {}  # Adictinary to keep track of frequency of respective word
   
     for word in nltk.word_tokenize(new_text):
      if word not in wor_frequency.keys():
          wor_frequency[word] = 1  # adding new word to dictinary
      else:
          wor_frequency[
              word
          ] += 1  # increasing the frequecy of the word present in the dictinary

     highest = max(
    wor_frequency.values()
)  # taking the highest value of frequecies to normalize all the values

     for word in wor_frequency.keys():
    # normalizing frequecies
      wor_frequency[word] = wor_frequency[word] / highest

     sentence_scores = {}

     for i in range(len(sents)):
      sent = sents[i]
      o_sent = original_sents[i]
      words = nltk.word_tokenize(sent)
      for word in words:
          if sent not in sentence_scores.keys():
              #  creating a sentence score for sentences present in text
              sentence_scores[o_sent] = wor_frequency[word.lower()]
          else:
              # updating score of sentence
              sentence_scores[o_sent] += wor_frequency[word.lower()]

# putting a threshould of 0.3 times orginal length ,for summary length
     summary_lines = nlargest(
    int(len(sents) * 0.3), sentence_scores, key=sentence_scores.get
)
   
     final_summary = ""
   
     for line in summary_lines:
       final_summary = final_summary + " " + line
   
     print(final_summary)
     st.write(final_summary)
   except ValueError:
    st.write('NAN')
