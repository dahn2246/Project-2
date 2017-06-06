import Sqlite as sql 
import Variables

# 0 - home/away/total
# 1 - 0.0
# 2 - Starters
# 3 - Minutes Played
# 4 - Field Goals
# 5 - Field Goal Attempts
# 6 - Field Goal Percentage
# 7 - 3-Point Field Goals
# 8 - 3-Point Field Goal Attempts
# 9 - 3-Point Field Goal Percentage
# 10 - Free Throws
# 11 - Free Throw Attempts
# 12 - Free Throw Percentage
# 13 - Offensive Rebounds
# 14 - Defensive Rebounds
# 15 - Total Rebounds
# 16 - Assists
# 17 - Steals
# 18 - Blocks
# 19 - Turnovers
# 20 - Personal Fouls
# 21 - Points
# 22 - Plus/Minus
# 23 - True Shooting Percentage
# 24 - Effective Field Goal Percentage
# 25 - 3-Point Attempt Rate
# 26 - Free Throw Attempt Rate
# 27 - Offensive Rebound Percentage
# 28 - Defensive Rebound Percentage
# 29 - Total Rebound Percentage
# 30 - Assist Percentage
# 31 - Steal Percentage
# 32 - Block Percentage
# 33 - Turnover Percentage
# 34 - Usage Percentage
# 35 - Offensive Rating
# 36 - Defensive Rating

"""---------------------------------------------------

Four Factors Analysis for Offensive teams. Four factors include:  Shooting 40%, Turnovers 25%, Rebounding 20%, Free Throws 15%

EX. 
-1.12 *(.4) +  -0.1*(.25)  +  0.52*(.2)  +  -0.57*(.15)     =    -2.54     

eFG% (index 24) + TOV% (index 33) + ORB% (index 27) + FT% (index 12)
---------------------------------------------------"""
def fourFactorsInsert(team, year = None):
    year = '2017'
    
    gameNames = sql.getAllGamesofTeam(team, year)
    teamStats = []
    
    for game in gameNames:
        teamStats.append(sql.getTeamStats(team, game))
        
#     for i in teamStats:
#         print(i)

    """Four Factors Set up. Get entire statistical regular season and then find average"""
    home, home_n = [], 0
    away, away_n = [], 0
    total, total_n = [], 0
     
    """Try to make all numbers into float"""
    for i in range(0,len(teamStats)):
        for j in range(0,len(teamStats[i])):
            if(teamStats[i][j] == '' or teamStats[i][j] == 'None' or teamStats[i][j] == None):
                teamStats[i][j] = 0 
            else:
                try:
                    teamStats[i][j] = float(teamStats[i][j])
                except:
                    pass
                     
#     for i in teamStats:
#         print(i)
     
    """This section will iterate through entire teamStats
    Then add it up and find the average of each statistic """
    for i in teamStats:
        if(i[0] == 'home'):
            if(len(home) == 0):
                for individualStats in i:
                    home.append(individualStats)
            else:
                for index in range(3, len(i)):
                    home[index] += i[index]
            home_n += 1
            
        elif(i[0] == 'away'):
            if(len(away) == 0):
                for individualStats in i:
                    away.append(individualStats)
            else:
                for index in range(3, len(i)):
                    away[index] += i[index]
            away_n += 1
        
        if(len(total) == 0):
            for individualStats in i:
                total.append(individualStats)
            total[0] = 'total'
        else:
            for index in range(3, len(i)):
                total[index] += i[index]
        total_n += 1
    
    """Find average of each statistic. """     
    for i in range(0,len(home)):
        try:
            home[i] /= home_n
            away[i] /= away_n
            total[i] /= total_n
        except:
            pass
    
    averages = []
    averages.append(home)
    averages.append(away)
    averages.append(total)
    
    sql.insertFFA(team, averages, year)

def updateAllTeams(year):
    var = Variables.Variables()
    teams = var.teams
    
    for i in teams:
        fourFactorsInsert(i)
    
# updateAllTeams(2017)

def fourFactorsCompare(team1, team2, year):
    stats1 = sql.getFFA(team1, year)
    stats2 = sql.getFFA(team2, year)
    
    """Shooting 40%, Turnovers 25%, Rebounding 20%, Free Throws 15%"""
    """eFG% (index 24) + TOV% (index 33) + ORB% (index 27) + FT% (index 12)"""
    FFA1 = stats1[24] * 0.4 + stats1[33] * .25 + stats1[27] * .2 + stats1[12] * .15
#     FFA2 = 


"""---------------------------------------------------------

Returns FFA analysis for Offensive Rating only

------------------------------------------------------"""
def FFAteam(team, year):
    stats = sql.getFFA(team, year)
#     print(stats[2])
    total = stats[2]
    FFA1 = (total[24]*100) * 0.4 + total[33] * .25 + total[27] * .2 + (total[12]*100) * .15
    
    return FFA1

def getAllFFA(year):
    var = Variables.Variables()
    teams = var.teams
    offensiveRating = []
    
    for (i,j) in teams.items():
        """Do an insert sort type of thing"""
        ffaTemp = FFAteam(i,2017)
        if(len(offensiveRating) == 0): 
            offensiveRating.append([i,j,ffaTemp])
            continue
        
        for k in range(0,len(offensiveRating)):
            if(ffaTemp > offensiveRating[k][2]):
                offensiveRating.insert(k, [i, j, ffaTemp])
                break
            if(k == len(offensiveRating) - 1):
                offensiveRating.insert(k + 1, [i, j, ffaTemp])
                break

    return offensiveRating
"""   TESTING """
#     print(total[24])
#     print(total[33])
#     print(total[27])
#     print(total[12])




    










