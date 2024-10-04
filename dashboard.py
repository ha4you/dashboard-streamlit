import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengimpor dataset
order_items_df = pd.read_csv('order_items_dataset.csv')
products_df = pd.read_csv('products_dataset.csv')
orders_df = pd.read_csv('orders_dataset.csv')

# Mengubah tipe data tanggal
orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'], errors='coerce')
orders_df['order_delivered_customer_date'] = pd.to_datetime(orders_df['order_delivered_customer_date'], errors='coerce')

# Menghitung waktu pengiriman
orders_df['delivery_time'] = (orders_df['order_delivered_customer_date'] - orders_df['order_purchase_timestamp']).dt.days

# Streamlit Title
st.title('Dashboard Analisis Penjualan')

# Analisis 1: Distribusi Waktu Pengiriman
st.subheader('Distribusi Waktu Pengiriman Produk')
delivery_time = orders_df['delivery_time'].dropna()
fig1, ax1 = plt.subplots()
sns.histplot(delivery_time, bins=30, kde=True, ax=ax1)
ax1.set_title('Distribusi Waktu Pengiriman (hari)')
ax1.set_xlabel('Waktu Pengiriman (hari)')
ax1.set_ylabel('Frekuensi')
st.pyplot(fig1)

# Rata-rata waktu pengiriman
average_delivery_time = delivery_time.mean()
st.write(f"Rata-rata Waktu Pengiriman: {average_delivery_time:.2f} hari")

# Analisis 2: Total Penjualan Per Kategori Produk
st.subheader('Total Penjualan Per Kategori Produk')
merged_df = order_items_df.merge(products_df, on='product_id', how='inner')
if 'product_category_name' in merged_df.columns:
    merged_df = merged_df[merged_df['product_category_name'].notna()]
    category_sales = merged_df.groupby('product_category_name').agg({'price': 'sum'}).reset_index()
    category_sales = category_sales.sort_values(by='price', ascending=False)

    fig2, ax2 = plt.subplots()
    sns.barplot(x='price', y='product_category_name', data=category_sales, ax=ax2)
    ax2.set_title('Total Penjualan Per Kategori Produk')
    ax2.set_xlabel('Total Penjualan')
    ax2.set_ylabel('Kategori Produk')
    st.pyplot(fig2)

# Analisis Segmentasi Pelanggan
st.subheader('Segmentasi Pelanggan')

# Gabungkan orders_df dengan order_items_df untuk mendapatkan total pengeluaran per pelanggan
orders_with_price = orders_df.merge(order_items_df[['order_id', 'price']], on='order_id', how='left')

# Hitung segmentasi berdasarkan total pesanan dan pengeluaran
customer_segmentation = orders_with_price.groupby('customer_id').agg({'order_id': 'count', 'price': 'sum'}).reset_index().rename(columns={'order_id': 'total_orders', 'price': 'total_spent'})

# Visualisasikan segmentasi pelanggan
fig3, ax3 = plt.subplots()
sns.scatterplot(x='total_orders', y='total_spent', data=customer_segmentation, ax=ax3)
ax3.set_title('Segmentasi Pelanggan: Total Pembelian vs Total Pengeluaran')
ax3.set_xlabel('Jumlah Pembelian')
ax3.set_ylabel('Total Pengeluaran')
st.pyplot(fig3)

# Jalankan aplikasi Streamlit
