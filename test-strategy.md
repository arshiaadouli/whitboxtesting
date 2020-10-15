Test Strategy for testing Calendar.py

The test cases were selected by functionanlities/user stories
This was done to create different 'units' of the program to test seperately. 
Unit testing made debugging more efficient by isolating these units. 
To test the system as a whole, continous integration testing was used.
This was done to ensure that the units interacted with each other as required.

Testing Units (by functionality/user stories) - 

1. As a user, I can see events and reminders for at least 5 years in past from the today’s
date



2. As a user, I can see events and reminders for at least next two years (in future)


3. As a user, I can navigate through different days, months, and years in the calendar so
that I can view the details of events. For example, if the year 2019 is selected, all events
and reminders(and any other information associated to the event) will be shown. This
means on selecting the specific event or reminder I can see the detailed information.

This was categorised into 10 test cases.
    For valid inputs in 3 formats where events exit for that time period-
        1. YYYY
        2. YYYY-MM
        3. YYYY-MM-DD
    For valid inputs in 3 formats where events do not exit for that time period-
        4. YYYY
        5. YYYY-MM
        6. YYYY-MM-DD
    For invalid inputs in 3 formats -
        7. YYYY
        8. YYYY-MM
        9. YYYY-MM-DD
    10. Empty input string



4. As a user, I can search events and reminders using different key words.


5. As a user, I can delete events and reminders
