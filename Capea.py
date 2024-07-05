import streamlit as st
import os
import json
from PIL import Image

# Directorio donde se guardarán las imágenes
IMG_DIR = "./imagenes"

# Archivo para almacenar la información de las imágenes
IMAGE_INFO_FILE = "./image_info.json"

# Cargar la información de las imágenes desde el archivo
if os.path.exists(IMAGE_INFO_FILE):
    with open(IMAGE_INFO_FILE, 'r') as f:
        image_info = json.load(f)
else:
    image_info = {}

# Crear el directorio si no existe
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

st.title('Subida y visualización de imágenes')

# Entrada de texto para el ID de Instagram
user_id = st.text_input('Introduce tu ID de Instagram').strip().lower()

# Cambiamos el radio button por un selectbox en el centro
page = st.radio("Elige una página", ["Subir imagen", "Ver imágenes"])


if page == "Subir imagen":
    # Comprobamos si el usuario ya ha subido una imagen
    if user_id in [info['uploader'] for info in image_info.values()]:
        st.write('Ya has subido una imagen.')
    else:
        # Subida de la imagen
        uploaded_file = st.file_uploader("Elige una imagen", type=['png', 'jpg', 'jpeg'])
        image_name = st.text_input('Introduce un nombre para la imagen')

        if uploaded_file is not None and image_name and user_id:
            image = Image.open(uploaded_file)
            image.save(os.path.join(IMG_DIR, image_name + '.png'))
            # Inicializar la información de la imagen
            image_info[image_name] = {'uploader': user_id, 'likes': []}
            st.success('Imagen guardada con éxito!')
            # Guardar la información de las imágenes en el archivo
            with open(IMAGE_INFO_FILE, 'w') as f:
                json.dump(image_info, f)
            st.experimental_rerun()

elif page == "Ver imágenes":
    # Ordenamos las imágenes por likes
    sorted_images = sorted(image_info.items(), key=lambda item: len(item[1]['likes']), reverse=True)
    # Visualización de las imágenes
    for image_name, info in sorted_images:
        image = Image.open(os.path.join(IMG_DIR, image_name + '.png'))
        likes = len(info['likes'])
        st.image(image, caption=f'{image_name} ({likes} likes)', use_column_width=True)
        if user_id and st.button(f'Like {image_name}') and user_id not in info['likes']:
            info['likes'].append(user_id)
            # Actualizar el archivo de información de las imágenes cada vez que se hace clic en el botón 'Like'
            with open(IMAGE_INFO_FILE, 'w') as f:
                json.dump(image_info, f)
