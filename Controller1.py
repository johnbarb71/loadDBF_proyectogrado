from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from dbfread import DBF
from datetime import date, datetime, timedelta
import mysql.connector
import threading
import os

#COnexion BBDD
cnx = mysql.connector.connect(user='su_usuario', password='su_password',host='127.0.0.1',database='su_database')


   
class Product:

    caminoCantArt = ""


    def __init__(self, window):
        

        cursor = cnx.cursor()

        #ejecuta la exportacion, check y schelude
        def Exportar():
            self.info_label['text'] = "Exportando archivo..."
            # Deshabilitar el botón mientras se descarga el archivo.
            self.export_button['state'] = "disabled"
            # Iniciar la descarga en un nuevo hilo.
            t = threading.Thread(target=exportarCantArt)
            t.start()
            # Comenzar a chequear periódicamente si el hilo ha finalizado.
            schedule_check(t)

        def schedule_check(t):
            frame.after(100, check_if_done, t)

        # Si el hilo ha finalizado, restaruar el botón y mostrar un mensaje.
        def check_if_done(t):
            if not t.is_alive():
                print('termino')
                self.info_label['text'] = "¡El archivo se ha exportado!"
                # Restablecer el botón.
                self.export_button['state'] = "normal"
            else:
                # Si no, volver a chequear en unos momentos.
                schedule_check(t)

        def abrir_archivo():
            self.caminoCantArt = ""

            archivoAbierto = filedialog.askopenfilename(initialdir = "/temp",title = "Seleccione un archivo", filetypes = (("dbf files","*.dbf"),("all files","*.*")))
            # print(archivoAbierto)
            self.caminoCantArt = archivoAbierto
            print(self.caminoCantArt)
            self.name.insert(0,archivoAbierto)

        def exportarCantArt():
            print(self.caminoCantArt)
            table = DBF(self.caminoCantArt, load=True, encoding='unicode_escape')
            print(table._count_records())
            for dato in table:
                print(dato['CODIGO'], dato['NOMBRE'])
                id = int(dato['CODIGO'])
                codigo1 = str(dato['BARRAS'])
                codigo2 = str(dato['BARRA1'])
                linea = str(dato['LINEA'])
                nombre = str(dato['NOMBRE'])
                paqxcaja = int(dato['PAQXCAJA'])
                unixcaja = int(dato['UNIXCAJA'])
                paqxdisp = int(dato['UNIXDISP'])

                add_art = ("INSERT INTO products"
                            "(`id`, `codigo1`, `codigo2`, `linea`, `nombre`, `paqxcaja`, `unixcaja`, `paqxdisp`) "
                            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")

                dato_art = (id,codigo1,codigo2,linea,nombre,paqxcaja,unixcaja,paqxdisp)

                cursor.execute(add_art,dato_art)
                cnx.commit()
            cursor.close()
            cnx.close()

        self.wind = window
        self.wind.title('Exportar Base de Datos')

        
        #label
        self.info_label = Label(self.wind, text = "Esto reescribira la Base de Datos y borrara las cantidades")
        self.info_label.grid(row=0, columnspan=6, sticky = W + E)
        self.info_label.config(fg="white",    # Foreground
                                bg="green",   # Background
                                font=("Verdana",10)) 
        
        #Crear un contenedor
        frame = LabelFrame(self.wind, text = 'Exportar cantidades')
        frame.grid(row = 1, column = 0, columnspan = 6, pady = 20)
        frame.config(fg="black", font=("Verdana", 9))

        #Label
        Label(frame, text = 'Seleccione el archivo').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1,column=1)
        #Button seleccionar archivo DBF
        Button(frame, text = 'Seleccione el INARTICU.dbf', command = abrir_archivo).grid(row=2, column=1)
        
        #Button
        self.export_button = ttk.Button(frame, text = 'Exportar', command = Exportar)
        self.export_button.grid(row=3, columnspan=3, sticky = W + E)

       


if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    #window.iconbitmap('img\Facturafacil.ico')
    window.mainloop()
else:
    print('error entrando a Main')


