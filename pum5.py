import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import StandardScaler
import matplotlib.cm as cm

# Load the data
data = pd.read_excel("datasets/Online Retail.xlsx")

# Data overview
print(data.head())
print(data.info())
print(data.describe())

# Check the data types of the 'InvoiceNo' column
print(data['InvoiceNo'].dtype)

# Convert 'InvoiceNo' column to string data type
data['InvoiceNo'] = data['InvoiceNo'].astype(str)

# Filter out rows where InvoiceNo starts with 'C'
data = data[~data['InvoiceNo'].str.startswith('C')]


# Drop unnecessary columns
data = data.drop(columns=['StockCode', 'Description', 'Country'])

# Drop rows with missing CustomerID
data = data.dropna(subset=['CustomerID'])

# Convert CustomerID to string
data['CustomerID'] = data['CustomerID'].astype(str)

# Remove negative quantities
data = data[data['Quantity'] > 0]

# Set reference date for recency calculation
reference_date = pd.Timestamp('2011-12-30')

# Create Recency, Frequency, and Monetary columns
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
data['Recency'] = (reference_date - data['InvoiceDate']).dt.days
data['Monetary'] = data['Quantity'] * data['UnitPrice']

# Aggregate data to get single entry per customer
rfm_data = data.groupby('CustomerID').agg({
    'Recency': 'min',
    'InvoiceNo': 'nunique',
    'Monetary': 'sum'
}).rename(columns={'InvoiceNo': 'Frequency'}).reset_index()

# Normalize the RFM data
scaler = StandardScaler()
rfm_normalized = scaler.fit_transform(rfm_data[['Recency', 'Frequency', 'Monetary']])

def plot_silhouette(X, cluster_labels):
    n_clusters = len(np.unique(cluster_labels))
    silhouette_avg = silhouette_score(X, cluster_labels)
    sample_silhouette_values = silhouette_samples(X, cluster_labels)

    fig, ax1 = plt.subplots(1, 1)
    fig.set_size_inches(18, 7)

    ax1.set_xlim([-0.1, 1])
    ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

    y_lower = 10
    for i in range(n_clusters):
        ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.nipy_spectral(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper), 0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
        y_lower = y_upper + 10

    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
    ax1.set_yticks([])
    ax1.set_xticks(np.arange(-0.1, 1.1, 0.1))

    plt.show()

# Try different numbers of clusters
for n_clusters in [2, 3, 4, 5, 6]:
    clusterer = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = clusterer.fit_predict(rfm_normalized)

    print(f"For n_clusters = {n_clusters}, the silhouette score is {silhouette_score(rfm_normalized, cluster_labels):.3f}")

    plot_silhouette(rfm_normalized, cluster_labels)


# Final model with the best number of clusters
best_n_clusters = 3  # Suppose 3 was the best based on silhouette scores
final_model = KMeans(n_clusters=best_n_clusters, random_state=42)
rfm_data['Cluster'] = final_model.fit_predict(rfm_normalized)

# Interpretation of clusters
cluster_summary = rfm_data.groupby('Cluster').agg({
    'Recency': ['mean', 'median'],
    'Frequency': ['mean', 'median'],
    'Monetary': ['mean', 'median']
}).reset_index()

print(cluster_summary)

# Visualization of clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(data=rfm_data, x='Recency', y='Monetary', hue='Cluster', palette='Set1', s=100)
plt.title('Customer Segmentation based on RFM')
plt.show()

