
"""---------------------------------------------------------------------

Returns first instance of string inside quotes

---------------------------------------------------------------------"""
def getInsideQuotes(string):
    quoteHold = string.find('"')
    
    if(quoteHold == -1):
        return string
    
    string = string[quoteHold+1:]
    quoteHold = string.find('"')
    
    if(quoteHold == -1):
        return string
    
    return string[:quoteHold]


# test = ' 23434 "string" 34343 '
# print(getInsideQuotes(test))
