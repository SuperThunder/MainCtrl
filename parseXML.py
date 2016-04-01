def getValuesBetweenTags(tag, xmlstr):  # find all instances of an XML tag and return the value within it

    index = 0
    tagStartIndexes = []  # contains list of index of starting characters of tags
    tagEndIndexes = []  # Contains indexes of the last character of the values within the tags
    startTag = '<' + tag + '>' # Add opening and closing tags to differentiate start and end tags
    endTag = '</' + tag

    while index < len(xmlstr):

        # Find start of tag
        index = xmlstr.find(startTag, index)
        if index == -1: break  # -1 indicates no str found by str.find(), will show up after 3 times are found
        tagStartIndexes.append(index + len(startTag))  # start of values will be index + tag length

        # Find end of tag
        index = xmlstr.find(endTag, index)
        if index == -1:
            print 'Error: Found XML start tag but no end tag'  # This should never happen
            break
        tagEndIndexes.append(index - 1)  # Last char of value will be 1 less than start of end tag

        index += len(endTag)  # Index is at start of end tag so this brings it forward enough

    return tagStartIndexes, tagEndIndexes


# Tests the functionality of the parser. Use for debug.
def testmodule():
    xml = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><GetNextTripsForStopResponse xmlns="http://octranspo.com"><GetNextTripsForStopResult><StopNo xmlns="http://tempuri.org/">8766</StopNo><StopLabel xmlns="http://tempuri.org/">CRICHTON CHARLES</StopLabel><Error xmlns="http://tempuri.org/" /><Route xmlns="http://tempuri.org/"><RouteDirection><RouteNo>9</RouteNo><RouteLabel>Rideau</RouteLabel><Direction>Southbound</Direction><Error /><RequestProcessingTime>20160331124800</RequestProcessingTime><Trips><Trip><TripDestination>Bank</TripDestination><TripStartTime>12:44</TripStartTime><AdjustedScheduleTime>12</AdjustedScheduleTime><AdjustmentAge>0.75</AdjustmentAge><LastTripOfSchedule>false</LastTripOfSchedule><BusType>4LB - IN</BusType><Latitude>45.412276</Latitude><Longitude>-75.659030</Longitude><GPSSpeed>0.5</GPSSpeed></Trip><Trip><TripDestination>Bank</TripDestination><TripStartTime>13:04</TripStartTime><AdjustedScheduleTime>31</AdjustedScheduleTime><AdjustmentAge>-1</AdjustmentAge><LastTripOfSchedule>false</LastTripOfSchedule><BusType>4LB - IN</BusType><Latitude /><Longitude /><GPSSpeed /></Trip><Trip><TripDestination>Bank</TripDestination><TripStartTime>13:24</TripStartTime><AdjustedScheduleTime>51</AdjustedScheduleTime><AdjustmentAge>-1</AdjustmentAge><LastTripOfSchedule>false</LastTripOfSchedule><BusType>4E - DEH</BusType><Latitude /><Longitude /><GPSSpeed /></Trip></Trips></RouteDirection></Route></GetNextTripsForStopResult></GetNextTripsForStopResponse></soap:Body></soap:Envelope>'
    sts, eds = getValuesBetweenTags('AdjustedScheduleTime', xml)
    timeList = []
    for i in range(0, 3):  # goes from 0 to 2
        timeList.append('')
        for k in range(sts[i], eds[i]+1):
            timeList[i] += str(xml[k])
            print xml[k],  # comma to prevent newline
        print ''  # cause newline

    print timeList
    #print xml[sts[0]], xml[eds[0]]
    #print sts, eds

#testmodule()
