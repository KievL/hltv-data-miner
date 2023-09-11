import time
import subprocess
import pygetwindow as gw

def exec_browser(queue):
    #Browser .exe path
    chrome_path = queue.get()
    
    try:
        window1 = gw.getWindowsWithTitle("Google Chrome")

        browser_process = subprocess.Popen(chrome_path) 
        time.sleep(3)

        queue.put('ready_to_start')
        counter = 0

        while True: 
            window2 = gw.getWindowsWithTitle("Google Chrome")           
            if len(window2)<=len(window1) :
                browser_process = subprocess.Popen(chrome_path) 
                queue.put('wait_browser')
                time.sleep(3)
            else:
                queue.put('allowed')
            time.sleep(0.1)

    except WindowsError as e:
        print(f"An error ocurred: {e}")       
        print(f"Use a valid PATH for Google Chrome on properties.txt")   
    except Exception as e:
        print(f"An error ocurred: {e}") 
    finally:
        queue.put('cancel')

