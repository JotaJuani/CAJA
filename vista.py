import tkinter as tk
import datetime as dt
from tkinter import StringVar, Label, Entry, ttk, Radiobutton, Button
from modelo import ModeloPoo


class Ventanita:
    def setProvider(self, main_frame2):
        provider = self.modelopoo1.getProviderByIndex(
            self.entry_proveedor.current())
        print(provider)

        product = self.modelopoo1.get_lista_productos(provider)
        product = product if product else [{}]
        formatted_products = [
            f"{prod ['nombre']}" for prod in product if 'nombre' in prod]

        self.entry_producto['values'] = formatted_products

    def __init__(self, windows):

        self.modelopoo1 = ModeloPoo()
        self.var_metodo_pago = StringVar()
        self.var_dnipac = StringVar()
        self.var_nombre_paciente = StringVar()
        self.var_apellido_paciente = StringVar()
        self.lista_proveedores = StringVar()
        self.var_proveedor = StringVar()
        self.var_producto = StringVar()
        self.var_cantidad = StringVar()
        self.var_precio = StringVar()
        self.var_medico = StringVar()
        self.var_fecha_inicio = dt.datetime.now().strftime("%d/%m/%Y %H:%M")

        ###### VISTA ######
        self.root = windows
        self.root.title("Ortopedia Almafuete ")
        self.root.geometry("840x695")

        self.root = tk.Frame()
        self.root.pack()
        self.root.configure(bg="lightpink")

        # frame 1
        main_frame1 = tk.LabelFrame(
            self.root, width=500, height=75, text="Ingrese los datos del paciente")
        main_frame1.grid(row=0, column=0, padx=5, pady=5)
        # labels 1
        self.dnipac = Label(
            main_frame1, text="DNI", bg="#FFCCCC")
        self.dnipac.grid(row=0, column=0, padx=5, pady=5)

        self.name_paciente = Label(
            main_frame1, text="Nombre", bg="#FFCCCC")
        self.name_paciente.grid(row=0, column=1, padx=5, pady=5)

        self.surname_paciente = Label(
            main_frame1, text="Apellido", bg="#FFCCCC")
        self.surname_paciente.grid(row=0, column=3, padx=5, pady=5)

        # entries frame1
        self.entry_dnipac = Entry(
            main_frame1, textvariable=self.var_dnipac, bg="#FFDDDD")
        self.entry_dnipac.grid(row=1, column=0, padx=5, pady=5)

        self.entry_nombre_paciente = Entry(
            main_frame1, textvariable=self.var_nombre_paciente, bg="#FFDDDD")
        self.entry_nombre_paciente.grid(row=1, column=1, padx=5, pady=5)

        self.entry_surname_paciente = Entry(
            main_frame1, textvariable=self.var_apellido_paciente, bg="#FFDDDD")
        self.entry_surname_paciente.grid(row=1, column=3, padx=5, pady=5)

        # frame 2
        main_frame2 = tk.LabelFrame(self.root, text="Datos del producto")
        main_frame2.grid(row=1, column=0, sticky="nswe", padx=5, pady=5)
        # labels 2
        self.proveedor = Label(main_frame2, text="Proveedor", bg="#FFCCCC")
        self.proveedor.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.producto = Label(main_frame2, text="Producto", bg="#FFCCCC")
        self.producto.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.cantidad = Label(main_frame2, text="Cantidad", bg="#FFCCCC")
        self.cantidad.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        self.precio = Label(main_frame2, text="Precio", bg="#FFCCCC")
        self.precio.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.medico = Label(main_frame2, text="Medico", bg="#FFCCCC")
        self.medico.grid(row=1, column=3, sticky="w", padx=5, pady=5)

        # entries frame2
        self.entry_proveedor = ttk.Combobox(
            main_frame2, textvariable=self.var_proveedor, width=40)
        self.entry_proveedor.grid(row=1, column=0, padx=10, pady=10)
        provider = self.modelopoo1.get_lista_proveedores()
        provider = provider if provider else [{}]
        formatted_providers = [f"{prov['nombre']}" for prov in provider]

        self.entry_proveedor['values'] = formatted_providers
        self.entry_proveedor.current(0)
        self.entry_producto = ttk.Combobox(
            main_frame2, textvariable=self.var_producto, width=40)
        self.entry_producto.grid(row=3, column=0, padx=10, pady=10)
        self.entry_proveedor.bind(
            "<<ComboboxSelected>>", lambda _: self.setProvider(main_frame2))
        self.setProvider(main_frame2)

        self.entry_cantidad = ttk.Spinbox(
            main_frame2, from_=1, to_=10, textvariable=self.var_cantidad)
        self.entry_cantidad.grid(row=1, column=1, padx=10, pady=10)
        self.var_cantidad.set("1")

        self.entry_precio = Entry(
            main_frame2, textvariable=self.var_precio, bg="#FFDDDD")
        self.entry_precio.grid(row=3, column=1, padx=10, pady=10)
        self.var_medico.set(" Seleccione un médico")

        self.var_medico_combobox = ttk.Combobox(main_frame2, textvariable=self.var_medico, values=[
            "Di Menna", "Halliburton", "Maenza", "Rochas L", "Rochas E", "Loma"])
        self.var_medico_combobox.grid(row=2, column=3, padx=10, pady=10)
        self.label_pago = tk.Label(main_frame2, text="Método de pago")
        self.label_pago.grid(row=0, column=5, sticky="w", padx=25, pady=25)

        efectivo_radio_button = Radiobutton(
            main_frame2, text="Efectivo", variable=self.var_metodo_pago, value="Efectivo", padx=10, pady=10)
        efectivo_radio_button.grid(row=1, column=5, padx=25, pady=10)
        mp_radio_button = Radiobutton(
            main_frame2, text="Mercado Pago", variable=self.var_metodo_pago, value="Mercado Pago", padx=10, pady=10)
        mp_radio_button.grid(row=2, column=5, padx=25, pady=10)
        tarjetas_radio_button = Radiobutton(
            main_frame2, text="Tarjeta", variable=self.var_metodo_pago, value="Tarjeta", padx=10, pady=10)
        tarjetas_radio_button.grid(row=3, column=5, padx=25, pady=10)

        # frame 4
        main_frame4 = tk.LabelFrame(self.root, text="Ventas")
        main_frame4.grid(row=3, column=0, sticky="nswe", padx=5, pady=5)

        self.tree = ttk.Treeview(main_frame4)
        self.tree["columns"] = ("col1", "col2", "col3",
                                "col4", "col5", "col6", "col7")
        self.tree.column("#0", width=50, minwidth=50, anchor="w")
        self.tree.column("col1", width=80, minwidth=80, anchor="w")
        self.tree.column("col2", width=170, minwidth=170, anchor="w")
        self.tree.column("col3", width=80, minwidth=80, anchor="w")
        self.tree.column("col4", width=90, minwidth=80, anchor="w")
        self.tree.column("col5", width=100, minwidth=80, anchor="w")
        self.tree.column("col6", width=100, minwidth=80, anchor="w")
        self.tree.column("col7", width=150, minwidth=80, anchor="w")

        self.tree.heading("#0", text="id")
        self.tree.heading("col1", text="Proveedor")
        self.tree.heading("col2", text="Producto")
        self.tree.heading("col3", text="Cantidad")
        self.tree.heading("col4", text="Precio")
        self.tree.heading("col5", text="Medico")
        self.tree.heading("col6", text="Metodo de Pago")
        self.tree.heading("col7", text="Fecha")
        self.tree.grid(row=14, column=0, columnspan=8)

        main_frame6 = tk.LabelFrame(self.root, text="")
        main_frame6.grid(row=4, column=0, sticky="nswe", padx=5, pady=5)

        ### BOTONES ######
        self.boton_alta = Button(
            main_frame6,
            text="Alta",
            command=lambda: self.modelopoo1.alta(
                self.var_dnipac,
                self.var_nombre_paciente,
                self.var_apellido_paciente,
                self.var_proveedor,
                self.var_producto,
                self.var_cantidad,
                self.var_precio,
                self.var_medico,
                self.var_fecha_inicio,
                self.var_metodo_pago,
                self.tree,
            ),
            bg="#FF69B4",
            fg="white",
            relief="flat",
            borderwidth=2
        )

        self.boton_alta.grid(row=6, column=1, pady=(
            10), padx=(50), sticky=tk.W + tk.E)

        self.boton_borrar = Button(
            main_frame6,
            text="Borrar",
            command=lambda: self.modelopoo1.borrar(self.tree),
            bg="#FF69B4",
            fg="white",
            relief="flat",
            borderwidth=2
        )
        self.boton_borrar.grid(row=6, column=7, pady=(
            10), padx=(50), sticky=tk.W + tk.E)

        self.boton_seleccionar = Button(
            main_frame6,
            text="Seleccionar",
            command=lambda: self.modelopoo1.seleccionar(
                self.var_dnipac,
                self.var_nombre_paciente,
                self.var_apellido_paciente,
                self.var_proveedor,
                self.var_producto,
                self.var_cantidad,
                self.var_precio,
                self.var_medico,

                self.var_metodo_pago,
                self.tree,
            ),
            bg="#FF69B4",
            fg="white",
            relief="flat",
            borderwidth=2
        )
        self.boton_seleccionar.grid(row=6, column=2, pady=(
            10), padx=(50), sticky=tk.W + tk.E)

        self.boton_modificar = Button(
            main_frame6,
            text="Modificar",
            command=lambda: self.modelopoo1.modificar(
                self.var_dnipac,
                self.var_nombre_paciente,
                self.var_apellido_paciente,
                self.var_proveedor,
                self.var_producto,
                self.var_cantidad,
                self.var_precio,
                self.var_medico,
                self.var_metodo_pago,
                self.tree,
            ),
            bg="#FF69B4",
            fg="white",
            relief="flat",
            borderwidth=2
        )
        self.boton_modificar.grid(row=6, column=5, pady=(
            10), padx=(50), sticky=tk.W + tk.E)

        self.boton_imprimir = Button(
            main_frame6,
            text="Imprimir",
            command=lambda: self.modelopoo1.imprimir(
                self.var_fecha_inicio,
                self.var_dnipac,
                self.var_producto,
                self.var_proveedor,
                self.var_cantidad,
                self.var_precio,
                self.var_metodo_pago,
            ),
            bg="#FF69B4",
            fg="white",
            relief="flat",
            borderwidth=2
        )
        self.boton_imprimir.grid(row=6, column=4, pady=(
            10), padx=(50), sticky=tk.W + tk.E)

    def getProviderIndex(combo):
        return combo.current()

    def actualiza_inicial(
        self,
    ):
        self.modelopoo1.actualizar_treeview(self.tree)
