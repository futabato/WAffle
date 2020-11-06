from sklearn.cluster import KMeans
from sklearn.datasets import load_iris

data = load_iris()

n_clusters = 3
model = KMeans(n_clusters=n_clusters)
model.fit(data.data)

print(model.labels_)
print(model.cluster_centers_)