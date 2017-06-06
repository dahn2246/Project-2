import sqlite3

"""----------------------------------------------------------------------
-table called allgames2017: 

rowID | gameName | 

-Every game has a table named:

abbreviation1_abbreviation2_date (yr/month/date)
abbreviation1 is home team

------------------------------------------------------------------------
2016-2017 NBA season: 
Regular Season from Oct to 12 April 2017 
Playoffs later on. 
                    

**************Important sqlite queries:***************************
Create table : CREATE TABLE tablename (date TEXT)

Insert : INSERT INTO tablename (variable) VALUES ()
    ex. INSERT INTO stocktable (TICKER) VALUES ('AAPL')

Get all tables from database : "SELECT name FROM sqlite_master WHERE type = 'table';" 

Delete table : "DROP TABLE IF EXISTS " + tablename

Delete row in table : "DELETE FROM tablename WHERE column = columnname
    ex. DELETE FROM stocklist WHERE TICKER = SWKS 

Delete duplicates inside table : "DELETE FROM stocklist WHERE rowid NOT IN (SELECT MAX(rowid) FROM stocklist GROUP BY TICKER)"

Get All tables : "SELECT name FROM sqlite_master WHERE type = 'table';"

Get Column Names : PRAGMA table_info('table_name') 

Update Entries : UPDATE table SET variable = ? WHERE rowid = 5

-----------------------------------------------------------------------"""
def execute(commands, input):
    conn = sqlite3.connect('NBA.db')
    c = conn.cursor()
    
    if(input == None or input == False):
        c.execute(commands)
    else:
        c.execute(commands,input)
    
    conn.commit()
    conn.close()


def executeReturn(commands):
    returnArray = []
    conn = sqlite3.connect('NBA.db')
    c = conn.cursor()

    cursor = c.execute(commands)
        
    for i in cursor:
        returnArray.append(i)
    
    conn.commit()
    conn.close()
    
    return returnArray    


"""-----------------------------------------------------------------------------

Insert Game data 

-----------------------------------------------------------------------------"""
def insertSQL(data):
    """Table name will abbrv1_abbrv2_date (yr/month/date) """
    """Has abbrv1, full name, abbrv2, full name, date """
#     print(data)
    gameInfo = data[0] 
    date = gameInfo[4][0] + '_' + gameInfo[4][1] + '_' + gameInfo[4][2]
    tableName = gameInfo[0] + '_' + gameInfo[2] + '_' + date
    
    gameTemp = executeReturn("SELECT * FROM allgames2017")
    tableNames = []
    for i in gameTemp:
        tableNames.append(i[1])
    if(len(gameTemp) != 0):
        lastRow = int(gameTemp[len(gameTemp) - 1][0])
        lastRow += 1
    else:
        lastRow = 0
    
    if(tableName in tableNames):
        return
    
    execute("INSERT INTO allgames2017 VALUES (? , ?)", [lastRow, tableName])
    
    for i in data:
        if(gameInfo[0] in i):
            i[4] = date
        
#     for i in data:
#         print(i)
     
    longestRow = 0 
    for i in data:
        if(len(i) > longestRow):
            longestRow = len(i) 
      
    ''' Make text CC1 TEXT, CC2 TEXT, .... '''
    columnText = ""
    questionText = ""
             
    for i in range(0,longestRow):
        columnText += 'CC' + str(i) + ' TEXT,'
        questionText += '?,'
    columnText = columnText[0:len(columnText)-1]
    questionText = questionText[0:len(questionText)-1]
      
#     print(columnText)
#     for i in data:
#         print(i)
       
    execute('DROP TABLE IF EXISTS ' + tableName, None)
    execute('CREATE TABLE ' + tableName + '(' + columnText + ')', None)
       
    '''Feed data into sqlite'''
    for i in range(0, len(data)):
        tempArray = []
  
        for j in range(0,longestRow):
            if(j < len(data[i])):
                tempArray.append(data[i][j])
            else:
                tempArray.append("")
#         print(tempArray)
        execute('INSERT INTO ' + tableName + ' VALUES (' + questionText + ')', tempArray)
        
        

def getSingleGame(tableName):
    data = executeReturn("SELECT * FROM " + tableName)
    returnArray = []
    team1 = tableName.split('_')[0]
    team2 = tableName.split('_')[1]
    
    count = 0
    
    """ Data straight from sql is in the form:
    (team1_abbrv, team1, team2_abbrv, team2, date)
    ('Starters', 'Minutes Played',...)
    (....)
    (team2_abbrv, team2, team1_abbrv, team1, date)
    ('Starters', 'Minutes Played', ...)
    (....)
    
    Variable name array and actual statistics arrays are not lined up properly.
    
    The function of the next lines of code is to line up the data properly and then
    return this in an array. 
    """
    
    for i in data:
        temp = []
        for j in i:
            temp.append(j)
        
        count += 1
        
        """If array is name of statistics, add two spaces"""
        if('Starters' in temp or 'Minutes Played' in temp):
            returnArray.append(["",""] + temp)
            continue
        
        """If array is total team statistics (where temp[0] is 240 or higher), 
        add three spaces, and add next row, then delete it.  """ 
        try: 
            float(temp[0])
            
            temp2 = []
            
            for j in temp:
                if(j != ""):
                    temp2.append(j)
            
            temp = ["","","teamStats"] + temp2
#             print(data[count])
            for next in data[count]:
                if(next != "" and next != temp[3]):
                    temp.append(next)
            data.remove(data[count])
            returnArray.append(temp)
            continue
        except: 
            pass
            
        """Otherwise just add row """
        returnArray.append(temp)

    return returnArray

def getTeamStats(teamName, tableName):
    stats = getSingleGame(tableName)
    
    if(teamName in stats[0][0:1]):
        for i in stats: 
            if('teamStats' in i):
                i[0] = 'home'
                return i
    
    skip = 0
    for i in stats:
        if('teamStats' in i and skip < 1):
            skip += 1 
            pass
        elif('teamStats' in i and skip >= 1):
            i[0] = 'away'
            return i
 
# def getPlayerStats(tableName):

"""-----------------------------------------------------------------------------

All games of a certain team

-----------------------------------------------------------------------------"""
def getAllGamesofTeam(teamName, year):
    games = executeReturn("SELECT * FROM allgames" + str(year))
    allGames = []
    
    for i in games:
        gameName = i[1].split('_')
        if(teamName in gameName):
            allGames.append(i[1])
    
    return allGames

"""-----------------------------------------------------------------------------

Returns all the games in table allgames + str(year)

-----------------------------------------------------------------------------"""
def allGamesofYear(year):
    temp = executeReturn("SELECT * FROM allgames" + str(year))
    allGames = []
    
    for i in temp: 
        allGames.append(i)
    
    return allGames


"""-----------------------------------------------------------------------------

Inserts four factor analysis and retrieves it. Will insert 

home statistics....
away statistics....
total statistics....

-----------------------------------------------------------------------------"""
def insertFFA(team, data, year):
    tableName = team + "_FFA" + str(year)
    print(tableName)
    
    longestRow = 0 
    for i in data:
        if(len(i) > longestRow):
            longestRow = len(i) 
      
    ''' Make text CC1 TEXT, CC2 TEXT, .... '''
    columnText = ""
    questionText = ""
             
    for i in range(0,longestRow):
        columnText += 'CC' + str(i) + ' TEXT,'
        questionText += '?,'
    columnText = columnText[0:len(columnText)-1]
    questionText = questionText[0:len(questionText)-1]
      
    print(columnText)
    for i in data:
        print(i)
       
    execute('DROP TABLE IF EXISTS ' + tableName, None)
    execute('CREATE TABLE ' + tableName + '(' + columnText + ')', None)
       
    '''Feed data into sqlite'''
    for i in range(0, len(data)):
        tempArray = []
  
        for j in range(0,longestRow):
            if(j < len(data[i])):
                tempArray.append(data[i][j])
            else:
                tempArray.append("")
#         print(tempArray)
        execute('INSERT INTO ' + tableName + ' VALUES (' + questionText + ')', tempArray)


def getFFA(team, year):
    tableName = team + "_FFA" + str(year)

    temp = executeReturn("SELECT * FROM " + tableName)
    returnData = []
    
    for i in temp:
        tempArr = [] 
        for j in i:
            try:
                tempArr.append(float(j))
            except:
                tempArr.append(j)
        returnData.append(tempArr)
    
    return returnData
# 
# FFA = getFFA('CLE', 2017)
# for i in FFA:
#     print(i)

# allGames = allGamesofYear(2017)
# for i in allGames:
#     print(i)
#     ID = float(i[0])
#     
#     if(ID >= 1230):
#         execute('DELETE FROM allgames2017 WHERE rowID = ?', [i[0]])


# getAllGamesofTeam('CLE','2017')
        
# data = getSingleGame('MEM_DET_2016_12_21')
# for i in data:
#     print(i)
# print(getTeamStats('DET', 'MEM_DET_2016_12_21'))

  
# for i in data:
#     if('gasolma01' in i):
#         index = i.index('gasolma01') + 1
#         break
#   
# 
# # 
# # for i in data:
# #     print(i)
# 
# for i in range(0,len(data[0])):
#     temp = []
#     for j in [1]:
#         temp.append(data[j][i])
#     print(str(i) + " - " + temp[0])
        
# execute('DELETE FROM allgames2017 WHERE rowID = "14"  ' , None)
# data = executeReturn("SELECT name FROM sqlite_master WHERE type = 'table';")
# data = executeReturn("SELECT * FROM allgames2017")
# for i in data:
#     print(i)

# execute('CREATE TABLE allgames2017 (rowID TEXT, gameName TEXT)', None)

# gameTemp = executeReturn("SELECT * FROM allgames2017")
# print(gameTemp[len(gameTemp) - 1][0])
