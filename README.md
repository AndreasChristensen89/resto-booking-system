command used for copying authentication templates to directory. Once copied we can make changes to the styling, and the content
cp -r ../.pip-modules/lib/python3.8/site-packages/allauth/templates/* ./templates

Due to error when creating user I was advised to implement the following in settings.py:
ACCOUNT_EMAIL_VERIFICATION = 'none'
![registration error](/static/images/readme-pictures/registration-error.png "error when registering a user")

28/10/2021 - for some reason Django logs user out when following link to reservation_detail.html.
Browser: Chrome
Console displays: "POST /accounts/logout/ HTTP/1.1" 302 0
User is logged back in when hitting the back button in browser
29/10/2021 - bug was fixed. Had to change the render function in ReservationDetail to include "user": User, instead of "user": User.username.

Installed Pillow for image upload

1/11/2021 - I can make reservations with no problems, but it does show an 302 error, similar with loggin in.
Console displays: "POST /reservations/reserve_table/ HTTP/1.1" 302 0

Implemented authetication check when canceling and updating reservations. The check is already done on the reservation list, but the url can be typed in as long as you know the username, which opens up the possibility for non-users to change the reservation.
-   no longer an issue. user.authentication added.

Add restaurant model to have the restaurant be able to set reservation interval - DONE

If a user double books (same user, and duration of booking overlaps) a validation error is not given. Table check is done but tables are not given which is because of the chance that a user may want to reserve a table for someone else in the same timeslot.

The following was added in settings.py to work with emails during development, should not be there when submitting:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

Check why Django admin in Heroku doesn't load css - DISABLE_COLLECTSTATIC on heroku vars

To add:
Check if user has first_name, otherwise ask them to fill in. This way we can cut first_name and last_name from booking and only use User info - ADDED

On booking_list add comment as pop-out to card.

Added extra script to base.html


TABLE SORT LOGIC - 

ANY TABLE:
Admin can change sorting method or turn it off completely in the BookingDetails model
1. Firstly, the function seeks to bring an exact match with table-size/number of people. 
    - If there are no exact matches it will look for table-size minus one
    - This is done to keep groups at the same table, and also to preserve other tables (smaller tables are valuable for dates/small families)
    - If there are no matches it will store the best option for 1 table
2. Follows to find best option (fewest seat losses) when combining any two tables
3. Follows to find best option (fewest seat losses) when combining any three tables
4. All options are then compared to each other to find best match
    - fewest tables are prioritised, meaning if losses are equal it will pick the option with the fewest tables
        - 1-table-option is only compared to 2-table-option. If a single table can fit a group, and with fewer or equal losses than a two-table option, then a 3-table option is not worth considering due to loss of smaller tables. As mentioned above, smaller tables are valuable and should be kept for smaller groups.
        - e.g. if available tables' sizes are [2, 2, 4, 10], a group of 8 will be given a table of 10, even though the total-seat loss of 2+2+4 == 0. If only the table for 10 is used, then three tables remain for a potential of more groups, compared to only a table of 10.
    - fewer losses are then prioritised
        - 2-table option and 3-table option are compared
5. If three tables are not sufficient then tables will be added one by one, largest to smallest.
    - If sum of seats exceeds number of guests then last table will not be added, and it, along with the following smaller tables, is checked for which one gives fewest losses.
    - Seeks to only add one table to preserve tables
6. Once tables are assigned Admin is still free to change tables in admin settings.
7. This logic assumes that the restaurant is able to move tables around

SAME ZONE TABLE


TESTING
Currently I have no other solution when testing than to comment out the current database, and then uncommenting the sqlite2 database in settings.py

Current bugs to fix:
- It's possible to create reservations with identical content. However, this makes it impossible to open the details. Console displays: MultipleObjectsReturned at /reservations/lollol/
get() returned more than one Reservation -- it returned 2!
- When updating the reservation the table function does't run again, so tables assigned stay the same even if number of people exceed capacity.
    - If a guests wish to increase number of people, the admin does not have access to availability-logic when assigning new tables
- When creating a reservation the updated_bookings page sets it to "not updated" because it's booked within the same minut. However, if a user updates the reservation, e.g. number of people, within that minute, it is still registered as "not updated".
    - If I change the setting to be within the same second, it's automatically added as "updated" since created_on and updated_on may be added in different seconds.
<!-- - Admin cannot book tables with specifying booking_end - prepopulated-fields to be tested
- bootstrap widget implementation from this site: https://pypi.org/project/django-bootstrap-datepicker-plus/
    - Not currently implemented, however, the following is installed: pip install django-bootstrap-datepicker-plus -->
- When logged in as user the pagination still thinks that all bookings are there, even though the user only has e.g. 1 booking, so it might show 3 pages to paginate
<!-- - Booking error: I knew 29/11 was booked at 17:00 - tried to see available times for 40 guests on that day - 14:30 is marked as an available time, which means they have the booking until 17:30, which is too long. -->
- Need to fix reset password form - seems to work now
- May not be bug, but no reservations cannot be made if admin has not set opening hours or booking interval
<!-- - Raise validationerror for outside opening hours doesn't show - I set crispy fields to only show certain fields thereby hiding messages -->
- Fix favicon
- Move profile url from reservations


Fixed bugs
- Update booking doesn't work for some reason. Information is not updated. Gives following error: "POST /bookings/LavaBoy/update/ HTTP/1.1" 302 0 - Was due to view function. The save() command was in the wrong order
- Cancel function on site doesn't work if there are multiple reservations with the same slug
    Added random string to every slug due to double slugs if first name + last name is the same as another reservation
- Right now I cannot add the three hours to booking_start "normally" using timedelta since the datetime input is presented in string form. Therefore, I added four steps to recreate a string with three hours added.
    booking_start now uses datetime format
- When 12:00 is booked, django writes 12 as "noon", and the function doesn't work because it expects an integer
    now uses datetime, and is no longer an issue
- When calculating available seats the system assumes that closing time is on an full-hour mark. Does not calculate properly if e.g. 20:30 is the closing time
    No longer uses this feature. User is shown validation error in form and uses datetime to calculate available tables
- Need to fix DeleteView and UpdateView to fit new app - turns out I needed to rename the folder where my templates were put in. It was still called "bookings", but is now called "reservations"
- Same user can make many bookings at the same datetime - implemented a check for booking.author in all bookings and test for booking_start. Needed to adjust for length of returns as it always returns one conflicting, which is the booking being made, which is due to double-save. Used print to see the variables along the way
- When running tests in booking.tests.py (python3 manage.py test bookings) it gives the following error:
Creating test database for alias 'default'...
/workspace/.pip-modules/lib/python3.8/site-packages/django/db/backends/postgresql/base.py:304: RuntimeWarning: Normally Django will use a connection to the 'postgres' database to avoid running initialization queries against the production database when it's not needed (for example, when running tests). Django was unable to create a connection to the 'postgres' database and will use the first PostgreSQL database instead.
  warnings.warn(
Got an error creating the test database: permission denied to create database - Need to comment out database in settings and remove commentout for sqlite3 database. Flip back when done testing

TIPS
To reset database: python manage.py migrate MyApp zero

I set use_tz to False in settings.py in order to avoid the timezone input from bookings.booking_start

Remember in reservations.bookings.generate_request_end() to set duration to:
duration = BookingDetails.objects.all()[0].booking_duration
For testing purposes it has been commented out and set to 180

Due to message on the 06-12-2021, Gitpod had new dependencies. Followed the instructions:
    - find -name "deps.txt" - no results, so meant that I had the older version
    - ran pip3 freeze > unins.txt && pip3 uninstall -y -r unins.txt && rm unins.txt
    - pip3 install django gunicorn
    - pip3 install dj_database_url psycopg2
    - pip3 install dj3-cloudinary-storage
    - pip3 install django-allauth
    - pip3 freeze --local > requirements.txt
    - saved, commited, and pushed
    - pip3 install Pillow
    - pip3 freeze --local > requirements.txt
From here onwards, whenever you (re)start your workspace, you need to do two things:
run 
- pip3 freeze > unins.txt && pip3 uninstall -y -r unins.txt && rm unins.txt - first, and then run:
- pip3 install -r requirements.txt - second

Picture credits from freepik

cta-menu:
<a href='https://www.freepik.com/photos/food'>Food photo created by valeria_aksakova - www.freepik.com</a>
cta-contact:
<a href='https://www.freepik.com/photos/space'>Space photo created by freepik - www.freepik.com</a>
cta-profile
<a href='https://www.freepik.com/photos/technology'>Technology photo created by rawpixel.com - www.freepik.com</a>
-updated cta-profile
<a href='https://www.freepik.com/vectors/people'>People vector created by studiogstock - www.freepik.com</a>
- updated cta-contact
<a href='https://www.freepik.com/photos/telephone'>Telephone photo created by freepik - www.freepik.com</a>

sign-up-cta:
<a href='https://www.freepik.com/photos/hand'>Hand photo created by rawpixel.com - www.freepik.com</a>