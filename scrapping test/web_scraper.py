import requests
from bs4 import BeautifulSoup
import json

url = 'https://en.m.wikipedia.org/wiki/FIFA_100'
doc_format = 'html.parser'
id_main_table = 'main_table_countries_today'

def get_best_players():
    player_data = []
    hdr = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=hdr)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, doc_format)
        table = soup.find("table", {"class": "wikitable plainrowheaders sortable"})

        if table:
            rows = table.find_all('tr')
            print(f"Number of rows: {len(rows)}")
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 5:
                    player_name = cols[1].a.text.strip()
                    player_link = cols[1].a["href"]
                    player_nationality = cols[2].a.text.strip()

                    if cols[3].a:
                        player_position = cols[3].a.text.strip()
                    else:
                        player_position = cols[3].text.strip()

                    player = {"name": player_name,
                              "page_link": player_link,
                              "nationality": player_nationality,
                              "position": player_position}

                    player_data.append(player)
                        
    
    else:
        print(f"page was not found: {response.status_code}")


    return player_data

def get_player_stats(player_data):
    player_stats = []
    hdr = {'User-Agent': 'Mozilla/5.0'}
    
    for player in player_data:
        player_name = player["name"]
        url = "https://en.m.wikipedia.org" + player["page_link"]
        response = requests.get(url, headers=hdr)
        
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, doc_format)

            tables = soup.find_all("table", {"class": "wikitable"})
            if tables:
                print("- n tables:", len(tables))
                stats = {"player_name": player_name}

                for i, table in enumerate(tables):
                    table_name = ""
                    
                    caption_tag = table.find('caption')
                    if caption_tag:
                        table_title = caption_tag.get_text(strip=True).lower()
                        if "club" in table_title:
                            table_name = "club"
                        elif "national" in table_title and not "international" in table_title:
                            table_name = "national"
                        
                        if table_name:
                            print(f"\n=== Table {i + 1} ===")
                            rows = table.find_all('tr')

                            last_row = rows[-1]
                            values = last_row.find_all("th")

                            goals = values[-1].get_text(strip=True)
                            apps = values[-2].get_text(strip=True)

                            if table_name == "club":
                                stats["club_goals"] = goals
                                stats["club_apps"] = apps
                            else:
                                stats["nat_goals"] = goals
                                stats["nat_apps"] = apps
                print(stats)
                player_stats.append(stats)    

    return player_stats
    
player_data = get_best_players()


player_stats = get_player_stats(player_data)


with open('data/player_data.json', 'w') as fp:
    json.dump(player_data, fp)

with open('data/player_stats.json', 'w') as fp:
    json.dump(player_stats, fp)