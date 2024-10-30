import socket
import des


def server_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5050  # Port to listen on

    server_socket = socket.socket()  # Get instance
    server_socket.bind((host, port))  # Bind host address and port together
    server_socket.listen(1)  # Configure how many clients the server can listen simultaneously
    print(f"Server listening on {host}:{port}...")

    key_string = "ABCD1234"  # Hardcoded key on the server side

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

    print("Waiting for connection...")
    conn, addr = server_socket.accept()  # Accept new connection
    print(f"Got connection from: {addr}\n")

    while True:
        data = conn.recv(1024)  # Receive data stream
        if not data:
            break
        encrypted_message = data.decode('utf-8')
        print(f"✉️  Received from client (encrypted hex): {encrypted_message}")

        decrypted_message = decrypt_message(encrypted_message)
        print(f"🔓 Decrypted message from client: {decrypted_message}\n")

        message_to_send = input("➡️  Send message to the client: ")
        encrypted_response = encrypt_message(message_to_send)
        print(f"🔒 Encrypted message to send (hex): {encrypted_response}\n")
        conn.sendall(encrypted_response.encode())  # Send data to the client

    conn.close()  # Close the connection


if __name__ == '__main__':
    server_program()