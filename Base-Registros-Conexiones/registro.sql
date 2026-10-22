CREATE TABLE IF NOT EXISTS conexiones (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Dominio TEXT NOT NULL,
    Fecha_Consulta TEXT NOT NULL,
    Bloqueado INTEGER NOT NULL CHECK(Bloqueado IN (0, 1)),
    Dispositivo INTEGER NOT NULL,
    FOREIGN KEY (Dispositivo) REFERENCES dispositivos(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS dispositivos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Dispositivo TEXT NOT NULL,
    Nombre TEXT
);

CREATE INDEX IF NOT EXISTS dominios_indx ON conexiones(Dominio);
CREATE INDEX IF NOT EXISTS dispositivos_indx ON conexiones(Dispositivo);
CREATE INDEX IF NOT EXISTS fechas_indx ON conexiones(Fecha_Consulta);