import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64



def add_background(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                              url("data:image/png;base64,{encoded_string}");
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_background("Desktop - 5.png")

# Set title for the dashboard
st.title("Dashboard Analisis Data Rumah")

# Provide a brief introduction
st.write("""
Selamat datang di Dashboard Analisis Data Rumah. Jelajahi visualisasi data untuk memahami pola dan tren dalam dataset rumah Anda.
Silakan pilih jenis visualisasi dari menu di sebelah kiri.
""")

# Sidebar for navigation
st.sidebar.title("Navigasi")
st.sidebar.write("Pilih visualisasi untuk ditampilkan:")

# Add a select box in the sidebar for visualization options
option = st.sidebar.selectbox(
    "Pilihan Visualisasi",
    ("Tampilkan Dataset", "Distribusi Harga Rumah", "Korelasi Fitur", "Hubungan Harga dengan Luas Lahan", "K-Medoids Clustering", "Silhouette Scores", "Gambar Scatter Plots")
)

# Main content area
st.header("Visualisasi yang Dipilih")

# Load dataset
def load_dataset():
    # Menggunakan dataset yang telah diolah sebelumnya
    dataset_path = "data_rumah_updated.xlsx"  # Sesuaikan dengan nama file Anda
    df = pd.read_excel(dataset_path, engine="openpyxl")
    return df

df = load_dataset()

if option == "Tampilkan Dataset":
    st.subheader("Dataset Rumah")
    st.write("Berikut adalah tampilan dari dataset rumah yang telah diolah:")
    st.dataframe(df)

elif option == "Distribusi Harga Rumah":
    st.subheader("Distribusi Harga Rumah")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['harga'], bins=30, kde=True, color='blue')
    plt.title("Distribusi Harga Rumah")
    plt.xlabel("Harga")
    plt.ylabel("Frekuensi")
    st.pyplot(plt)
    st.write("""
    **Deskripsi:** Visualisasi ini menunjukkan distribusi harga rumah dalam dataset. Histogram memberikan gambaran frekuensi harga tertentu.
    """)

elif option == "Korelasi Fitur":
    st.subheader("Korelasi Fitur")
    
    # Hanya pilih kolom numerik untuk korelasi
    numeric_df = df.select_dtypes(include=['number'])
    
    if numeric_df.empty:
        st.error("Dataset tidak memiliki kolom numerik untuk dihitung korelasi.")
    else:
        # Hapus data kosong sebelum perhitungan
        numeric_df = numeric_df.dropna()
        
        # Hitung matriks korelasi
        correlation_matrix = numeric_df.corr()
        
        # Visualisasi heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1)
        plt.title("Matriks Korelasi")
        st.pyplot(plt)
        
        st.write("""
        **Deskripsi:** Heatmap ini menunjukkan korelasi antara fitur numerik dalam dataset.
        Korelasi positif (+) menunjukkan hubungan linier searah, sedangkan korelasi negatif (-) menunjukkan hubungan terbalik.
        """)

elif option == "Hubungan Harga dengan Luas Lahan":
    st.subheader("Hubungan Harga dengan Luas Lahan")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df['luas_lahan'], y=df['harga'], alpha=0.6)
    plt.title("Hubungan Harga dengan Luas Lahan")
    plt.xlabel("Luas Lahan")
    plt.ylabel("Harga")
    st.pyplot(plt)
    st.write("""
    **Deskripsi:** Grafik scatter ini menunjukkan hubungan antara harga rumah dan luas tanah.
    Grafik ini membantu mengidentifikasi pola hubungan antara kedua variabel tersebut.
    """)

elif option == "K-Medoids Clustering":
    st.subheader("K-Medoids Clustering")

    # Display existing clustering plot
    st.image("kmedoids_clustering.png", caption="K-Medoids Clustering", use_container_width=True)

    st.write("""
    **Deskripsi:** Visualisasi ini menunjukkan hasil clustering menggunakan K-Medoids.
    Setiap titik pada grafik mewakili data yang dikelompokkan ke dalam cluster tertentu.
    """)

elif option == "Silhouette Scores":
    st.subheader("Silhouette Scores for K-Medoids Clustering")
    st.image("silhouette_scores.png", caption="Silhouette Scores for K-Medoids Clustering", use_container_width=True)
    st.write("""
    **Deskripsi:** Grafik ini menunjukkan Silhouette Scores untuk berbagai jumlah cluster pada K-Medoids. Nilai Silhouette Score yang lebih tinggi menunjukkan kualitas clustering yang lebih baik.
    """)

elif option == "Gambar Scatter Plots":
    st.subheader("Scatter Plots")

    # Add the three scatter plots to the dashboard
    st.image("output.png", caption="Jumlah Kamar vs Harga", use_container_width=True)
    st.image("output2.png", caption="Jumlah Luas Lahan vs Harga", use_container_width=True)
    st.image("output3.png", caption="Jumlah Luas Bangunan vs Harga", use_container_width=True)

    st.write("""
    **Deskripsi:** Grafik ini menunjukkan hubungan antara harga rumah dan variabel tertentu, seperti jumlah kamar, luas lahan, dan luas bangunan.
    Grafik membantu menganalisis pola hubungan antar variabel tersebut.
    """)

# Add a footer or additional notes
st.sidebar.info("""
**Catatan:** Pastikan dataset Anda memiliki kolom numerik untuk visualisasi bekerja dengan benar.
Terima kasih telah menggunakan dashboard ini!
""")
