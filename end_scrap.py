from multiprocessing import Queue
import keyboard

def end_key(queue: Queue):  
    keyboard.wait('esc')

    queue.put('end')     
