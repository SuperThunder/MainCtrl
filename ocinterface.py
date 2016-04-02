import requests  # used to make the HTTP POST requests with data to OC Transpo's API
import parseXML  # Finds all instances of XML tag values


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

    print "Next two times:", times

    return times, startTime1st


# So this is a really stupid way of finding the times of the next busses
# We find the location in the XML string of the tag preceding the information, which gives us the character
# location of the first character, then add enough characters to get to the time number and check
# whether it's single or double digit by looking for a / character after
def findTimes(xmlstr):
    # Use this as a workaround to the XML libraries not handling SOAP XML very well
    # http://stackoverflow.com/questions/3873361/finding-multiple-occurrences-of-a-string-within-a-string-in-python
    index = 0
    i = 0
    timeList = []
    keywords = ['AdjustedScheduleTime', 'AdjustmentAge']  # the two key tags we need to find in the XML
    digits = '1234567890'

    timeList = parseXML.getValuesBetweenTags('AdjustedScheduleTime', xmlstr)
    adjAgeList = parseXML.getValuesBetweenTags('AdjustmentAge', xmlstr)
    firstStartTime = parseXML.getValuesBetweenTags('TripStartTime', xmlstr)[0]
    estTypes = isGPS(adjAgeList)

    # Set a time to the invalid value if it is not a proper estimate
    for times in range(0 , 2):
        if estTypes[i] != 'Yes':
            timeList[i] = -100


    '''
    # run the function twice so it finds the first and second instance of a time estimate in the XML
    while(i < 2):
        index = xmlstr.find(keywords[0], index)  # start at present index, avoids searching already searched part
        time = str(xmlstr[index+21])  # From the start of 'Adjusted', the time starts 21 chars later

        if(xmlstr[index+22] != '<'):
            time += str(xmlstr[index+22])  # add the extra digit if the time is double digited, triple will never happen

        # Check time estimate for 2nd bus
        index = xmlstr.find(keywords[1], index)  # check whether the time is not GPS or hasn't been updated in a while
        timeSinceUpdate = str(xmlstr[index+14])
        if(xmlstr[index+15] in digits):
            timeSinceUpdate += str(xmlstr[index+15])  # check if time since last update is double digit

        # note: OC Transpo use '-1' in the AdjusmentAge field to signify a non-GPS time
        #todo: cleanup error handling a little bit more
        if(timeSinceUpdate.isdigit()==True and int(timeSinceUpdate) < 2):  # check that time is a live GPS estimate
            print "Time %d time since GPS time was updated: " %(i+1), timeSinceUpdate
            timeList.append(time)  # add time to list of the two next times
        else:
            print "Time %d non-GPS or accurate time, AdjustmentAge value: %s" %(i+1, timeSinceUpdate)
            timeList.append('-100')  # keep the non-GPS signifying time

        index += 50  # add enough to index to avoid finding end tag of current AdjustedScheduleTime
        i += 1  # iterate to next time given by OC Transpo
        '''

    return timeList, firstStartTime

# Check the AdjustmentAge field to see if a time value is a good (recent) GPS estimate
def isGPS(adjAgeList):
    estTypeList = []
    for i in range(0, 2):
        if str(int(adjAgeList[i])).isdigit() and adjAgeList[i] > 0 and adjAgeList[i] < 2:  # Str->int->str since isdigit() not true for floats
            estTypeList.append('Yes')
        else:
            estTypeList.append('No')

    print estTypeList
    return estTypeList

