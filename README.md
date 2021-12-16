# Quini 6 Scrapping

Web Scrapping de la pagina Quini 6 https://www.quini-6-resultados.com.ar/ con Selenium.\
Se obtienen los resultadors de los sorteos y se almacenan en una base de datos Sqlite3

Para instalar el virtualenv -> virtualenv --python=/usr/bin/python3 venv
Luego de esto configuramos el ide para que use el python que se nos creo en venv/bin/python
Esto lo hacemos desde Preferences(o settings) y buscamos "Python Interpreter"

Para instalar todas las librerias necesarias para poder correr el proyecto debemos activar el virtualenv ´source venv/bin/activate´ (desde una consola)
Y luego correr el comando ´pip3 install -r requirements.txt´. Esto lo que va hacer es instalar todas las dependencias dentro del entorno virtual
