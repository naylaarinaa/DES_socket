import socket
import des


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5050  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    print(f"Connected to server at {host}:{port}\n")

    key_string = "ABCD1234"  # Hardcoded key on the client side
    def encrypt_message(message):
        des.reset_state()
        des.initialize_key(key_string)
        des.plain_to_binary(message)
        des.apply_pads()
        cipher_bits = ''.join(des.encryption_DES(i, i + 64) for i in range(0, len(des.text_bits), 64))
        return ''.join(des.binary_to_hex[cipher_bits[i:i + 4]] for i in range(0, len(cipher_bits), 4))

    def decrypt_message(hex_cipher):
        des.reset_state()
        des.initialize_key(key_string)
        des.keys.reverse()
        des.text_bits[:] = [int(bit) for bit in ''.join(des.hex_to_binary[char] for char in hex_cipher)]
        des.apply_pads()
        bin_message = ''.join(des.decryption_DES(i, i + 64) for i in range(0, len(des.text_bits), 64))
        return ''.join(des.binary_to_text[bin_message[i:i + 8]] for i in range(0, len(bin_message), 8))

    while True:
        message_to_send = input("➡️  Send message to the server: ")
        if message_to_send.lower().strip() == 'bye':
            break  # Exit loop if the user types 'bye'
        
        encrypted_message = encrypt_message(message_to_send)
        print(f"🔒 Encrypted message (hex): {encrypted_message}\n")
        client_socket.sendall(encrypted_message.encode())

        data = client_socket.recv(1024)
        if not data:
            break
        encrypted_response = data.decode('utf-8')
        print(f"✉️  Received from server (encrypted hex): {encrypted_response}")

        decrypted_response = decrypt_message(encrypted_response)
        print(f"🔓 Decrypted message from server: {decrypted_response}\n")

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
