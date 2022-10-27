import threading
from queue import Queue
from PIL import Image
import os
import time
import multiprocessing

# file_queue = Queue()

def compress_pic(fileindex):
    files = []
    while True:

        new_files = os.listdir(fileindex)
        comp_files = []
        if len(new_files) > len(files):
            comp_files = set(new_files).difference(set(files))
        files = os.listdir(fileindex)
        comp_files = list(comp_files)



        i = 0
        while i < len(comp_files):
            try:
                thread_A = threading.Thread(target=compress_single,kwargs={"file":fileindex+ "\\" + comp_files[i]})
                thread_B = threading.Thread(target=compress_single, kwargs={"file": fileindex + "\\" + comp_files[i+1]})
                thread_C = threading.Thread(target=compress_single, kwargs={"file": fileindex + "\\" + comp_files[i+2]})
                thread_A.start()
                thread_B.start()
                thread_C.start()
                thread_B.join()
                thread_A.join()
                thread_C.join()
                #im = Image.open(fileindex+ "\\" + comp_files[i])
                #im.save(fileindex+ "\\" + comp_files[i], quality=30)
                i += 3
            except:
                try:
                    thread_A = threading.Thread(target=compress_single,
                                                kwargs={"file": fileindex + "\\" + comp_files[i]})
                    thread_B = threading.Thread(target=compress_single,
                                                kwargs={"file": fileindex + "\\" + comp_files[i + 1]})
                    thread_A.start()
                    thread_B.start()
                    thread_B.join()
                    thread_A.join()
                    i += 2
                except:
                    try:
                        thread_A = threading.Thread(target=compress_single,
                                                    kwargs={"file": fileindex + "\\" + comp_files[i]})
                        thread_A.start()
                        thread_A.join()
                        i += 1
                    except:
                        print(comp_files[i])


                #print("False")



def compress_some(files, fileindex):
    i = 0
    while i < len(files):
        compress_single(fileindex+"\\"+files[i])
        i += 1

def compress_single(file):
    im = Image.open(file)
    im.save(file, quality = 30)

compress_pic("Capture")



