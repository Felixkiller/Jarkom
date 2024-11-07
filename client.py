import socket
import time

def udp_client():
    server_address = ('localhost', 12000)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1)  # 1 second timeout

    retries = 3  # how many times the client will try to reach the server if no response

    for i in range(10):  # pings 10 times
        send_time = time.time()  # Time when the ping is sent
        message = "ping " + str(send_time)  # Message to be sent

        while retries > 0:
            try:
                # Send the message to the server
                client_socket.sendto(message.encode(), server_address)

                # Wait for a response from the server
                response, _ = client_socket.recvfrom(1024)
                print(f"Received response: {response.decode()} from server.")

                # If response is received, exit the retry loop
                break

            except socket.timeout:
                print(f"Request timed out. Retries left: {retries - 1}")
                retries -= 1
            except Exception as e:
                print(f"An error occurred: {e}")
                break  # Exit if there's another error

        if retries == 0:
            print("Failed to receive a response after 3 retries.")

    # Close the socket after all pings
    client_socket.close()

if __name__ == "__main__":
    udp_client()

