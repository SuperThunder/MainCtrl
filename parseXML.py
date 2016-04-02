def getValuesBetweenTags(tag, xmlstr):  # find all instances of an XML tag and return the value within it

    index = 0
    tagStartIndexes = []  # contains list of index of starting characters of tags
    tagEndIndexes = []  # Contains indexes of the last character of the values within the tags
    tagList = []
    startTag = '<' + tag + '>'  # Add opening and closing tags to differentiate start and end tags
    endTag = '</' + tag

    #print 'Looking for tag', tag

    #todo: find way to handle differentiating between having found all instances of tag and no instances of tag existing at all (ex: at night when no busses running)
    while index < len(xmlstr):

        # Find start of tag
        tagLoc = xmlstr.find(startTag, index)
        if index == 0 and tagLoc == -1:  # If nothing is found on first search
            print 'No times found'
            return ['-100', '-100', '-100']
        if tagLoc == -1:
            break  # -1 indicates no str found by str.find(), normally shows up after all 3 tags found
        tagStartIndexes.append(tagLoc + len(startTag))  # start of values will be index + tag length

        # Find end of tag
        tagLoc = xmlstr.find(endTag, index)
        if tagLoc == -1:
            print 'Error: Found XML start tag but no end tag'  # This should never happen
            break
        tagEndIndexes.append(tagLoc - 1)  # Last char of value will be 1 less than start of end tag

        index = tagLoc + len(endTag)  # Bring index past last found closing tag

    for i in range(len(tagEndIndexes)):  # Scales to however many tags were found
        tagList.append('')  # Add a blank entry to time list
        #print tagStartIndexes[i], tagEndIndexes[i]+1
        for k in range(tagStartIndexes[i], tagEndIndexes[i]+1):
            tagList[i] += str(xmlstr[k])

    return tagList


# Tests the functionality of the parser. Use for debug.
def testmodule():
    xml = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><GetNextTripsForStopResponse xmlns="http://octranspo.com"><GetNextTripsForStopResult><StopNo xmlns="http://tempuri.org/">8766</StopNo><StopLabel xmlns="http://tempuri.org/">CRICHTON CHARLES</StopLabel><Error xmlns="http://tempuri.org/" /><Route xmlns="http://tempuri.org/"><RouteDirection><RouteNo>9</RouteNo><RouteLabel>Rideau</RouteLabel><Direction>Southbound</Direction><Error /><RequestProcessingTime>20160402012857</RequestProcessingTime><Trips /></RouteDirection></Route></GetNextTripsForStopResult></GetNextTripsForStopResponse></soap:Body></soap:Envelope>'
    tags = getValuesBetweenTags('AdjustedScheduleTime', xml)
    print tags
#testmodule()
