import socket                   # Import socket module
import time
import sys
'''
This class provides a function that makes it very easy to set up a listening server
that sends a file to another server (a connecting client).

For uses with different parallel tests, it is recommended that you serialize
whatever object you are using to pass through if it is not a simple text file. (See documentation on how to do this)

'''
class Sender():

    '''
	Given a port number (integer), an ip_addr (as a string), and a file_to_send 
	(name of file in Current Working Directory (CWD) as string), this function
	carries out all necessary requirements in python to send a file through sockets
    '''
    def send_txt(self, port_num, ip_addr, file_to_send):

	#initialize sending socket, binding the given ip address and port together
        sending_socket = socket.socket()
        sending_socket.bind((ip_addr, port_num))
	#tell this socket to listen for a connection
        sending_socket.listen(5)
        print ip_addr, ' listening on ', port_num, ' ...'
		#initialize objects that will receive the connection from other server 
		#(this is a tuple, where conn is the connection object and addr is the ip_addr of the connecting server)
        conn, addr = sending_socket.accept()
        print 'Got connection from', addr
		#Initialize file pointer which will read the sending file to the sending object 
        pointer_for_sending_file = open(file_to_send, 'rb')
        reader = pointer_for_sending_file.read(4096)
        while (reader):
            try:
                conn.send(reader)
            except (socket.error):
                continue
            reader = pointer_for_sending_file.read(4096)
	
	#close pointer to sending file
        pointer_for_sending_file.close()
        print 'Done Sending'
        conn.send('Thank you for connecting')
	#close connection since it is not being used anymore
        conn.close()
	#close socket since it is not being used anymore
        sending_socket.close()
