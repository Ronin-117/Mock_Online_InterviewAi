import numpy as np
import faiss
from model2vec import StaticModel

# Load model (only load once!)
model = StaticModel.from_pretrained("minishlab/potion-base-2M")

# Get the embedding dimension by encoding a sample text
sample_embedding = model.encode(["sample text"])
embedding_dimension = sample_embedding.shape[1]

# Load FAISS index and labels
index = faiss.read_index("completeness.index")
labels = np.load("completeness_labels.npy")

def is_complete_sentence(text, k=10):  # k is the number of nearest neighbors to consider
    """
    Classifies if a text is complete or incomplete based on FAISS nearest neighbor search.
    """
    text_embedding = model.encode([text]).astype('float32') #Ensure the input is float32

    # Search the FAISS index
    distances, indices = index.search(text_embedding, k)  # Search for the k-nearest neighbors

    # Get the labels of the nearest neighbors
    neighbor_labels = labels[indices[0]] # indices is of shape (1, k)

    # Majority vote to determine the predicted class
    complete_count = np.sum(neighbor_labels == 1)  # 1 represents 'complete'
    incomplete_count = np.sum(neighbor_labels == 0) # 0 represents 'incomplete'

    return complete_count > incomplete_count  # Return True if complete, False otherwise

test_text = "hello my name is Neil"
is_complete = is_complete_sentence(test_text)
print(f"'{test_text}' is complete: {is_complete}")