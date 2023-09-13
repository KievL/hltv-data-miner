import keyboard
import time
import pyperclip
from bs4 import BeautifulSoup
import json
from multiprocessing import Queue
 
def get_result_page(page_url: str, queue: Queue) -> str:
    #Wait till browser is ready to work
    while queue.get() =='wait_browser':
        pass

    keyboard.press_and_release('ctrl+t')
    time.sleep(0.2)
    keyboard.press_and_release('ctrl+l')
    time.sleep(0.2)
    pyperclip.copy(page_url)
    keyboard.press_and_release('ctrl+v')
    time.sleep(0.1)
    keyboard.press_and_release('enter')
    time.sleep(3)
    keyboard.press_and_release('ctrl+a')
    time.sleep(0.4)
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.6)
    keyboard.press_and_release('ctrl+w')
    return pyperclip.paste()

def scrap(queue: Queue, queue2: Queue):      
    matches_href = []
    
    #Start the scrap
    allow_to_go = queue2.get()
    if allow_to_go=='cancel':
        return

    hltv_pages_desired = queue.get()

    #Get every match of each hltv result page (100 matches per page)
    for page in range(hltv_pages_desired):
        attempts = 0
        while True: 
            try:
                url = 'view-source:https://www.hltv.org/results?offset='+str(page*100)
                html_url = get_result_page(url, queue2)
                page_html = BeautifulSoup(html_url, 'html.parser')
                results_target = page_html.find(class_='results-holder allres')
                results_sublist = results_target.find_all(class_='results-sublist')                
            except Exception as e:                                
                print("An error occurred: ", e, ". Trying again...")
                attempts=attempts+1
            else:
                break
            finally:
                if attempts>=6:
                    raise Exception('Not able to get data from HLTV.')


        #Filling the matches_href list with matches URL
        for rsb in results_sublist:
            match_result = rsb.find_all(class_='result')

            for r in match_result:                        
                match_href = r.parent.get('href')
            
                matches_href.append(match_href)

    with open("matches.json", "r") as f1:
        matches_ondisk = json.load(f1)

        #Scraping each match from matches_href list
        for i in range(len(matches_href)):                
            current_match = {}
            href_id = matches_href[i]

            #Check if ESC (Cancel scrap) was pressed
            try:                
                stop_message = queue.get_nowait()
                if stop_message == "end":
                    print('Stopping web scraping')
                    break
            except:
                pass

            #Check if the match ir already on json. If it's not in, the match page will be scraped
            if href_id in matches_ondisk:
                current_match = matches_ondisk[href_id]
            else:
                errors = 0
                while True:
                    try:
                        #Get match html
                        url_match = 'view-source:https://www.hltv.org'+str(matches_href[i])
                        match_html = get_result_page(url_match, queue2)
                        match_html = BeautifulSoup(match_html, 'html.parser')

                        #Get team names
                        for j,teamsName in enumerate(match_html.find_all(class_='team')):
                            if j>1:
                                break
                            current_match['team_'+str(j+1)] = teamsName.find(class_='teamName').string
                        
                        #Get the series (bo3, bo5, bo1...)
                        series = 'bo'+str(len(match_html.find_all(class_='mapholder')))
                        current_match['series'] = series

                        #Get maps picked names
                        maps = match_html.find_all(class_='mapname')
                        maps_list = []
                        for m in maps:
                            maps_list.append(m.string)
                        current_match['maps']=maps_list

                        #Get teams picks and bans
                        bans_t1 = []
                        bans_t2 = []
                        picks_t1 = []
                        picks_t2 = []

                        picks_and_bans = match_html.find_all(class_="standard-box veto-box")                                    
                        picks_and_bans = picks_and_bans[1].find('div').find_all('div')                                   

                        for veto in picks_and_bans:
                            veto_string = veto.string
                            veto_string_list = veto_string.split(" ")

                            if current_match['team_1'] in veto_string:
                                if 'removed' in veto_string:
                                    bans_t1.append(veto_string_list[0]+veto_string_list[-1])
                                elif 'picked' in  veto_string:
                                    picks_t1.append(veto_string_list[0]+veto_string_list[-1])                        
                            elif current_match['team_2'] in veto_string:
                                if 'removed' in veto_string:
                                    bans_t2.append(veto_string_list[0]+veto_string_list[-1])
                                elif 'picked' in  veto_string:
                                    picks_t2.append(veto_string_list[0]+veto_string_list[-1])

                        current_match['bans_team1'] = bans_t1
                        current_match['bans_team2'] = bans_t2
                        current_match['picks_team1'] = picks_t1
                        current_match['picks_team2'] = picks_t2

                        #Get teams players
                        players_t1 = []
                        players_t2 = []

                        players = match_html.find_all(class_='player-nick')  
                        players_names = list(map(lambda name: name.string, players))
                        players_t1 = players_names[:5]
                        players_t2 = players_names[15:20]  

                        current_match['players_team1']=players_t1
                        current_match['players_team2']=players_t2

                        #Get teams ranking
                        rankings = match_html.find_all(class_='teamRanking')
                        try:
                            ranking_team1 = rankings[0].a.text #World ranking #XX
                            ranking_team1 = ranking_team1[ranking_team1.find("#")+1:]
                        except:
                            ranking_team1="Unranked"
                        
                        try:
                            ranking_team2 = rankings[1].a.text #World ranking #XX
                            ranking_team2 = ranking_team2[ranking_team2.find("#")+1:]
                        except:
                            ranking_team2="Unranked"

                        current_match['team1_ranking']=ranking_team1
                        current_match['team2_ranking']=ranking_team2

                        #Get match date
                        date_txt = match_html.find(class_="timeAndEvent").find(class_="date").text.split(' ') #DDDD of MM AAAA
                        day = date_txt[0][:-2] if len(date_txt[0][:-2]) > 1 else '0'+date_txt[0][:-2]
                        year = date_txt[3]

                        def month_to_number(month: str) -> str:
                            if month=='January':
                                return '01'
                            elif month=='Feburary':
                                return '02'
                            elif month=='March':
                                return '03'
                            elif month=='April':
                                return '04'
                            elif month=='May':
                                return '05'
                            elif month=='June':
                                return '06'
                            elif month=='July':
                                return '07'
                            elif month=='August':
                                return '08'
                            elif month=='September':
                                return '09'
                            elif month=='October':
                                return '10'
                            elif month=='November':
                                return '11'
                            else:
                                return '12'
                            
                        month= month_to_number(date_txt[2])
                        date_txt = year+'-'+month+'-'+day
                        current_match['date']=date_txt

                        #Get maps won by each team
                        maps_series = match_html.find_all(class_="mapholder")

                        maps_won_team1 = []
                        maps_won_team2 = []

                        for mp in maps_series:
                                            
                            won_by = mp.find(class_="results-left won")
                            if won_by == None:
                                won_by = mp.find(class_="results-left won pick")                
                                
                            mp_name = mp.find(class_="mapname").text
                            
                            if won_by is None:
                                not_played_map = mp.find(class_="optional")

                                if(not_played_map is None):
                                    maps_won_team2.append(mp_name)

                            else:
                                maps_won_team1.append(mp_name)

                        current_match['maps_won_team1'] = maps_won_team1
                        current_match['maps_won_team2'] = maps_won_team2

                        #Get winstreak and maps won
                        past_matches = match_html.find_all(class_="past-matches-box")
                        past_matches_t1 = past_matches[0]
                        past_matches_t2 = past_matches[1]

                        try:
                            #Format: 'XX match win streak'
                            winstreak_t1 = int(past_matches_t1.find(class_="past-matches-streak").text.split(" ")[0])
                        except:
                            winstreak_t1 = 0
                        
                        try:
                            #Format: 'XX match win streak'
                            winstreak_t2 = int(past_matches_t2.find(class_="past-matches-streak").text.split(" ")[0])
                        except:
                            winstreak_t2 = 0
                        
                        current_match['winstreak_t1'] = winstreak_t1
                        current_match['winstreak_t2'] = winstreak_t2

                        past_maps_won_t1 = 0
                        past_maps_won_t2 = 0
                        past_maps_lost_t1 = 0
                        past_maps_lost_t2 = 0            

                        def count_maps_won_and_lost(pst_matches: str, won=0, lost=0):
                            past_matches_score = pst_matches.find_all(class_='past-matches-score')

                            for scr in past_matches_score:

                                score = scr.text.split('-')
                                #From string to int
                                score = list(map(lambda x : int(x), score))

                                ##Left score or score[0] is t1's score
                                ##Test if it is a series score or a map score
                                
                                if score[0]+score[1]<=5:
                                    won= won + score[0]
                                    lost= lost + score[1]
                                else:
                                    if score[0] > score[1]:
                                        won= won + 1
                                    else:                    
                                        lost= lost+1

                            return won, lost
                        
                        past_maps_won_t1, past_maps_lost_t1 = count_maps_won_and_lost(past_matches_t1)
                        past_maps_won_t2, past_maps_lost_t2 = count_maps_won_and_lost(past_matches_t2)

                        current_match['past_maps_won_t1'] = past_maps_won_t1
                        current_match['past_maps_lost_t1'] = past_maps_lost_t1
                        current_match['past_maps_won_t2'] = past_maps_won_t2
                        current_match['past_maps_lost_t2'] = past_maps_lost_t2

                        #HtH wins and overtimes
                        hth = match_html.find(class_="head-to-head")
                        hth_info = hth.find_all(class_="bold")
                        
                        ## Wins T1 - Overtimes - Wins T2
                        current_match['hth_wins_t1'] = int(hth_info[0].text)
                        current_match['hth_wins_t2'] = int(hth_info[2].text)
                        current_match['hth_overtimes'] = int(hth_info[1].text)
                        break 

                    except Exception as e:
                        errors= errors+1
                        print("Retrying due:", e)
                        if errors>=6:
                            print("Unable to get data from:  ", current_match)
                            break
            
            if href_id not in matches_ondisk:
                matches_ondisk[href_id]=current_match

    with open('matches.json', 'w') as f:
        json.dump(matches_ondisk, f, indent=4)   
