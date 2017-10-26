import socket                   # Import socket module
import time
import sys
from send import Sender
from receive import Receiver
from collections import defaultdict
import pickle
import time

pointer_to_log = open('worker_log_14.txt', 'a')

new_receiver = Receiver()
new_receiver.receive_txt(5000, '10.100.0.14', '10.100.0.13', 'book_from_13')

fp_to_book = open("book_from_13","r")

wordcount = defaultdict(int)

for word in fp_to_book.read().split():
    wordcount[word] += 1


pickle_out = open("dict_pickle", "wb")
pickle.dump(wordcount, pickle_out)
pickle_out.close()

new_sender = Sender()
new_sender.send_txt(5001, '10.100.0.14', 'dict_pickle')
end_time = int(time.time() * 1000000)
pointer_to_temp_log = open('temp.txt','r')
start_time = int(pointer_to_temp_log.readline())

total_compute_time_ms = str(end_time - start_time)

pointer_to_log.write("Total Worker Computation Time (In Microseconds): " + total_compute_time_ms + '\n')

pointer_to_log.close()
pointer_to_temp_log.close()
