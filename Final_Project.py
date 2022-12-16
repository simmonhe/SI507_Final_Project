from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import os
import json
import requests

# Get the website html

def fetch_data(*, update:bool = False, json_cache:str, url:str):
    if update:
        json_data = None
    else:
        try:
            with open(json_cache, 'r') as file:
                json_data = json.load(file)
                print("fetched data from local cache!")
        except(FileNotFoundError, json.JSONDecodeError) as e:
            print(f'No local cache found... ({e})')
            json_data = None
    if not json_data:
        print("Fetching new json data... (Creating local cache)")
        json_data = requests.get(url).json()
        with open(json_cache,'w') as file:
            json.dump(json_data,file)

    return json_data

url = 'https://www.basketball-reference.com/leagues/NBA_2022.html'
json_cache = 'final_cache.json'
# data: dict=fetch_data(update=False, json_cache=json_cache,url=url)
req = Request(url)
html_page = urlopen(req)
soup = BeautifulSoup(html_page, 'html.parser')

# print(soup)



class Node:
  def __init__(self, value):
    self.value = value
    self.child_node = []

    # parameter for teams
    self.team_name = ''
    self.team_age = 0
    self.team_wins=0
    self.team_losses=82
    self.team_pts=0
    self.team_off_rtg=0
    self.team_def_rtg=0
    self.team_pace=0
    self.team_threePA=0
    self.team_trb=0
    self.team_ast=0
    self.team_stl=0
    self.team_blk=0
    self.team_star=''
    self.team_E_or_W=''
    self.team_ws_total=0
    self.team_ws_top=0
    self.team_ws={}
    self.team_player={}

    self.star_stat={}
    self.star_name=''

  def set_child_node(self, new_child_node):
    self.child_node.append(new_child_node)
    
  def get_child_node(self):
    return self.child_node
  
  def get_value(self):
    return self.value
  
League=Node(0)
East=Node(1)
West=Node(1)
League.set_child_node(East)
League.set_child_node(West)
# print(League.get_child_node())
# print(East.value)
team_dict={}
team_abbreviation_dict={'Hawks':'ATL', 'Celtics':'BOS', 'Nets':'BRK', 'Hornets':'CHO', 'Bulls':'CHI', 'Cavaliers':'CLE', 'Mavericks':'DAL', 'Nuggets':'DEN', 'Pistons': 'DET', 'Warriors':'GSW', 'Rockets':'HOU', 'Pacers':'IND', 'Clippers':'LAC', 'Lakers':'LAL', 'Grizzlies':'MEM', 'Heat':'MIA', 'Bucks':'MIL', 'Timberwolves':'MIN', 'Pelicans':'NOP', 'Knicks':'NYK', 'Thunder':'OKC', 'Magic':'ORL', '76ers':'PHI', 'Suns':'PHO', 'Blazers':'POR', 'Kings':'SAC', 'Spurs':'SAS', 'Raptors':'TOR', 'Jazz':'UTA', 'Wizards':"WAS"}
team_color_dict={'Hawks':'#C8102E',  'Celtics':'#007A33', 'Nets':'#000000', 'Hornets':'#1D1160', 'Bulls':'#CE1141', 'Cavaliers':'#860038', 'Mavericks':'#00538C', 'Nuggets':'#0E2240', 'Pistons': '#1D42BA', 'Warriors':'#1D428A', 'Rockets':'#CE1141', 'Pacers':'#FDBB30', 'Clippers':'#C8102E', 'Lakers':'#552583', 'Grizzlies':'#5D76A9', 'Heat':'#98002E', 'Bucks':'#00471B', 'Timberwolves':'#0C2340', 'Pelicans':'#0C2340', 'Knicks':'#F58426', 'Thunder':'#007AC1', 'Magic':'#0077C0', '76ers':'#006BB6', 'Suns':'#E56020', 'Blazers':'#E03A3E', 'Kings':'#5A2D81', 'Spurs':'#C4CED4', 'Raptors':'#CE1141', 'Jazz':'#002B5C', 'Wizards':"#002B5C"}
team_lst=list(team_abbreviation_dict.keys())
MIA_dict={}
# print(team_abbreviation_dict['Hawks'])
# print(team_lst)



# STEP!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# initialze all the teams, spliting by conference
table_confs_standings_E=soup.find('table', id='confs_standings_E')
# print(table_confs_standings_E)
rows_confs_standings_E = table_confs_standings_E.find_all('tr')
# print(rows_confs_standings_E)
for row in rows_confs_standings_E:
  if row.a:
    lst=row.a.text.split(' ')
    # print(lst)
    team_name=lst[1]
    if len(lst)==3:
      team_name=lst[2]
    # print(team_name)
    team_dict[team_name]=Node(2)
    team_dict[team_name].team_E_or_W='East'
    team_dict[team_name].team_name=team_name
    East.set_child_node(team_dict[team_name])

table_confs_standings_W=soup.find('table', id='confs_standings_W')
rows_confs_standings_W = table_confs_standings_W.find_all('tr')
for row in rows_confs_standings_W:
  if row.a:
    lst=row.a.text.split(' ')
    # print(lst)
    team_name=lst[1]
    if len(lst)==3:
      team_name=lst[2]
    # print(team_name)
    team_dict[team_name]=Node(2)
    team_dict[team_name].team_E_or_W='West' 
    team_dict[team_name].team_name=team_name
    West.set_child_node(team_dict[team_name])

# print(team_dict['Warriors'].team_E_or_W)


# STEP!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# scraping data for each team
table_advanced=soup.find('table', id='advanced-team')
rows_advanced = table_advanced.find_all('tr')
for row in rows_advanced:
  xs=row.find_all('th')
  cols=row.find_all('td')
  lst=[]
  
  for col in cols:
    if row.a:
      lst=row.a.text.split(' ')
      # print(lst)
      team_name=lst[1]
      if len(lst)==3:
        team_name=lst[2]
      # print(team_name)
    if(col.get('data-stat')=='age'):
      # print(col.text)
      team_dict[team_name].team_age = col.text
    elif (col.get('data-stat')=='wins'):
      # print(col.text)
      team_dict[team_name].team_wins = col.text
    elif (col.get('data-stat')=='losses'):
      # print(col.text)
      team_dict[team_name].team_losses = col.text
    elif (col.get('data-stat')=='off_rtg'):
      # print(col.text)
      team_dict[team_name].team_off_rtg = col.text
    elif (col.get('data-stat')=='def_rtg'):
      # print(col.text)
      team_dict[team_name].team_def_rtg = col.text
    elif (col.get('data-stat')=='pace'):
      # print(col.text)
      team_dict[team_name].team_pace = col.text


table_per_game=soup.find('table', id='per_game-team')
rows_per_game = table_per_game.find_all('tr')

for row in rows_per_game:
  xs=row.find_all('th')
  cols=row.find_all('td')
  lst=[]
  for col in cols:
    if col.a:
      lst=col.a.text.split(' ')
      # print(lst)
      team_name=lst[1]
      if len(lst)==3:
        team_name=lst[2]
    # print(team_lst)
    if(col.get('data-stat')=='fg3a'):
      # print(col.text)
      team_dict[team_name].team_threePA = col.text
    elif (col.get('data-stat')=='pts'):
      # print(col.text)
      team_dict[team_name].team_pts = col.text
    elif (col.get('data-stat')=='trb'):
      # print(col.text)
      team_dict[team_name].team_trb = col.text
    elif (col.get('data-stat')=='ast'):
      # print(col.text)
      team_dict[team_name].team_ast = col.text
    elif (col.get('data-stat')=='blk'):
      # print(col.text)
      team_dict[team_name].team_blk = col.text
    elif (col.get('data-stat')=='stl'):
      # print(col.text)
      team_dict[team_name].team_stl = col.text

# print(team_dict['Pelicans'].team_stl)
# print(team_dict['Pelicans'].value)
# print(team_dict['Pelicans'].team_E_or_W)


# Funtion starts here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Scraping player ws data for each team.
# @cached_token('token-cache-2222.json')
def scrap_each_team_url(team_abbr):
  url = 'https://www.basketball-reference.com/teams/'+team_abbr+'/2022.html'

  req = Request(url)
  html_page = urlopen(req)
  soup = BeautifulSoup(html_page, 'html.parser')
  return soup

def scrap_each_team_player(team_full_name):
    team_abbr=team_abbreviation_dict[team_full_name]
    soup1=scrap_each_team_url(team_abbr)
    # print(soup)
    table_advanced=soup1.find('table', id='advanced')
    # print(table_advanced)
    rows_team_advanced = table_advanced.find_all('tr')
    # print(rows_team_advanced)
    team_dict[team_full_name].team_ws_total=0.0
    team_dict[team_full_name].team_ws_top=0.0
    for row in rows_team_advanced:
        cols=row.find_all('td')
        for col in cols:
            if(col.get('data-stat')=='player'):
                # print(col.text)
                player_name=col.text
            elif (col.get('data-stat')=='ws'):
                # print(player_name)
                # print(team_full_name)
                # print(col.text)
                team_dict[team_full_name].team_player[player_name] = col.text
                team_dict[team_full_name].team_ws_total += float(col.text)
                if float(col.text)>team_dict[team_full_name].team_ws_top:
                    team_dict[team_full_name].team_ws_top=float(col.text)
                    team_dict[team_full_name].team_star=player_name
        
    table_per_game=soup1.find('table', id='per_game')
    # print(table_advanced)
    rows_team_per_game = table_per_game.find_all('tr')
    # print(rows_team_advanced)
    for row in rows_team_per_game:
        left_cols=row.find_all('td', {"class": "left"})
        cols=row.find_all('td',{'class': "right"})
        star_flag=False
        for left_col in left_cols:
        # print(left_col.text)
            if left_col.text==team_dict[team_full_name].team_star:
                star_flag=True
        # print(star_flag)
        for col in cols:
            if (col.get('data-stat')=='pts_per_g' and star_flag==True):
                # print(col.text)
                team_dict[team_full_name].star_stat['pts'] = col.text
                # print(team_dict[team_name].star_stat['pts'])
            elif (col.get('data-stat')=='trb_per_g' and star_flag==True):
                # print(col.text)
                team_dict[team_full_name].star_stat['trb'] = col.text
            elif (col.get('data-stat')=='ast_per_g' and star_flag==True):
                # print(col.text)
                team_dict[team_full_name].star_stat['ast'] = col.text
            elif (col.get('data-stat')=='stl_per_g' and star_flag==True):
                # print(col.text)
                team_dict[team_full_name].star_stat['stl'] = col.text
            elif (col.get('data-stat')=='blk_per_g' and star_flag==True):
                # print(col.text)
                team_dict[team_full_name].star_stat['blk'] = col.text
scrap_each_team_player('Bucks')
# print(team_dict['Bucks'].team_player['Jrue Holiday'])
# print(team_dict['Bucks'].team_star)
# print(team_dict['Bucks'].team_ws_top)
# print(team_dict['Bucks'].team_ws_total)


def find_team_in_conference(team_lst,E_or_W):
    E_or_W_team_lst=[]
    for i in team_lst:
        if team_dict[i].team_E_or_W==E_or_W:
            E_or_W_team_lst.append(team_dict[i].team_name)
    return E_or_W_team_lst
find_team_in_conference(team_lst,'West')


def find_offensive_team(team_lst, team_lst_selected):
    high_score_lst=[]
    offensive_team_lst=[]
    for i in team_lst:
        high_score_lst.append(float(team_dict[i].team_off_rtg))
    high_score_lst.sort()
    tenth_high_score=high_score_lst[-15]
    # print(high_score_lst)
    # print(tenth_high_score)
    for i in team_lst_selected:
        if float(team_dict[i].team_off_rtg)>=tenth_high_score:
            offensive_team_lst.append(team_dict[i].team_name)
        #   print(offensive_team_lst)
    return offensive_team_lst
# find_offensive_team(team_lst)


def find_defensive_team(team_lst, team_lst_selected):
    lost_score_lst=[]
    defensive_team_lst=[]
    for i in team_lst:
        lost_score_lst.append(float(team_dict[i].team_def_rtg))
    lost_score_lst.sort()
    tenth_low_score=lost_score_lst[15]
    #   print(lost_score_lst)
    #   print(tenth_low_score)
    for i in team_lst_selected:
        if float(team_dict[i].team_def_rtg)<=tenth_low_score:
            defensive_team_lst.append(team_dict[i].team_name)
        #   print(defensive_team_lst)
    return defensive_team_lst
# find_defensive_team(team_lst)


def find_threePA_team(team_lst, team_lst_selected, favor):
    value_lst=[]
    new_team_lst=[]
    for i in team_lst:
        value_lst.append(float(team_dict[i].team_threePA))
    value_lst.sort()
    #   print(value_lst)
    if favor==True:
        tenth_high_score=value_lst[-15]
    #   print(tenth_high_score)
        for i in team_lst_selected:
            if float(team_dict[i].team_threePA)>=tenth_high_score:
                new_team_lst.append(team_dict[i].team_name)
        #   print(new_team_lst)
    elif favor==False:
        tenth_low_score=value_lst[15]
        for i in team_lst_selected:
            if float(team_dict[i].team_threePA)<=tenth_low_score:
                new_team_lst.append(team_dict[i].team_name)
    return new_team_lst

# find_threePA_team(team_lst,True)


def find_pace_team(team_lst, team_lst_selected, fast):
    value_lst=[]
    new_team_lst=[]
    for i in team_lst:
        value_lst.append(float(team_dict[i].team_pace))
    value_lst.sort()
    #   print(value_lst)
    if fast==True:
        tenth_high_score=float(value_lst[-15])
        # print(tenth_high_score)
        for i in team_lst_selected:
            if float(team_dict[i].team_pace)>=tenth_high_score:
                new_team_lst.append(team_dict[i].team_name)
        # print(new_team_lst)
        return new_team_lst
    else:
        tenth_low_score=value_lst[15]
        # print(tenth_low_score)
        for i in team_lst_selected:
            if float(team_dict[i].team_pace)<=tenth_low_score:
                new_team_lst.append(team_dict[i].team_name)
        # print(new_team_lst)
        return new_team_lst


def find_age_team(team_lst, team_lst_selected, young):
    value_lst=[]
    new_team_lst=[]
    for i in team_lst:
        value_lst.append(float(team_dict[i].team_age))
    value_lst.sort()
    #   print(value_lst)
    if young==False:
        tenth_high_score=float(value_lst[-15])
        # print(tenth_high_score)
        for i in team_lst_selected:
            if float(team_dict[i].team_age)>=tenth_high_score:
                new_team_lst.append(team_dict[i].team_name)
        # print(new_team_lst)
        return new_team_lst
    else:
        tenth_low_score=value_lst[15]
        # print(tenth_low_score)
        for i in team_lst_selected:
            if float(team_dict[i].team_age)<=tenth_low_score:
                new_team_lst.append(team_dict[i].team_name)
        # print(new_team_lst)
        return new_team_lst

# fast=False
# # print(team_lst)
# find_pace_team(team_lst,fast)
# for team in team_lst:
#   print(team)
#   star_name= team_dict[team].team_star
#   team_dict[team].team_star=Node(3)
#   team_dict[team].team_star.star_name=star_name
#   team_dict[team].set_child_node(team_dict[team].team_star)
#   lst=team_dict[team].get_child_node()
#   for i in lst:
#     print(i.star_name)


def already_1():
    print("Which team do you want to know more about?")
    usr_already_team=input()
    print(usr_already_team, 'points per game', team_dict[usr_already_team].team_pts)
    print(usr_already_team, 'rebounds per game', team_dict[usr_already_team].team_trb)
    print(usr_already_team, 'assists per game', team_dict[usr_already_team].team_ast)
    print(usr_already_team, 'blocks per game', team_dict[usr_already_team].team_blk)
    print(usr_already_team, 'steals per game', team_dict[usr_already_team].team_stl)


def already_four_options():
  print("Enter 1 for searching data of a specific team on your own; 2 for comparing among several teams;")
  print(" 3 for searching for teams that are top in some field; 4 for player list of a team. Other input to quit")
  usr_option=input()
  if usr_option=='1':
    already_1()
  elif usr_option=='2':
    print("Please enter some teams names and split them with '/'.")
    usr_compare_team_input=input()
    usr_compare_team_lst=usr_compare_team_input.split('/')

    barWidth = 0.15
    team_recommended_stat_bar_lst=[[0]*5 for i in range(len(usr_compare_team_lst)) ]
    team_recommended_position_lst=[[0]*5 for i in range(len(usr_compare_team_lst)) ]
    team_recommended_stat_index=0
    team_recommended_label=[0]*len(usr_compare_team_lst)
    for i in usr_compare_team_lst:
      # print(team_dict[i].team_name, team_dict[i].team_pts)
      team_recommended_stat_bar_lst[team_recommended_stat_index]=[float(team_dict[i].team_pts), float(team_dict[i].team_trb), float(team_dict[i].team_ast), float(team_dict[i].team_stl), float(team_dict[i].team_blk)]
      team_recommended_label[team_recommended_stat_index]=team_dict[i].team_name
      team_recommended_position_lst[team_recommended_stat_index]=[(0+barWidth*team_recommended_stat_index), (1+barWidth*team_recommended_stat_index),(2+barWidth*team_recommended_stat_index),(3+barWidth*team_recommended_stat_index),(4+barWidth*team_recommended_stat_index)]
      plt.bar(team_recommended_position_lst[team_recommended_stat_index], team_recommended_stat_bar_lst[team_recommended_stat_index], color=team_color_dict[i], width=barWidth, edgecolor='white', label=team_recommended_label[team_recommended_stat_index])
      team_recommended_stat_index += 1
    plt.xlabel('group', fontweight='bold')
    plt.xticks([r + barWidth for r in range(5)], ['PTS', 'TRB', 'AST', 'STL', 'BLK'])
    plt.legend()
    plt.show()
  elif usr_option=='3':
    print("We can find the most offensive team(1), the most defensive team(2), the best three shooting team(3), the fastes-paced team(4), the youngest team(5) and the oldest team(6) for you. ")
    usr_option_3=input()
    print("How many team you want to know? For example top5 or top 10. Enter a value between 1 to 15")
    usr_option_3_amount=int(input())
    if(usr_option_3=='1'):
      print(find_offensive_team(team_lst,team_lst)[-usr_option_3_amount:])
    elif(usr_option_3=='2'):
      print(find_defensive_team(team_lst,team_lst)[-usr_option_3_amount:])
    elif(usr_option_3=='3'):
      print(find_threePA_team(team_lst,team_lst)[-usr_option_3_amount:])
    elif(usr_option_3=='4'):
      print(find_pace_team(team_lst,team_lst)[-usr_option_3_amount:])
    elif(usr_option_3=='5'):
      print(find_age_team(team_lst,team_lst,True)[-usr_option_3_amount:])
    elif(usr_option_3=='5'):
      print(find_age_team(team_lst,team_lst,False)[-usr_option_3_amount:])
  elif usr_option == '4' :
    print("Which team do you want to know more about?")
    usr_already_team=input()
    scrap_each_team_player(usr_already_team)
    print(list(team_dict[usr_already_team].team_player.keys()))
  print("Do you want to search again with other functions?(yes/no)")
  usr_4_again=input()
  if usr_4_again=='yes':
    print("!!!!!!!!!")
    already_four_options()




categories = ['PTS','BLK','STL',
              'AST', 'TRB']

fig = go.Figure()
print("Dear users, welcome to our NBA search! This is a project for both new NBA fans to get to know NBA and already NBA fans who want to get some data about NBA teams. ")
print("May I ask whether you are a new fan or not?(yes/no)")
usr_new_or_not=input()
if(usr_new_or_not=='yes'):
  print("Welcome to NBA fan world!!! Before I do suggestion for you, could you tell me where do you live? (East/West)")
  user_E_or_W=input()
  user_lst_after_E_or_W=find_team_in_conference(team_lst,user_E_or_W)
  print(user_lst_after_E_or_W)
  print("Nice! I would pay more attention on teams in East conference so that you can have a better chance to support the team in person!")
  print("Well, what I would like to ask nex is 'Basing on your person preference, would you like offensive game style or defensive game style?(offensive/defensive)")
  user_off_def=input()
  if(user_off_def)=='offensive':
      user_lst_after_off_def=find_offensive_team(team_lst, user_lst_after_E_or_W)
  elif(user_off_def)=='defensive':
      user_lst_after_off_def=find_defensive_team(team_lst, user_lst_after_E_or_W)
  print(user_lst_after_off_def)
  print("3 points shooting is the main trend of the league nowadays. Would you like a team focuses on 3 points shooting?(yes/no)")
  user_favor_three=input()
  if user_favor_three=='yes':
      user_favor_three=True
  elif user_favor_three=='no':
      user_favor_three=False
  user_lst_after_three=find_threePA_team(team_lst, user_lst_after_off_def,user_favor_three)
  print(user_lst_after_three)
  print("Nice! Do you want a younger team so that you can witness their getting more and more matured or a more experienced team?(young/experienced)")
  user_favor_age=input()
  if user_favor_age=='young':
      user_favor_age=True
  elif user_favor_age=='experienced':
      user_favor_age=False
  user_lst_after_age=find_age_team(team_lst,user_lst_after_three,user_favor_age)
  print(user_lst_after_age)


  # ploting out player the radar chart
  # print(stats)
  stats=[[0]*5 for i in range(len(user_lst_after_age))]
  star_stat_index=0
  team_label=[0]*len(user_lst_after_age)

  for i in user_lst_after_age:
      scrap_each_team_player(i)
      print(team_dict[i].team_name, team_dict[i].team_star)
      print(team_dict[i].star_stat)
      team_label[star_stat_index]=team_dict[i].team_star
      stats[star_stat_index]=[float(x) for x in list(team_dict[i].star_stat.values())]
      stats[star_stat_index]=[*stats[star_stat_index],stats[star_stat_index][0]]
      for i in stats[star_stat_index]:
        i=float(i)
      star_stat_index += 1
  print("For the team(s) listed above, we would recommend one player for each team. Also, a radar chart of these players will be showed.")

  categories = ['Total Rebounds', 'Assist', 'Steal', 'Block', 'Points']
  categories = [*categories, categories[0]]
  label_loc = np.linspace(start=0, stop=2 * np.pi, num=6)
  plt.figure(figsize=(8, 8))
  plt.subplot(polar=True)
  for i in range(len(user_lst_after_age)):
    # print(stats[i])
    plt.plot(label_loc, stats[i], label=team_label[i])
  plt.title('NBA Player Radar Chart', size=20, y=1.05)
  lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
  plt.legend()
  plt.show()
  print("Let's also see the comparison between the teams!")
  print("Hope you have already got a team in your mind! Now all you need to do is to go ahead and enjoy the excitement NBA provides!")

  # plotting out the sacked team stat bar plot
  barWidth = 0.15
  team_recommended_stat_bar_lst=[[0]*5 for i in range(len(user_lst_after_age)) ]
  team_recommended_position_lst=[[0]*5 for i in range(len(user_lst_after_age)) ]
  team_recommended_stat_index=0
  team_recommended_label=[0]*len(user_lst_after_age)
  for i in user_lst_after_age:
    # print(team_dict[i].team_name, team_dict[i].team_pts)
    team_recommended_stat_bar_lst[team_recommended_stat_index]=[float(team_dict[i].team_pts), float(team_dict[i].team_trb), float(team_dict[i].team_ast), float(team_dict[i].team_stl), float(team_dict[i].team_blk)]
    team_recommended_label[team_recommended_stat_index]=team_dict[i].team_name
    team_recommended_position_lst[team_recommended_stat_index]=[(0+barWidth*team_recommended_stat_index), (1+barWidth*team_recommended_stat_index),(2+barWidth*team_recommended_stat_index),(3+barWidth*team_recommended_stat_index),(4+barWidth*team_recommended_stat_index)]
    plt.bar(team_recommended_position_lst[team_recommended_stat_index], team_recommended_stat_bar_lst[team_recommended_stat_index], color=team_color_dict[i], width=barWidth, edgecolor='white', label=team_recommended_label[team_recommended_stat_index])
    team_recommended_stat_index += 1

  plt.xlabel('group', fontweight='bold')
  plt.xticks([r + barWidth for r in range(5)], ['PTS', 'TRB', 'AST', 'STL', 'BLK'])

  plt.legend()
  plt.show()

  print("Ready to make your choice for the team? Enter to know more about it!")
  print(team_lst)
  print("Please type to team name you are interested in")
  usr_favor_team=input()
  print("In 21-22 Season, your team won", team_dict[usr_favor_team].team_wins, "games. Wish them good luck this season!")
elif(usr_new_or_not=='no'):
  categories_for_search = ['pts', 'trb','ast', 'blk','stl']
  print("Hi fan, our project can enable you to search data for any team or do some ranking and comparison between teams.")
  
  
  already_four_options()
  print("Bye Bye!")


