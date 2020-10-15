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

        array = []
        for event in events:
            if event['start']['dateTime'] >= starting_time and event['start']['dateTime'] <= ending_time and event['end']['dateTime'] >= starting_time and event['end']['dateTime'] <= ending_time:
                event_summary = event.get('summary', 'unnamed')
                event_reminders = event.get('reminders', [])
                event_id = event.get('id', 'unknown')
                json = {'event_summary': event_summary, 'reminders': event_reminders, 'id': event_id}
                array.append(json)
        return array
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



    def delete_event(self, api, events, index):

        if(index > len(events)):
            return "out of index"
        elif index < 0:
            return "Negative index"
        else:
            event_id = events[index]['id']

            api.events().delete(calendarId='primary', eventId=event_id).execute()
            return "Success"


    # def delete_ev(self, api, event_id):
    #     try:
    #         api.events().delete(calendarId='primary', eventId=event_id).execute()
    #         return "Success"
    #
    #     except:
    #         return "Failed"





calendar = Calendar()
api = calendar.get_calendar_api()
events=calendar.get_five_year_event_past(api)
# print(calendar.delete_ev(api, "asd"))