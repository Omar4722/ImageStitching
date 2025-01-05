#pip install customtkinter
#pip install pillow

from customtkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename

# Configuración de la ventana principal
app = CTk()
app.geometry("800x500")
set_appearance_mode("dark")

# Función para limpiar la ventana principal
def limpiar_ventana():
    for widget in app.winfo_children():
        widget.destroy()

# Función para refrescar la ventana con contenido nuevo
def abrir_contenido_secundario():
    limpiar_ventana()  # Elimina los widgets actuales de la ventana principal

    # Contenido nuevo
    etiqueta = CTkLabel(master=app, text="Bienvenido al Sistema", font=("Arial", 30))
    etiqueta.pack(pady=20)

    # Crear un panel para mostrar las imágenes
    panel_imagenes = CTkFrame(master=app, width=500, height=200, fg_color="white")
    panel_imagenes.pack(pady=10)

    max_columnas = 3  # Número máximo de columnas por fila
    imagen_index = [0]  # Índice para controlar posición en cuadrícula (fila, columna)
    posiciones = {}  # Diccionario para almacenar las posiciones de las imágenes
    imagen_seleccionada = [None]  # Imagen actualmente seleccionada
    imagen_para_intercambio = [None]  # Segunda imagen seleccionada para intercambio

    # Función para cargar y previsualizar una imagen
    def cargar_imagen():
        archivo = askopenfilename(filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
        if archivo:
            img = Image.open(archivo).resize((150, 150))
            ctk_img = CTkImage(light_image=img, size=(150, 150))

            fila = imagen_index[0] // max_columnas
            columna = imagen_index[0] % max_columnas

            # Crear un marco para la imagen
            img_frame = CTkFrame(master=panel_imagenes, fg_color="white", corner_radius=10)
            img_frame.grid(row=fila, column=columna, padx=10, pady=10)

            img_label = CTkLabel(master=img_frame, image=ctk_img)
            img_label.image = ctk_img  # Evitar que la imagen sea recolectada por el garbage collector
            img_label.pack()

            # Asociar posición inicial
            posiciones[img_frame] = (fila, columna)

            # Asociar eventos de selección
            img_frame.bind("<Button-1>", lambda event, frame=img_frame: seleccionar_imagen(frame))
            img_label.bind("<Button-1>", lambda event, frame=img_frame: seleccionar_imagen(frame))

            imagen_index[0] += 1  # Incrementar el índice para la siguiente imagen

    # Función para seleccionar una imagen
    def seleccionar_imagen(frame):
        nonlocal imagen_para_intercambio
        if imagen_seleccionada[0] is None:
            imagen_seleccionada[0] = frame
            frame.configure(fg_color="red")  # Resaltar la primera imagen seleccionada
        elif imagen_para_intercambio[0] is None and frame != imagen_seleccionada[0]:
            imagen_para_intercambio[0] = frame
            frame.configure(fg_color="blue")  # Resaltar la segunda imagen seleccionada

        if imagen_seleccionada[0] and imagen_para_intercambio[0]:
            indicador_seleccion.configure(text="Dos imágenes seleccionadas", text_color="green")
        elif imagen_seleccionada[0]:
            fila, columna = posiciones[imagen_seleccionada[0]]
            indicador_seleccion.configure(text=f"Imagen seleccionada: Fila {fila}, Columna {columna}", text_color="green")

    # Función para eliminar la imagen seleccionada
    def eliminar_imagen():
        if imagen_seleccionada[0] is not None:
            imagen = imagen_seleccionada[0]
            imagen.grid_forget()  # Eliminar visualmente
            del posiciones[imagen]  # Eliminar de posiciones
            imagen_seleccionada[0] = None  # Reiniciar selección
            indicador_seleccion.configure(text="No hay imagen seleccionada", text_color="gray")

    # Función para intercambiar imágenes
    def intercambiar_imagenes():
        if imagen_seleccionada[0] and imagen_para_intercambio[0]:
            # Obtener las posiciones actuales
            pos1 = posiciones[imagen_seleccionada[0]]
            pos2 = posiciones[imagen_para_intercambio[0]]

            # Intercambiar las posiciones
            posiciones[imagen_seleccionada[0]] = pos2
            posiciones[imagen_para_intercambio[0]] = pos1

            # Reubicar los frames en la cuadrícula
            imagen_seleccionada[0].grid(row=pos2[0], column=pos2[1], padx=10, pady=10)
            imagen_para_intercambio[0].grid(row=pos1[0], column=pos1[1], padx=10, pady=10)

            # Resetear la selección
            imagen_seleccionada[0].configure(fg_color="white")
            imagen_para_intercambio[0].configure(fg_color="white")
            imagen_seleccionada[0] = None
            imagen_para_intercambio[0] = None

            indicador_seleccion.configure(text="Imágenes intercambiadas", text_color="blue")
        else:
            indicador_seleccion.configure(text="Seleccione dos imágenes para intercambiar", text_color="red")

    boton_cargar = CTkButton(
        master=app,
        text="Cargar Imagen",
        command=cargar_imagen,
        corner_radius=10,
        fg_color="#C850C0",
        hover_color="#4158D0"
    )
    boton_cargar.pack(pady=10)

    boton_eliminar = CTkButton(
        master=app,
        text="Eliminar Imagen",
        command=eliminar_imagen,
        corner_radius=10,
        fg_color="#FF5733",
        hover_color="#C70039"
    )
    boton_eliminar.pack(pady=10)

    boton_intercambiar = CTkButton(
        master=app,
        text="Intercambiar",
        command=intercambiar_imagenes,
        corner_radius=10,
        fg_color="#33A1FF",
        hover_color="#1E90FF"
    )
    boton_intercambiar.pack(pady=10)

    indicador_seleccion = CTkLabel(master=app, text="No hay imagen seleccionada", font=("Arial", 12), text_color="gray")
    indicador_seleccion.pack(pady=5)

    boton_volver = CTkButton(
        master=app,
        text="Volver",
        command=abrir_contenido_principal,  # Vuelve al contenido original
        corner_radius=10,
        fg_color="#C850C0",
        hover_color="#4158D0"
    )
    boton_volver.pack(pady=10)

# Contenido inicial de la ventana principal
def abrir_contenido_principal():
    limpiar_ventana()  # Elimina los widgets actuales

    # Etiqueta principal
    label = CTkLabel(master=app, text="PanoraDrone", font=("Arial", 40))
    label.place(relx=0.5, rely=0.05, anchor="center")

    # Cargar imagen
    img = Image.open("logo.jpg").resize((200, 200))
    ctk_img = CTkImage(light_image=img, size=(200, 200))
    img_label = CTkLabel(master=app, image=ctk_img)
    img_label.place(relx=0.5, rely=0.4, anchor="center")

    # Botón principal
    btn = CTkButton(
        master=app,
        text="Iniciar",
        corner_radius=32,
        fg_color="#C850C0",
        hover_color="#4158D0",
        border_color="#FFCC70",
        border_width=2,
        command=abrir_contenido_secundario  # Cambia al contenido secundario
    )
    btn.place(relx=0.5, rely=0.8, anchor="center")

# Inicializar el contenido principal
abrir_contenido_principal()

# Bucle principal de la aplicación
app.mainloop()
