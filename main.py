import web_scrapper
import open_browser
import end_scrap
import multiprocessing

if __name__ == "__main__":
    queue = multiprocessing.Queue()
    queue2 = multiprocessing.Queue()

    with open('properties.txt', 'r') as props:
        chrome_path = props.readline()[12:-1]
        hltv_pages_desired = int(props.readline()[26:]) 

        browser_Process = multiprocessing.Process(target=open_browser.exec_browser, args=(queue2,))
        end_Process = multiprocessing.Process(target=end_scrap.end_key, args=(queue,))
        scrapper_Process = multiprocessing.Process(target=web_scrapper.scrap, args=(queue,queue2))  

        browser_Process.start()  
        queue2.put(chrome_path)
        
        scrapper_Process.start() 
        queue.put(hltv_pages_desired)

        end_Process.start()        

        scrapper_Process.join()
        end_Process.terminate()
        browser_Process.terminate()   
    

