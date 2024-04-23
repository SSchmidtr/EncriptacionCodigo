import sqlite3

def enviar(mensaje):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    # Create a table
    conn.execute(f"""INSERT INTO messages (alice, bob, message) VALUES (?, ?, ?)""", ('ALICE', 'BOB', mensaje))
    conn.commit()
    conn.close()
    print("Mensaje enviado correctamente")