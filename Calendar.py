# Make sure you are logged into your Monash student account.
# Go to: https://developers.google.com/calendar/quickstart/python
# Click on "Enable the Google Calendar API"
# Configure your OAuth client - select "Desktop app", then proceed
# Click on "Download Client Configuration" to obtain a credential.json file
# Do not share your credential.json file with anybody else, and do not commit it to your A2 git repository.
# When app is run for the first time, you will need to sign in using your Monash student account.
# Allow the "View your calendars" permission request.


# Students must have their own api key
# No test cases needed for authentication, but authentication may required for running the app very first time.
# http://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html


# Code adapted from https://developers.google.com/calendar/quickstart/python
from __future__ import print_function
import datetime
import pickle
import os.path
from unittest.mock import Mock

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

"""
description: Class representing Calendars
"""
class Calendar:
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    """
    description: method to get the calendar api
    inputs: None
    returns: calendar api
    """
    def get_calendar_api(self):
        SCOPES = ["https://www.googleapis.com/auth/calendar"]

        """
        Get an object which allows you to consume the Google Calendar API.
        You do not need to worry about what this function exactly does, nor create test cases for it.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('calendar', 'v3', credentials=creds)

    """
        description: method to get all the upcoming events in the future from the calendar
        inputs: api - calendar api; starting_time - time when user wants the events from; 
        number_of_events - the number of events user wants to look at
        returns: a list of the details of the number of events requested from the starting_time
    """
    def get_upcoming_events(self, api, starting_time, number_of_events):
        """
        Shows basic usage of the Google Calendar API.
        Prints the start and name of the next n events on the user's calendar.
        """
        if number_of_events == 1:
            return False
        if (number_of_events <= 0):
            raise ValueError("Number of events must be at least 1.")

        events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                          maxResults=number_of_events, singleEvents=True,
                                          orderBy='startTime').execute()
        return events_result.get('items', [])

        # Add your methods here.

    """
    description: method to get all the upcoming events in the future till 2 years after from
    the present time from the calendar
    inputs: api - calendar api
    returns: a list of the details of events from the present time to 2 years in the future
    """
    def get_two_year_event_future(self, api):

        starting_time = datetime.datetime.utcnow().isoformat() + 'Z'
        ending_time = (datetime.datetime.utcnow() + datetime.timedelta(days=2 * 365)).isoformat() + 'Z'
        events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                          timeMax=ending_time, singleEvents=True,
                                          orderBy='startTime', showDeleted=None).execute()

        events = events_result.get('items', [])
        # return events

        array = []
        for event in events:
            if event['start']['dateTime'] >= starting_time and event['start']['dateTime'] <= ending_time:
                event_summary = event.get('summary', 'unnamed')
                event_reminders = event.get('reminders', [])
                event_id = event.get('id', 'unknown')
                json = {'event_summary': event_summary, 'reminders': event_reminders, 'id': event_id}
                array.append(json)
        return array

    """
    description: method to get all the past events from the calendar from 5 years before from the present time
    inputs: api - calendar api
    returns: a list of the details of events from the 5 years ago to the present time
    """
    def get_five_year_event_past(self, api):

        ending_time = datetime.datetime.utcnow().isoformat() + 'Z'
        starting_time = (datetime.datetime.utcnow() - datetime.timedelta(days=5 * 365)).isoformat() + 'Z'
        events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                          timeMax=ending_time, singleEvents=True,
                                          orderBy='startTime', showDeleted=None).execute()

        events = events_result.get('items', [])
        #return events
        array = []
        for event in events:
            if event['start']['dateTime'] >= starting_time and event['start']['dateTime'] <= ending_time and \
                    event['end']['dateTime'] >= starting_time and event['end']['dateTime'] <= ending_time:
                event_summary = event.get('summary', 'unnamed')
                event_reminders = event.get('reminders', [])
                event_id = event.get('id', 'unknown')
                json = {'event_summary': event_summary, 'reminders': event_reminders, 'id': event_id}
                array.append(json)
        return array

    """
    description: method to get all the events from the calendar from starting_time to ending_time
    inputs: api - calendar api; starting_time - time when user wants the events from;
    ending_time - time when user wants the events till;
    number_of_events - the number of events user wants to look at;
    returns: a list of the details of all the events from the starting_time till ending_time
    """
    def get_all_events(self, api, starting_time, ending_time):

        events_result = api.events().list(calendarId='primary', timeMin=starting_time, timeMax=ending_time, singleEvents=True,orderBy='startTime', showDeleted=None).execute()

        events = events_result.get('items', [])
        return events

    """
        description: method to find the events from the calendar by their name
        inputs: api - calendar api; name - name of the event
        returns: "found" if event of given name found otherwise returns "not found"
    """
    def find_events_by_name(self, api, name):
        # the search is done based on the "queried" keyword
        events_result = api.events().list(calendarId='primary', singleEvents=True,
                                          orderBy='startTime', q=name).execute()
        events = events_result.get('items', [])
        array=[]
        for event in events:
            event_summary = event.get('summary', 'unnamed')
            event_reminders = event.get('reminders', [])
            event_id = event.get('id', 'unknown')
            json = {'event_summary': event_summary, 'reminders':event_reminders, 'id':event_id}
            array.append(json)
        for elem in array:
            if name in elem.get("event_summary"):
                return "found"
        return "not found"

    """
        description: method to navigate and find all the events from the calendar according to 
        time requested by user
        inputs: api - calendar api; year - year when user wants the events;
        month - month when user wants the events from;
        day - day when user wants the events from;
        string - specifies what format user gave input in i.e. (YYYY, YYYY-MM or YYYY-MM-DD);
        returns: a list of the details of all the events from the given time period
    """
    def navigate(self, api, year, month, day, string):
        if string=='year':
            startDate = datetime.datetime(year, 1, 1).isoformat() + 'Z'
            endDate = datetime.datetime(year + 1, 1, 1).isoformat() + 'Z'
        elif string=="month":
            if month == 12:
                endDate = datetime.datetime(year + 1, 1, 1).isoformat() + 'Z'
            elif month >12:
                return []
            else:
                endDate = datetime.datetime(year, month + 1, 1).isoformat() + 'Z'

        elif string=="day":
            if month == 12:

                try:
                    endDate = datetime.datetime(year, month, day+1).isoformat() + 'Z'
                except:
                    endDate = datetime.datetime(year, 1, 1).isoformat() + 'Z'
            else:
                try:
                    endDate = datetime.datetime(year, month, day + 1).isoformat() + 'Z'
                except:
                     endDate = datetime.datetime(year, month+1, 1).isoformat() + 'Z'



        # startTime = "T00:00:00+00:00"
        # 'start': {'dateTime': '2020-09-28T07:30:00+10:00'}, '
        events = []
        try:
            startDate = datetime.datetime(year, month, day).isoformat() + 'Z'
        except:
            return ["error"]
        """
        if month == 12:
            endDate = datetime.datetime(year + 1, 1, day).isoformat() + 'Z'
        else:
            try:
                endDate = datetime.datetime(year, month + 1, day+1).isoformat() + 'Z'
            except:
                endDate = datetime.datetime(year, month + 2, 1).isoformat() + 'Z'
        """
        events = self.get_all_events(api, startDate, endDate)
        return events

    """
    description: method to enable user to navigate and find all the events from the calendar according
    for a time period of their choosing
    If they want events for a whole year, they will enter year in YYYY format
    If they want events for a specific month, they will enter time in YYYY-MM format
    If they want events for a specific date, they will enter time in YYYY-MM-DD format
    After the time period has been selected, and IF any events exist for that time period, 
    the summary of those events will be displayed through a menu and user can chose which 
    event they want the details for. The details for the chosen event will be shown to the user
    inputs: api - calendar api; year - year when user wants the events;
    returns: 1 if navigation successful otherwise returns 0
    """

    def navigateUser(self, api):
        time = str(input("Enter time period"))
        timeList = time.split('-')
        print(timeList)
        year = timeList[0]
        events = []
        if len(timeList) == 1:
            if year=='':
                events = ['error']
            else:
                year = int(timeList[0])
                events = self.navigate(api, year, 1, 1,"year")
        elif len(timeList) == 2:
            print("time list 2")
            year = int(timeList[0])
            month = int(timeList[1])
            print("month  = " + str(month))

            events = self.navigate(api, year, month, 1, "month")
            if month > 12:
                events = ['error']
        elif len(timeList) == 3:
            year = int(timeList[0])
            month = int(timeList[1])
            day = int(timeList[2])
            events = self.navigate(api, year, month, day, "day")
        print("events line 175 = " + str(len(events)))

        i = 0
        for event in events:
            if event == 'error':
                return 0
            i += 1
            print(str(i) + ". " + str(event.get('summary')) + "\n")
        print("line 235:", len(events))
        if len(events) > 0:
            event_number = int(input("Select event number"))


            try:
                print(events[event_number - 1])
            except:
                print("Wrong option number entered")
                print("line 238: ", len(events))
                return 0

        return 1

    """
        description: method to enable user to delete event of their choice
        inputs: api - calendar api; year - year when user wants the events;
        events - list of events to delete from
        index - index of event to be deleted
        returns: "Success" if deletion successful, "out of index" if index provided is out of range,
        "Negative index" if index provided is a negative number, otherwise returns "Error" if network issues occur
    """
    def delete_event(self, api, events, index):

        if (index >= len(events)):
            return "out of index"
        elif index < 0:
            return "Negative index"
        else:
            try:
                event_id = events[index]['id']
                api.events().delete(calendarId='primary', eventId=event_id).execute()
                return "Success"
            except:  # in case of some network issues
                return "Error"

    """
    description: method calls the delete_event method with appropriate arguments
    inputs: api - calendar api; year - year when user wants the events;
    id - event id
    returns: True if deletion successful
    """
    def delete_ev(self, api, id):
        if api.events().delete(calendarId='primary', eventId=id).execute()=='':
            return True


calendar = Calendar()
api = calendar.get_calendar_api()
startDate = datetime.datetime(20, 5, 1).isoformat() + 'Z'
#print(len(calendar.get_all_events(api,startDate,datetime.datetime(2020, 6, 1).isoformat() + 'Z')))
# print(calendar.navigateUser(api))

# print(calendar.find_events_by_name(api, "zxc"))

# print(startDate)