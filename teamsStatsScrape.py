import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

driver = webdriver.Chrome()
url = 'https://www.nba.com/stats/teams/traditional'
driver.get(url)
time.sleep(5)  # Waits for 5 seconds
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
player_stats_table = soup.find('table', class_='Crom_table__p1iZz')

if player_stats_table:
    rows = player_stats_table.find_all('tr')[1:]
    team_data = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 0:
            team_name = cells[1].text.strip()
            wins = cells[3].text.strip()
            losses = cells[4].text.strip()
            winRatio = cells[5].text.strip()
            points_per_game = cells[7].text.strip()
            fgRatio = cells[10].text.strip()
            _3pointRatio = cells[13].text.strip()

            team_data.append({
                'Team': team_name,
                'wins': wins,
                'losses': losses,
                'Win Percentage': winRatio,
                'Points Per Game': points_per_game,
                'Field Goal Percentage': fgRatio,
                '3 point Percentage': _3pointRatio
            })
    csv_filename = 'teams_stats.csv'
    fieldnames = ['Team', 'wins', 'losses', 'Win percentage','Points Per Game','Field Goal Percentage', '3 point '
                                                                                                        'Percentage']
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for team in team_data:
            writer.writerow(team)
else:
    print("Player statistics table not found on the webpage.")

driver.quit()
