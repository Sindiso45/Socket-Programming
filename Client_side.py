import threading
import random
import xml.etree.ElementTree as ET
import os
import time
import queue
import socket

# Define ITstudent class
class ITstudent:
    def __init__(self, name, id, program, courses):
        self.name = name
        self.id = id
        self.program = program
        self.courses = courses

    def average_mark(self):
        return sum(self.courses.values()) / len(self.courses)

    def passed(self):
        return self.average_mark() >= 50

# Shared Buffer/Queue
buffer = queue.Queue(maxsize=10)
buffer_lock = threading.Lock()
buffer_full = threading.Semaphore(0)
buffer_empty = threading.Semaphore(10)

# Define producer function
def producer():
    while True:
        buffer_empty.acquire()  # Wait if buffer is full
        buffer_lock.acquire()

        # Generate random data for ITstudent
        name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
        id = ''.join(random.choices('0123456789', k=8))
        program = random.choice(['BSc Computer Science', 'BSc Software Engineering', 'BSc Information Technology'])
        courses = {
            'Programming': random.randint(0, 100),
            'Database': random.randint(0, 100),
            'Networking': random.randint(0, 100)
        }
        # Create ITstudent instance and wrap into XML
        student = ITstudent(name, id, program, courses)
        root = ET.Element('ITstudent')
        name_element = ET.SubElement(root, 'Name')
        name_element.text = student.name
        id_element = ET.SubElement(root, 'ID')
        id_element.text = student.id
        program_element = ET.SubElement(root, 'Program')
        program_element.text = student.program
        courses_element = ET.SubElement(root, 'Courses')
        for course, mark in student.courses.items():
            course_element = ET.SubElement(courses_element, 'Course')
            course_element.set('name', course)
            mark_element = ET.SubElement(course_element, 'Mark')
            mark_element.text = str(mark)
        # Save XML to file
        filename = f'student{len(os.listdir(".")) + 1}.xml'
        tree = ET.ElementTree(root)
        tree.write(filename)

        buffer.put(filename)  # Add filename to the buffer
        buffer_lock.release()
        buffer_full.release()  # Signal that buffer has data

        time.sleep(1)  # Sleep for some time before producing the next item

# Define consumer function
def consumer():
    while True:
        buffer_full.acquire()  # Wait if buffer is empty
        buffer_lock.acquire()

        filename = buffer.get()  # Get filename from buffer
        buffer_lock.release()
        buffer_empty.release()  # Signal that buffer has space

        # Parse XML file and create ITstudent instance
        tree = ET.parse(filename)
        root = tree.getroot()
        name_element = root.find('Name')
        name = name_element.text
        id_element = root.find('ID')
        id = id_element.text
        program_element = root.find('Program')
        program = program_element.text
        courses_element = root.find('Courses')
        courses = {}
        for course_element in courses_element:
            course_name = course_element.get('name')
            mark_element = course_element.find('Mark')
            mark = int(mark_element.text)
            courses[course_name] = mark
        student = ITstudent(name, id, program, courses)

        # Calculate average and pass/fail
        average = student.average_mark()
        if student.passed():
            pass_fail = 'Pass'
        else:
            pass_fail = 'Fail'

        # Print student information and results
        print(f'Student Name: {student.name}')
        print(f'Student ID: {student.id}')
        print(f'Programme: {student.program}')
        print('Courses and Marks:')
        for course, mark in student.courses.items():
            print(f'  {course}: {mark}')
        print(f'Average Mark: {average:.2f}')
        print(f'Pass/Fail: {pass_fail}')
        print()

        os.remove(filename)  # Remove XML file

        time.sleep(1)  # Sleep for some time before consuming the next item

# Define server function
def server():
    server_address = ('localhost', 6066)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)

    while True:
        print('Waiting for a client to connect...')
        client_socket, client_address = server_socket.accept()
        print(f'Client connected: {client_address}')

        cons_thread = threading.Thread(target=consumer)
        cons_thread.start()

        while True:
            filename = buffer.get()  # Get filename from buffer

            # Send filename to the client
            client_socket.sendall(filename.encode())

            # Check if the server has stopped sending data
            if not filename:
                break

            time.sleep(1)  # Sleep for some time before sending the next filename

        cons_thread.join()  # Wait for consumer thread to finish

        client_socket.close()

# Start producer and server threads
prod_thread = threading.Thread(target=producer)
server_thread = threading.Thread(target=server)
prod_thread.start()
server_thread.start()
