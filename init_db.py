from pathlib import Path
import sqlite3
#YYYY-MM-DD HH:MM:SS formato que debo seguir para recordarlo
#primero obtenemos el path del directorio a partir del path del archivo
RUTA_BD = Path(__file__).resolve().parent / "cazachollos.db"
#asignamos string multilinea con el script SQL a la variable SQL_TABLAS
SQL_TABLAS = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Marca (
    id_marca INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_marca TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Modelo (
    id_modelo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_marca INTEGER NOT NULL,
    nombre_modelo TEXT NOT NULL,
    potencia_cv INTEGER,
    combustible TEXT,
    FOREIGN KEY (id_marca) REFERENCES Marca(id_marca)
);

CREATE TABLE IF NOT EXISTS Anunciante (
    id_anunciante INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_anunciante TEXT NOT NULL,
    tipo_vendedor TEXT,
    ubicacion TEXT,
    email TEXT,
    telefono TEXT
);

CREATE TABLE IF NOT EXISTS Anuncio_limpio (
    id_anuncio INTEGER PRIMARY KEY AUTOINCREMENT,
    id_modelo INTEGER NOT NULL,
    id_anunciante INTEGER NOT NULL,
    titulo TEXT,
    anio_matriculacion INTEGER NOT NULL,
    kilometros INTEGER NOT NULL,
    cambio_marchas TEXT,
    fecha_publicacion TEXT,
    estado_anuncio TEXT NOT NULL DEFAULT 'Activo',
    FOREIGN KEY (id_modelo) REFERENCES Modelo(id_modelo),
    FOREIGN KEY (id_anunciante) REFERENCES Anunciante(id_anunciante)
);

CREATE TABLE IF NOT EXISTS Historial_precios (
    id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
    id_anuncio INTEGER NOT NULL,
    fecha_registro TEXT NOT NULL, 
    precio REAL NOT NULL,
    FOREIGN KEY (id_anuncio) REFERENCES Anuncio_limpio(id_anuncio)
);

CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    rol TEXT NOT NULL,
    nombre_de_usuario TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    contrasena TEXT NOT NULL,
    telefono TEXT
);

CREATE TABLE IF NOT EXISTS Preferencias_usuario (
    id_usuario INTEGER PRIMARY KEY,
    factor_chollo REAL NOT NULL DEFAULT 20.0,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS Favorito (
    id_usuario INTEGER NOT NULL,
    id_anuncio INTEGER NOT NULL,
    PRIMARY KEY (id_usuario, id_anuncio),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_anuncio) REFERENCES Anuncio_limpio(id_anuncio)
);

CREATE TABLE IF NOT EXISTS Log_BD (
    id_log INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    tabla_afectada TEXT NOT NULL,
    tipo_operacion TEXT NOT NULL,
    detalles TEXT,
    fecha_hora TEXT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS Datos_empresa (
    id_empresa INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_empresa TEXT NOT NULL,
    cif_empresa TEXT,
    direccion TEXT,
    telefono TEXT,
    email TEXT,
    informacion_empresa TEXT
);
"""


def crear_BD():
    #Crea el archivo SQLite y todas las tablas si no existen.
    if RUTA_BD.exists():
        print(f"La base de datos ya existe en: "+RUTA_BD+". No se ha modificado.")
        return
    conexion = sqlite3.connect(RUTA_BD)     #conectamos a la ruta de la bd
    try:    #ejecutamos el script SQL para crear las tablas
        conexion.executescript(SQL_TABLAS)
        conexion.commit()
    finally:
        conexion.close()


