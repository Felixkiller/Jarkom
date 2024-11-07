import socket
import base64
import time

# SMTP commands
HELO_CMD = "HELO client\r\n"
EHLO_CMD = "EHLO client\r\n"
MAIL_FROM_CMD = "MAIL FROM: <{}>\r\n"
RCPT_TO_CMD = "RCPT TO: <{}>\r\n"
DATA_CMD = "DATA\r\n"
QUIT_CMD = "QUIT\r\n"

# SMTP server info
SMTP_SERVER = "smtp.ukdc.ac.id"  # Example: Gmail SMTP server
SMTP_PORT = 587  # Use 587 for TLS, or 465 for SSL
SMTP_USER = "felixjuatsa@gmail.com"  # Replace with your email address
SMTP_PASSWORD = "your_password"  # Replace with your email password (or app password if 2FA enabled)

# Email details
SENDER_EMAIL = "your_email@gmail.com"
RECIPIENT_EMAIL = "friend_email@example.com"
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

    # Greet the server
    send_command(server_socket, HELO_CMD)  # You can replace with EHLO_CMD if needed

    # Authenticate (Optional - You may need this for servers that require authentication)
    # For Gmail, you can use base64 encoding of the password in the AUTH command
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
