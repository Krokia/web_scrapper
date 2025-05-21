import requests
from bs4 import BeautifulSoup

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
    hdr = {'User-Agent': 'Mozilla/5.0'}
    
    for player in player_data:
        player_name = player["name"]
        url = "https://en.m.wikipedia.org" + player["page_link"]
        response = requests.get(url, headers=hdr)
        
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, doc_format)
            tables = soup.find("table", {"class": "wikitable"})
            
            if tables:
                for table in tables:
                    if table:
                        tbody = table.find("tbody")
                        print(f"name: {player_name}, n tables: {len(tables)}, tbody: {tbody}")
                        


                

    
player_data = get_best_players()
print(player_data)

player_stats = get_player_stats(player_data)
print(player_stats)

