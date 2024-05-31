import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError
from io import BytesIO
import os
import tempfile
import time
import math

# Streamlit uygulaması başlığı
st.title("Google Drive Dosya Yükleme")

# Google Drive API kimlik bilgilerini yükle
creds = service_account.Credentials.from_service_account_file(
    'anahtar.json',
    scopes=['https://www.googleapis.com/auth/drive']
)
drive_service = build('drive', 'v3', credentials=creds)

# Dosya yükleme formu
uploaded_file = st.file_uploader("Dosya Seçin", type=["jpg", "jpeg", "png", "pdf", "doc", "docx", "mp4", "avi", "mov"])

# Kullanıcının dosya adını girmesi için bir alan
file_name = st.text_input("Dosya adını girin", value="")

# Gönder butonu
if st.button("Gönder"):
    if uploaded_file is not None:
        try:
            # Dosya boyutunu al
            file_size = uploaded_file.size

            # Dosyayı parçalara bölmek için chunk boyutunu belirle (örneğin, 5 MB)
            chunk_size = 10 * 1024 * 1024

            # Dosya parça sayısını hesapla
            num_chunks = math.ceil(file_size / chunk_size)

            # Dosya meta verileri
            file_metadata = {
                'name': file_name if file_name else uploaded_file.name,
                'parents': ['1DEu_u231cqH7dTTIJbIt-QFHc5A8in6l']  # Hedef klasör ID'sini buraya girin
            }

            # Yükleniyor penceresi
            with st.spinner("Dosya Google Drive'a yükleniyor..."):
                try:
                    # Dosyayı parçalara bölerek yükle
                    for i in range(num_chunks):
                        # Dosya parçasını oku
                        chunk = uploaded_file.read(chunk_size)

                        # Dosya parçasını BytesIO nesnesine yaz
                        chunk_buffer = BytesIO(chunk)

                        # Dosya parçasını Google Drive'a yükle
                        media = MediaIoBaseUpload(chunk_buffer, mimetype=uploaded_file.type, chunksize=chunk_size, resumable=True)
                        if i == 0:
                            # İlk parçayı yükle ve dosya ID'sini al
                            file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                            file_id = file.get('id')
                        else:
                            # Sonraki parçaları yükle
                            drive_service.files().update(fileId=file_id, media_body=media).execute()

                    st.success(f"{file_metadata['name']} başarıyla Google Drive'a yüklendi. Dosya ID: {file_id}")
                except HttpError as error:
                    st.error(f"Dosya yüklenirken bir hata oluştu: {error}")
                    # Hata olması durumunda 5 saniye bekleyip tekrar deneyelim
                    time.sleep(5)
                    st.experimental_rerun()
        except Exception as e:
            st.error(f"Dosya yüklenirken bir hata oluştu: {str(e)}")
    else:
        st.warning("Lütfen bir dosya seçin.")