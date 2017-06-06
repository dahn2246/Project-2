import bs4
from bs4 import BeautifulSoup
from urllib import request
import Utility
import Variables
from numpy.f2py.crackfortran import rmbadname1
import Sqlite as sql

def parseTables(html):
    """---------------------------------------
    Return table should include in this order
    Team Name
    Statistic Name
    Player with statistics
    Team Statistics
    ---------------------------------------"""
    vars = Variables.Variables()
    teams = vars.teams
    players = [] 
    playerStats = []
    statisticArray = []
    teamName = html.table.caption.string
    
    """Add team name [Acronym , Full Name ] """
    for (i,j) in teams.items():
        if teamName.find(i) > -1 or teamName.find(j) > -1: 
            playerStats.append([i,j])
            continue
    
    """Adds statistic name (minutes, points, assists etc) """
    lines = html.find_all('th')
    for i in lines:
#         print(i)
        tempKeyword = 'aria-label="'
        statistic = str(i).find(tempKeyword)
        tempString = str(i)
        if(statistic != -1 and statistic != None):
            stat = ""
            statistic += len(tempKeyword)
            while(tempString[statistic] != '"'):
                stat += tempString[statistic]
                statistic += 1
#             print(stat)
            if(stat != "" and stat not in statisticArray and stat != 'Reserves'):
                statisticArray.append(stat)

    playerStats.append(statisticArray)
    
    """Adds actual statistic"""
    lines = html.find_all('tr')
    raw = []
    for i in lines:
        temp = []
        """This string is only in player tags"""
        htmlFind = str(i).find('th class="left "')
        if(htmlFind != -1 and htmlFind != None):
            """th tag has player name information """
            for j in i.find_all('th'):
                """Get data inside csk="name" 
                    data-append-scv = "name"  """
                 
                namesTemp = str(j)
                getStr1 = str(j).find('csk=')
                getStr2 = str(j).find('data-append-csv=')
                 
                name1 = Utility.getInsideQuotes(namesTemp[getStr1:getStr2])
                name2 = Utility.getInsideQuotes(namesTemp[getStr2:])
                if(name1 == "" or name1 == "<"):
                    continue
                elif(name2 =="" or name2 ==">"):
                    continue
                 
                temp.append(name1)
                temp.append(name2)
                 
                playerName = i.find_all('a')
                if(len(playerName) > 0):
                    temp.append(playerName[0].string.strip())
                else:
                    continue
                 
            """td tags have statistics"""
            for j in i.find_all('td'):
                temp.append(j.string)
                 
            raw.append(temp)
    
#     print(statisticArray)
    """Combine player stats and remove total team stats """
    for i in raw:
#         print(i)
        if len(i) == 0: 
            pass
  
        player = i[1]
          
        if player not in players:
            players.append(player)
            playerStats.append(i)
        elif player in players:
            for j in playerStats:
                if j[1] == player:
                    """Do not include player name, id, minutes etc second time """
                    for stats in i[4:]:
                        j.append(stats)
    
    return playerStats
#     print('TEST')
#     print('')
#     for i in playerStats:
#         print(i)
#     print(len(playerStats))


"""---------------------------------------------------------------------

This function will accept team, and date in string. Date should be in Year/Mo/Day (ex. 2017/03/30)
The function will attempt a connection and get all player data from the website. 
If connection fails or something happens, returns None

---------------------------------------------------------------------"""
def dlChart(team , date, gameName = None):
    playerTable = []
    date = date.split('/')
    
    """Basketball-Reference website has games in following format: 
    http://www.basketball-reference.com/boxscores/ + year + month (ex. 03) + day (ex. 31) + 0 + home team acronym """
    if(gameName != None):
        NBAurl = "http://www.basketball-reference.com/boxscores/" + gameName + ".html"
        date = gameName[0:4] + '/' + gameName[4:6] + '/' + gameName[6:8]
        date = date.split('/')
        print(date)
    else:
        NBAurl = "http://www.basketball-reference.com/boxscores/" + date[0] + date[1] + date[2] + "0" + team + ".html"
#     print(NBAurl)
    try:
        tempWebFile = request.urlopen(NBAurl).read()
    except:
        return None
    tempData = BeautifulSoup(tempWebFile,"lxml")
#     html = tempData.prettify()
#     print(html)

    """Comments """
#     comments = tempData.find_all(string=lambda text:isinstance(text, bs4.Comment))
#     for i in comments:
#         print(i)

    """lines is an array with 4 different tables  """
    lines = tempData.find_all('table')
    table1 = BeautifulSoup(str(lines[0]) + str(lines[1]), 'lxml')
    team1 = parseTables(table1)
    
    table2 = BeautifulSoup(str(lines[2]) + str(lines[3]), 'lxml')
    team2 = parseTables(table2)
    
    temp = []
    for i in team2[0]:
        temp.append(i)
    
    for i in team1[0]:
        team2[0].append(i)
    team2[0].append(date)
    
    for i in temp:
        team1[0].append(i)
    team1[0].append(date)
    
#     for i in team1:
#         print(len(i))
#         print(i)
#            
#     print(" ----" )
#        
#     for i in team2:
#         print(len(i))
#         print(i)
    
    returnArray = []
    
    for i in team1:
        returnArray.append(i)
    for i in team2:
        returnArray.append(i)
#     
#     for i in returnArray:
#         print(i)
#         
    return returnArray

#     """HTML has all the information. Information wanted is in tables
#     'csk=' has players in table
#     'data-stat = "mp"' is minutes played
#     """
#     player_stats = ["mp", "fg", "fga", "fg_pct", "fg3", "fg3a", "fg3_pct", "ft", "fta", "ft_pct",
#                     "orb", "drb", "trb", "ast", "stl", "blk", "tov", "pf", "pts", "plus_minus",
#                      ]


#     print(html)
def parseWholeSeason(lines):
    for i in lines:
        tempKeyword = 'class="left " csk="'
        keywordIndex = str(i).find(tempKeyword)
        tempString = str(i)
        if(keywordIndex != -1 and keywordIndex != None):
            gameName = ""
            keywordIndex += len(tempKeyword)
            while(tempString[keywordIndex] != '"'):
                gameName += tempString[keywordIndex]
                keywordIndex += 1
            print(gameName)
            sql.insertSQL(dlChart('0','0', gameName))


def getWholeSeason(year):
    vars = Variables.Variables()
    teams = vars.teams
    
    months = ['october', 'november', 'december', 'january', 'febuary', 'march', 'april' ]
#     months = ['february', 'march', 'april' ]
    
    for month in months:
        NBAurl = "http://www.basketball-reference.com/leagues/NBA_" + str(year) + "_games-" + month + ".html" 
        
        try:
            tempWebFile = request.urlopen(NBAurl).read()
        except:
            return None
        tempData = BeautifulSoup(tempWebFile,"lxml")
        lines = tempData.find_all('tr')
        parseWholeSeason(lines)

    
def updateGames(year):
    allGames = sql.allGamesofYear(year)
    temp = allGames[len(allGames) - 1][1].split('_')
    lastGame = temp[2] + temp[3] + temp[4] + '0' + temp[1]
    print(lastGame)
    lastMonth = int(temp[3])
    foundLastgame = False
    
    vars = Variables.Variables()
    teams = vars.teams
    
    months = ['october', 'november', 'december', 'january', 'febuary', 'march', 'april', 'may', 'june' ]
    monthIndex = [10, 11, 12, 1, 2, 3, 4, 5, 6]
    start = monthIndex.index(lastMonth)
    print(start)
    
    while(start < len(months)):
        month = months[start]
        print(month)
        NBAurl = "http://www.basketball-reference.com/leagues/NBA_" + str(year) + "_games-" + month + ".html" 
        try:
            tempWebFile = request.urlopen(NBAurl).read()
        except:
            return None
        tempData = BeautifulSoup(tempWebFile,"lxml")
        lines = tempData.find_all('tr')
     
        for i in lines:
            tempKeyword = 'class="left " csk="'
            keywordIndex = str(i).find(tempKeyword)
            tempString = str(i)
            if(keywordIndex != -1 and keywordIndex != None):
                gameName = ""
                keywordIndex += len(tempKeyword)
                while(tempString[keywordIndex] != '"'):
                    gameName += tempString[keywordIndex]
                    keywordIndex += 1
                
                if(gameName == lastGame):
                    foundLastgame = True
                    continue
                
                if(foundLastgame == True):
                    print(gameName)
#                     sql.insertSQL(dlChart('0','0', gameName
        start += 1

# updateGames(2017)

#     for i in lines:
#         print(i)
    
#     months = [10, 11, 12, 1, 2, 3, 4]
#     
#     """Regular Season Starts Oct - Apr"""
#     for month in months: 
#         days = daysMonth.get(month)
#         
#         for day in range(1,days):
#             """Convert Days/Months/Year into proper string """
#             if(day < 10):
#                 tempDay = '0' + str(day)
#             else: 
#                 tempDay = str(day)
#                 
#             if(month < 10):
#                 tempMonth = '0' + str(month)
#             else: 
#                 tempMonth = str(month)
#             
#             if(month >= 10): 
#                 year = str( int(year) - 1)
#                  
#             date = year + '/' + tempMonth + '/' + tempDay
#                         
#             for team in teams:
#                 print(str(team) + " : " + str(date))
#                 tempChart = dlChart(team, date)
#                 if(tempChart != None):
#                     print("game")
#                     sql.insertSQL(dlChart(team , date))


# getWholeSeason("2017")
            
# getWholeSeason('2017')
#http://www.basketball-reference.com/boxscores/201704100BOS.html
# sql.insertSQL(dlChart('BOS', '2017/04/10'))
# dlChart('MIL', '2017/03/03')