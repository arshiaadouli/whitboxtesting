Test Strategy for testing Calendar.py

The test cases were selected by functionanlities/user stories
This was done to create different 'units' of the program to test seperately. 
Unit testing made debugging more efficient by isolating these units. 
To test the system as a whole, continous integration testing was used.
This was done to ensure that the units interacted with each other as required.

Testing Units (by functionality/user stories) - 

1. As a user, I can see events and reminders for at least 5 years in past from the today’s
date

Since the requirements specifically state that the user can see events from
5 years in the past to present, we have to check if the program behaves
as expected on the boundaries. Hence, the boundary testing approach was opted.

This functionality was divided into 4 test cases - 

    1. No events exist
    Events exist - 
        2. If events exist before start time (i.e before 5 years), they shouldn't come up
        3. If events are after end time (i.e present) they shouldn't come up
        4. If the event between start time and end time they should come up

2. As a user, I can see events and reminders for at least next two years (in future)

Since the requirements specifically state that the user can see events from
present to 2 years in the future, we have to check if the program behaves
as expected on the boundaries. Hence, the boundary testing approach was opted.

This functionality was divided into 4 test cases - 

    1. No events exist
    Events exist - 
        2. If events exist before start time (i.e now), they shouldn't come up
        3. If events are after end time (i.e after 2 years) they shouldn't come up
        4. If the event between start time and end time they should come up

3. As a user, I can navigate through different days, months, and years in the calendar so
that I can view the details of events. For example, if the year 2019 is selected, all events
and reminders(and any other information associated to the event) will be shown. This
means on selecting the specific event or reminder I can see the detailed information.

Category Partitioning
This functionality was divided by 2 inputs needed by the program
And was categorised into a total of 13 test cases. 

To test first input of getting time period from user - 

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

To test second input of getting required event from user -

    This was categorised into 3 test cases.
    
    1. When there are no events to show
    2. Invalid Input
    3. Valid Input

This was done to handle all types of input combinations. 

4. As a user, I can search events and reminders using different key words.

This functionality was categorised into 2 test cases - 

    1. Event found
    2. Event not found
    
This was done because testing for invalid/valid arguments seperately wasn't
required since if an invalid argument was provided, the event would fall under
the 'not found' category. And if a valid argument was provided, it would fall 
under the 'found' category.


5. As a user, I can delete events and reminders

The factor which is important in deleting events and reminders is
that the number of events in the selected range can either be zero or more. 
Therefore, we categoriesed the test accroding to the 3 types
of input which will have different results.


This functionality was categorised into 3 test cases -

    1. Valid event
    2. Invalid event: Negative Index
    3. Event is out of range
