import sys
import unittest
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

    # # Add more test cases here
    # @patch('Calendar.open')
    # def test1(self, mock_api):
    #     num_events = 2
    #     time = "2020-08-03T00:00:00.000000Z"
    #
    #     calendar = Calendar()
    #     events = calendar.get_five_year_event_past(mock_api)
    #     events = calendar.get_two_year_event_future(mock_api)
    #     events = calendar.get_upcoming_events(mock_api, time, num_events)
    #     self.assertEqual(
    #         mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 3
    #     )
    #     print(mock_api.events.return_value.list.call_args_list[0])
    #     print(mock_api.events.return_value.list.call_args_list[1])
    #     print(mock_api.events.return_value.list.call_args_list[2])











def main():

    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()