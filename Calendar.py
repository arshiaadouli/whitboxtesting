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
SCOPES = ["https://www.googleapis.com/auth/calendar"]


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

def get_two_year_event_future(api):
    
    time_now = datetime.datetime.utcnow().isoformat() + 'Z'
    time_end = (datetime.datetime.utcnow() + datetime.timedelta(days=2 * 365)).isoformat() + 'Z'

    return get_all_events(api, time_now, time_end)


def get_five_year_event_past(api):
    
    time_end = datetime.datetime.utcnow().isoformat() + 'Z'
    time_start = (datetime.datetime.utcnow() - datetime.timedelta(days=5 * 365)).isoformat() + 'Z'


    return get_all_events(api, time_start, time_end)


    
    
def get_all_events(api, starting_time, ending_time):
    

    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      timeMax=ending_time, singleEvents=True,
                                      orderBy='startTime', showDeleted=None).execute()
    events = events_result.get('items', [])
    print(events)
    first_stmt=''
    second_stmt=''
    for event in events:
        event_summary = event.get('summary', 'unnamed')
        if event['reminders']['useDefault']:
            rem_dur = 10

            print("summary is " + event_summary + " reminder method is: popup, the duration of the reminder is "+str(rem_dur))
        else:
            if event['reminders'].get('overrides', [])==[]:
                break
            for override in event['reminders']['overrides']:
                
                print("'summary':"+ event_summary +" 'method :' "+ override['method'] +" 'minutes': " +str(override['minutes']))
    return events


def find_events_by_id(api, name):
    #the search is done based on the "queried" keyword
    events_result = api.events().list(calendarId='primary', singleEvents=True,
                                      orderBy='startTime', q=name).execute()
    return events_result.get('items', [])

def get_eventId(events, index):
    dic=add_to_dictionary(events)
    return dic[index][0]

def add_attendies(api, att_email, events, index):
    event_id = events[index]['id']
    if att_email[len(att_email)-19:len(att_email)]=="@student.monash.edu":

        events_result = api.events().get(calendarId='primary', eventId=event_id).execute()
        event = events_result
        if event.get('attendees', None)==None:
            event['attendees'] = []
        x = {'email': att_email}
        event['attendees'].append(x)
        # print(event)

        updated_event = api.events().update(calendarId='primary', eventId=event_id,
                                            body=event).execute()
        return updated_event
    else:
        return "wrong email format"
def delete_event(api, events, index):
    event_id = events[index]['id']
    try:
        api.events().delete(calendarId='primary', eventId=event_id).execute()
    except:
        print("no event is existed")
    return 0;

def delete_reminder(api, events, index, idx_reminder):
    try:
        event_reminder = events[index].get('reminders', [])
        if(event_reminder['useDefault']):
            events[index]['reminders']['useDefault']=False
            events[index]['reminders']['overrides']=[]
            print(events[index])
            api.events().update(calendarId='primary', eventId = events[index]['id'], body=events[index]).execute()
            return "the reminder is removed"
        else:
            try:
                if events[index]['reminders'].get('overrides', None)!=None:
                    idx = events[index]['reminders']['overrides'][idx_reminder]
                    print(idx)
                    events[index]['reminders']['overrides'].remove(idx)
                    api.events().update(calendarId='primary', eventId = events[index]['id'], body=events[index]).execute()
                    print(events)
                    return "the reminder is removed"
                else:
                    return "no reminder is existed to be deleted"

            except:
                return "overrides index error"
    except IndexError:
        return "event index error"



def add_to_dictionary(events):
    dic={}
    index = 1;
    for event in events:
        dic[index] = [event['id'], event['summary']]
        index+=1;
    return dic

def insert_event(api, summary, start_date, start_time, end_date, end_time):
    body={'summary':summary, 'start':{'dateTime': start_date+'T'+start_time+'+10:00'}, 'end':{'dateTime': end_date+'T'+end_time+'+10:00'}, 'reminders':{'useDefault':False, 'overrides': []}}
    api.events().insert(calendarId='primary', body=body).execute()

def add_reminder(api, events, index, method, minutes):
    if events[index].get('reminders', None)==None:
        events['index']['reminders'] = {useDefault:'False'}
    if events[index]['reminders'].get('overrides', None)==None:
        events[index]['reminders']['overrides']=[]
    events[index]['reminders']['overrides'].append({'method':method, 'minutes':minutes})
    api.events().update(calendarId='primary', eventId=events[index]['id'], body=events[index]).execute()

def main():
    api = get_calendar_api()
    # insert_event(api, "steve jobs", '2020-10-4', '20:00:00', '2020-10-4', '21:00:00')
    events = get_two_year_event_future(api)
    # add_reminder(api, events, 2, 'email', 30)
    add_attendies(api, "yami0001@student.monash.edu", events, 2)




    # time_start = datetime.datetime.utcnow().isoformat() + 'Z'
    # time_end = (datetime.datetime.utcnow() + datetime.timedelta(days=2*365)).isoformat() + 'Z'
    



    
    # # print("the answer:")
    # # print(delete_reminder(api, events, 2, 2))
    # # print(add_attendies(api, "ysadasdasdsada@student.monash.edu", events, 1))
    # # print(delete_reminder(api, events, 1, 0))
    # events = get_two_year_event_future(api)




    # events = get_two_years_event_future(api)
    # event = events[0];
    # event['reminders']['useDefault'] = False;
    # event['reminders']['overrides'] = [];
    # event['reminders']['overrides'].append({'method':'popup', 'minutes':5})
    # api.events().update(calendarId='primary', eventId = event['id'], body=event).execute()

    



    













    # events_result = api.events().list(calendarId='primary', showDeleted=None, singleEvents=True).execute()
    # events = events_result.get('items', [])
    # print(events)


    
    # events = get_two_years_event(api, time_now, time_end)
    # print(add_to_dictionary(events))

    # add_attendies(api, "aado0003@student.monash.edu", events , 1)

    # print(get_five_year_event_past(api)[0]['start']['dateTime']=='2017')


    # events_result = api.events().list(calendarId='primary', showDeleted=None, singleEvents=True).execute()
    # events = events_result.get('items', [])
    # try:
    #     for event in events:
    #         api.events().delete(calendarId='primary', eventId=event['id']).execute()
    # except:
    #     pass

    # api.events().insert(calendarId = 'primary', body={'summary':'arshiaasdasdas', 'start': {'dateTime': '2020-09-28T07:36:49+10:00'}, 'end': {'dateTime': '2020-09-28T08:36:49+10:00'}}).execute()





    # events = get_two_years_event(api, time_now, time_end)
    # events = find_events_by_id(api, 'arshia')
    # for event in events:
    #     eventId = event['id']
    #     try:
    #         api.events().delete(calendarId='primary', eventId=eventId).execute()
    #     except:
    #         print("event id with id of " + eventId + " has been deleted")




if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()


