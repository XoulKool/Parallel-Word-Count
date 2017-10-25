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

def divide_and_receive_work(ChildConnect, port_num, binding_ip, connecting_ip, book_to_count, name_of_dict_file):
    sender = Sender()
    receiver = Receiver()
    sender.send_txt(port_num, binding_ip, book_to_count)
    receiver.receive_txt(port_num + 1, binding_ip, connecting_ip, name_of_dict_file)
    unpickled_dict = open(name_of_dict_file, "rb")
    word_dict = pickle.load(unpickled_dict)
    ChildConnect.send(word_dict)


pointer_to_time_log = open('master_log.txt', 'a')
pointer_to_word_count = open('word_count.txt', 'w+')
start_time = int(time.time() * 1000000)

total_num_lines = 0

with open('les_mis.txt') as f:
    total_num_lines = sum(1 for _ in f)

os.system("split --lines=" + str((total_num_lines + 3)/3) + " --numeric-suffixes --suffix-length=2 les_mis.txt t")

ParentConnect1, ChildConnect1 = Pipe()
ParentConnect2, ChildConnect2 = Pipe()
ParentConnect3, ChildConnect3 = Pipe()
give_work_to_14 = Process(target=divide_and_receive_work, args=(ChildConnect1, 5000, '10.100.0.13', '10.100.0.14', 't00', 'pickled_dict_from_14'))
give_work_to_25 = Process(target=divide_and_receive_work, args=(ChildConnect2, 5002, '10.100.0.13', '10.100.0.25', 't01', 'pickled_dict_from_25'))
give_work_to_26 = Process(target=divide_and_receive_work, args=(ChildConnect3, 5004, '10.100.0.13', '10.100.0.26', 't01', 'pickled_dict_from_26'))
give_work_to_14.start()
give_work_to_25.start()
give_work_to_26.start()

dict_from_26 = Counter(ParentConnect3.recv())
dict_from_25 = Counter(ParentConnect2.recv())
dict_from_14 = Counter(ParentConnect1.recv())

give_work_to_26.join()
give_work_to_25.join()
give_work_to_14.join()

final_wordCount = dict_from_14 + dict_from_26 + dict_from_25

for k,v in final_wordCount.items():
    pointer_to_word_count.write(k + ':   ' + str(v) + '\n')

end_time = int(time.time() * 1000000)
total_compute_time_ms = str(end_time - start_time)

pointer_to_time_log.write("Total Compute Time (in Microseconds): " + total_compute_time_ms + '\n')
