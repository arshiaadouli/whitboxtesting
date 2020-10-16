import sys
import unittest
import datetime
from unittest.mock import Mock, patch
# Add other imports here if needed
import calendar

from Calendar import Calendar


class CalendarTest(unittest.TestCase):

    # This test tests number of upcoming events.
    def test_get_upcoming_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        calendar = Calendar()
        events = calendar.get_upcoming_events(mock_api, time, num_events)

        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1
        )

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['maxResults'], num_events)

    """
    description: this test case will test the get_five_year_event_past() when the given event(s) are in
    last five years
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('Calendar.open')  # accessing calendar events and other details using patching the Calendar.open
    def test_five_year_event_past_in_range(self, mock_api):
        cal = Calendar()
        # specify ret val
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = [
            {
                'id': '59kstuco11fiikf4v831pmfcte',
                'summary': 'first event', 'start': {'dateTime': '2016-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2018-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            }
        ]  # creating events in mock object for having some test data

        event = cal.get_five_year_event_past(mock_api)  # replace mock with the api in the function

        expected_value = [
            {'event_summary': 'first event', 'reminders': {'useDefault': True}, 'id': '59kstuco11fiikf4v831pmfcte'}]
        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1
            # checking if the request for getting the events has been made once
        )
        args, kwargs = mock_api.events.return_value.list.call_args_list[0]  # getting the first(only) call's arguments
        ending_time = datetime.datetime.utcnow().isoformat() + 'Z'
        starting_time = (datetime.datetime.utcnow() - datetime.timedelta(days=5 * 365)).isoformat() + 'Z'

        self.assertEqual(kwargs['timeMin'][0:19], starting_time[
                                                  0:19])  # asserting whether the starting time is the time which is passed to the timeMin argument
        self.assertEqual(kwargs['timeMax'][0:19], ending_time[
                                                  0:19])  # asserting whether the ending time is the time which is passed to the timeMax argument
        self.assertEqual(event,
                         expected_value)  # asserting whether the result of the function is the same as the expected value

    """
    description: this test case will test the get_five_year_event_past() when some of the given event(s) are in 
    before range(before than last five years)
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('Calendar.open')  # accessing calendar events and other details using patching the Calendar.open
    def test_five_year_event_past_before_range(self, mock_api):
        cal = Calendar()
        # specify ret val
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = [
            {
                'id': '59kstuco11fiikf4v831pmfcte',
                'summary': 'first event', 'start': {'dateTime': '2016-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2018-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },

            {
                'id': '60ksturo11fiikg4v831pjfcte',
                'summary': 'second event', 'start': {'dateTime': '2010-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2011-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            }
        ]  # creating events in mock object for having some test data

        event = cal.get_five_year_event_past(mock_api)  # replace mock with the api in the function

        expected_value = [
            {'event_summary': 'first event', 'reminders': {'useDefault': True}, 'id': '59kstuco11fiikf4v831pmfcte'}]
        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1
            # checking if the request for getting the events has been made once
        )
        args, kwargs = mock_api.events.return_value.list.call_args_list[0]  # getting the first(only) call's arguments
        ending_time = datetime.datetime.utcnow().isoformat() + 'Z'
        starting_time = (datetime.datetime.utcnow() - datetime.timedelta(days=5 * 365)).isoformat() + 'Z'
        """
        this below code check the 19 element of timeMin and starting time because they are almost equal and they difference 
        is around 0.001 seconds
        """
        self.assertEqual(kwargs['timeMin'][0:19], starting_time[
                                                  0:19])  # asserting whether the starting time is the time which is passed to the timeMin argument
        self.assertEqual(kwargs['timeMax'][0:19], ending_time[
                                                  0:19])  # asserting whether the ending time is the time which is passed to the timeMax argument
        self.assertEqual(event,
                         expected_value)  # asserting whether the result of the function is the same as the expected value

    """
    description: this test case will test the get_five_year_event_past() when the given event(s) are created 
    after todays date
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('Calendar.open')  # accessing calendar events and other details using patching the Calendar.open
    def test_five_year_event_past_after_range(self, mock_api):
        cal = Calendar()
        # specify ret val
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = [
            {
                'id': '59kstuco11fiikf4v831pmfcte',
                'summary': 'first event', 'start': {'dateTime': '2016-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2018-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },

            {
                'id': '60ksturo11fiikg4v831pjfcte',
                'summary': 'second event', 'start': {'dateTime': '2021-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2022-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            }
        ]  # creating events in mock object for having some test data

        event = cal.get_five_year_event_past(mock_api)  # replace mock with the api in the function

        expected_value = [
            {'event_summary': 'first event', 'reminders': {'useDefault': True}, 'id': '59kstuco11fiikf4v831pmfcte'}]
        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1
            # checking if the request for getting the events has been made once
        )
        args, kwargs = mock_api.events.return_value.list.call_args_list[0]  # getting the first(only) call's arguments
        ending_time = datetime.datetime.utcnow().isoformat() + 'Z'
        starting_time = (datetime.datetime.utcnow() - datetime.timedelta(days=5 * 365)).isoformat() + 'Z'

        self.assertEqual(kwargs['timeMin'][0:19], starting_time[
                                                  0:19])  # asserting whether the starting time is the time which is passed to the timeMin argument
        self.assertEqual(kwargs['timeMax'][0:19], ending_time[
                                                  0:19])  # asserting whether the ending time is the time which is passed to the timeMax argument
        self.assertEqual(event,
                         expected_value)  # asserting whether the result of the function is the same as the expected value

    """
    description: this test case will test the get_five_year_event_past() when no events are given
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('Calendar.open')  # accessing calendar events and other details using patching the Calendar.open
    def test_five_year_event_past_empty(self, mock_api):
        cal = Calendar()
        # specify ret val
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = []

        event = cal.get_five_year_event_past(mock_api)  # replace mock with the api in the function

        expected_value = []
        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1
            # checking if the request for getting the events has been made once
        )
        args, kwargs = mock_api.events.return_value.list.call_args_list[0]  # getting the first(only) call's arguments
        ending_time = datetime.datetime.utcnow().isoformat() + 'Z'
        starting_time = (datetime.datetime.utcnow() - datetime.timedelta(days=5 * 365)).isoformat() + 'Z'

        self.assertEqual(kwargs['timeMin'][0:19], starting_time[
                                                  0:19])  # asserting whether the starting time is the time which is passed to the timeMin argument
        self.assertEqual(kwargs['timeMax'][0:19], ending_time[
                                                  0:19])  # asserting whether the ending time is the time which is passed to the timeMax argument
        self.assertEqual(event,
                         expected_value)  # asserting whether the result of the function is the same as the expected value

    """
    description: this test case will test the get_two_year_event_future() when the given event(s) are in next two
    years from now
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('Calendar.open')  # accessing calendar events and other details using patching the Calendar.open
    def test_two_year_event_future_in_range(self, mock_api):
        cal = Calendar()
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = [
            {
                'id': '59kstuco11fiikf4v831pmfcte',
                'summary': 'first event', 'start': {'dateTime': '2020-11-15T07:30:00+11:00'},
                'end': {'dateTime': '2021-11-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },

            {
                'id': '60ktugro11fiijg4v831pjfabc',
                'summary': 'second event', 'start': {'dateTime': '2021-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2022-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            }
        ]  # creating events in mock object for having some test data

        event = cal.get_two_year_event_future(mock_api)  # replace mock with the api in the function

        expected_value = [
            {'event_summary': 'first event', 'reminders': {'useDefault': True}, 'id': '59kstuco11fiikf4v831pmfcte'},
            {'event_summary': 'second event', 'reminders': {'useDefault': True}, 'id': '60ktugro11fiijg4v831pjfabc'}

        ]
        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1
            # checking if the request for getting the events has been made once
        )
        args, kwargs = mock_api.events.return_value.list.call_args_list[0]  # getting the first(only) call's arguments
        starting_time = datetime.datetime.utcnow().isoformat() + 'Z'
        ending_time = (datetime.datetime.utcnow() + datetime.timedelta(days=2 * 365)).isoformat() + 'Z'

        self.assertEqual(kwargs['timeMin'][0:19], starting_time[
                                                  0:19])  # asserting whether the starting time is the time which is passed to the timeMin argument
        self.assertEqual(kwargs['timeMax'][0:19], ending_time[
                                                  0:19])  # asserting whether the ending time is the time which is passed to the timeMax argument
        self.assertEqual(event,
                         expected_value)  # asserting whether the result of the function is the same as the expected value

    """
    description: this test case will test the get_two_year_event_future() when the given event(s) are in next two
    years from now
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('Calendar.open')  # accessing calendar events and other details using patching the Calendar.open
    def test_two_year_event_future_before_range(self, mock_api):
        cal = Calendar()
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = [
            {
                'id': '59kstuco11fiikf4v831pmfcte',
                'summary': 'first event', 'start': {'dateTime': '2018-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2018-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },

            {
                'id': '60ktugro11fiijg4v831pjfabc',
                'summary': 'second event', 'start': {'dateTime': '2019-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2019-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            }
        ]  # creating events in mock object for having some test data

        event = cal.get_two_year_event_future(mock_api)  # creating events in mock object for having some test data

        expected_value = []
        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1
            # checking if the request for getting the events has been made once
        )
        args, kwargs = mock_api.events.return_value.list.call_args_list[0]  # getting the first(only) call's arguments
        starting_time = datetime.datetime.utcnow().isoformat() + 'Z'
        ending_time = (datetime.datetime.utcnow() + datetime.timedelta(days=2 * 365)).isoformat() + 'Z'

        self.assertEqual(kwargs['timeMin'][0:19], starting_time[
                                                  0:19])  # asserting whether the starting time is the time which is passed to the timeMin argument
        self.assertEqual(kwargs['timeMax'][0:19], ending_time[
                                                  0:19])  # asserting whether the ending time is the time which is passed to the timeMax argument
        self.assertEqual(event,
                         expected_value)  # asserting whether the result of the function is the same as the expected value

    """
    description: this test case will test the get_two_year_event_future() when the given event(s) are started or ended
    before now
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('Calendar.open')  # accessing calendar events and other details using patching the Calendar.open
    def test_two_year_event_future_after_range(self, mock_api):
        cal = Calendar()
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = [
            {
                'id': '59kstuco11fiikf4v831pmfcte',
                'summary': 'first event', 'start': {'dateTime': '2020-11-15T07:30:00+11:00'},
                'end': {'dateTime': '2020-11-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },

            {
                'id': '60ktugro11fiijg4v831pjfabc',
                'summary': 'second event', 'start': {'dateTime': '2025-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2025-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            }
        ]  # creating events in mock object for having some test data

        event = cal.get_two_year_event_future(mock_api)  # creating events in mock object for having some test data

        expected_value = [

            {'event_summary': 'first event', 'reminders': {'useDefault': True}, 'id': '59kstuco11fiikf4v831pmfcte'}

        ]
        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1
            # checking if the request for getting the events has been made once
        )
        args, kwargs = mock_api.events.return_value.list.call_args_list[0]  # getting the first(only) call's arguments
        starting_time = datetime.datetime.utcnow().isoformat() + 'Z'
        ending_time = (datetime.datetime.utcnow() + datetime.timedelta(days=2 * 365)).isoformat() + 'Z'

        self.assertEqual(kwargs['timeMin'][0:19], starting_time[
                                                  0:19])  # asserting whether the starting time is the time which is passed to the timeMin argument
        self.assertEqual(kwargs['timeMax'][0:19], ending_time[
                                                  0:19])  # asserting whether the ending time is the time which is passed to the timeMax argument
        self.assertEqual(event,
                         expected_value)  # asserting whether the result of the function is the same as the expected value

    """
    description: this test case will test the get_two_year_event_future() when no events are given
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('Calendar.open')  # accessing calendar events and other details using patching the Calendar.open
    def test_two_year_event_future_empty(self, mock_api):
        cal = Calendar()
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = []

        event = cal.get_two_year_event_future(mock_api)  # creating events in mock object for having some test data

        expected_value = []
        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1
            # checking if the request for getting the events has been made once
        )
        args, kwargs = mock_api.events.return_value.list.call_args_list[0]  # getting the first(only) call's arguments
        starting_time = datetime.datetime.utcnow().isoformat() + 'Z'
        ending_time = (datetime.datetime.utcnow() + datetime.timedelta(days=2 * 365)).isoformat() + 'Z'

        self.assertEqual(kwargs['timeMin'][0:19], starting_time[
                                                  0:19])  # asserting whether the starting time is the time which is passed to the timeMin argument
        self.assertEqual(kwargs['timeMax'][0:19], ending_time[
                                                  0:19])  # asserting whether the ending time is the time which is passed to the timeMax argument
        self.assertEqual(event,
                         expected_value)  # asserting whether the result of the function is the same as the expected value

    """
    description: this test case will test the functionality of event_event() function if the index 
    is valid (in range index)
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('Calendar.open')  # accessing calendar events and other details using patching the Calendar.open
    def test_delete_event_valid(self, mock_api):
        cal = Calendar()

        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = [
            {
                'id': '59kstuco11fiikf4v831pmfcte',
                'summary': 'first event', 'start': {'dateTime': '2020-11-15T07:30:00+11:00'},
                'end': {'dateTime': '2022-11-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },

            {
                'id': '60ktugro11fiijg4v831pjfabc',
                'summary': 'second event', 'start': {'dateTime': '2020-11-15T07:30:00+11:00'},
                'end': {'dateTime': '2022-11-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },
            {
                'id': '60ktugro11fiijg4v831pjfabc',
                'summary': 'third event', 'start': {'dateTime': '2020-11-15T07:30:00+11:00'},
                'end': {'dateTime': '2022-11-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },
            {
                'id': '60ktugro11fiijg4v831pjfabc',
                'summary': 'forth event', 'start': {'dateTime': '2020-11-15T07:30:00+11:00'},
                'end': {'dateTime': '2022-11-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            }
        ]  # creating events in mock object for having some test data

        event = cal.get_two_year_event_future(mock_api)     # creating events in mock object for having some test data
        self.assertEqual(cal.delete_event(mock_api, event, 3), "Success")   #assert between the function with valid index and valid index delete message which is success

    """
    description: this test case will test the functionality of event_event() function if the index we use
    is negative(invalid)
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('Calendar.open')  # accessing calendar events and other details using patching the Calendar.open
    def test_delete_event_negative(self, mock_api):
        cal = Calendar()

        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = [
            {
                'id': '59kstuco11fiikf4v831pmfcte',
                'summary': 'first event', 'start': {'dateTime': '2022-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2023-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },

            {
                'id': '60ktugro11fiijg4v831pjfabc',
                'summary': 'second event', 'start': {'dateTime': '2020-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2022-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },
            {
                'id': '60ktugro11fiijg4v831pjfabc',
                'summary': 'third event', 'start': {'dateTime': '2020-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2022-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },
            {
                'id': '60ktugro11fiijg4v831pjfabc',
                'summary': 'forth event', 'start': {'dateTime': '2020-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2022-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            }
        ]  # creating events in mock object for having some test data

        event = cal.get_two_year_event_future(mock_api)      # creating events in mock object for having some test data
        print(event)
        self.assertEqual(cal.delete_event(mock_api, event, -2), "Negative index")       #assert between the function with negative index and negative index message which is Negative index


    """
    description: this test case will test the functionality of event_event() function if the index we use
    is out of range(similar to index error)
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('Calendar.open')  # accessing calendar events and other details using patching the Calendar.open
    def test_delete_event_out_of_range(self, mock_api):  # delete_event(api, event, index)
        # with patch('Calendar.open') as mock_event:
        cal = Calendar()

        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = [
            {
                'id': '59kstuco11fiikf4v831pmfcte',
                'summary': 'first event', 'start': {'dateTime': '2022-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2023-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },

            {
                'id': '60ktugro11fiijg4v831pjfabc',
                'summary': 'second event', 'start': {'dateTime': '2020-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2022-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },
            {
                'id': '60ktugro11fiijg4v831pjfabc',
                'summary': 'third event', 'start': {'dateTime': '2020-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2022-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },
            {
                'id': '60ktugro11fiijg4v831pjfabc',
                'summary': 'forth event', 'start': {'dateTime': '2020-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2022-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            }
        ]  # creating events in mock object for having some test data

        event = cal.get_two_year_event_future(mock_api)      # creating events in mock object for having some test data
        self.assertEqual(cal.delete_event(mock_api, event, 12), "out of index")     #assert between the function with out of range index and out of range index message which is out of index

    """
    description: this test case will test the functionality of find_events_by_name when the keyword
    is in existed the event summary 
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('Calendar.open')  # accessing calendar events and other details using patching the Calendar.open
    def test_search_keyword_found(self, mock_api):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"
        q = "Manika"
        # mock_api = Mock()
        calendar = Calendar()
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = [
            {
                'id': '59kstuco11fiikf4v831pmfcte',
                'summary': 'first event', 'start': {'dateTime': '2016-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2018-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },
            {
                'id': '59kstuco11fiikf4v831pmfcte',
                'summary': 'Arshia Manika', 'start': {'dateTime': '2016-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2018-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },
        ]  # creating events in mock object for having some test data
        events = calendar.find_events_by_name(mock_api, "Manika")   # replacing api with mock object in find_events_by_name
        # using valid key word in the function argument
        self.assertEqual(events, "found")   # assert between the function and valid expected output

        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1
            #making sure that the request for getting the events has made only once
        )

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]  # getting api argument
        self.assertEqual(kwargs['q'], q)  # check that the keyword has been passed successfully

    """
    description: this test case will test the functionality of find_events_by_name when the keyword
    is in NOT existed the event summary 
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('Calendar.open')  # accessing calendar events and other details using patching the Calendar.open
    def test_search_keyword_notFound(self, mock_api):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"
        q = "python"
        # mock_api = Mock()
        calendar = Calendar()
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = [
            {
                'id': '59kstuco11fiikf4v831pmfcte',
                'summary': 'first event', 'start': {'dateTime': '2016-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2018-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },
            {
                'id': '59kstuco11fiikf4v831pmfcte',
                'summary': 'Arshia Manika', 'start': {'dateTime': '2016-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2018-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },
        ]  # creating events in mock object for having some test data
        events = calendar.find_events_by_name(mock_api, "python")
        # replacing api with mock object in find_events_by_name
        # using valid key word in the function argument
        self.assertEqual(events, "not found")       # assert between the function and valid expected output

        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1
            # making sure that the request for getting the events has made only once
        )

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]      # getting api argument
        self.assertEqual(kwargs['q'], q)        # check that the keyword has been passed successfully

    """
    description: this test case is testing navigate function if only year is given as first user input 
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('builtins.input', side_effect=['2020', '1'])
    # builtins.input is used to test functionality dependant on input from the user
    # side_effect[0]: Time Period Input by User
    # side_effect[1]: Event option number input by user
    def test_navigate_year(self, mock_api):
        cal = Calendar()
        result = cal.navigateUser(mock_api)
        self.assertEqual(result, 1)  # 1 return value signifies that navigation was successful

    """
    description: this test case is testing navigate function if  only year and month is given as first user input 
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('builtins.input', side_effect=['2020-05', '1'])
    # builtins.input is used to test functionality dependant on input from the user
    # side_effect[0]: Time Period Input by User
    # side_effect[1]: Event option number input by user
    def test_navigate_month(self, mock_api):
        cal = Calendar()
        result = cal.navigateUser(mock_api)
        self.assertEqual(result, 1)  # 1 return value signifies that navigation was successful

    """
    description: this test case is testing navigate function if full day(year-month) is given as first user input 
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('builtins.input', side_effect=['2020-09-16', '1'])
    # builtins.input is used to test functionality dependant on input from the user
    # side_effect[0]: Time Period Input by User
    # side_effect[1]: Event option number input by user
    def test_navigate_day(self, mock_api):
        cal = Calendar()
        result = cal.navigateUser(mock_api)
        self.assertEqual(result, 1)  # 1 return value signifies that navigation was successful

    """
    description: this test case is testing navigate function if no events are existed in the given data
    and the full date is given in the date 
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('builtins.input', side_effect=['2020-12-16'])
    # builtins.input is used to test functionality dependant on input from the user
    # side_effect[0]: Time Period Input by User
    # side_effect[1]: Event option number input by user
    def test_navigate_day_no_event(self, mock_api):
        cal = Calendar()
        result = cal.navigateUser(mock_api)
        self.assertEqual(result, 1)  # 1 return value signifies that navigation was successful

    """
    description: this test case is testing navigate function if no events are existed in the given data
    and only the year and month is given in the date 
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('builtins.input', side_effect=['2020-12'])
    # builtins.input is used to test functionality dependant on input from the user
    # side_effect[0]: Time Period Input by User
    # side_effect[1]: Event option number input by user
    def test_navigate_month_no_event(self, mock_api):
        cal = Calendar()
        result = cal.navigateUser(mock_api)
        self.assertEqual(result, 1)  # 1 return value signifies that navigation was successful

    """
    description: this test case is testing navigate function if no events are existed in the given data
    and only the year is given in the date 
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('builtins.input', side_effect=['2024'])
    # builtins.input is used to test functionality dependant on input from the user
    # side_effect[0]: Time Period Input by User
    # side_effect[1]: Event option number input by user
    def test_navigate_year_no_event(self, mock_api):
        cal = Calendar()
        result = cal.navigateUser(mock_api)
        self.assertEqual(result, 1)  # 1 return value signifies that navigation was successful

    """
        description: this test case is testing navigate function if invalid month is given  
        inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('builtins.input', side_effect=['2020-56'])
    # builtins.input is used to test functionality dependant on input from the user
    # side_effect[0]: Time Period Input by User
    # side_effect[1]: Event option number input by user
    def test_navigate_year_invalid_month(self, mock_api):
        cal = Calendar()
        result = cal.navigateUser(mock_api)
        self.assertEqual(result, 0)  # 0 return value signifies that navigation was unsuccessful

    """
    description:this test case is testing navigate function when invalid day is given
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('builtins.input', side_effect=['2020-04-78'])
    # builtins.input is used to test functionality dependant on input from the user
    # side_effect[0]: Time Period Input by User
    # side_effect[1]: Event option number input by user
    def test_navigate_year_invalid_day(self, mock_api):
        cal = Calendar()
        result = cal.navigateUser(mock_api)
        self.assertEqual(result, 0)  # 0 return value signifies that navigation was unsuccessful

    """                                                                                                                                                                                                                                                                                                                         
    description: this test case is testing navigate function when empty input is provided
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('builtins.input', side_effect=[''])
    # builtins.input is used to test functionality dependant on input from the user
    # side_effect[0]: Time Period Input by User
    # side_effect[1]: Event option number input by user
    def test_navigate_year_empty(self, mock_api):
        cal = Calendar()
        result = cal.navigateUser(mock_api)
        self.assertEqual(result, 0)  # 0 return value signifies that navigation was unsuccessful

    """
    description: this test case is testing navigate function when the time period is input correctly but the event 
    option number selected is invalid i.e. input is out of range
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('builtins.input', side_effect=['2022', '15'])
    # builtins.input is used to test functionality dependant on input from the user
    # side_effect[0]: Time Period Input by User
    # side_effect[1]: Event option number input by user
    def test_navigate_2nd_input_invalid(self, mock_api):
        mock_api.events.return_value.list.return_value.execute.return_value.get.return_value = [
            {
                'id': '59kstuco11fiikf4v831pmfcte',
                'summary': 'first event', 'start': {'dateTime': '2022-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2023-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },

            {
                'id': '60ktugro11fiijg4v831pjfabc',
                'summary': 'second event', 'start': {'dateTime': '2020-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2022-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },
            {
                'id': '60ktugro11fiijg4v831pjfabc',
                'summary': 'third event', 'start': {'dateTime': '2020-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2022-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            },
            {
                'id': '60ktugro11fiijg4v831pjfabc',
                'summary': 'forth event', 'start': {'dateTime': '2020-10-15T07:30:00+11:00'},
                'end': {'dateTime': '2022-10-15T08:30:00+11:00'},
                'reminders': {'useDefault': True}
            }
        ]
        cal = Calendar()
        result = cal.navigateUser(mock_api)
        self.assertEqual(result, 0)  # 0 return value signifies that navigation was unsuccessful

    """
    description: this test case is testing navigate function when both, the time period
    and the event selection option, are input correctly
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('builtins.input', side_effect=['2020', '1'])
    # builtins.input is used to test functionality dependant on input from the user
    # side_effect[0]: Time Period Input by User
    # side_effect[1]: Event option number input by user
    def test_navigate_2nd_input_valid(self, mock_api):
        cal = Calendar()
        result = cal.navigateUser(mock_api)
        self.assertEqual(result, 1)  # 1 return value signifies that navigation was successful

    """
    description: this test case is testing navigate function when the time period is input correctly but the event
    option number selected is invalid i.e. input is not provided
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('builtins.input', side_effect=['2029'])
    # builtins.input is used to test functionality dependant on input from the user
    # side_effect[0]: Time Period Input by User
    # side_effect[1]: Event option number input by user
    def test_navigate_2nd_input_invalid_(self, mock_api):
        cal = Calendar()
        result = cal.navigateUser(mock_api)
        self.assertEqual(result, 1)  # 1 return value signifies that navigation was successful

    """
    description: this test case is testing navigate function when the time period is input correctly and is in the
    format YYYY-MM-DD but the event option number is not provided
    inputs: mock_api : it represents the the mock object of the google calendar API
    """

    @patch('builtins.input', side_effect=['2020-12-31'])
    # builtins.input is used to test functionality dependant on input from the user
    # side_effect[0]: Time Period Input by User
    # side_effect[1]: Event option number input by user
    def test_navigate_2nd_input_valid_fullYear(self, mock_api):
        cal = Calendar()
        result = cal.navigateUser(mock_api)
        self.assertEqual(result, 1)  # 1 return value signifies that navigation was successful


def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
