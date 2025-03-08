from model2vec import StaticModel

# Load a pretrained Model2Vec model
model = StaticModel.from_pretrained("minishlab/potion-base-2M")

# Compute text embeddings
embeddings = model.encode(["hello how are you"])

print("emb:",embeddings)
