import sqlite3

def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    return "No hay inverso"

e = 29
p = 13
q = 11
n = p * q
phi = (p-1) * (q-1)

d = 29

conn = sqlite3.connect('messages.db')

cursor = conn.cursor()

cursor.execute("""SELECT * FROM messages""")

datos = cursor.fetchall()
cipher_text = datos[-1][2]

k = []
for i in cipher_text:
    k.append(ord(i))

print(k)

# Desencriptar mensaje ch^e mod n por cada letra del mensaje encriptado:
message_enc = [pow(ch, 29, n) for ch in k]
message = "".join(chr(ch) for ch in message_enc)
print(message)

conn.commit()

conn.close()