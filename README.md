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

Consider two step reservation:
1. page for entering datetime and number of people - calls check functions - if approved redirects to personal details
2. personal details form

FORM NOTES
Right now I cannot add the three hours to booking_start, as it is presented in a string form. 

Bugs to fix:
- It's possible to create reservations with identical content. However, this makes it impossible to open the details. Console displays: MultipleObjectsReturned at /reservations/lollol/
get() returned more than one Reservation -- it returned 2!
- Update booking doesn't work for some reason. Information is not updated. Gives following error: "POST /bookings/LavaBoy/update/ HTTP/1.1" 302 0

TIPS
To reset database: python manage.py migrate MyApp zero
