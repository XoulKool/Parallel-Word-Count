import socket                   # Import socket module
import time
import sys
from send import Sender
from receive import Receiver
import pickle
import os
import time
from multiprocessing import Process, Pipe
from collections import Counter

#Lucy edited this

NUMPROCESSES = 3

'''
Function which the Process import targets. This function requires:
a ChildConnect [a Pipe object],
a port_num (an int), 
a binding_ip (a string of the ip_address of the machine that you are running this code on), 
a connecting_ip(a string of the ip_address of the machine you would like to receive an object from),
a book_to_count (a string consisting of the name of the book you are sending to the other servers)
and a name_of_dict_file (a string consisting of the name with which you would like to save the object received from another server)


Take careful note, the port_num you use with this function must NOT be within two integers of a port used previously or this codebase will almost certainly not work.
e.g. if this function is called using port_num == 5000 and you wish to use it again, you can not put in the integers 4999-5001 as viable port numbers
considering after the ports 5000 and 5001 will now be taken.
[all other integers are viable options, but I like to go in increments of two, so I would use 5002 as next port]
'''
def divide_and_receive_work(ChildConnect, port_num, binding_ip, connecting_ip, book_to_count, name_of_dict_file):
	#instantiate sender and receiver
    sender = Sender()
    receiver = Receiver()
	#begin sending file
    sender.send_txt(port_num, binding_ip, book_to_count)
	#begin receiving dictionary for other server, being sure to use a different port than the sender
    receiver.receive_txt(port_num + 1, binding_ip, connecting_ip, name_of_dict_file)
	#open file pointer to read from received pickled dictionary file
    unpickled_dict = open(name_of_dict_file, "rb")
	#unpickle dictionary file and save it to an actual dictionary object
    word_dict = pickle.load(unpickled_dict)
	#send dictionary objject through Pipe object to Parent process
    ChildConnect.send(word_dict)


#time stamp beginning of master process
start_time = int(time.time() * 1000000)
#open pointer to log as well txt file which will store the completed word count
pointer_to_time_log = open('master_log.txt', 'a')
pointer_to_word_count = open('word_count.txt', 'w+')

#Initialize a variable to count the total number of lines in the txt file to send
total_num_lines = 0
#Use loop to calculate total nummber of lines in file
with open('les_mis.txt') as f:
    total_num_lines = sum(1 for _ in f)
#Use OS command to split the file into three places by the total number of lines/# of workers
os.system("split --lines=" + str((total_num_lines + NUMPROCESSES)/NUMPROCESSES) + " --numeric-suffixes --suffix-length=2 les_mis.txt t")

#Create Pipes that the Parents and Child can send objects through, one for each parent-child process
ParentConnect1, ChildConnect1 = Pipe()
ParentConnect2, ChildConnect2 = Pipe()
ParentConnect3, ChildConnect3 = Pipe()
#Use process module to set up processes which invoke previously defined function
# as a separate process which distributes and then retrieves work from the connecting worker
give_work_to_14 = Process(target=divide_and_receive_work, args=(ChildConnect1, 5000, '10.100.0.13', '10.100.0.14', 't00', 'pickled_dict_from_14'))
give_work_to_25 = Process(target=divide_and_receive_work, args=(ChildConnect2, 5002, '10.100.0.13', '10.100.0.25', 't01', 'pickled_dict_from_25'))
give_work_to_26 = Process(target=divide_and_receive_work, args=(ChildConnect3, 5004, '10.100.0.13', '10.100.0.26', 't01', 'pickled_dict_from_26'))
#Begin these processes
give_work_to_14.start()
give_work_to_25.start()
give_work_to_26.start()

#Open pipe to child to receive work from each process

#In particular, the work that is passed through are dictionaries.
#We can use the Counter module (available in Python standard lib)
#To then add up all of the values of all of the dictionaries.
#This gives an effective way to combine all of the frequenies of words counted by all of the workers

dict_from_26 = Counter(ParentConnect3.recv())
dict_from_25 = Counter(ParentConnect2.recv())
dict_from_14 = Counter(ParentConnect1.recv())
#Wait until all these processes are done and join them back to Parent
give_work_to_26.join()
give_work_to_25.join()
give_work_to_14.join()

#Use the Counter aspect of these dictionaries to add up all of the values of the unique keys to get a final wordcount
final_wordCount = dict_from_14 + dict_from_26 + dict_from_25

#Use a loop to print each word and it's number of occurences in a txt file.
for k,v in final_wordCount.items():
    pointer_to_word_count.write(k + ':   ' + str(v) + '\n')
#Timestammp for end compute time
end_time = int(time.time() * 1000000)
#Calculate total compute time
total_compute_time_ms = str(end_time - start_time)
#Write total compute time to log
pointer_to_time_log.write("Total Compute Time (in Microseconds): " + total_compute_time_ms + '\n')
