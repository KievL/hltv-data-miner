# hltv-data-miner
Web scraper designed to extract data from CS:GO matches featured on HLTV.org.

## How does it work?
HLTV has a protection against requests that blocks the scripts from getting the match pages HTML code using *requests* and *webdriver* libraries. Therefore, this web scraper provides an alternative solution to this problem. The script simulates a browser, opens "manually" the source code of each match page and scrapes it. The idea is to basically automate the manual process of getting the source code of a web page. 

What the program will do is: it will open your Google Chrome, open the source code of each desired website ("view-source:https://www.hltv.org/fallen-is-the-goat", for example), scrape it and save all data scraped in a JSON file. 

The libraries used in order to make this process automatic are: *subprocess*, *keyboard* and *pyperclip*. 
The library used to scraping is *BeautifulSoup*.
*Multiprocessing* is used to coordinate the modules.

## How to use it?
 * __Step 1__: Edit *properties.txt*. On *chrome_path* you have to put Google Chrome's executable path. For example:
 *chrome_path=C:\Program Files\Google\Chrome\Application\chrome.exe*

 After that, on *hltv_result_pages_desired* you have to put how many result pages you want to scrape. Each result page has 100 matches. The scraping process always starts on the first page. So, if you want to scrape the latest 1000 matches, for example, you should put:
 *hltv_result_pages_desired=10*

 * __Step 2__: Inside the directory, run on *CMD* or any terminal: *"python main.py"*

 Or just execute the *main.py* script in some way, and the scraping will start.

 If you want to stop the scraping process, press *ESC*. The scraped matches will be saved in the JSON file.

 You should not use your PC while the script is running. It will take around an hour to scrape data from 750 matches. But you can cancel the process at any point by pressing *ESC*.

## Output object
All data scraped is saved in *matches.json*. The keys in the JSON are matches URL used as IDs. The values are lists containing:

 * *series* : 'bo1', 'bo3' or 'bo5' (string)
 * *maps* : list containing all maps played in the series (list of strings)
 * *team_1* : team 1 name (string)
 * *team_2* : team 2 name (string)
 * *bans_team1* : list containing team 1 bans (list of strings)
 * *bans_team2* : list containing team 2 bans (list of strings)
 * *picks_team1* : list containing team 1 picks (list of strings)
 * *picks_team2* : list containing team 2 picks (list of strings)
 * *players_team1* : list containing team 1 player names (list of strings)
 * *players_team2* : list containing team 2 player names (list of strings)
 * *team1_ranking* : ranking of team 1 when the match was played (string)
 * *team2_ranking* : ranking of team 2 when the match was played (string)
 * *date* : when the match was played YYYY-MM-DD (string)
 * *maps_won_team1* : list containing maps won by team 1 in the series (list of strings)
 * *maps_won_team2* : list containing maps won by team 2 in the series (list of strings)
 * *winstreak_t1* : win streak of the team 1 before the game (int)
 * *winstreak_t2* : win streak of the team 2 before the game (int)
 * *past_maps_won_t1* : maps won in the last 3 months by team 1 (int)
 * *past_maps_won_t2* : maps won in the last 3 months by team 2 (int)
 * *past_maps_lost_t1* : maps lost in the last 3 months by team 1 (int)
 * *past_maps_lost_t2* : maps lost in the last 3 months by team 2 (int)
 * *hth_wins_t1* : head-to-head wins by team 1 (int)
 * *hth_wins_t2* : head-to-head wins by team 2 (int)
 * *hth_overtimes : head-to-head overtimes (int)




