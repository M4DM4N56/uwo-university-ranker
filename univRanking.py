def getInformation(chosenCountry, topUniF, capitalsF):
    try:
        chosenCountry = chosenCountry.upper()
        topUniF = open(topUniF, "r", encoding='utf8')
        capitalsF = open(capitalsF, "r", encoding='utf8')
        output = open("output.txt", "w")

        # processing university file into a nice list
        uniList = []
        topUniF.readline().strip()
        lines = topUniF.readline().strip()

        while lines != "":
            uniList.append(lines.split(","))
            lines = topUniF.readline().strip()

        # processing capital file into a nice list
        capList = []
        capitalsF.readline().strip()
        cLines = capitalsF.readline().strip()

        while cLines != "":
            capList.append(cLines.split(","))
            cLines = capitalsF.readline().strip()

        # running tests 1-9
        universities_count(uniList, output)  # 1
        countries_list(uniList, output)  # 2
        continents_list(uniList, capList, output)  # 3
        international_best(uniList, output, chosenCountry)  # 4
        country_best(uniList, output, chosenCountry)  # 5
        country_average(uniList, output, chosenCountry)  # 6
        relative_average(uniList, capList, output, chosenCountry)  # 7
        country_capital(capList, output, chosenCountry)  # 8
        capital_universities(uniList, output)  # 9

        # closing files
        output.close()
        topUniF.close()
        capitalsF.close()

    # in case file is not found
    except FileNotFoundError:
        print("Something went wrong when opening file")


# test 1
def universities_count(uniList, output):
    output.write("Total number of universities => " + str(len(uniList)))


# test 2
def countries_list(uniList, output):
    global newUniList
    newUniList = []

    # adding countries to country set
    for i in uniList:
        country = i[2].upper()
        if country not in newUniList:
            newUniList.append(country)

    # turn list into a string for easy printing
    countryList = ""
    for j in newUniList:
        countryList = countryList + j + ","
    # prints set
    output.write("\nAvailable countries => " + countryList[:-1])


# test 3
def continents_list(uniList, capList, output):
    newContList = []

    # for every country in uniList, search all of capList for new continents to add to list
    for i in uniList:
        for j in capList:
            if i[2].upper() == j[0].upper():
                if j[5] not in newContList:
                    newContList.append(j[5])

    # the same logic as test 2
    continentList = ""
    for j in newContList:
        continentList = continentList + j + ","
    # prints set
    output.write("\nAvailable continents => " + continentList[:-1])


# test 4
def international_best(uniList, output, chosenCountry):

    # finds the highest university on the list that has the country name
    for i in uniList:
        if i[2].upper() == chosenCountry:
            print("")
            output.write("\nAt international rank => " + i[0] + " the university name is => " + i[1])
            break


# test 5
def country_best(uniList, output, chosenCountry):

    # finds the university with the #1 score of the given country
    for i in uniList:
        if i[2].upper() == chosenCountry:
            if int(i[3]) == 1:
                output.write("\nAt national rank => 1 the university name is => " + i[1])


# test 6
def country_average(uniList, output, chosenCountry):
    global nationalAvg
    schools = 0
    uniScoreTotal = 0

    # accumulates the scores from all universities in the country
    for i in uniList:
        if i[2].upper() == chosenCountry.upper():
            uniScoreTotal += float(i[8])
            schools += 1

    # in case schools = 0
    try:
        nationalAvg = (uniScoreTotal / schools).__round__(2)
    except ZeroDivisionError:
        print("Divided by zero")

    output.write("\nThe average score => " + str(nationalAvg) + "%")


# test 7
def relative_average(uniList, capList, output, chosenCountry):
    uniHighScore = 0
    uniContinent = ""
    relativeScore = 0

    # finds continent of given country
    for h in capList:
        if h[0].upper() == chosenCountry:
            uniContinent = h[5]
            break

    # takes every line in uniList
    for i in uniList:
        for j in capList:
            # if found country has the same continent
            if i[2].upper() == j[0].upper():
                if j[5].upper() == uniContinent.upper():
                    # sees if it's the new highest score in the university
                    if float(i[8]) > uniHighScore:
                        uniHighScore = float(i[8])

    # in case uniHighScore = 0
    try:
        relativeScore = ((float(nationalAvg) / uniHighScore) * 100).__round__(2)
    except ZeroDivisionError:
        print("Divided by zero")

    output.write(
        "\nThe relative score to the top university in " + uniContinent + " is => (" + str(nationalAvg) + " / " + str(
            uniHighScore) + ") x 100% = " + str(relativeScore) + "%")


# test 8
def country_capital(capList, output, chosenCountry):
    global capital
    capital = "None"

    # finds country's capital in capList
    for i in capList:
        if i[0].upper() == chosenCountry:
            capital = i[1]
            break

    output.write("\nThe capital is => " + str(capital))


# test 9
def capital_universities(uniList, output):
    output.write("\nThe universities that contain the capital name =>")
    capitalCount = 0

    # finds if university contains the capital name
    for i in uniList:
        if capital in i[1]:
            capitalCount += 1
            output.write(str("\n    #" + str(capitalCount) + " " + i[1]))
