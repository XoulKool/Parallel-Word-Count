import socket                   # Import socket module
import time
import sys
import pickle

class Receiver():

    def receive_txt(self, port_num, binding_ip, connecting_ip, name_of_receiving_file):
        receiving_socket = socket.socket()
        receiving_socket.bind((binding_ip, port_num))
	pointer_to_temp_log = open('temp.txt', 'w+')
        pointer_to_receiving_file = open(name_of_receiving_file, 'wb')
        while (1):
            try:
                receiving_socket.connect((connecting_ip, port_num))
            except:
                #print connecting_ip, ' Not ready. Trying again in 2 seconds'
                time.sleep(.01)
                continue
            break
	pointer_to_temp_log.write(str(int(time.time() * 1000000)) + '\n')
        while (1):
            data = receiving_socket.recv(4096)
            if not data:
                break
            pointer_to_receiving_file.write(data)
        pointer_to_receiving_file.close()
        receiving_socket.close()
	pointer_to_temp_log.close()
