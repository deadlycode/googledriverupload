import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO

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
        # Dosya içeriğini BytesIO kullanarak oku
        file_content = BytesIO(uploaded_file.read())

        # Dosya meta verileri
        file_metadata = {
            'name': file_name if file_name else uploaded_file.name,
            'parents': ['1DEu_u231cqH7dTTIJbIt-QFHc5A8in6l']  # Hedef klasör ID'sini buraya girin
        }

        # Yükleniyor penceresi
        with st.spinner("Dosya Google Drive'a yükleniyor..."):
            # Dosyayı Google Drive'a yükle
            media = MediaIoBaseUpload(file_content, mimetype=uploaded_file.type, resumable=True)
            file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        st.success(f"{file_metadata['name']} başarıyla Google Drive'a yüklendi. Dosya ID: {file.get('id')}")
    else:
        st.warning("Lütfen bir dosya seçin.")