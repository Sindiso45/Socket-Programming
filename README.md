# Socket Programming. Producer-Consumer Problem

This is a Python implementation of the Producer-Consumer problem using threading, synchronization, and socket programming. The program simulates a producer generating student data and a consumer processing that data.

## Requirements

- Python 3.x

## Usage

1. Run the `Server_side.py and Client_side` file to start the producer and server threads.
2. The producer generates random student data and saves it in XML files.
3. The consumer consumes the data from the XML files and performs calculations.
4. The consumer prints the student information, average marks, and pass/fail status.
5. The server thread communicates with the client using socket programming.
6. The client receives the filenames of the XML files and can consume the data.

## Customization

- You can modify the `ITstudent` class to include additional fields or modify the existing ones according to your requirements.
- Adjust the sleep time in the `producer` and `consumer` functions to control the rate at which data is produced and consumed.
- Customize the server address and port in the code if needed.

## Notes

- This implementation is a basic demonstration and may require additional error handling and exception management in a production environment.
- The code assumes a local environment; modify the server address if running on a different network or host.
