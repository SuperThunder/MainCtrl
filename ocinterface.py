import requests  # used to make the HTTP POST requests with data to OC Transpo's API
import parseXML  # Finds all instances of XML tag values

# TODO: compartmentalize everything wayyyyyyy more
# this is the function to be called from outside with the stop information to get the time info
def getNextTimes(stopInfo):

    # get API data from outside file
    infoFile = open("../apiinfo.txt")
    apiData = infoFile.read().splitlines()  # apiData is a list of the lines in the infoFile, without \n chars

    print "Using API info", apiData
    appID = apiData[0]  # know that in file first line is API ID and second is key
    apiKey = apiData[1]

    infoFile.close()

    # We need to send parameters as part of the API request
    # This always involves API ID/key and a stop number/route
    apiInfo = {'appID': appID, 'apiKey': apiKey, 'routeNo': stopInfo.RouteNum, 'stopNo': stopInfo.StopNum}

    # Use requests library to make the request to OC Transpo with the needed parameters
    timesReq = requests.post('https://api.octranspo1.com/v1.2/GetNextTripsForStop', data=apiInfo)  # note POST not GET

    print timesReq.text  # prints raw XML info

    # get next three times
    times, startTime1st = findTimes(timesReq.content)

    print "Next times:", times

    return times, startTime1st



def findTimes(xmlstr):
    # todo: figure out the program crashing bugs that happens here but only after several days
    # maybe unhandled internet connectivity issue?
    timeList = parseXML.getValuesBetweenTags('AdjustedScheduleTime', xmlstr)
    try:
        if timeList[0] == '-100':  # If none of the estimates are good, return all invalid values now
            return [-100, -100, -100], '-100'
    except IndexError:
        print "Index error with timelist", timeList
    except:
        print "Unknown error with timelist", timeList


    adjAgeList = parseXML.getValuesBetweenTags('AdjustmentAge', xmlstr)
    startTimeList = parseXML.getValuesBetweenTags('TripStartTime', xmlstr)
    startTime1st = "\"" + startTimeList[0] + "\""
    #estTypes = isGPS(adjAgeList)

    # Check for cases in which less than the normal 3 estimates are given; ex at night when busses don't run
    if len(timeList) == 1:
        timeList.append(-100)
        timeList.append(-100)
    elif len(timeList) == 2:
        timeList.append(-100)
    elif len(timeList) == 3:  # Normal length, don't need to do anything
        timeList = timeList  # todo: figure out a less odd way of not doing anything
    else:
        timeList = ['-100', '-100', '-100']  # If the time list has is somehow bigger or smaller than expected

    # Check if the time is a valid GPS, scheduled time, or not given
    for i in range(len(adjAgeList)):
        adjAge = adjAgeList[i]
        adjAgeInt = int(round(float(adjAge)))

        if adjAge[0].isdigit() and adjAgeInt >= 0 and adjAgeInt < 2:
            continue
        elif adjAgeList[i] == '-1':
            timeList[i] = -50
        else:
            timeList[i] = -100

    return timeList, startTime1st

# Check the AdjustmentAge field to see if a time value is a good (recent) GPS estimate
def isGPS(adjAgeList):
    estTypeList = []
    #print adjAgeList
    for i in range(len(adjAgeList)):
        adjAge = adjAgeList[i]
        adjAgeInt = int(round(float(adjAge)))

        if adjAge[0].isdigit() and adjAgeInt >= 0 and adjAgeInt < 2:
            estTypeList.append('Yes')
        else:
            estTypeList.append('No')

    print "GPS: ", estTypeList
    return estTypeList

