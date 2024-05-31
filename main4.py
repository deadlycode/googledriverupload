import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import os
import tempfile
import time

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
            # Geçici klasör oluştur
            with tempfile.TemporaryDirectory() as temp_dir:
                # Geçici dosya yolu oluştur
                temp_file_path = os.path.join(temp_dir, uploaded_file.name)

                # Dosyayı geçici klasöre kaydet
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Dosya meta verileri
                file_metadata = {
                    'name': file_name if file_name else uploaded_file.name,
                    'parents': ['1DEu_u231cqH7dTTIJbIt-QFHc5A8in6l']  # Hedef klasör ID'sini buraya girin
                }

                # Yükleniyor penceresi
                with st.spinner("Dosya Google Drive'a yükleniyor..."):
                    try:
                        # Dosyayı Google Drive'a yükle
                        media = MediaFileUpload(temp_file_path, mimetype=uploaded_file.type, resumable=True)
                        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                        st.success(f"{file_metadata['name']} başarıyla Google Drive'a yüklendi. Dosya ID: {file.get('id')}")
                    except HttpError as error:
                        st.error(f"Dosya yüklenirken bir hata oluştu: {error}")
                        # Hata olması durumunda 5 saniye bekleyip tekrar deneyelim
                        time.sleep(5)
                        st.experimental_rerun()
        except Exception as e:
            st.error(f"Dosya yüklenirken bir hata oluştu: {str(e)}")
    else:
        st.warning("Lütfen bir dosya seçin.")