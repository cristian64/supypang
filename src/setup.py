# Hay que instalar py2exe. Una vez instalado, se debe ejecutar setup.py con el parámetro py2exe:
# C:\ruta_donde_esta_el_codigo\> setup.py py2exe
# (como python está instalado, se reconocerá la extensión .py y se ejecutará correctamente)
#
# Una vez ejecutado el script setup.py, la aplicación "standalone" está en la carpeta dist del directorio.
# A veces no incluye todas las librerías y hay que copiarlas desde C:\Python26\Lib\site-packages\pygame


from distutils.core import setup;
import py2exe;

setup(windows=["main.py"], name='Supy Pang', author='Equipo ME', author_email='buzon@equipome.com', url='www.equipome.com', );


#setup(
#    windows = [
#        {
#            "script": "with_gui.py",
#            "icon_resources": [(1, "myicon.ico")]
#        }
#    ],
#)