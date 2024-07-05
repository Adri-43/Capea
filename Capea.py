import streamlit as st
import os
import json
from PIL import Image
import imageio
# Carpeta donde se guardarán las fotos 📁
IMG_DIR = "./fotos"

# Archivo para guardar la info de las fotos 📄
IMAGE_INFO_FILE = "./info_fotos.json"

# Cargamos la info de las fotos desde el archivo 🔄
if os.path.exists(IMAGE_INFO_FILE):
    with open(IMAGE_INFO_FILE, 'r') as f:
        info_fotos = json.load(f)
else:
    info_fotos = {}

# Creamos la carpeta si no existe 📂
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

st.title('📸 Sube y vota las mejores fotos!')

# Introduce tu ID de Instagram 📱
user_id = st.text_input('Escribe tu instagram para que todos puedan ver la foto que has subido🔝').strip().lower()

opcion = st.selectbox("Elige una opción", ["Tomar foto 🤳🏼", "Subir foto 📤", "Ver fotos 📸"])

if opcion == "Hazte un selfie 🤳🏼":
    # Comprobamos si ya has subido una foto 🔄
    if user_id in [info['uploader'] for info in info_fotos.values()]:
        st.write('Ya has subido una foto. 📸')
    else:
        foto_tomada = st.camera_input('Clica para hacer la foto')
        if foto_tomada is not None:
            nombre_foto = st.text_input('Añade la descripcion:')
            if nombre_foto:
                with open(os.path.join(IMG_DIR, nombre_foto + '.png'), 'wb') as f:
                    f.write(foto_tomada.getvalue())
                info_fotos[nombre_foto] = {'uploader': user_id, 'likes': []}
                st.success('¡Foto guardada con éxito! 🎉')
                with open(IMAGE_INFO_FILE, 'w') as f:
                    json.dump(info_fotos, f)
                st.experimental_rerun()


elif opcion == "Subir foto 📤":
    # Comprobamos si ya has subido una foto 🔄
    if user_id in [info['uploader'] for info in info_fotos.values()]:
        st.write('Ya has subido la foto. 📸')
    else:
        # Sube tu foto 📥
        foto_subida = st.file_uploader("Elige una foto", type=['png', 'jpg', 'jpeg'])
        nombre_foto = st.text_input('Añade la descripcion:')

        if foto_subida is not None and nombre_foto and user_id:
            foto = Image.open(foto_subida)
            foto.save(os.path.join(IMG_DIR, nombre_foto + '.png'))
            # Guardamos la info de la foto 📝
            info_fotos[nombre_foto] = {'uploader': user_id, 'likes': []}
            st.success('¡Foto guardada con éxito! 🎉')
            # Guardamos la info de las fotos en el archivo 📋
            with open(IMAGE_INFO_FILE, 'w') as f:
                json.dump(info_fotos, f)
            st.experimental_rerun()

elif opcion == "Ver fotos 📸":
    # Ordenamos las fotos por likes ❤️
    fotos_ordenadas = sorted(info_fotos.items(), key=lambda item: len(item[1]['likes']), reverse=True)
    # Mostramos las fotos 📸
    for nombre_foto, info in fotos_ordenadas:
        foto = Image.open(os.path.join(IMG_DIR, nombre_foto + '.png'))
        likes = len(info['likes'])
        descripcion = nombre_foto  # Aquí puedes reemplazar 'nombre_foto' con la descripción de la foto
        st.image(foto, use_column_width=True)
        st.write(f'@{info["uploader"]} ➡️ {descripcion} ({likes}❤️)')
        if user_id:
            if st.button('❤️', key=nombre_foto) and user_id not in info['likes']:
                info['likes'].append(user_id)
                # Actualizamos el archivo de info de las fotos cada vez que se da like 👍
                with open(IMAGE_INFO_FILE, 'w') as f:
                    json.dump(info_fotos, f)
            elif user_id in info['likes']:
                st.write(f'Ya le has dado like a esta foto! ❤️')
