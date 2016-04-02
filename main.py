import sqlite3  # use python's built in sqlite3 utility for the database management
import datetime  # Gets full date/time for timestamping
import time  # Used for sleep functionality
import ocinterface  # Interfaces with the OC Transpo API

CREATE_TABLES = 0  # flag for if the database is being generated for the first time

def main():
    # todo: switch to real DB when collecting full data
    busTimes = dbOpen('9timesTEST.db')

    # program runs until stopped in command line
    while True:

        checkTime()

        stop8766Info = stopValues()
        stop8766Info = fill9Info(stop8766Info)
        stop8766Info = stopTimeInfoRet(stop8766Info)

        dbAdd(busTimes, stop8766Info)
        busTimes.commit()  # need to commit changes (insertion/deletion/etc) made to database

    # Close the database connection
    dbClose(busTimes)


def dbOpen(database):

    dbConn = sqlite3.connect(database)  # database connector
    print('Database opened successfully')

    # add the appropriate tables we need, toggle flag if rebuilding db
    if(CREATE_TABLES == 1):
        dbConn.execute('''CREATE TABLE Times
        (StopNum INT NOT NULL,
        RouteNum INT NOT NULL,
        PollTime STRING NOT NULL,
        TimeToNext INT,
        NextBusStartTime STRING,
        TimeTo2nd INT,
        TimeTo3rd INT);
        ''')
        # above: creating table called TIMES
        # the primary key is a unique value to a table to identify it
        # StopNum: number of the bus stop
        # RouteNum: number of the route being tracked
        # time to next and next after busses can be null to signify no GPS estimate available

        print('Table created successfully')

    return dbConn


def dbAdd(dbConn, stopInfo):

    # need to have quotations as part of the string here or SQL doesn't like it
    timeStr = stopInfo.PollTime.strftime("\"%c\"")  # converts datetime object into string

    dbCommand = """INSERT INTO Times (StopNum, RouteNum, PollTime, TimeToNext, NextBusStartTime, TimeTo2nd, TimeTo3rd) VALUES (%d, %d, %s, %d, %s, %d, %d)""" \
                % (stopInfo.StopNum, stopInfo.RouteNum, timeStr, stopInfo.TimeToNext, stopInfo.NextBusStartTime, stopInfo.TimeTo2nd, stopInfo.TimeTo3rd)
    print(dbCommand)

    dbConn.execute(dbCommand)


def dbClose(database):

    database.close()
    print('Database closed succesfully')


# get the GPS estimates info from OC transpo and return it in the named tuple format
def stopTimeInfoRet(stopInfo):

    stopInfo.PollTime = datetime.datetime.now()  # get the time just before doing the call to OC Transpo
    times, startTime = ocinterface.getNextTimes(stopInfo)  # get the times to the next buses (GPS only likely for 1st)

    # Naming convention unfortunately switches a lot because of database entry/class attribute style
    stopInfo.TimeToNext = int(times[0])
    stopInfo.TimeTo2nd = int(times[1])
    stopInfo.TimeTo3rd = int(times[2])
    stopInfo.NextBusStartTime = startTime

    return stopInfo


def fill9Info(stop8766Info):
    # fills in stop and route info for the primary test stop
    stop8766Info.StopNum = 8766
    stop8766Info.RouteNum = 9
    return stop8766Info


def checkTime(): # halts program until start of next minute by waiting an appropriate amount of time
    currentTime = datetime.datetime.now()
    timeToWait = 60 - currentTime.second
    #timeToWait = 5
    time.sleep(timeToWait) # sleep for the number of seconds until the next minute


class stopValues:
    # need to give some kind of initialized values
    StopNum = -1  # OC Transpo stop number
    RouteNum = -1  # OC Transpo bus route number
    PollTime = datetime.datetime.now()  # the date and time at which the API call was made
    TimeToNext = -100  # the estimated time to the next bus arrival at StopNum of the RouteNum bus
    NextBusStartTime = ''  # the time the next bus to arrive set out
    TimeTo2nd = -100  # the estimated time to the 2nd next bus
    TimeTo3rd = -100


main()

