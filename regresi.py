# -*- coding: utf-8 -*-
"""Regresi.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yzSNRJVQNplvhVUK5HVAcMe4w9bwGUH5
"""

from google.colab import drive
drive.mount('/content/drive')

import os
os.listdir('/content/drive/MyDrive')

"""# Data Loading
Agar dataset lebih mudah dipahami, langkah pertama yang perlu kita lakukan adalah memuat datanya. Jangan lupa untuk mengimpor library pandas agar kita bisa membaca file data.

Pada contoh kasus ini kita akan mengimpor data dari secara manual ke Google Colab. Kondisi ini terjadi ketika dataset ada di komputer lokal, Anda bisa mengunggahnya langsung ke file storage di Google Colab. Jika menggunakan tools lain atau menyimpan data di Google Drive, pastikan untuk menyesuaikan path data yang sesuai.

Langkah pertama, impor library yang diperlukan. Anda bisa melakukannya di awal, atau membaginya ke dalam sel kode sesuai kebutuhan.
"""

import pandas as pd
df_train = pd.read_csv('/content/drive/MyDrive/train.csv')
print(df.head())  # Tampilkan beberapa baris pertama

df_test = pd.read_csv("/content/drive/MyDrive/test.csv")
df_test

"""# Data Cleaning dan Transformation
Kita akan melihat informasi dasar tentang dataset, seperti jumlah baris, kolom, tipe data, dan jumlah nilai yang hilang.

Pertama-tama, mari kita periksa tipe data dari masing-masing fitur yang ada di dataset. Tujuan dari pemeriksaan tipe data ini adalah untuk memastikan seluruh tipe data yang ada sudah sesuai dan tidak ada kekeliruan (contoh: data numerik terdeteksi str (string)). Sehingga, pada akhirnya Anda tidak akan mengalami kesulitan ketika melakukan preprocessing data karena tipe data yang ada sudah sesuai dan bisa melalui proses dengan lebih seamless.
"""

# Menampilkan ringkasan informasi dari dataset
df_train.info()

"""Selanjutnya, Anda perlu melakukan analisis statistik deskriptif dari dataset yang digunakan. Tujuan analisis statistik deskriptif dalam proses data cleaning pada machine learning adalah untuk memahami karakteristik dasar dari data yang sedang diproses.

Dengan melakukan analisis statistik deskriptif, kita bisa memastikan bahwa data yang digunakan untuk melatih model machine learning adalah data yang representatif, berkualitas tinggi, dan bebas dari masalah yang dapat memengaruhi hasil akhir. Berikut adalah contoh kode untuk melakukan analisis deskriptif.
"""

# Menampilkan statistik deskriptif dari dataset
df_train.describe(include="all")

"""Terakhir, Anda perlu melakukan pemeriksaan terhadap data yang hilang (missing value). Tujuannya untuk mencegah kesalahan ketika melakukan analisis, mencegah error pada model, dan meningkatkan performa model. Dengan melakukan pemeriksaan missing value, Anda dapat memastikan bahwa proses analisis data dan pelatihan model machine learning berjalan dengan baik, sehingga hasil yang diperoleh lebih valid dan akurat. Berikut salah satu contoh kode untuk melakukan pemeriksaan missing value"""

missing_values = df_train.isnull().sum()
missing_values[missing_values > 0]

"""Seperti yang sudah diimbau pada awal materi ini, data yang Anda gunakan sudah tergolong bersih dan tidak memiliki missing value sehingga proses pembersihan data terlihat sangat mudah. Agar tantangannya semakin terasa, mari kita berpindah ke tahap berikutnya, yaitu menangani outliers.

Seperti yang Anda ketahui bahwa outliers merupakan salah satu blocker dalam membangun model machine learning yang optimal. Hal ini bisa disebabkan oleh berbagai hal seperti kesalahan pengisian data, error yang terjadi ketika pengumpulan data, dan lain sebagainya.

Salah satu cara mengatasi outliers adalah dengan menggunakan metode IQR (Interquartile Range) adalah salah satu pendekatan yang efektif. IQR adalah rentang antara kuartil pertama (Q1) dan kuartil ketiga (Q3) dalam data. Nilai yang terletak di luar batas IQR dianggap sebagai outlier.

Mari kita periksa terlebih dahulu apakah dataset yang digunakan memiliki outlier atau tidak menggunakan kode berikut.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

for feature in df_train.columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df_train[feature])
    plt.title(f'Box Plot of {feature}')
    plt.show()

"""Perhatikan visualisasi data di atas, apakah Anda dapat menyimpulkan sesuatu? Yup, nilai yang berada di bawah batas minimum atau di atas batas maksimum dianggap sebagai outlier. Ada dua pilihan yang biasa dilakukan untuk mengatasi permasalahan ini.

Anda dapat memilih untuk menghapus outlier.
Menggantinya dengan nilai yang lebih moderat (seperti batas terdekat), atau menerapkan transformasi.
Nah, pada kasus ini, kita akan memilih untuk menghapus data outlier dengan asumsi bahwa outlier yang terjadi merupakan human error dan tidak ada pengaruh yang besar pada analisis deskriptif. Mari kita mulai pemeriksaan outlier menggunakan metode IQR dengan menggunakan kode berikut.
"""

# Contoh sederhana untuk mengidentifikasi outliers menggunakan IQR
Q1 = df_train.quantile(0.25)
Q3 = df_train.quantile(0.75)
IQR = Q3 - Q1
# Filter dataframe untuk hanya menyimpan baris yang tidak mengandung outliers pada kolom numerik
condition = ~((df_train < (Q1 - 1.5 * IQR)) | (df_train > (Q3 + 1.5 * IQR))).any(axis=1)
df_train = df_train.loc[condition, df_train.columns]

"""Apakah Anda melihat perbedaannya? Benar sekali! Setelah penanganan outliers menggunakan IQR, distribusi data menjadi lebih merata dan terpusat, dengan mean dan median yang mendekati satu sama lain. Di lain sisi, varians dan standar deviasi akan berkurang, lalu rentang data menyusut karena nilai yang berbeda telah diatasi.

Jika Anda perhatikan, ketika melakukan analisis deskriptif di awal ada beberapa hal yang menarik seperti distribusi data yang berbeda, standar deviasi yang masih besar, hingga rentang data yang berbeda-beda. Nah, untuk mengatasi permasalahan tersebut, mari kita lakukan standardisasi pada data agar dapat mengoptimalkan proses pelatihannya kelak.

Berhubung seluruh tipe data yang ada pada dataset ini numerikal maka Anda tidak perlu melakukan transformasi atau pengubahan tipe data. Sehingga, pada tahapan standardisasi, kita bisa langsung memanggil library andalan, yaitu StandardScaler.
"""

from sklearn.preprocessing import StandardScaler

# Memastikan hanya data dengan tipe numerikal yang akan diproses
numeric_features = df_train.select_dtypes(include=['number']).columns
numeric_features

# Standardisasi fitur numerik
scaler = StandardScaler()
df_train[numeric_features] = scaler.fit_transform(df_train[numeric_features])

"""Standardisasi penting untuk memastikan bahwa semua fitur dalam dataset memiliki skala yang sama sehingga mempermudah model untuk belajar dengan lebih baik dan memberikan hasil yang lebih akurat serta stabil.

Selanjutnya, Anda perlu memastikan bahwa data yang digunakan sudah bersih dengan mengecek duplikasi data.
"""

# Mengidentifikasi baris duplikat
duplicates = df.duplicated()

print("Baris duplikat:")
print(df[duplicates])

"""Seperti yang sudah dijelaskan pada awal materi ini, data yang Anda gunakan sudah tergolong bersih sehingga data ini tidak memiliki duplikasi atau nilai kosong.

Beralih ke tahap berikutnya, yaitu exploratory dan explanatory data. Pada tahap ini, Anda perlu meningkatkan kemampuan critical thinking agar dapat menggali informasi sedalam-dalamnya sehingga dapat memperoleh insight yang bermanfaat. Mari kita mulai dengan melihat karakteristik data yang sudah diolah sebelumnya.
"""

df.describe(include='all')

"""Data yang Anda miliki sudah memiliki distribusi yang cukup baik, hal tersebut dibuktikan dengan standar deviasi yang mendekati satu dan rentang nilai yang sama. Mari visualisasikan agar bentuknya terlihat lebih jelas."""

# Menghitung jumlah variabel
num_vars = df.shape[1]

# Menentukan jumlah baris dan kolom untuk grid subplot
n_cols = 4  # Jumlah kolom yang diinginkan
n_rows = -(-num_vars // n_cols)  # Ceiling division untuk menentukan jumlah baris

# Membuat subplot
fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, n_rows * 4))

# Flatten axes array untuk memudahkan iterasi jika diperlukan
axes = axes.flatten()

# Plot setiap variabel
for i, column in enumerate(df.drop(columns=["id"]).columns):
    df[column].hist(ax=axes[i], bins=20, edgecolor='black')
    axes[i].set_title(column)
    axes[i].set_xlabel('Value')
    axes[i].set_ylabel('Frequency')

# Menghapus subplot yang tidak terpakai (jika ada)
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# Menyesuaikan layout agar lebih rapi
plt.tight_layout()
plt.show()

"""Standardisasi yang Anda lakukan dapat membantu mengurangi efek bias atau skewness dari data yang tidak merata distribusinya. Dengan menempatkan fitur-fitur dalam skala yang sama, model machine learning lebih mudah untuk menemukan pola yang relevan seperti gambar di atas. Selain itu, ketika variabel-variabel berada pada skala yang berbeda secara signifikan, model machine learning mungkin menjadi tidak stabil dan memberikan hasil yang buruk. Standardisasi mengurangi risiko ini dengan membuat semua variabel berada dalam rentang yang konsisten.

Karena distribusi data yang Anda miliki sudah cukup baik, selanjutnya kita perlu memilih fitur yang memiliki hubungan dengan fitur target atau pada kasus ini adalah FloodProbability.
"""

# Menghitung korelasi antara variabel target dan semua variabel lainnya
target_corr = df.corr()['FloodProbability']

# (Opsional) Mengurutkan hasil korelasi berdasarkan kekuatan korelasi
target_corr_sorted = target_corr.abs().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
target_corr_sorted.plot(kind='bar')
plt.title(f'Correlation with Flood Probability')
plt.xlabel('Variables')
plt.ylabel('Correlation Coefficient')
plt.show()

"""Sekali lagi, data yang kita gunakan pada kasus ini memang sudah dibuat sedemikian rupa sehingga fitur-fitur yang ada memang memiliki hubungan yang sama dengan fitur target. Lalu, apa artinya? Dengan adanya hubungan antara semua fitur dengan target, Anda tidak perlu menghilangkan fitur sehingga dataset ini siap untuk memasuki tahap selanjutnya, yaitu splitting.

Data splitting adalah langkah penting dalam workflow machine learning untuk memastikan bahwa model yang dibangun dapat digeneralisasikan dengan baik pada data yang belum pernah dilihat. Ini dapat menghindari bias evaluasi dan mengoptimalkan model dengan benar, dan memberikan estimasi kinerja yang lebih akurat. Mari kita split data menggunakan kode berikut.
"""

import sklearn
from sklearn import datasets

# Memisahkan fitur (X) dan target (y)
X = df.drop(columns=['FloodProbability'])
y = df['FloodProbability']

from sklearn.model_selection import train_test_split

# membagi dataset menjadi training dan testing
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# menghitung panjang/jumlah data
print("Jumlah data: ",len(X))
# menghitung panjang/jumlah data pada x_test
print("Jumlah data latih: ",len(x_train))
# menghitung panjang/jumlah data pada x_test
print("Jumlah data test: ",len(x_test))

"""Dari sini kita bisa melihat bahwa dari jumlah data yang digunakan dapat dibagi menjadi dua subset yang berbeda dengan proporsi yang sudah ditentukan. Pada kasus ini kita akan menggunakan 676.708 data latih dan 169.178 data testing.

Dengan begitu data splitting memungkinkan kita untuk mengevaluasi kinerja model secara objektif. Dengan memisahkan data pelatihan dan pengujian, Anda bisa melihat seberapa baik model bekerja pada data yang belum pernah dilihat yang menyimulasikan kondisi dunia nyata. Ini membantu menghindari overfitting sehingga model dapat bekerja dengan sangat baik pada data pelatihan tetapi buruk pada data baru.

Selain itu, dengan membagi data menjadi bagian-bagian yang lebih kecil seperti set pelatihan dan set validasi memungkinkan Anda untuk menyetel hyperparameter model. Set validasi membantu dalam mengoptimalkan model tanpa memengaruhi data pengujian, yang sebaiknya hanya digunakan sekali untuk evaluasi akhir.

Setelah proses data splitting dilakukan langkah berikutnya dalam workflow machine learning adalah modelling. Proses ini melibatkan pelatihan model menggunakan set pelatihan yang telah kita siapkan, dan kemudian mengevaluasi kinerjanya dengan data pengujian atau validasi.

Setelah data terbagi, Anda dapat melatih model menggunakan training set. Model akan belajar dari fitur-fitur yang ada dalam data ini dan mencoba memetakan hubungan antara fitur dan target. Mari kita lakukan modelling atau pelatihan model menggunakan tiga algoritma yang berbeda.

#LARS
"""

from sklearn import linear_model
lars = linear_model.Lars(n_nonzero_coefs=1).fit(x_train, y_train)

pred_lars = lars.predict(x_test)

"""Setelah model dilatih Anda dapat menguji kinerja model pada data validasi. Proses ini penting agar model tidak hanya optimal pada data pelatihan, tetapi juga bekerja dengan baik pada data baru."""

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
mae_lars = mean_absolute_error(y_test, pred_lars)
mse_lars = mean_squared_error(y_test, pred_lars)
r2_lars = r2_score(y_test, pred_lars)

print(f"MAE: {mae_lars}")
print(f"MSE: {mse_lars}")
print(f"R²: {r2_lars}")

"""Nah, agar Anda dapat membandingkan ketiga model yang akan dibangun, mari kita buat sebuah DataFrame seperti berikut."""

# Membuat dictionary untuk menyimpan hasil evaluasi
data = {
    'MAE': [mae_lars],
    'MSE': [mse_lars],
    'R2': [r2_lars]
}

# Konversi dictionary menjadi DataFrame
df_results = pd.DataFrame(data, index=['Lars'])
df_results

"""# Linear Regression"""

from sklearn.linear_model import LinearRegression
LR = LinearRegression().fit(x_train, y_train)

pred_LR = LR.predict(x_test)

mae_LR = mean_absolute_error(y_test, pred_LR)
mse_LR = mean_squared_error(y_test, pred_LR)
r2_LR = r2_score(y_test, pred_LR)

print(f"MAE: {mae_LR}")
print(f"MSE: {mse_LR}")
print(f"R²: {r2_LR}")

"""Dari sini sudah terlihat jelas perbedaan performa yang dihasilkan, tetapi untuk membuktikan ini yang terbaik mari kita bandingkan dengan salah satu algoritma lainnya."""

df_results.loc['Linear Regression'] = [mae_LR, mse_LR, r2_LR]
df_results

"""# Gradient Boosting Regressor"""

from sklearn.ensemble import GradientBoostingRegressor

GBR = GradientBoostingRegressor(random_state=184)
GBR.fit(x_train, y_train)

pred_GBR = GBR.predict(x_test)

mae_GBR = mean_absolute_error(y_test, pred_GBR)
mse_GBR = mean_squared_error(y_test, pred_GBR)
r2_GBR = r2_score(y_test, pred_GBR)

print(f"MAE: {mae_GBR}")
print(f"MSE: {mse_GBR}")
print(f"R²: {r2_GBR}")

df_results.loc['GradientBoostingRegressor'] = [mae_GBR, mse_GBR, r2_GBR]
df_results