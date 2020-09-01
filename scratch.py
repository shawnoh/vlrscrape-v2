# -----------------------------------------------
# created by Shawn Oh
# 9/1/2020
# -----------------------------------------------

# using https://realpython.com/python-web-scraping-practical-introduction/

import numpy as np
import matplotlib.patches as mp
from matplotlib import pyplot as plt
from urllib.request import urlopen


def splitByRating(eloList, numSplit, splitList):
    splitIndex = 0
    minStd = 99999
    finalSplit = 0
    while splitIndex < len(eloList):
        firstStd = np.std(eloList[:splitIndex])
        secondStd = np.std(eloList[splitIndex:])
        sumStd = firstStd * firstStd + secondStd * secondStd  # minimize variance by minimizing sum of squares of std

        if sumStd < minStd:
            minStd = sumStd
            finalSplit = splitIndex
        splitIndex = splitIndex + 1

    if numSplit > 1:
        if finalSplit != 1:  # may need to change this back to 0
            splitList.append(splitByRating(eloList[0:finalSplit], numSplit - 1, splitList))
        if finalSplit != len(eloList) - 1:
            splitList.append(finalSplit + splitByRating(eloList[finalSplit:], numSplit - 1, splitList))

    return finalSplit


def createColorBar(numberTeams, splitList):
    finalBar = []
    colIndex = 0
    ix = 0
    for splitInd in splitList:
        while ix < splitInd:
            finalBar.append(COLORLIST[colIndex])
            ix = ix + 1
        colIndex = colIndex + 1
    while ix < numberTeams:
        finalBar.append(COLORLIST[colIndex])
        ix = ix + 1
    return finalBar


def createHandles(splitList):
    handles = []
    for teamN in range(0, len(splitList) + 1):
        handleLabel = "Tier " + str(teamN + 1) + " Team"
        handles.append(mp.Patch(color=COLORLIST[teamN], label=handleLabel))
    return handles


def appendRegionData(regionChoice, htmlList):
    page = urlopen(BASEURL + REGIONURLLIST[regionChoice - 1])
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    html.replace("\t", "")
    wholeTeamDataStart = html.find("<tbody>") + len("<tbody")
    wholeTeamDataEnd = html.find("</tbody>")
    wholeTeamData = html[wholeTeamDataStart:wholeTeamDataEnd].split("</tr>")
    for htmlLine in wholeTeamData:
        htmlList.append(htmlLine.split("\n"))


def openSettings(maxTeamCount, numSubdiv):
    exitFlag = False
    while not exitFlag:
        print("1: Maximum teams shown per graph")
        print("2: Number of recursive subdivisions for team tiers")
        settingChoice = int(input("Enter number of setting you wish to edit, or 3 to exit: "))

        if settingChoice == 1:
            maxTeamsInput = int(input("Enter maximum number of teams (1-1000) shown per graph: "))
            if 1 <= maxTeamsInput <= 1000:
                maxTeamCount = maxTeamsInput
            else:
                print("ERROR: Invalid amount of teams.\n")
        elif settingChoice == 2:
            subDivInput = int(input("Enter amount of subdivisions (1-3) for team tiers: "))
            if 1 <= subDivInput <= 3:
                numSubdiv = subDivInput
            else:
                print("ERROR: Invalid subdivision count.\n")
        elif settingChoice == 3:
            exitFlag = True
        else:
            print("ERROR: Invalid selection.\n")
    return maxTeamCount, numSubdiv


def createPlot(keys, values):
    fig, ax = plt.subplots()
    ax.bar(keys, values, color = colorBar)
    plotTitle = REGIONLIST[choice - 1] + " VALORANT Team Ratings"
    if MAXTEAMS < 1000:
        plotTitle = "Top " + str(MAXTEAMS) + " " + plotTitle
    plt.title(plotTitle)
    plt.ylabel("ELO Rating")
    plt.xlabel("Team")
    plt.grid(True)
    eloLow = values[len(values) - 1]
    eloHigh = values[0]
    plt.ylim(eloLow - (eloLow % 100), eloHigh - (eloHigh % 100) + 100)  # dynamic y-range rounded by 100
    plt.xticks(rotation=90)  # rotate team names to improve clarity
    plt.legend(handles=handleList)  # creates Team Tier key
    fig.set_size_inches(16, 12)

    print("Close graph window to return to selection menu.")
    plt.show(block = True)


COLORLIST = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "gray"]
REGIONLIST = ["World", "Europe", "North America", "Latin America", "Oceania", "Asia-Pacific", "Korea"]
REGIONURLLIST = ["placeholder", "europe", "north-america", "latin-america", "oceania", "asia-pacific", "korea"]
REGIONSHORTHAND = ["PLACEHOLDER", "EU", "NA", "LAT", "OCE", "ASIA", "KR"]
MAXTEAMS = 1000
NUMSPLITS = 2
BASEURL = "https://www.vlr.gg/rankings/"

exitMenu = False
while not exitMenu:
    teamData = []
    i = 1
    skipGraph = False
    for region in REGIONLIST:
        print(str(i) + ": " + region)
        i = i + 1

    choice = int(input("Enter number 1-7 for region elo graph, 8 for settings, or 9 to exit: "))
    if choice == 1:
        for i in range(0, len(REGIONLIST) - 1):
            appendRegionData(i, teamData)
    elif 2 <= choice <= 7:
        appendRegionData(choice, teamData)
    elif choice == 8:
        MAXTEAMS, NUMSPLITS = openSettings(MAXTEAMS, NUMSPLITS)
        skipGraph = True
    elif choice == 9:
        exitMenu = True
    else:
        print("ERROR: Invalid selection.\n")
        skipGraph = True

    if not exitMenu and not skipGraph:
        teamElo = {}
        dicKeys = []
        dicValues = []

        for team in teamData:
            for line in team:
                if line.find("\"rank-item-team\"") >= 0:
                    a = line.find("data-sort-value=\"") + len("data-sort-value=\"")
                    b = line[a:].find('"')
                    name = line[a:a + b]
                elif line.find("rank-item-rating") >= 0:
                    a = line.find("data-sort-value=\"") + len("data-sort-value=\"")
                    b = line[a:].find('"')
                    rating = int(line[a:a + b])
            teamElo[name] = rating

        if choice == 1:
            sortedTEV = sorted(teamElo.items(), key=lambda x: x[1], reverse=True)
            for tupleX in sortedTEV:
                dicKeys.append(tupleX[0])
                dicValues.append(int(tupleX[1]))
        else:
            dicKeys = list(teamElo.keys())
            dicValues = list(teamElo.values())

        dicKeys = dicKeys[:MAXTEAMS]
        dicValues = dicValues[:MAXTEAMS]
        splitIndices = []
        splitIndices.append(splitByRating(dicValues, NUMSPLITS, splitIndices))

        splitIndices = list(dict.fromkeys(splitIndices))  # create a dict from list and remake list to remove dupes
        splitIndices.sort()
        print(splitIndices)

        colorBar = createColorBar(len(dicKeys), splitIndices)
        handleList = createHandles(splitIndices)
        createPlot(dicKeys, dicValues)
