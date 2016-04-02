def getValuesBetweenTags(tag, xmlstr):  # find all instances of an XML tag and return the value within it

    index = 0
    tagStartIndexes = []  # contains list of index of starting characters of tags
    tagEndIndexes = []  # Contains indexes of the last character of the values within the tags
    tagList = []
    startTag = '<' + tag + '>'  # Add opening and closing tags to differentiate start and end tags
    endTag = '</' + tag

    print 'Looking for tag', tag

    #todo: find way to handle differentiating between having found all instances of tag and no instances of tag existing at all (ex: at night when no busses running)
    while index < len(xmlstr):

        # Find start of tag
        index = xmlstr.find(startTag, index)
        print index
        if index == 0:  # If index isn't moved can indiciate no string found
            print 'No times found', index
            return ['-100', '-100', '-100']

        if index == -1: break  # -1 indicates no str found by str.find(), will show up after 3 times are found or if tag not present
        tagStartIndexes.append(index + len(startTag))  # start of values will be index + tag length

        # Find end of tag
        index = xmlstr.find(endTag, index)
        if index == -1:
            print 'Error: Found XML start tag but no end tag'  # This should never happen
            break
        tagEndIndexes.append(index - 1)  # Last char of value will be 1 less than start of end tag

        index += len(endTag)  # Index is at start of end tag so this brings it forward enough

    for i in range(0, 3):  # goes from 0 to 2
        tagList.append('')  # Add a blank entry to time list
        print i
        print tagStartIndexes[i], tagEndIndexes[i]+1
        for k in range(tagStartIndexes[i], tagEndIndexes[i]+1):
            tagList[i] += str(xmlstr[k])

    return tagList


# Tests the functionality of the parser. Use for debug.
def testmodule():
    xml = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><GetNextTripsForStopResponse xmlns="http://octranspo.com"><GetNextTripsForStopResult><StopNo xmlns="http://tempuri.org/">8766</StopNo><StopLabel xmlns="http://tempuri.org/">CRICHTON CHARLES</StopLabel><Error xmlns="http://tempuri.org/" /><Route xmlns="http://tempuri.org/"><RouteDirection><RouteNo>9</RouteNo><RouteLabel>Rideau</RouteLabel><Direction>Southbound</Direction><Error /><RequestProcessingTime>20160402012857</RequestProcessingTime><Trips /></RouteDirection></Route></GetNextTripsForStopResult></GetNextTripsForStopResponse></soap:Body></soap:Envelope>'
    tags = getValuesBetweenTags('AdjustedScheduleTime', xml)
    print tags

#testmodule()
