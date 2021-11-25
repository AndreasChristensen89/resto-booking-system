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

1/11/2021 - I can make reservations with no problems, but it does show an 302 error, similar with loggin in.
Console displays: "POST /reservations/reserve_table/ HTTP/1.1" 302 0

Implemented authetication check when canceling and updating reservations. The check is already done on the reservation list, but the url can be typed in as long as you know the username, which opens up the possibility for non-users to change the reservation.
-   no longer an issue. user.authentication added.

Add restaurant model to have the restaurant be able to set reservation interval

Consider two step reservation:
1. page for entering datetime and number of people - calls check functions - if approved redirects to personal details
2. personal details form

TABLE SORT LOGIC:
1. Firstly, the function seeks to bring an exact match with table-size/number of people.
2. If there are no exact matches it will look for table-size minus one
    - This is done to keep groups at the same table, and also to preserve other tables (smaller tables are valuable for dates/small families)
3. If there are no matches it will store the best option for 1 table
4. Follows to find best option (fewest seat losses) when combining any two tables
5. Follows to find best option (fewest seat losses) when combining any three tables
6. All options are then compared to each other to find best match
    - fewest tables are prioritised, meaning if losses are equal it will pick the option with the fewest tables
        - 1-table-option is only compared to 2-table-option. If a single table can fit a group, and with fewer or equal losses than a two-table option, then a 3-table option is not worth considering due to loss of smaller tables. As mentioned above, smaller tables are valuable and should be kept for smaller groups.
        - e.g. if available tables' sizes are [2, 2, 4, 10], a group of 8 will be given a table of 10, even though the total-seat loss of 2+2+4 == 0. If only the table for 10 is used, then three tables remain for a potential of more groups, compared to only a table of 10.
    - fewer losses are then prioritised
        - 2-table option and 3-table option are compared
7. This is the basic logic, and admin can change which tables are given at any point.

FORM NOTES
Right now I cannot add the three hours to booking_start "normally" using timedelta since the datetime input is presented in string form. Therefore, I added four steps to recreate a string with three hours added.

Bugs to fix:
- It's possible to create reservations with identical content. However, this makes it impossible to open the details. Console displays: MultipleObjectsReturned at /reservations/lollol/
get() returned more than one Reservation -- it returned 2!
- When updating the reservation the table function does't run again, so tables assigned stay the same even if number of people exceed capacity.
    - If a guests wish to increase number of people, the admin does not have access to availability-logic when assigning new tables
- When creating a reservation the updated_bookings page sets it to "not updated" because it's booked within the same minut. However, if a user updates the reservation, e.g. number of people, within that minute, it is still registered as "not updated".
    - If I change the setting to be within the same second, it's automatically added as "updated" since created_on and updated_on may be added in different seconds.
- Admin cannot book tables with specifying booking_end - prepopulated-fields to be tested
- When 12:00 is booked, django writes 12 as "noon", and the function doesn't work because it expects an integer
- bootstrap widget implementation from this site: https://pypi.org/project/django-bootstrap-datepicker-plus/
    - Not currently implemented, however, the following is installed: pip install django-bootstrap-datepicker-plus
- When logged in as user the pagination still thinks that all bookings are there, even though the user only has e.g. 1 booking, so it might show 3 pages to paginate
- When calculating available seats the system assumes that closing time is on an full-hour mark. Does not calculate properly if e.g. 20:30 is the closing time
- Booking error: I knew 29/11 was booked at 17:00 - tried to see available times for 40 guests on that day - 14:30 is marked as an available time, which means they have the booking until 17:30, which is too long.
- Cancel function on site doesn't work if there are multiple reservations with the same slug


Fixed bugs
- Update booking doesn't work for some reason. Information is not updated. Gives following error: "POST /bookings/LavaBoy/update/ HTTP/1.1" 302 0 - Was due to view function. The save() command was in the wrong order

TIPS
To reset database: python manage.py migrate MyApp zero

I set use_tz to False in settings.py in order to avoid the timezone input from bookings.booking_start
