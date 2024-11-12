import socket
import ssl
import base64

# SMTP commands
HELO_CMD = "HELO client\r\n"
EHLO_CMD = "EHLO client\r\n"
MAIL_FROM_CMD = "MAIL FROM: <{}>\r\n"
RCPT_TO_CMD = "RCPT TO: <{}>\r\n"
DATA_CMD = "DATA\r\n"
QUIT_CMD = "QUIT\r\n"
STARTTLS_CMD = "STARTTLS\r\n"

# SMTP server info
SMTP_SERVER = "smtp.gmail.com"  # Ganti dengan server SMTP Anda
SMTP_PORT = 465  # Port untuk SSL
SMTP_USER = "felixjuatsa@gmail.com"  # Ganti dengan email Anda
SMTP_PASSWORD = "demonakuma666"  # Ganti dengan password aplikasi jika 2FA aktif

# Email details
SENDER_EMAIL = "felix233401012@studentukdc.ac.id"  # Ganti dengan email pengirim
RECIPIENT_EMAIL = "felixjuatsa@gmail.com"  # Ganti dengan email penerima
SUBJECT = "Test Email from SMTP Client"
BODY = "Hello, this is a test email sent from my custom SMTP client."

def create_connection(server, port):
    """Create a TCP connection to the SMTP server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server, port))
    return client_socket

def send_command(socket, command):
    """Send a command to the mail server and receive a response."""
    socket.send(command.encode())
    response = socket.recv(1024).decode()
    print(f"Response: {response}")
    return response

def send_email():
    # Establish TCP connection
    server_socket = create_connection(SMTP_SERVER, SMTP_PORT)

    # Receive server's greeting message
    greeting_response = send_command(server_socket, "")  # Expecting a "220" code
    if "220" not in greeting_response:
        print("Server greeting failed.")
        server_socket.close()
        return

    # Greet the server
    send_command(server_socket, HELO_CMD)  # or EHLO_CMD if preferred (for extended features)
    
    # Request SSL for secure communication (this is necessary for port 587)
    response = send_command(server_socket, SSL_CMD)
    if "220" in response:
        print("STARTTLS accepted, switching to secure connection")
        # Wrap the socket in a TLS layer
        context = ssl.create_default_context()
        server_socket = context.wrap_socket(server_socket, server_hostname=SMTP_SERVER)
        
    # Greet the server
    send_command(server_socket, HELO_CMD)  # or EHLO_CMD if preferred (for extended features)

    # Request SSL for secure communication (this is necessary for port 587)
    response = send_command(server_socket, SSL_CMD)
    if "220" in response:
        print("STARTTLS accepted, switching to secure connection")
        # Wrap the socket in a TLS layer
        context = ssl.create_default_context()
        server_socket = context.wrap_socket(server_socket, server_hostname=SMTP_SERVER)

    # Authenticate (Optional - You may need this for servers that require authentication)
    auth_cmd = "AUTH LOGIN\r\n"
    send_command(server_socket, auth_cmd)
    send_command(server_socket, base64.b64encode(SMTP_USER.encode()).decode() + "\r\n")
    send_command(server_socket, base64.b64encode(SMTP_PASSWORD.encode()).decode() + "\r\n")

    # Specify the sender's email
    send_command(server_socket, MAIL_FROM_CMD.format(SENDER_EMAIL))

    # Specify the recipient's email
    send_command(server_socket, RCPT_TO_CMD.format(RECIPIENT_EMAIL))

    # Start sending the email data
    send_command(server_socket, DATA_CMD)

    # Send the email headers and body
    email_content = f"Subject: {SUBJECT}\r\nTo: {RECIPIENT_EMAIL}\r\nFrom: {SENDER_EMAIL}\r\n\r\n{BODY}\r\n."
    send_command(server_socket, email_content)

    # Quit the session
    send_command(server_socket, QUIT_CMD)
