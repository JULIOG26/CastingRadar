CASTINGS_TABLE = """
CREATE TABLE IF NOT EXISTS castings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    empresa TEXT,
    contacto TEXT,
    email TEXT,
    telefono TEXT,
    ciudad TEXT,
    pais TEXT,
    tipo TEXT,
    perfil TEXT,
    descripcion TEXT,
    fecha_publicacion TEXT,
    fecha_limite TEXT,
    url TEXT,
    fuente TEXT,
    estado TEXT DEFAULT 'Nuevo',
    fecha_importacion TEXT
);
"""