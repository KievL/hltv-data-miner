from multiprocessing import Queue
import keyboard

def end_key(queue: Queue): 
    #If ESC if pressed, the scrap stops and the pages scraped are saved in the JSON file.     
    keyboard.wait('esc')

    queue.put('end')     
