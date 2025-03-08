import re
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import string

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
    
def is_complete_sentence(text):
    """
    Checks if a string is likely a complete sentence.  Prioritizes speed with reasonable accuracy.
    """
    text = text.strip()

    # Empty string check
    if not text:
        return False

    # Basic punctuation check (ends with . ! ?)
    if text[-1] not in ['.', '!', '?']:
        return False

    # Check for common interruption phrases at the end
    interruption_phrases = ["but", "so", "and", "because", "if", "however", "although","then"]
    for phrase in interruption_phrases:
        if text.lower().endswith(phrase):
            return False

    # Abbreviation check (e.g., "Dr." is probably complete)
    if re.search(r"\w\.", text[:-1]):  # Exclude the final punctuation
        return True

    # NLTK Tokenization & Length check for at least three words after removing stopwords
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    table = str.maketrans('', '', string.punctuation) #remove punctuations
    stripped = [w.translate(table) for w in words] #remove punctuations
    words = [w for w in stripped if w.isalpha()] #only get alphabets
    words = [w for w in words if not w in stop_words]
    if len(words) < 3:
        return False
    return True


# Example usage
print(is_complete_sentence("The cat sat on the mat."))  # True
print(is_complete_sentence("Running quickly down the"))  # False
print(is_complete_sentence("The time is now."))  # True
print(is_complete_sentence("What is the capital?")) #False
print(is_complete_sentence("Please.")) #False
print(is_complete_sentence("Please close the door but")) #False
print(is_complete_sentence("Dr. is here."))  # True
print(is_complete_sentence("")) # False