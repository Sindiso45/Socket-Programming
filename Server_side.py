import socket
import xml.etree.ElementTree as ET

# Define consumer function
def consume_data(filename):
    # Parse XML file and retrieve data
    tree = ET.parse(filename)
    root = tree.getroot()

    name_element = root.find('Name')
    name = name_element.text

    # Print the XML file name and the data inside
    print(f"XML File: {filename}")
    print(f"Student Name: {name}")
    # Print other extracted data as needed
    # ...
    print()

# Create client socket and connect to the server
server_address = ('localhost', 6066)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

while True:
    # Receive filename from server
    filename = client_socket.recv(2048).decode()

    # Check if the server has stopped sending data
    if not filename:
        break

    # Consume the data from the XML file
    consume_data(filename)

# Close the client socket
client_socket.close()
