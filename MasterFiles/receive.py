import socket                   # Import socket module
import time
import sys
'''
This class provides the utility to recieve a file from a sending server. 

(Turning the server this runs on as a client)
'''
class Receiver():

    '''
	Given a port number (integer) binding_ip(string), connecting_ip[the IP 

address you wish to get the file from](string) and
	the name of the receiving file(string) this function uses sockets to 

receive a 
	txt file from a listening server
    '''
    def receive_txt(self, port_num, binding_ip, connecting_ip, name_of_receiving_file):
	#instantiate socket
        receiving_socket = socket.socket()
	#bind ip of the server to the port number
        receiving_socket.bind((binding_ip, port_num))
	#instantiate a pointer to new file which will store the file to bereceived
        pointer_to_receiving_file = open(name_of_receiving_file, 'wb')
        while (1):
	    #Now try to connect to the server over and over again until a connection is reached.  If a connection cannot be reached try again (every .01 seconds)
            try:
                receiving_socket.connect((connecting_ip, port_num))
            except:
                time.sleep(.01)
                continue
            break
        #Receive data until there is no more to be received.
        while (1):
            data = receiving_socket.recv(4096)
            if not data:
                break
	    #Write data to file
            pointer_to_receiving_file.write(data)
	#close poointer to file and socket connection
        pointer_to_receiving_file.close()
        receiving_socket.close()
