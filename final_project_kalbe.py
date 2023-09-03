# -*- coding: utf-8 -*-
"""Final Project_Kalbe.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e8WyXqlXy9TWLDjbHoNaN4M16lq5HKi8

## Library
"""

import pandas as pd
import numpy as np
import seaborn as sns

#untuk model liear regression
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans

#metriks untuk evaluasi model
from sklearn.metrics import mean_squared_error

#untuk latih dan uji data
from sklearn.model_selection import train_test_split

#untuk visualisasi data
import matplotlib.pyplot as plt
import seaborn as sns

#metode time series ARIMA
from statsmodels.tsa.arima.model import ARIMA

"""## Import Data"""

df_customer = pd.read_csv('Customer.csv', sep= ';')
df_product = pd.read_csv('Product.csv', sep= ';')
df_store = pd.read_csv('Store.csv', sep= ';')
df_transaction = pd.read_csv('Transaction.csv', sep= ';')

print(df_customer)

"""## Data Cleansing and Preparation"""

# Missing Value
missing1 = df_customer.isnull().sum()
missing2 = df_product.isnull().sum()
missing3 = df_store.isnull().sum()
missing4 = df_transaction.isnull().sum()

# Duplicate Rows
duplicate1 = df_customer.duplicated()
duplicate2 = df_product.duplicated()
duplicate3 = df_store.duplicated()
duplicate4 = df_transaction.duplicated()

# Describe data
df_customer.describe()

df_customer.info()

df_product.describe()

df_product.info()

df_store.describe()

df_store.info()

df_transaction.describe()

df_transaction.info()

"""## Merge Data"""

merge1 = pd.merge(df_customer, df_transaction, on='CustomerID')
merge2 = pd.merge(merge1, df_product, on='ProductID')
merged = pd.merge(merge2, df_store, on='StoreID')
merged.head()

merged.info()

merged.duplicated().sum()

"""## Machine Learning Regression (Time Series)"""

# Menyesuaikan tipe data ke format yang sesuai
merged['Date'] = pd.to_datetime(merged['Date'])
merged['Latitude'] = merged['Latitude'].apply(lambda x: x.replace(',','.')).astype(float)
merged['Longitude'] = merged['Longitude'].apply(lambda x: x.replace(',','.')).astype(float)

# data Time Series
data_time = merged.groupby('Date')['Qty'].sum().reset_index()

# Persiapan data Time Series
data = data_time.set_index('Date')
# resample
data1 = data.resample('D').sum()

data1.head()

# Data Visualization
data1.plot(figsize=(12,6))

# Train data dengan cara memisahkannya
train_size = int(len(data2) * 0.8)
train_data, test_data = data2[:train_size], data2[train_size:]
print(train_data.shape, test_data.shape)

import seaborn as sns
plt.figure(figsize=(12,5))
sns.lineplot(data=train_data, x=train_data.index, y=train_data['Qty'])
sns.lineplot(data=test_data, x=test_data.index, y=test_data['Qty'])
plt.show()

# menggunakan metode time series ARIMA (Autoregressive Integrated Moving Average)

# misalakan sudah memiliki data time series dengan'train_data' :
# 1. Tentukan nilai =
p = 2  # Order of Autoregression
d = 2  # Degree of Differencing
q = 2  # Order of Moving Average

# 2. model ARIMA dengan parameter
model = ARIMA(train_data, order=(p, d, q))

# 3: Latih model
model_fit = model.fit()

start_idx = len(train_data)
end_idx = len(train_data) + len(test_data) - 1
predictions = model_fit.predict(start=start_idx, end=end_idx, dynamic=False)

# Evaluasi performa
from sklearn.metrics import mean_squared_error
mse = mean_squared_error(test_data, predictions)
print(f"Mean Squared Error: {mse}")

import matplotlib.pyplot as plt

plt.figure(figsize=(12,5))
plt.plot(test_data, label='Qty')
plt.plot(predictions, color='red', label='Predicted')
plt.legend()
plt.show()

"""## Machine Learning Clustering"""

# Menggabungkan data berdasarkan CustomerID
aggregate = merged.groupby('CustomerID').agg({
    'TransactionID': 'count',
    'Qty': 'sum',
    'TotalAmount': 'sum'
}).reset_index()

aggregate

# persiapan data clustering
X = aggregate[['TransactionID', 'Qty', 'TotalAmount']]

# Model KMeans
kmeans = KMeans(n_clusters=n_clusters, random_state=42)

# clustering data
aggregate_data['cluster'] = kmeans.fit_predict(X)

import matplotlib.pyplot as plt

plt.scatter(aggregate['Qty'], aggregate_data['TotalAmount'], c=aggregate_data['cluster'], cmap='rainbow')
plt.xlabel('Qty')
plt.ylabel('Total Amount')
plt.title('Clustering Result')
plt.show()

# Membuat WCSS (Within-Cluster Sum of Squares)
wcss= []
for n in range (1,11):
    model1 = KMeans(n_clusters=n, init='k-means++', n_init = 10, max_iter=100, tol =0.0001, random_state = 100)
    model1.fit(X)
    wcss.append(model1.inertia_)
print(wcss)

plt.figure(figsize=(10,8))
plt.plot(list(range(1,11)), wcss, color = 'blue', marker = 'o', linewidth=2, markersize=12, markerfacecolor= 'm',
         markeredgecolor= 'm')
plt.title('WCSS vs Number of Cluster', fontsize = 15)
plt.xlabel('Number of Cluster')
plt.ylabel('WCSS')
plt.xticks(list(range(1,11)))
plt.grid()
plt.show()

# mengoptimalkan Model Clustering dengan K
model1 = KMeans(n_clusters=4, init='k-means++', n_init=10, max_iter=300, tol=0.0001, random_state=100)
model1.fit(X)
labels1=model1.labels_
centroids1 =model1.cluster_centers_

df_cluster = aggregate.drop(columns = ['CustomerID'])
df_cluster.head()

# cluster ke dalam dataset
df_cluster['cluster'] = model1.labels_
df_cluster.head()

plt.figure(figsize=(6,6))
sns.pairplot(data=df_cluster,hue='cluster',palette='Set1')
plt.show()

df_cluster['CustomerID'] = aggregate['CustomerID']
df_cluster_mean = df_cluster.groupby('cluster').agg({
    'CustomerID':'count',
    'TransactionID':'mean',
    'Qty':'mean',
    'TotalAmount':'mean'})
df_cluster_mean.sort_values('CustomerID', ascending = False)

"""## Kesimpulan

## Cluster 0
- Cluster dengan jumlah pelanggan paling rendah.

1.   Pelanggan dalam Cluster ini memiliki peringkat tertinggi dalam setiap metrik mereka.

Rekomendasi:
1. Tawarkan program loyalitas untuk menjaga transaksi tetap tinggi.
Lakukan penilaian kepuasan pelanggan.
2. Dorong peningkatan penjualan produk dengan harga yang lebih tinggi.

##Cluster 1

1.   Cluster dengan jumlah pelanggan terbesar.
2.   Ciri utama dari Cluster ini adalah bahwa Cluster ini berada di peringkat ketiga dalam setiap metrik (transaction, quantity, total amount).

Rekomendasi:

1.   Memperkuat relasi dengan pelanggan.
2.   Melakukan penelitian atau survei untuk meningkatkan minat dari pelanggan yang dominan.

##Cluster 2

1. Cluster dengan karakteristik pelanggan yang menduduki posisi kedua tertinggi dalam setiap metrik.

Rekomendasi:

1. Rutin memberikan promosi untuk merangsang peningkatan transaksi.
2. Meningkatkan penjualan produk dengan harga yang lebih tinggi.

##Cluster 3

1. Cluster dengan karakteristik pelanggan yang memiliki peringkat terendah dalam setiap metrik.

Rekomendasi:

1. Memberikan potongan harga yang besar untuk merangsang peningkatan transaksi pelanggan.
2. Menyediakan promosi untuk transaksi dengan jumlah barang yang lebih tinggi.
3. Melakukan penelitian untuk mengenali peluang pengembangan produk.
"""

