import random 
from enviar_mensaje import enviar
from sha1 import sha1_funcion, hmac_sha1

def modulo(a,b):
    h = 1
    if b < 0:
        h = -1

    i = 0
    resultado = True
    while resultado:
        p = h*i
        num = p*a
        for k in range(a):
            if num + k == b:
                return k
        i+=1

# funcion calcular d
def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    return "No hay inverso"


# Elegir proceso de encriptar
p = 13
q = 11
n = p * q
phi = (p-1) * (q-1)

e = 29

d = mod_inverse(e, phi)

# Crear mensaje
m = input("Ingresa aqui el texto a encriptar: ")

message_encoded = [ord(ch) for ch in m]
cipher_text = [pow(ch, e, n) for ch in message_encoded]
print(cipher_text)

t = ""
for i in cipher_text:
    t += chr(i)

# Desencriptar mensaje ch^e mod n por cada letra del mensaje encriptado:
message_enc = [pow(ch, d, n) for ch in cipher_text]
message = "".join(chr(ch) for ch in message_enc)
print(d)

enviar(t)