import os
from tkinter.messagebox import showinfo
import re
from docxtpl import DocxTemplate
from datetime import datetime
from peewee import *


"""
        ############################
        ###### BASE DE DATOS ######
        ############################
"""

db = SqliteDatabase("mi_base2.db")


class BaseModel(Model):
    class Meta:
        database = db


class id_proveedores(BaseModel):
    id = PrimaryKeyField()
    proveedores = CharField()


class id_productos(BaseModel):
    id = PrimaryKeyField()
    idproveedor = ForeignKeyField(id_proveedores, to_field='id')
    PRODUCTOS = CharField()


class pacientes(BaseModel):
    id = PrimaryKeyField()
    dni = CharField()
    var_nombre_paciente = CharField()
    var_apellido_paciente = CharField()


class Ventas(BaseModel):
    # dnipac = IntegerField()
    paciente = ForeignKeyField(model=pacientes, field='id')
    proveedor = ForeignKeyField(id_proveedores, field='id')
    producto = CharField()
    var_cantidad = IntegerField()
    precio = CharField()
    medico = CharField()
    fecha_inicio = DateTimeField()
    metodo_pago = CharField()


try:
    db.connect()
    db.create_tables([Ventas, id_proveedores, id_productos, pacientes])

except:
    print("La tabla ya existe")


"""
        #############################################
        ######## FUNCIONES PARA DECORADORES #########
        #############################################
"""

# proveedores_seleccionados = id_proveedores.select()
# for proveedor in proveedores_seleccionados:
#     print(f"ID: {proveedor.id}, Proveedor: {proveedor.proveedor}")


def alta_alta(func):
    def wrapper(*args, **kwargs):
        mi_listado = []
        for x in args[1:8]:
            mi_listado[1:8] = x.get()
            print(x.get())
            v1 = x.get()

        alta_registro = os.path.dirname(
            (os.path.abspath(__file__)) + "\\alta_registro.txt"
        )

        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        texto = "Alta " + str(v1) + " " + fecha_hora + "\n"

        with open("alta_registro.txt", "a") as alta_registro:
            alta_registro.write(texto)

        return func(*args, **kwargs)

    return wrapper


def baja_eliminacion(func):
    def wrapper(*args, **kwargs):
        baja_registro = os.path.dirname(
            (os.path.abspath(__file__)) + "\\baja_registro.txt"
        )
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        texto = "Baja de registro " + fecha_hora + "\n"
        with open("baja_registro.txt", "a") as baja_registro:
            baja_registro.write(texto)

        showinfo("ELIMINA, registro")
        return func(*args, **kwargs)

    return wrapper


def modifica_registro(func):
    def wrapper(*args, **kwargs):
        modif_registro = os.path.dirname(
            (os.path.abspath(__file__)) + "\\modif_registro.txt"
        )
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        texto = "Modifica registro el " + fecha_hora + "\n"
        with open("modif_registro.txt", "a") as modif_registro:
            modif_registro.write(texto)

        showinfo("MODIFICA, REGISTRO")
        return func(*args, **kwargs)

    return wrapper


def selecciona_registros(func):
    def wrapper(*args, **kwargs):
        showinfo("SELECCION, REGISTRO")
        return func(*args, **kwargs)

    return wrapper


def actu_actualizacion(func):
    def wrapper(*args, **kwargs):
        showinfo("ACTUALIZA, BASE")
        return func(*args, **kwargs)

    return wrapper


"""
        ############################
        ######## FUNCIONES #########
        ###########################
"""
lista_proveedores = []


class ModeloPoo():
    def __init__(
        self,
    ):
        pass

    
    def get_lista_proveedores(self):
        listToReturn = []
        global lista_proveedores
        if len(lista_proveedores) > 0:
            listToReturn = lista_proveedores
        else:
            for proveedores in id_proveedores.select():
                listToReturn.append(
                    {"nombre": proveedores.proveedores, "id": proveedores.id})
                lista_proveedores = listToReturn
        return listToReturn

    def getProviderByIndex(self, index):
        return lista_proveedores[index] if len(lista_proveedores[index]) >= 0 else []

    def get_lista_productos(self,idproveedor):
        lista_productos = []
       
        for producto in id_productos.select().where("idproveedor" == idproveedor):
            lista_productos.append(
                {"id": producto.id, "nombre": producto.PRODUCTOS})
        return lista_productos

    # def get_lista_productos():
    #     lista_productos = []
    #     result = id_productos.select()
    #     for producto in result:
    #         lista_productos.append(
    #             {"id": producto.idproveedor, "nombre": producto.PRODUCTOS})
    #     return lista_productos

    @actu_actualizacion
    def actualizar_treeview(self, mitreview):
        records = mitreview.get_children()
        for element in records:
            mitreview.delete(element)
           # Ventas.get(Ventas.paciente_id != None)
        for fila in Ventas.select():
            mitreview.insert(
                "",
                0,
                text=fila.id,
                values=(
                    fila.paciente_id,
                    fila.fecha_inicio,
                    fila.proveedor_id,
                    fila.producto,
                    fila.var_cantidad,
                    fila.precio,
                    fila.metodo_pago,
                    fila.medico,

                ),
            )

    @alta_alta
    def alta(
        self,
        dnipac,
        var_nombre_paciente,
        var_apellido_paciente,
        proveedor,
        producto,
        var_cantidad,
        precio,
        var_medico,
        var_fecha_inicio,
        var_metodo_pago,
        tree,
    ):
        cadena = var_nombre_paciente.get()
        patron_letras = "^[A-Za-záéíóúñ  ]*$"  # Regex para caracteres letras
        cadena1 = var_apellido_paciente.get()

        patron_numeros = "^[0-9]+$"  # Regex para caracteres numericos
        if not re.match(patron_letras, cadena):
            print("Error in nombre")
        if not re.match(patron_letras, cadena1):
            print("Error in apellido")

        if re.match(patron_letras, cadena) and re.match(patron_letras, cadena1):
            ventas = Ventas()
            paciente = pacientes()
            proveedores = id_proveedores()
            productos = id_productos()

            paciente.dni = dnipac.get()
            paciente.var_nombre_paciente = var_nombre_paciente.get()
            paciente.var_apellido_paciente = var_apellido_paciente.get()
            proveedores.proveedor = proveedor.get()
            productos.producto = producto.get()
            ventas.var_cantidad = var_cantidad.get()
            ventas.precio = precio.get()
            medico_seleccionado = var_medico.get()
            ventas.medico = medico_seleccionado
            ventas.medico = var_medico.get()
            ventas.fecha_inicio = var_fecha_inicio

            metodo_p_seleccionado = var_metodo_pago.get()
            ventas.metodo_pago = metodo_p_seleccionado
            paciente.save()
            ventas.paciente = paciente

            print(ventas)
            ventas.save()
            valor = precio.get()
            valor = int(valor)
            valor_registro = (
                dnipac.get(),
                var_nombre_paciente.get(),
                var_apellido_paciente.get(),
                proveedor.get(),
                producto.get(),
                var_cantidad.get(),
                precio.get(),
                var_medico.get(),
                var_fecha_inicio,
                var_metodo_pago.get(),
            )
            valor_registro = valor_registro
            print(valor_registro)
            dnipac.set(" ")
            var_nombre_paciente.set(" ")
            var_apellido_paciente.set(" ")
            proveedor.set(" ")
            producto.set(" ")
            var_cantidad.set(" ")
            precio.set(" ")
            var_medico.set(" ")
            var_fecha_inicio
            var_metodo_pago.set(" ")
            self.actualizar_treeview(tree)
            if valor >= 0:
                showinfo("ALTA REGISTRADA")
            else:
                showinfo("Valor, error")
                raise ("Valor negativo permitido")
        else:
            print("Error Precio")
            showinfo("Error, Precio")

    @baja_eliminacion
    def borrar(self, tree):
        valor = tree.selection()
        item = tree.item(valor)
        mi_id = item["text"]
        valor = (mi_id,)
        eliminar = Ventas.get(Ventas.id == valor)
        eliminar.delete_instance()
        print("HA ELIMINADO UN REGISTRO")
        self.actualizar_treeview(tree)

    @modifica_registro
    def modificar(
        self,
        dnipac,
        var_nombre_paciente,
        var_apellido_paciente,
        proveedor,
        producto,
        var_cantidad,
        precio,
        var_medico,
        var_fecha_inicio,
        var_metodo_pago,
        tree,
    ):
        cadena = var_nombre_paciente.get()
        patron_letras = "^[A-Za-záéíóúñ]*$"  # Regex para caracteres letras
        cadena1 = var_apellido_paciente.get()
        patron_numeros = "^[0-9]+$"  # Regex para caracteres numericos

        if re.match(patron_letras, cadena) and re.match(patron_letras, cadena1):
            valor = tree.selection()
            item = tree.item(valor)
            mi_id = item["text"]
            valor = (mi_id,)
            modifica = Ventas.get(Ventas.id == valor)
            modifica = Ventas.update(
                dnipac=dnipac.get(),
                var_nombre_paciente=var_nombre_paciente.get(),
                var_apellido_paciente=var_apellido_paciente.get(),
                proveedor=proveedor.get(),
                producto=producto.get(),
                var_cantidad=var_cantidad.get(),
                precio=precio.get(),
                var_medico=var_medico.get(),
                fecha_inicio=var_fecha_inicio,
                var_metodo_pago=var_metodo_pago.get(),
            ).where(Ventas.id == valor)
            modifica.execute()
            valor1 = precio.get()
            valor1 = int(valor1)
            dnipac.set("")
            var_nombre_paciente.set("")
            var_apellido_paciente.set("")
            proveedor.set("")
            producto.set("")
            var_cantidad.set("")
            precio.set("")
            var_medico.set("")
            var_fecha_inicio
            var_metodo_pago.set("")
            self.actualizar_treeview(tree)
            if valor1 >= 0:
                print("HA MODIFICO UN REGISTRO")
            else:
                showinfo("valor - error")
                raise ("Valor negativo permitido")
        else:
            print("Error campo Modificar")
            showinfo("Error Modificar")

    @selecciona_registros
    def seleccionar(
        self,
        dnipac,
        var_nombre_paciente,
        var_apellido_paciente,
        proveedor,
        producto,
        var_cantidad,
        precio,
        var_medico,
        var_fecha_inicio,
        metodo_de_pago,
        tree,
    ):
        valor = tree.selection()
        item = tree.item(valor)
        mi_id = item["text"]
        mi_id = int(mi_id)
        valor = (mi_id,)
        dnipac.set(item["values"][0])
        var_nombre_paciente.set(item["values"][1])
        var_apellido_paciente.set(item["values"][2])
        proveedor.set(item["values"][3])
        producto.set(item["values"][4])
        var_cantidad.set(item["values"][5])
        precio.set(item["values"][6])
        var_medico.set(item["values"][7])
        var_fecha_inicio.set(item["values"][8])
        metodo_de_pago.set(item["values"][9])
        print("HA SELECCIONADO UN REGISTRO")

    def imprimir(self, var_dnipac, var_producto, var_proveedor, var_precio, var_fecha_inicio):
        doc = DocxTemplate("invoice1.docx")
        dnipac = var_dnipac.get()
        producto = var_producto.get()
        proveedor = var_proveedor.get()
        precio = var_precio.get()
        fecha_inicio = var_fecha_inicio.get()

        doc.render({"var_fecha_inicio": fecha_inicio,
                    "var_dnipac": dnipac,
                    "var_producto": producto,
                    "var_proveedor": proveedor,
                    "var_precio": precio
                    })

        doc_name = "new_invoce" + dnipac + \
            datetime.now().strftime("%Y-%m-%d-%H%M%S") + ".docx"
        doc.save(doc_name)
        showinfo("Alta recibo", "El recibo esta listo para imprimir")


'''
#
        class Ventas(BaseModel):
    dnipac = IntegerField()
    var_nombre_paciente = CharField()
    var_apellido_paciente = CharField()
    proveedor = CharField()
    producto = CharField()
    var_cantidad = IntegerField()
    precio = DecimalField()
    medico = CharField()
    fecha_inicio = DateTimeField()
    metodo_pago = CharField()


try:
    db.connect()
    db.create_tables([Ventas])

except:
    print("La tabla ya existe")

'''

# select * from pacientes
# Join ventas  as ventas
# on vestas.pacientes == pacientes.id
# where pacientes.baja != False
