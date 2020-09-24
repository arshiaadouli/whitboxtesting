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

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def get_calendar_api():
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


def get_upcoming_events(api, starting_time, number_of_events):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    if (number_of_events <= 0):
        raise ValueError("Number of events must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])

    # Add your methods here.


def get_two_years_event(api, starting_time, ending_time):

    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      timeMax=ending_time, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])


def find_events_by_id(api, name):
    #the search is done based on the "queried" keyword
    events_result = api.events().list(calendarId='primary', singleEvents=True,
                                      orderBy='startTime', q=name).execute()
    return events_result.get('items', [])


def add_attendies(api, att_email, event_id):
    if att_email[len(att_email)-19:len(att_email)]=="@student.monash.edu":

        events_result = api.events().get(calendarId='primary', eventId=event_id).execute()
        event = events_result
        if not event.get('attendees', []):
            event['attendees'] = []
        x = {'email': att_email}
        event['attendees'].append(x)
        print(event)
        updated_event = api.events().update(calendarId='primary', eventId=event_id,
                                            body=event).execute()
        print(updated_event)
    else:
        print("wrong email format")
def delete_event(api, event_id):
    # delete the first event first
    try:
        api.events().delete(calendarId='primary', eventId=event_id).execute()
    except:
        print("no event is existed")
    return 0;

def add_to_dictionary(events):
    dic={}
    for event in events:
        dic[event['id']] = event['summary']
    return dic

def main():
    api = get_calendar_api()
    time_now = datetime.datetime.utcnow().isoformat() + 'Z'
    time_end = (datetime.datetime.utcnow() + datetime.timedelta(days=2 * 365)).isoformat() + 'Z'
    events = get_two_years_event(api, time_now, time_end)
    add_attendies(api, "aado0002@student.monash.edu", events[1]['id']);





    # events = get_two_years_event(api, time_now, time_end)
    # events = find_events_by_id(api, 'arshia')
    # for event in events:
    #     eventId = event['id']
    #     try:
    #         api.events().delete(calendarId='primary', eventId=eventId).execute()
    #     except:
    #         print("event id with id of " + eventId + " has been deleted")

    # events = find_events_by_id(api, "arshia adouli")
    # print(events)
    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

    # add_attendies(api, "arshia adouli", "smoj0002@student.monash.edu")


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()


