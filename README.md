# Resto-Book

The idea behind this project is to create a site for a restaurant that can manage reservations.
On deployment all the restaurant details, including contact details, openings hours, booking details, meals, and categories have already been set up, however this can be edited as the admin wants thus making the design useable for other restaurants.
The content is auto generated on the pages, and the admin can set up their preferred criterias.

The design choice is dark which I find suitable for restaurants that prefer a clean and simple look.

## Features

### Existing Features:
* __Navigation Bar__
    * The navigation bar is found on all pages. It is dark grey with white text and changes according to if the user is logged in, and also whether the user is a superuser or not. The design is Bootstrap's own design (https://getbootstrap.com/docs/4.3/components/navbar/), which I have set to collapse when reaching mobile displays.
        * For non-users there are five links: "Home", "Menu", "Sign-up", "Login", and "Contact Information"
        ![Nav Bar - logged out](/static/images/readme-pictures/navigation-bar-logged-out.webp)
        * For users there are more options: "Home", "Menu", a drop-down box "Booking" with three links ("New Booking", "Upcoming Bookings", "Previous Bookings"), "Profile", "logout", and "Contact Information"
        ![Nav Bar - user](/static/images/readme-pictures/navigation-bar-user.webp)
        * For superusers there are different options: "Home", "Menu", drop-down box "Admin Actions" with three links ("Pending Bookings", "Updated Bookings", "Book Table"), "Admin Profile", "Logout", and "Contact Information"
        ![Nav Bar - superuser](/static/images/readme-pictures/navigation-bar-superuser.webp)
        * All user have the webpage icon that leads to the landing page

* __Landing page__:
    * The landing page has a dark-themed hero-image of fresh ingredients. There is a welcome message being generated according to who is logged in, and the details of the user. If the user is not logged in it will display the standard welcome message. If logged in, but with no name details added in profile, it will greet the user by username underneath the welcome message. If name details are provided it will use the provided first name in the greeting. The greeting appears into view after a second and a half, changing opacity from 0 to 100.

    ![Landing page - logged out](/static/images/readme-pictures/landing-page-logged-out.webp)
    ![Landing page - username](/static/images/readme-pictures/landing-page-user.webp)
    ![Landing page - user's name](/static/images/readme-pictures/landing-page-admin.webp)
    
    * Under the hero image are call-to-action divs. These also change when logged in/out.
        * If not logged in there are two divs with dark-yellow icons that link to the sign-up page and the login page. These are the call-to-actions as users must be logged in in order to make bookings. They move 10px upwards when hovering over them, thus giving an interactive feeling. For mobile view the two divs stack on top of each other.
        * If logged in there are three divs side by side with background pictures instead of icons: "contact", with a background picture of a phone linking to the contact-us page, "Menu", with a background picture of a menu slate and ingredients, linking to the menu-page, and "Profile", with a picture of faceless people, linking to the profile-page". All these divs also move 10px upwards when hovering over them. For mobile view the divs stack on top of each other.
    
    ![Landing page - cta's logged out](/static/images/readme-pictures/landing-page-admin.webp)
    ![Landing page - cta's logged in](/static/images/readme-pictures/landing-page-admin.webp)

* __Menu page__:
    * The menu page follows the dark theme and shows different fresh ingredients on a black surface. After a second a message comes into view, going form 0 opacity to 100 that says "Eat healthy and feel good". This page is the same regardless of user.
    ![Menu page - top](/static/images/readme-pictures/landing-page-admin.webp)
    * Underneath the main picture is an introductory message that reads "All our food is made from fresh and organic ingredients. Everything served has been put through a rigorous process to ensure optimal quality, health, and flavor."
    ![Menu page - message](/static/images/readme-pictures/landing-page-admin.webp)
    * Underneath the site auto generates the categories added by the admin, followed by all the meals connected to this category.
    The category is on a line of it's own, and underneath the pictures of the meals are displayed along with title, price, and description. Corners of the pictures are slighty rounded. On mobile view two meals are shown next to each other. On 576px three, which are then enlarged on 768px, and finally allowing four items side by side on 992px and above. All text is white, but price is slighty dimmed.
    ![Menu page - categories and meals](/static/images/readme-pictures/landing-page-admin.webp)

* __Sign-up page__:
    * Sign up page has a simple design, just showing a heading "Sign Up". Underneath is a paragraph that shows a link to the login page in case the user already has an account. Underneath comes the form, which consists of four fields: "Username", "E-mail", "Password", "Password(again)", and then a blue "Sign Up" button underneath. All fields except for E-mail are mandatory and marked with an "*".
    ![Sign up page](/static/images/readme-pictures/landing-page-admin.webp)


### Future features to implement

## Testing
### Django testing
* TestCase
* Applications
    * Contact
        * Test_views
        * Test_forms
    * Menu
        * Test_models
        * Test_views
    * Reservations
        * Test_booking
        * Test_views
        * Test_forms
        * Test_models
    * Restaurant
        * Test_models

### Browser Testing

### Media Queries

### Bugs discovered during testing:

### Unfixed Bugs:

### Validator Testing

## Deployment
### Deployment to Heroku


### Create a local clone
1.	Open GitHub and navigate to repository here (https://github.com/AndreasChristensen89/resto-booking-system).
2.	Click the Code drop-down menu.
3.	Options:
•	Download the ZIP file, unpack locally and open with IDE.
•	Copy git URL from HTTPS dialogue box.
4.	Open your chosen IDE and open the terminal in a directory.
5.	Use the "git clone" command with the copied git URL after.
6.	Clone of the project is created locally on your machine.


# Technologies Used

### Hosting and Developemtn

## Credits
### Pictures


### Text content


### Coding help


### Design


## User stories




command used for copying authentication templates to directory. Once copied we can make changes to the styling, and the content
cp -r ../.pip-modules/lib/python3.8/site-packages/allauth/templates/* ./templates

Due to error when creating user I was advised to implement the following in settings.py:
ACCOUNT_EMAIL_VERIFICATION = 'none'
![registration error](/static/images/readme-pictures/registration-error.png "error when registering a user")

ADMIN NOTES
Admin credentials (superuser)
username: admin
password: themagickey



In order for booking logic to work admin must set up the following (This is already set on deployment, but can be changed):
- Under Restaurant:
    - In BookingDetails add one object:
        - Specify Booking Duration - how many minutes each party will occupy the tables
        - Specify Table assign method - how or if the system should assign tables
        - Specify Method Limit - automatically set to 100. This is to set a max-limit of guests to the assign table function. e.g. function will not trigger if number of guests are higher than limit
    - In Opening Hours an object for each day must be added, Monday to Sunday:
        - Specify Weekday, opening time, and closing time

In order for menu to be displayed Admin must add items (This is already set on deployment, but can be changed):
- Under Menu:
    - In Categories add desired number of categories
    - In Meals add objects for each desired category:
        - Specify name, description, price, and for how many people
        - Image must be included
        - Meal must be linked to a category
        - Slug is automatically added



Installed Pillow for image upload

If a user double books (same user, and duration of booking overlaps) a validation error is not given. Table check is done but tables are not given which is because of the chance that a user may want to use his profile to reserve a table for someone else in the same timeslot.

Add restaurant model to have the restaurant be able to set reservation interval - DONE

The following was added in settings.py to work with emails during development, should not be there when submitting:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

To add:
Check if user has first_name, otherwise ask them to fill in. This way we can cut first_name and last_name from booking and only use User info - ADDED

On booking_list add comment as pop-out to card. - If declined it is there on the card

Added extra script to base.html

Added property to booking to see if it's in past or not


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
Add Logic here

TESTING
Currently I have no other solution when testing than to comment out the current database, and then uncommenting the sqlite2 database in settings.py

Current bugs to fix:
- When updating the reservation the table function does't run again, so tables assigned stay the same even if number of people exceed capacity.
    - If a guests wish to increase number of people, the admin does not have access to availability-logic when assigning new tables
    - If I change the setting to be within the same second, it's automatically added as "updated" since created_on and updated_on may be added in different seconds.
- Move profile url from reservations?
- Check conflicting user booking - testing
- Updating a booking removes the tables - see if can implement logic in updateview - does it? Can't replicate
- Fix message for opening hours to reflect latest reservation time - DONE
- Add alt text to pictures
- Add attributions to pictures
- Should I keep the moveable tables?
- Fix test for model, string + datetime shit
- Grey for pending?


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
- Got an error creating the test database: permission denied to create database - Need to comment out database in settings and remove commentout for sqlite3 database. Flip back when done testing
- Send email with reservation approved - DONE
- Implement deadline to cancel the booking - 5-6 hours - add warning in email, DONE
- When logged in as user the pagination still thinks that all bookings are there, even though the user only has e.g. 1 booking, so it might show 3 pages to paginate - queryset fixed
- It's possible to create reservations with identical content. However, this makes it impossible to open the details. Console displays: MultipleObjectsReturned at /reservations/lollol/ - slug auto-generated, and there are checks for double booking by same user. First_name and last_name are no longer used, so details from the user is inserted. User must put in details before bookings can be made.
- Booking error: I knew 29/11 was booked at 17:00 - tried to see available times for 40 guests on that day - 14:30 is marked as an available time, which means they have the booking until 17:30, which is too long. - No longer generates buttons for available times
- 28/10/2021 - for some reason Django logs user out when following link to reservation_detail.html.
Browser: Chrome
Console displays: "POST /accounts/logout/ HTTP/1.1" 302 0
User is logged back in when hitting the back button in browser
29/10/2021 - bug was fixed. Had to change the render function in ReservationDetail to include "user": User, instead of "user": User.username.
- 1/11/2021 - I can make reservations with no problems, but it does show an 302 error, similar with loggin in.
Console displays: "POST /reservations/reserve_table/ HTTP/1.1" 302 0 - Not a bug
- Implemented authetication check when canceling and updating reservations. The check is already done on the reservation list, but the url can be typed in as long as you know the username, which opens up the possibility for non-users to change the reservation. - no longer an issue. user authentication added.
- Check why Django admin in Heroku doesn't load css - DISABLE_COLLECTSTATIC on heroku vars - and debug = True in setting.py
- Raise validationerror for outside opening hours doesn't show - Fixed - I set crispy fields to only show certain fields thereby hiding messages

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

Compressing used by tinypng.com

cta-menu:
<a href='https://www.freepik.com/photos/food'>Food photo created by valeria_aksakova - www.freepik.com</a>
new menu - no attribution required, so just posting the link:
https://pixabay.com/photos/menu-pizza-pasta-vegetables-meal-3206749/
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

pain au chocolat:
<a href='https://www.freepik.com/photos/restaurant'>Restaurant photo created by azerbaijan_stockers - www.freepik.com</a>

porridge:
<a href='https://www.freepik.com/photos/nature'>Nature photo created by jcomp - www.freepik.com</a>

breakfast eggs:
<a href='https://www.freepik.com/photos/food'>Food photo created by jcomp - www.freepik.com</a>

cereals:
<a href='https://www.freepik.com/photos/food'>Food photo created by Racool_studio - www.freepik.com</a>