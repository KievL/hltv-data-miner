import web_scraper
import open_browser
import end_scrap
import multiprocessing

if __name__ == "__main__":
    #Queue end_process.py and web_scraper.py
    queue = multiprocessing.Queue()

    #Queue open_brower.py and web_scraper.py
    queue2 = multiprocessing.Queue()


    with open('properties.txt', 'r') as props:
        #chrome.exe PATH
        chrome_path = props.readline()[12:-1]

        #How many result pages are desired to be scraped
        hltv_pages_desired = int(props.readline()[26:]) 

        browser_Process = multiprocessing.Process(target=open_browser.exec_browser, args=(queue2,))
        end_Process = multiprocessing.Process(target=end_scrap.end_key, args=(queue,))
        scrapper_Process = multiprocessing.Process(target=web_scraper.scrap, args=(queue,queue2))  
        
        browser_Process.start() 
        #Send browser path to open_browser module 
        queue2.put(chrome_path)
        
        scrapper_Process.start() 
        #Send number of result pages to be scraped
        queue.put(hltv_pages_desired)

        end_Process.start()        

        scrapper_Process.join()
        end_Process.terminate()
        browser_Process.terminate()   
    

