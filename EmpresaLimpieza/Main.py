import gi

import sqlite3 as dbapi

from gi.overrides import Gdk

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk



#Crear tabla trabajos
'''try:
    bbdd = dbapi.connect("bbdd.dat")
    cursor = bbdd.cursor()
    #cursor.execute("Create table empleados(nombre text,dni text,telefono text)")
    #cursor.execute("insert into empleados VALUES('Encarnacion','45789432w','986745392')")
    bbdd.commit()
    cursor.execute("select * from empleados")
    for registro in cursor.fetchall():
        print("Nombre: " + registro[0])
        print("Dni: " + registro[1])
        print("Telefono: " + registro[2])
        print("----------")
    bbdd.commit()
except dbapi.OperationalError as erroOperacion:
    print ("upps parece que tenemos un problema (operationalError): " + str(erroOperacion))
except dbapi.DatabaseError as erroBaseDatos:
    print("tratamiento de otra excepcion"+ str(erroBaseDatos))'''





class FiestraPrincipal (Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Empresas a limpiar")
        self.set_size_request(300, 500)
#Creo un Notebook y lo añado a la ventana
        notebook = Gtk.Notebook()
        self.add(notebook)
#Creo la primera pagina del Notebook donde añadire un TreeView y un boton
        paxina1 = Gtk.Box()
        paxina1.set_border_width(10)
        columnas=["Empresa","Direccion","Empleado","Hora"]
        modelo = Gtk.ListStore(str,str,str,str)
#Conexion para añadir los datos de la base de datos de trabajos al TreeView
        try:
            bbdd=dbapi.connect("bbdd.dat")
            cursor = bbdd.cursor()
            cursor.execute("select * from trabajos")
            for registro in cursor.fetchall():
                axenda=[registro[0],registro[1],registro[2],registro[3]]
                modelo.append(axenda)
        except dbapi.OperationalError as erroOperacion:
            print("upps parece que tenemos un problema (operationalError): " + str(erroOperacion))
        except dbapi.DatabaseError as erroBaseDatos:
            print("Error en mostrar la base de datos" + str(erroBaseDatos))

        vista = Gtk.TreeView(model=modelo)

        for i in range(len(columnas)):
            celda = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(columnas[i], celda, text=i)
            vista.append_column(columna)

        caixa = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        caixa.pack_start(vista, False, False, 0)
#Metodo para seleccionar las lineas
        vista.get_selection().connect("changed", self.empresa_seleccionada)


        paxina1.add(caixa)
#Boton eliminar con un metodo para eliminar de la base de datos las empresas seleccionadas
        botonEliminar =Gtk.Button("Eliminar")
        botonEliminar.set_visible(True)
        botonEliminar.connect("clicked",self.empresa_eliminada)
        paxina1.add(botonEliminar)






        paxina2 = Gtk.Box()
        paxina2.set_border_width(10)


        caixaH = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        caixaH.set_homogeneous(True)
        caixaV1= Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        caixaV1.set_homogeneous(True)
        caixaV2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        caixaV2.set_homogeneous(True)


        lblEmpresa=Gtk.Label('Empresa: ')
        lblDireccion=Gtk.Label('Direccion: ')
        lblEmpleado=Gtk.Label('Empleado: ')
        lblHora=Gtk.Label('Hora: ')
        btnAceptar=Gtk.Button("Aceptar")
        btnAceptar.connect("clicked",self.añadir_empresa)

        btnInformacion=Gtk.Button("Informacion")
        btnDatos=Gtk.Button("Datos de contratos")
        btnInformacion.connect("clicked",self.abrir_ventana_informacion)
        btnDatos.connect("clicked",self.abrir_ventana_datos)

        self.entryEmpresa=Gtk.Entry()
        self.entryDireccion=Gtk.Entry()
        btnTrabajadores=Gtk.Button("Ir a trabajadores")
        btnTrabajadores.connect("clicked",self.abrir_ventana_trabajadores)


        self.modeloHora=Gtk.ListStore(str)
        self.modeloHora.append(["8am"])
        self.modeloHora.append(["9am"])
        self.modeloHora.append(["10am"])
        self.modeloHora.append(["11am"])
        self.modeloHora.append(["12am"])
        self.modeloHora.append(["1pm"])
        self.modeloHora.append(["2pm"])
        self.modeloHora.append(["3pm"])
        self.modeloHora.append(["4pm"])
        self.modeloHora.append(["5pm"])
        self.modeloHora.append(["6pm"])
        self.modeloHora.append(["7pm"])
        self.modeloHora.append(["8pm"])
        self.comboHora=Gtk.ComboBox.new_with_model_and_entry(self.modeloHora)
        self.comboHora.set_margin_top(30)
        self.comboHora.set_margin_bottom(30)
        self.comboHora.set_entry_text_column(0)



        self.modeloEmpleado=Gtk.ListStore(str)
        try:
            bbdd=dbapi.connect("bbdd.dat")
            cursor=bbdd.cursor()
            cursor.execute("select * from empleados")
            for registro in cursor.fetchall():
                self.modeloEmpleado.append([registro[0]])
        except dbapi.OperationalError as erroOperacion:
            print("upps parece que tenemos un problema (operationalError): " + str(erroOperacion))
        except dbapi.DatabaseError as erroBaseDatos:
            print("tratamiento de otra excepcion" + str(erroBaseDatos))

        self.comboEmpleado=Gtk.ComboBox.new_with_model_and_entry(self.modeloEmpleado)
        self.comboEmpleado.set_margin_top(30)
        self.comboEmpleado.set_margin_bottom(30)

        self.comboEmpleado.set_entry_text_column(0)



        caixaV2.add(self.entryEmpresa)
        caixaV2.add(self.entryDireccion)
        caixaV2.add(self.comboEmpleado)
        caixaV2.add(self.comboHora)
        caixaV2.add(btnTrabajadores)
        caixaV2.add(btnDatos)

        caixaV1.add(lblEmpresa)
        caixaV1.add(lblDireccion)
        caixaV1.add(lblEmpleado)
        caixaV1.add(lblHora)
        caixaV1.add(btnAceptar)
        caixaV1.add(btnInformacion)


        caixaH.add(caixaV1)
        caixaH.add(caixaV2)

        paxina2.add(caixaH)

        notebook.append_page(paxina2, Gtk.Label('Añadir empresa'))
        notebook.append_page(paxina1, Gtk.Label('Empresas'))

        self.connect ("delete-event",Gtk.main_quit)
        self.show_all()

    def abrir_ventana_trabajadores(self,ventana):
        self.destroy()
        VentanaTrabajadores()

    def abrir_ventana_informacion(self,ventana):
        self.destroy()
        VentanaInformacion()

    def abrir_ventana_datos(self,ventana):
        self.destroy()
        VentanaDatos()

    def añadir_empresa(self,empresa):
        indexHora=self.comboHora.get_active()
        modelHora=self.comboHora.get_model()
        itemHora=modelHora[indexHora]
        indexEmpleado=self.comboEmpleado.get_active()
        modelEmpleado=self.comboEmpleado.get_model()
        itemEmpleado=modelEmpleado[indexEmpleado]
        nEmpresa=self.entryEmpresa.get_text()
        direccion=self.entryDireccion.get_text()
        hora=itemHora[0]
        empleado=itemEmpleado[0]

        try:
            bbdd=dbapi.connect("bbdd.dat")
            cursor=bbdd.cursor()
            cursor.execute("insert into trabajos values('"+nEmpresa+"','"+direccion+"','"+empleado+"','"+hora+"')")
            bbdd.commit()
            self.destroy()
            FiestraPrincipal()
            
            
        except dbapi.OperationalError as erroOperacion:
            print("upps parece que tenemos un problema (operationalError): " + str(erroOperacion))
        except dbapi.DatabaseError as erroBaseDatos:
            print("tratamiento de otra excepcion" + str(erroBaseDatos))

    def empresa_seleccionada(self,seleccion):
        (modelo, punteiro) = seleccion.get_selected()
        self.eleccion=[modelo [punteiro][0], modelo[punteiro][1], modelo[punteiro][2], modelo[punteiro][3]]

    def empresa_eliminada(self,empresa):
        try:
            bbdd = dbapi.connect("bbdd.dat")
            cursor = bbdd.cursor()
            cursor.execute("delete from trabajos where empresa='"+self.eleccion[0]+"'")
            bbdd.commit()
            print("La empresa "+self.eleccion[0]+" ya no es cliente")
            self.destroy()
            FiestraPrincipal()
        except dbapi.OperationalError as erroOperacion:
            print("upps parece que tenemos un problema (operationalError): " + str(erroOperacion))
        except dbapi.DatabaseError as erroBaseDatos:
            print("tratamiento de otra excepcion" + str(erroBaseDatos))





class VentanaTrabajadores (Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Trabajadores")
        self.set_size_request(300,500)

        notebook = Gtk.Notebook()
        self.add(notebook)

        paxina1 = Gtk.Box()
        paxina1.set_border_width(10)
        columnas=["Nombre","Dni","Telefono"]
        modelo=Gtk.ListStore(str,str,str)

        try:
            bbdd = dbapi.connect("bbdd.dat")
            cursor = bbdd.cursor()
            cursor.execute("select * from empleados")
            for registro in cursor.fetchall():
                axenda = [registro[0], registro[1], registro[2]]
                modelo.append(axenda)
        except dbapi.OperationalError as erroOperacion:
            print("upps parece que tenemos un problema (operationalError): " + str(erroOperacion))
        except dbapi.DatabaseError as erroBaseDatos:
            print("Error en mostrar la base de datos" + str(erroBaseDatos))

        vista=Gtk.TreeView(model=modelo)

        for i in range(len(columnas)):
            celda = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(columnas[i], celda, text=i)
            vista.append_column(columna)
        caixa = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        caixa.pack_start(vista, False, False, 0)

        vista.get_selection().connect("changed", self.trabajador_seleccionado)


        paxina1.add(caixa)

        botonEliminar = Gtk.Button("Despedir")
        botonEliminar.set_margin_left(10)
        botonEliminar.set_visible(True)
        botonEliminar.connect("clicked", self.trabajador_despedido)
        paxina1.add(botonEliminar)

        paxina2 = Gtk.Box()
        paxina2.set_border_width(10)

        caixaH = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        caixaH.set_homogeneous(True)
        caixaV1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        caixaV1.set_homogeneous(True)
        caixaV2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        caixaV2.set_homogeneous(True)

        lblNombre = Gtk.Label('Nombre: ')
        lblDni = Gtk.Label('Dni: ')
        lblTelefono = Gtk.Label('Telefono: ')
        btnAceptar= Gtk.Button("Aceptar")
        btnAceptar.connect("clicked",self.contratar_trabajador)
        btnInformacion=Gtk.Button("Informacion")
        btnInformacion.connect("clicked",self.abrir_ventana_informacion)
        btnDatos=Gtk.Button("Datos de contratos")
        btnDatos.connect("clicked",self.abrir_ventana_datos)

        self.entryNombre = Gtk.Entry()
        self.entryDni = Gtk.Entry()
        self.entryTelefono=Gtk.Entry()


        btnEmpresas = Gtk.Button("Ir a empresas")
        btnEmpresas.connect("clicked",self.abrir_ventana_empresas)

        caixaV1.add(lblNombre)
        caixaV1.add(lblDni)
        caixaV1.add(lblTelefono)
        caixaV1.add(btnAceptar)
        caixaV1.add(btnInformacion)
        caixaV2.add(self.entryNombre)
        caixaV2.add(self.entryDni)
        caixaV2.add(self.entryTelefono)
        caixaV2.add(btnEmpresas)
        caixaV2.add(btnDatos)
        caixaH.add(caixaV1)
        caixaH.add(caixaV2)
        paxina2.add(caixaH)

        notebook.append_page(paxina2, Gtk.Label('Contratar empleado'))
        notebook.append_page(paxina1, Gtk.Label('Empleados'))

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def trabajador_seleccionado(self,seleccion):
        (modelo, punteiro) = seleccion.get_selected()
        self.eleccion=[modelo [punteiro][0], modelo[punteiro][1], modelo[punteiro][2]]

    def trabajador_despedido(self,eso):
        try:
            bbdd = dbapi.connect("bbdd.dat")
            cursor = bbdd.cursor()
            cursor.execute("delete from empleados where dni='"+self.eleccion[1]+"'")
            bbdd.commit()
            print(self.eleccion[0]+" fue despedido/a")
            self.destroy()
            VentanaTrabajadores()
        except dbapi.OperationalError as erroOperacion:
            print("upps parece que tenemos un problema (operationalError): " + str(erroOperacion))
        except dbapi.DatabaseError as erroBaseDatos:
            print("tratamiento de otra excepcion" + str(erroBaseDatos))

    def abrir_ventana_empresas(self,ventana):
        self.destroy()
        FiestraPrincipal()

    def abrir_ventana_informacion(self,ventana):
        self.destroy()
        VentanaInformacion()

    def abrir_ventana_datos(self,ventana):
        self.destroy()
        VentanaDatos()

    def contratar_trabajador(self,trabajador):
        nombre=self.entryNombre.get_text()
        dni=self.entryDni.get_text()
        tlf=self.entryTelefono.get_text()
        try:
            bbdd=dbapi.connect("bbdd.dat")
            cursor =bbdd.cursor()
            cursor.execute("insert into empleados values('"+nombre+"','"+dni+"','"+tlf+"')")
            bbdd.commit()
            self.destroy()
            VentanaTrabajadores()
            
        except dbapi.OperationalError as erroOperacion:
            print("upps parece que tenemos un problema (operationalError): " + str(erroOperacion))
        except dbapi.DatabaseError as erroBaseDatos:
            print("tratamiento de otra excepcion" + str(erroBaseDatos))

        print(nombre+" fue contrado/a")

class VentanaInformacion(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Informacion de nuestra empresa")
        self.set_size_request(300,500)
        caixa=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=5)
        caixa.set_homogeneous(True)
        caixaV=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=5)
        caixaV.set_homogeneous(True)

        texto="-Nombre: EmpresaDeLimpieza SL \n" \
              "-Direccion: Calle Limpia 10 \n" \
              "-Numero de contacto: 986 000 00/666 000 666\n" \
              "-Direccion de correo electronico: EmpresaDeLimpiezaSL@tolimpio.com\n" \
              "-Para consultar nuestros precios y mas informacion de la pagina \n ir a nuestra pagina web EmpresaDeLimpiezaSL.org"

        frame=Gtk.Frame()
        frame.set_margin_top(5)
        frame.set_margin_right(5)
        frame.set_margin_bottom(5)
        frame.set_margin_left(5)

        lblInformacion=Gtk.Label(texto)
        lblInformacion.modify_bg(Gtk.StateType.NORMAL,Gdk.Color(65535,65535,65535))
        lblInformacion.set_margin_left(2)
        frame.add(lblInformacion)
        btnIrEmpleados=Gtk.Button("Ir a empleados")
        btnIrEmpleados.connect("clicked",self.abrir_ventana_trabajadores)
        btnIrEmpresas=Gtk.Button("Ir a empresas")
        btnIrEmpresas.connect("clicked",self.abrir_ventana_empresas)
        btnIrDatosContrato=Gtk.Button("Ir a datos de contrato")
        btnIrDatosContrato.connect("clicked",self.abrir_ventana_datos)

        caixaV.add(btnIrEmpresas)
        caixaV.add(btnIrEmpleados)
        caixaV.add(btnIrDatosContrato)

        caixa.add(frame)
        caixa.add(caixaV)

        self.add(caixa)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def abrir_ventana_empresas(self, ventana):
        self.destroy()
        FiestraPrincipal()

    def abrir_ventana_datos(self, ventana):
        self.destroy()
        VentanaDatos()

    def abrir_ventana_trabajadores(self, ventana):
        self.destroy()
        VentanaTrabajadores()


class VentanaDatos(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Datos sobre los contratos")
        self.set_size_request(300,500)
        caixa=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=5)
        caixa.set_homogeneous(True)
        caixaV=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=5)
        caixaV.set_homogeneous(True)

        texto="1.Nostros elegimos al trabajador que realizara el trabajo\n" \
              "2.Nostros daremos la hora a la que se realizara la limpieza\n" \
              "3.Podremos dar por finalizado el contrato cuando nostros\n" \
              "  queramos sin penalizacion ninguna hacia nosotros\n" \
              "\nResumiendo,nosotros mandamos y punto."

        frame=Gtk.Frame()
        frame.set_margin_top(5)
        frame.set_margin_right(5)
        frame.set_margin_bottom(5)
        frame.set_margin_left(5)

        lblInformacion=Gtk.Label(texto)
        lblInformacion.modify_bg(Gtk.StateType.NORMAL,Gdk.Color(65535,65535,65535))
        lblInformacion.set_margin_left(2)
        frame.add(lblInformacion)
        btnIrEmpleados=Gtk.Button("Ir a empleados")
        btnIrEmpleados.connect("clicked",self.abrir_ventana_trabajadores)
        btnIrEmpresas=Gtk.Button("Ir a empresas")
        btnIrEmpresas.connect("clicked",self.abrir_ventana_empresas)
        btnIrInformacion=Gtk.Button("Ir a informacion")
        btnIrInformacion.connect("clicked",self.abrir_ventana_informacion)

        caixaV.add(btnIrEmpresas)
        caixaV.add(btnIrEmpleados)
        caixaV.add(btnIrInformacion)

        caixa.add(frame)
        caixa.add(caixaV)

        self.add(caixa)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def abrir_ventana_empresas(self,ventana):
        self.destroy()
        FiestraPrincipal()

    def abrir_ventana_informacion(self,ventana):
        self.destroy()
        VentanaInformacion()

    def abrir_ventana_trabajadores(self,ventana):
        self.destroy()
        VentanaTrabajadores()

if __name__=="__main__":
    fiestra= FiestraPrincipal()
    Gtk.main()

