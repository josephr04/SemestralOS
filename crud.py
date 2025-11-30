from database import conectar

# ===============================================
# CRUD para PLATOS
# ===============================================

def agregar_plato(nombre, precio, imagen, fecha_creacion):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO platos (nombre, precio, imagen, fecha_creacion)
        VALUES (%s, %s, %s, %s)
    """, (nombre, precio, imagen, fecha_creacion))
    conn.commit()
    conn.close()


def obtener_platos():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            id,
            nombre,
            precio,
            imagen,
            fecha_creacion
        FROM platos
        ORDER BY id ASC
    """)
    platos = cur.fetchall()
    conn.close()
    return platos


def actualizar_plato(id_, nombre, precio, imagen):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        UPDATE platos
        SET nombre = %s,
            precio = %s,
            imagen = %s
        WHERE id = %s
    """, (nombre, precio, imagen, id_))
    conn.commit()
    conn.close()


def eliminar_plato(id_):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM platos WHERE id = %s", (id_,))
    conn.commit()
    conn.close()


def existe_plato(nombre):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM platos WHERE LOWER(nombre) = LOWER(%s)", (nombre,))
    existe = cur.fetchone()[0] > 0
    conn.close()
    return existe
