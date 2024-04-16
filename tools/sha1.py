class SHA1:
    @staticmethod
    def left_rotate(n, b):
        return ((n << b) | (n >> (32 - b))) & 0xffffffff
    
    @staticmethod
    def sha1(texto):
        texto = bytearray(texto, 'utf-8')  # Convierte el mensaje en bytes
        original_byte_len = len(texto)  # Longitud original del mensaje en bytes
        original_bit_len = original_byte_len * 8  # Longitud original del mensaje en bits
        # Agrega el bit '1' al mensaje
        texto.append(0x80)
        # Agrega bits '0' hasta que la longitud del mensaje en bits sea 448 (mod 512)
        while len(texto) % 64 != 56:
            texto.append(0)
        # Agrega la longitud del mensaje original (antes del padding) como un entero de 64 bits big-endian
        texto += original_bit_len.to_bytes(8, byteorder='big')
        # Inicializa las variables:
        h0 = 0x67452301
        h1 = 0xEFCDAB89
        h2 = 0x98BADCFE
        h3 = 0x10325476
        h4 = 0xC3D2E1F0
        # Procesa cada bloque de 64 bytes
        for i in range(0, len(texto), 64):
            w = [0] * 80
            # Divide el bloque en 16 palabras de 32 bits big-endian
            for j in range(16):
                w[j] = int.from_bytes(texto[i + j*4:i + j*4 + 4], byteorder='big')
            # Extiende las 16 palabras en 80 palabras
            for j in range(16, 80):
                w[j] = SHA1.left_rotate(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1)
            a, b, c, d, e = h0, h1, h2, h3, h4
            # Main loop
            for j in range(80):
                if 0 <= j <= 19:
                    f = (b & c) | ((~b) & d)
                    k = 0x5A827999
                elif 20 <= j <= 39:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                elif 40 <= j <= 59:
                    f = (b & c) | (b & d) | (c & d)
                    k = 0x8F1BBCDC
                elif 60 <= j <= 79:
                    f = b ^ c ^ d
                    k = 0xCA62C1D6
                temp = (SHA1.left_rotate(a, 5) + f + e + k + w[j]) & 0xffffffff
                e = d
                d = c
                c = SHA1.left_rotate(b, 30)
                b = a
                a = temp
            # Añade el hash de este bloque al resultado final
            h0 = (h0 + a) & 0xffffffff
            h1 = (h1 + b) & 0xffffffff
            h2 = (h2 + c) & 0xffffffff
            h3 = (h3 + d) & 0xffffffff
            h4 = (h4 + e) & 0xffffffff
        # Produce el hash final (digest)
        return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

# Uso del algoritmo SHA-1oritmo SHA-1
hash_result = SHA1.sha1("The quick brown fox jumps over the lazy dog")
print("SHA1 Hash:", hash_result)
