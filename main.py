import Analysis

def main():
    print("This is a simple program to list the offensive rankings for all")
    print("NBA teams in the 2017 regular season. Rankings is based on ")
    print("Four Factors Analysis with the following weightings:")
    print("Shooting 40%, Turnovers 25%, Rebounding 20%, Free Throws 15%")
    offensiveRating = Analysis.getAllFFA(2017)
    for i in offensiveRating:
        print(i)
    

if __name__ == "__main__":
    main()

