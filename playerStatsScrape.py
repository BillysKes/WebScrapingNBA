import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

driver = webdriver.Chrome()
url = 'https://www.nba.com/stats/leaders'
driver.get(url)
time.sleep(5)  # Waits for 5 seconds
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
player_stats_table=soup.find('table', class_='Crom_table__p1iZz')

if player_stats_table:
    rows = player_stats_table.find_all('tr')[1:]
    player_data = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 0:
            player_name = cells[1].text.strip()
            team = cells[2].text.strip()
            points_per_game = cells[5].text.strip()
            player_data.append({
                'Player Name': player_name,
                'Team': team,
                'Points Per Game': points_per_game
            })
    csv_filename = 'player_stats.csv'
    fieldnames = ['Player Name', 'Team', 'Points Per Game']
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for player in player_data:
            writer.writerow(player)
else:
    print("Player statistics table not found on the webpage.")

driver.quit()
