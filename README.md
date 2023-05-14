# Pemetaan dan Deteksi Tambak Udang menggunakan Segmentasi YOLOv8
Selamat datang di proyek "Pemetaan dan Deteksi Tambak Udang menggunakan Segmentasi YOLOv8"! Proyek ini dibuat sebagai bagian dari tugas take home untuk melamar posisi sebagai Machine Vision Engineer di eFishery.
## Deskripsi Project
Proyek ini bertujuan untuk mengembangkan sistem yang dapat melakukan pemetaan dan deteksi tambak udang menggunakan teknik segmentasi berbasis YOLOv8. Dalam proyek ini, kami akan menggunakan data citra udara atau satelit untuk memetakan lokasi tambak udang dan mendeteksi keberadaan tambak pada citra tersebut. Dengan menerapkan YOLOv8, kita dapat mengidentifikasi dan memetakan area tambak udang dengan akurasi yang tinggi. Tujuan utama proyek ini adalah memberikan solusi teknologi yang dapat membantu dalam pemantauan dan pengelolaan tambak udang secara efisien.
## Solusi
Untuk memetakan kolam tambak udang berdasarkan data citra udara atau satelit menggunakan kordinat latitude dan longitude, digunakan solusi menggunakan deteksi segmentasi dimana model YOLOv8 digunakan untuk deteksi segmentasi. Solusi ini juga guna menjawab soal Take Home test yang terdiri dari 5 soal:
1. Untuk menghitung jumlah kolam tambak udang yang ada dalam suatu citra, pertama-pertama harus didapatkan citra udara/satelit untuk kordinat yang dituju. Maka dari itu menggunakan data scrapping yang sudah dibuat dan dengan kordinat yang telah disediakan,  maka didapatkan citra tersebut sebagai contoh berikut:
![image](https://github.com/fulankun1412/Ponds-Mapping-eFishery/assets/16248869/31ff8d0d-311a-40ae-b43d-dcb45e414178)

Dari citra tersebut dimasukkan ke dalam model deteksi dan segmentasi YOLOv8 yang sudah dilatih untuk mendeteksi kolam tambak udang menggunakan dataset yang sudah digunakan. berikut adalah hasil segmentasi dan jumalah tamabak udang yang berhasil di deteksi:
![image](https://github.com/fulankun1412/Ponds-Mapping-eFishery/assets/16248869/689f3c3a-bd2b-4c3c-a151-35faa2b36ac0)

2. Setelah perhitungan jumlah kolam selesai, maka selanjutnya perhitungan luas masin-masing kolam yang sudah terdeteksi. Solusi yang digunakan adalah menggunakan kontur dari masing-masing segmentasi kolam yang ada secara pixel dan luas pixel yang sudah didapatkan dikonversi kan ke dalam luas meter persegi.
```
# Dapatkan meter/pixel berdasarkan tingkat zaoom level dan lokasi latitude yang ingin diketahui. dan dapatkan skala untuk di kali dengan pixel untuk mendapatkan luas persegi M^2
METERS_PER_PX = (156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoomLevel))
RATIO_PIXEL_TO_SQUARE_M = METERS_PER_PX * METERS_PER_PX
```
Dengan menggunakan formula diatas maka didapatkan meter per pixel dan ration perkaliannya untuk mengubah pixel ke meter. Kemudian digunakan perhitungan kontur dan didapatkan hasil luas area hasil segmentasinya yang kemudian di konversi ke meter persegi dari pixel persegi.
```
areaPX = cv2.contourArea(pts,)
areaM = (round(areaPX * RATIO_PIXEL_TO_SQUARE_M, 3))
```
Sehingga nantinya menghasilkan dataframe seperti contoh berikut:
![image](https://github.com/fulankun1412/Ponds-Mapping-eFishery/assets/16248869/a5ecaad7-a795-4f6f-8839-c4fce51b033d)

Solusi untuk nomor 1 dan 2 sudah dapat di implementasikan dan bisa dicoba untuk penggunaan testing.
3. Untuk Geo Tagging menggunakan hash map
4.
5.

## Instalasi dan Penggunaan
Berikut adalah langkah-langkah untuk menginstal dan menjalankan proyek ini di local environtment, sangat disarankan untuk menggunakan virtual environment atau sudah terpasang docker:
### Python Lokal
1. Kloning repositori ini: Gunakan perintah git clone untuk mengkloning repositori ini ke direktori lokal.
```
git clone https://github.com/fulankun1412/Ponds-Mapping-eFishery.git
```
2. Pengaturan lingkungan virtual (opsional): Disarankan untuk membuat dan mengaktifkan lingkungan virtual Python sebelum melanjutkan instalasi dependensi. Anda dapat menggunakan venv atau alat serupa.
3. Instalasi dependensi: Masuk ke direktori proyek dan jalankan perintah berikut untuk menginstal dependensi yang diperlukan.
```
pip install -r requirements.txt
```
4. Untuk mengeksekusi aplikasi dan sehingga muncul interface aplikasinya, jalankan perintah eksekusi di dalam direktori
```
streamlit run app.py
```
5. Buka browser internet dan masuk ke localhost:8501, aplikasi terbuka selamat mencoba.

### docker-compose
1. Kloning repositori ini: Gunakan perintah git clone untuk mengkloning repositori ini ke direktori lokal.
```
git clone https://github.com/fulankun1412/Ponds-Mapping-eFishery.git
```
2. Jalankan perintah `docker-compose` ini untuk mulai build dan menjalankan langsung aplikasi
```
docker-compose up
```
3. Buka browser internet dan masuk ke localhost:8501, aplikasi terbuka selamat mencoba.

## Interface antar muka
### Input Latitude, Longitude dan Zoom Level
![image](https://github.com/fulankun1412/Ponds-Mapping-eFishery/assets/16248869/9eb06ade-a691-4f43-824b-6706f081b460)

### Hasil Generate Citra
![image](https://github.com/fulankun1412/Ponds-Mapping-eFishery/assets/16248869/7f5483ec-1a6d-46de-b9c0-c60b79c113cd)

### Hasil deteksi dan Perhitungan
![image](https://github.com/fulankun1412/Ponds-Mapping-eFishery/assets/16248869/bd31daf0-9ed9-4a2b-9166-ffc4d972518e)


## Referensi 
Dokumentasi YOLOv8: [Ultralytics YOLOv8](https://docs.ultralytics.com/modes/)
