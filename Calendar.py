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


class Calendar:
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

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

    def get_all_events(self, api, starting_time, ending_time):

        events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                          timeMax=ending_time, singleEvents=True,
                                          orderBy='startTime', showDeleted=None).execute()

        events = events_result.get('items', [])
        return events

    # def find_events_by_name(self, api, name):
    #     # the search is done based on the "queried" keyword
    #     events_result = api.events().list(calendarId='primary', singleEvents=True,
    #                                       orderBy='startTime', q=name).execute()
    #     events = events_result.get('items', [])
    #     array=[]
    #     for event in events:
    #         event_summary = event.get('summary', 'unnamed')
    #         event_reminders = event.get('reminders', [])
    #         event_id = event.get('id', 'unknown')
    #         json = {'event_summary': event_summary, 'reminders':event_reminders, 'id':event_id}
    #         array.append(json)
    #     return array

    def navigate(self, api, year, month=1, day=1):
        # startTime = "T00:00:00+00:00"
        # 'start': {'dateTime': '2020-09-28T07:30:00+10:00'}, '
        events = []
        startDate = datetime.datetime(year, month, day).isoformat() + 'Z'
        if month == 12:
            endDate = datetime.datetime(year + 1, 1, day).isoformat() + 'Z'
        else:
            endDate = datetime.datetime(year + 1, month + 1, day).isoformat() + 'Z'
        events = self.get_all_events(api, startDate, endDate)
        return events



    def navigateUser(self, api):
        time = str(input("Enter time period"))
        timeList = time.split('-')
        year = timeList[0]
        events = []
        if len(timeList) == 1:
            year = int(timeList[0])
            events = self.navigate(api, year)
        elif len(timeList) == 2:
            year = int(timeList[0])
            month = int(timeList[1])
            events = self.navigate(api, year, month)
        elif len(timeList) == 3:
            year = int(timeList[0])
            month = int(timeList[1])
            day = int(timeList[2])
            events = self.navigate(api, year, month, day)

        i = 0
        for event in events:
            i += 1
            print(str(i) + ". " + str(event.get('summary')) + "\n")

        event_number = input("Select event number")
        try:
            print(events[event_number - 1])
        except:
            print("Wrong option number entered")
        return None


        # selectedTimePeriod = 2020
        # selectedTimePeriod = 2020
        # selectedTimePeriod = 2020
        # 2020-03-03T12:23:45.000000Z
        # toDo: find out format of time entered
        # if only year given:
        # append rest of the details
        # start_time = 1st Jan of given year
        # end_time = 1st Jan of next year

        # elif year and month given:
        # start_time = 1st of given month and year
        # end_time = 1st Jan of next month and year

        # elif year month and date given:
        # start_time = 12:am given date month and year
        # end_time = 12:am given date next month and year

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

    def delete_ev(self, api, id):
        return api.events().delete(calendarId='primary', eventId=id).execute()



calendar = Calendar()
api = calendar.get_calendar_api()
events = calendar.get_two_year_event_future(api)
# print(calendar.delete_ev(api, "asd"))
print(calendar.navigate(api, 2020))
