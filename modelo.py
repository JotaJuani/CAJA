import os
from tkinter.messagebox import showinfo
import re
from docxtpl import DocxTemplate
from datetime import datetime
from peewee import *

db = SqliteDatabase("mi_base2.db")

class BaseModel(Model):
    class Meta:
        database = db

class id_proveedores(BaseModel):
    id = PrimaryKeyField()
    proveedores = CharField()

class id_productos(BaseModel):
    id = PrimaryKeyField()
    idproveedor_id = ForeignKeyField(id_proveedores, to_field='id')
    PRODUCTOS = CharField()

class pacientes(BaseModel):
    id = PrimaryKeyField()
    dni = CharField()
    var_nombre_paciente = CharField()
    var_apellido_paciente = CharField()

class Ventas(BaseModel):
    paciente_id = ForeignKeyField(model=pacientes, field='id')
    proveedor = ForeignKeyField(id_proveedores, field='id')
    producto = CharField()
    var_cantidad = IntegerField()
    precio = CharField()
    medico = CharField()
    fecha_inicio = DateTimeField()
    metodo_pago = CharField()
    dnipac = IntegerField()

try:
    db.connect()
    db.create_tables([Ventas, id_proveedores, id_productos, pacientes])

except:
    print("La tabla ya existe")

def alta_alta(func):
    def wrapper(*args, **kwargs):
        mi_listado = []
        for x in args[1:8]:
            mi_listado[1:8] = x.get()
            print(x.get())
            v1 = x.get()

        alta_registro = os.path.dirname(
            (os.path.abspath(__file__)) + "\\alta_registro.txt")

        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        texto = "Alta " + str(v1) + " " + fecha_hora + "\n"

        with open("alta_registro.txt", "a") as alta_registro:
            alta_registro.write(texto)

        return func(*args, **kwargs)

    return wrapper

def baja_eliminacion(func):
    def wrapper( *args, **kwargs):
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
    def wrapper(self, *args, **kwargs):
        modif_registro = os.path.dirname(
            (os.path.abspath(__file__)) + "\\modif_registro.txt"
        )
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        texto = "Modifica registro el " + fecha_hora + "\n"
        with open("modif_registro.txt", "a") as modif_registro:
            modif_registro.write(texto)

        showinfo("MODIFICA, REGISTRO")
        return func(self, *args, **kwargs)

    return wrapper

def selecciona_registros(func):
    def wrapper(self,*args, **kwargs):
        showinfo("SELECCION, REGISTRO")
        return func(self, *args, **kwargs)

    return wrapper

def actu_actualizacion(func):
    def wrapper(self,*args, **kwargs):
        showinfo("ACTUALIZA, BASE")
        return func(self, *args, **kwargs)

    return wrapper

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

    def get_lista_productos(self, idproveedor_id):
        lista_productos = []
        providerid = idproveedor_id["id"]
        for producto in id_productos.select().where(id_productos.idproveedor_id == providerid):
            lista_productos.append(
                {"id": producto.id, "nombre": producto.PRODUCTOS})
        return lista_productos

    @actu_actualizacion
    def actualizar_treeview(self, mitreview):
        records = mitreview.get_children()
        for element in records:
            mitreview.delete(element)
           
        for fila in Ventas.select():
            mitreview.insert("", 0, text=fila.id,
                values=(
                    fila.proveedor_id,
                    fila.producto,
                    fila.var_cantidad,
                    fila.precio,    
                    fila.fecha_inicio,
                    fila.metodo_pago,
                    fila.medico                    
                ) 
            )

    def imprimir(self, fecha_inicio, dnipac, producto, proveedor, cantidad, precio, var_metodo_pago):
            doc = DocxTemplate("invoice1.docx")
            fecha_inicio = datetime.now().strftime("%Y-%m-%d")
            dnipac = dnipac.get()
            producto = producto.get()        
            proveedor = proveedor.get()
            cantidad = cantidad.get()
            precio = precio.get()
            var_metodo_pago = var_metodo_pago.get() 

            doc.render({"var_fecha_inicio": fecha_inicio,
                        "var_dnipac": dnipac,
                        "var_producto": producto,
                        "var_proveedor": proveedor,
                        "var_cantidad": cantidad,
                        "var_precio": precio, 
                        "metodo_pago": var_metodo_pago,
                        })

            doc_name =  producto + "Recibo_de_venta" +\
                datetime.now().strftime("%Y-%m-%d") + ".docx"
            doc.save(doc_name)
            showinfo("Alta recibo", "El recibo esta listo para imprimir")

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
        patron_letras = "^[A-Za-záéíóúñ  ]*$" 
        cadena1 = var_apellido_paciente.get()
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
            ventas.proveedor_id= proveedor.get()
            ventas.producto = producto.get()
            ventas.var_cantidad = var_cantidad.get()
            ventas.precio = precio.get()
            ventas.medico = var_medico.get()
            ventas.medico = var_medico.get()
            ventas.fecha_inicio = var_fecha_inicio
            ventas.metodo_pago = var_metodo_pago.get()
            
            paciente.save()
            productos.save()
            ventas.save() 
            proveedores.save()
 
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
            print(f"Esta es la impresion de valor registro{valor_registro}")
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
        var_metodo_pago,
        tree,
    ):
        cadena = var_nombre_paciente.get()
        patron_letras = "^[A-Za-záéíóúñ]*$"  
        cadena1 = var_apellido_paciente.get()

        if re.match(patron_letras, cadena) and re.match(patron_letras, cadena1):
            valor = tree.selection()
            item = tree.item(valor)
            mi_id = item["text"]
            valor = (mi_id)
            modifica = Ventas.get(Ventas.id == valor)
            modifica = Ventas.update(
                dnipac=dnipac.get(),
                #var_nombre_paciente = var_nombre_paciente.get(),
                #var_apellido_paciente = var_apellido_paciente.get(),
                proveedor = proveedor.get(),
                producto = producto.get(),
                var_cantidad = var_cantidad.get(),
                precio = precio.get(),
                var_medico = var_medico.get(),
                var_metodo_pago = var_metodo_pago.get()
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
        valor = (mi_id)
        #dnipac.set(item["values"][0])
        #var_nombre_paciente.set(item["values"][1])
        #var_apellido_paciente.set(item["values"][2])
        proveedor.set(item["values"][0])
        producto.set(item["values"][1])
        var_cantidad.set(item["values"][2])
        precio.set(item["values"][3])
        var_medico.set(item["values"][4])
        #var_fecha_inicio.set(item["values"][8])
        metodo_de_pago.set(item["values"][5])
        print("HA SELECCIONADO UN REGISTRO")

    
