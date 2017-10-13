import socket                   # Import socket module
import time
import sys
import pickle

class Sender():

    def send_txt(self, port_num, ip_addr, file_to_send):
        sending_socket = socket.socket()
        sending_socket.bind((ip_addr, port_num))
        sending_socket.listen(5)
        print ip_addr, ' listening on ', port_num, ' ...' 
        conn, addr = sending_socket.accept()
        print 'Got connection from', addr
        pointer_for_sending_file = open(file_to_send, 'rb')
        reader = pointer_for_sending_file.read(4096)
        while (reader):
            try:
                conn.send(reader)
            except (socket.error):
                continue
            reader = pointer_for_sending_file.read(4096)
        pointer_for_sending_file.close()
        print 'Done Sending'
        conn.send('Thank you for connecting')
        conn.close()
        sending_socket.close()

    def send_pickle(self, port_num, ip_addr, object_to_pickle):

        sending_socket = socket.socket()
        sending_socket.bind((ip_addr, port_num))
        sending_socket.listenn(5)
        print ip_addr, ' listening...'
        conn, addr = sending_socket.accept()
        print 'Got Connection from ', addr
        data_to_send = pickle.dumps(object_to_pickle)
        conn.send(data_to_send)
        conn.close()
        sending_socket.close()
