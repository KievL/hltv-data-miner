import time
import subprocess
import pygetwindow as gw

def exec_browser(queue):
    #Browser .exe path
    chrome_path = queue.get()
    
    try:
        #Get number of Chromes oppened before the scrap
        window1 = gw.getWindowsWithTitle("Google Chrome")

        subprocess.Popen(chrome_path) 
        time.sleep(3)
        
        queue.put('ready_to_start')

        while True: 
            #Get the number of Chromes oppened while the scrap is being executed
            window2 = gw.getWindowsWithTitle("Google Chrome")   

            # if len(window2)<=len(window1), means that the chrome oppened to scrap was closed for some reason        
            if len(window2)<=len(window1) :
                subprocess.Popen(chrome_path) 
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

