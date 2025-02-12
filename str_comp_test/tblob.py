from textblob import TextBlob
import nltk
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('brown')

text = """
Each sunrise fills my heart with boundless joy and optimism, as if the world is a canvas of endless possibilities."""

blob = TextBlob(text)
blob.tags  # [('The', 'DT'), ('titular', 'JJ'),
#  ('threat', 'NN'), ('of', 'IN'), ...]

blob.noun_phrases  # WordList(['titular threat', 'blob',
#            'ultimate movie monster',
#            'amoeba-like mass', ...])

for sentence in blob.sentences:
    print("sent pol=",sentence.sentiment.polarity)
# 0.060
# -0.341