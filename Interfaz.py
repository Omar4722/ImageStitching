from customtkinter import *
from PIL import Image
from tkinter.filedialog import askopenfilename

# Configuración de la ventana principal
app = CTk()
app.geometry("800x600")
set_appearance_mode("dark")
set_default_color_theme("dark-blue")

# Variables globales para controlar la cuadrícula
filas = [3]  # Número de filas seleccionadas por el usuario
columnas = [3]  # Número de columnas seleccionadas por el usuario

# Función para limpiar la ventana principal
def limpiar_ventana():
    for widget in app.winfo_children():
        widget.destroy()

# Función para manejar el contenido secundario
def abrir_contenido_secundario():
    limpiar_ventana()

    # Contenido nuevo
    etiqueta = CTkLabel(master=app, text="Gestión de Superimagen", font=("Arial", 30))
    etiqueta.pack(pady=20)

    # Crear un panel para mostrar las imágenes
    panel_imagenes = CTkFrame(master=app, width=700, height=400, fg_color="white")
    panel_imagenes.pack(pady=10)

    imagen_index = [0]  # Índice para controlar posición en cuadrícula (fila, columna)
    posiciones = {}  # Diccionario para almacenar las posiciones de las imágenes
    imagen_seleccionada = [None]  # Imagen actualmente seleccionada
    imagen_para_intercambio = [None]  # Segunda imagen seleccionada para intercambio

    # Función para cargar y previsualizar una imagen
    def cargar_imagen():
        archivo = askopenfilename(filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
        if archivo:
            # Ajustar el tamaño de las imágenes
            img = Image.open(archivo).resize((200, 200))
            ctk_img = CTkImage(light_image=img, size=(200, 200))

            # Calcular la posición en la cuadrícula
            fila = imagen_index[0] // columnas[0]
            columna = imagen_index[0] % columnas[0]

            # Verificar si la cuadrícula tiene espacio suficiente
            if fila >= filas[0]:
                indicador_seleccion.configure(text="No hay más espacio en la cuadrícula", text_color="red")
                return

            # Crear un marco para la imagen
            img_frame = CTkFrame(master=panel_imagenes, fg_color="white", corner_radius=10, width=220, height=220)
            img_frame.grid(row=fila, column=columna, padx=10, pady=10)

            # Añadir la imagen al marco
            img_label = CTkLabel(master=img_frame, image=ctk_img)
            img_label.image = ctk_img
            img_label.pack(padx=10, pady=10)

            # Asociar posición inicial
            posiciones[img_frame] = (fila, columna)

            # Asociar eventos de selección
            img_frame.bind("<Button-1>", lambda event, frame=img_frame: seleccionar_imagen(frame))
            img_label.bind("<Button-1>", lambda event, frame=img_frame: seleccionar_imagen(frame))

            imagen_index[0] += 1

    # Función para seleccionar una imagen
    def seleccionar_imagen(frame):
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
            imagen.grid_forget()
            del posiciones[imagen]
            imagen_seleccionada[0] = None
            indicador_seleccion.configure(text="No hay imagen seleccionada", text_color="gray")

    # Función para intercambiar imágenes
    def intercambiar_imagenes():
        if imagen_seleccionada[0] and imagen_para_intercambio[0]:
            pos1 = posiciones[imagen_seleccionada[0]]
            pos2 = posiciones[imagen_para_intercambio[0]]

            posiciones[imagen_seleccionada[0]] = pos2
            posiciones[imagen_para_intercambio[0]] = pos1

            imagen_seleccionada[0].grid(row=pos2[0], column=pos2[1], padx=10, pady=10)
            imagen_para_intercambio[0].grid(row=pos1[0], column=pos1[1], padx=10, pady=10)

            imagen_seleccionada[0].configure(fg_color="white")
            imagen_para_intercambio[0].configure(fg_color="white")
            imagen_seleccionada[0] = None
            imagen_para_intercambio[0] = None

            indicador_seleccion.configure(text="Imágenes intercambiadas", text_color="blue")
        else:
            indicador_seleccion.configure(text="Seleccione dos imágenes para intercambiar", text_color="red")

    # Botones de control
    boton_cargar = CTkButton(master=app, text="Cargar Imagen", command=cargar_imagen, corner_radius=10)
    boton_cargar.pack(pady=10)

    boton_eliminar = CTkButton(master=app, text="Eliminar Imagen", command=eliminar_imagen, corner_radius=10)
    boton_eliminar.pack(pady=10)

    boton_intercambiar = CTkButton(master=app, text="Intercambiar", command=intercambiar_imagenes, corner_radius=10)
    boton_intercambiar.pack(pady=10)

    indicador_seleccion = CTkLabel(master=app, text="No hay imagen seleccionada", font=("Arial", 12), text_color="gray")
    indicador_seleccion.pack(pady=5)

    boton_volver = CTkButton(master=app, text="Volver", command=abrir_contenido_principal, corner_radius=10)
    boton_volver.pack(pady=10)

# Contenido inicial de la ventana principal
def abrir_contenido_principal():
    limpiar_ventana()

    # Encabezado elegante
    encabezado = CTkFrame(master=app, height=80, fg_color="#4158D0")
    encabezado.pack(fill="x")

    titulo = CTkLabel(master=encabezado, text="PanoraDrone", font=("Arial", 30, "bold"), text_color="white")
    titulo.place(relx=0.5, rely=0.5, anchor="center")

    # Contenedor principal
    contenido = CTkFrame(master=app, fg_color=None)
    contenido.pack(pady=20, expand=True, fill="both")

    # Etiqueta y menú para seleccionar tamaño de cuadrícula
    label_menu = CTkLabel(
        master=contenido,
        text="Selecciona el tamaño de la cuadrícula para la superimagen:",
        font=("Arial", 16),
    )
    label_menu.pack(pady=20)

    opciones = ["3x2", "3x3", "4x3", "5x4", "16x4"]

    def cambiar_tamano(opcion):
        f, c = map(int, opcion.split('x'))
        filas[0] = f
        columnas[0] = c

    menu_tamano = CTkOptionMenu(master=contenido, values=opciones, command=cambiar_tamano)
    menu_tamano.pack(pady=10)

    # Botón para iniciar
    btn_iniciar = CTkButton(master=contenido, text="Iniciar", command=abrir_contenido_secundario, corner_radius=20)
    btn_iniciar.pack(pady=40)

# Inicializar el contenido principal
abrir_contenido_principal()

# Bucle principal de la aplicación
app.mainloop()
