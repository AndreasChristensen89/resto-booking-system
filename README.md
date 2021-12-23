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
    * Navbar sticks to the top, using Bootstrap's "fixed-top" class. This does however cover the top part, so extra magins had to be created for headings.

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

* __Log-in page__:
    * Log in page has the same simple design as the sign-up page, just showing a heading "Log in". Underneath is a paragraph that shows a link to the login page in case the user has not already created an account. Underneath comes the form, which consists of two fields: "Username" and "Password", and then a blue "Sign in" button underneath, and right under is a check-box which the phrase"Remember Me" so the system will remember the user. Underneath the button is a link to reset the password in case the user has forgotten. All fields are mandatory and marked with an "*".
    ![Sign in page](/static/images/readme-pictures/landing-page-admin.webp)

* __Contact Information__:
    * The contact information page has the same design as the log-in and sign-up page. Underneath the heading is a paragraph that reads "Don't hesitate to send us a message if you have any questions, comments, or feedback. You can also reach us via the contact details down below". Below is the form for the user to send a message. There are three fields: "Name", "Email Address", and "Message". All fields are mandatory. Below is a blue send button.
    * Underneath is a section which holds two divs, one with the opening hours - these are generated from the OpeningHours model - and the other with the contact details of the establishment (made up). For mobile views these two divs are not side by side but stacked on top of each other.
    ![Contact Information page](/static/images/readme-pictures/landing-page-admin.webp)

* __Book Table page__:
    * The heading reads "Book Table" which is followed by two divs underneath, one with a form the other with the opening hours. They are side by side, but on mobile view the form is on top. The opening hours are there for convenience when making a booking. If the user has not updated their name details then the page will only display "Please fill in your name in the (link to profile section) before making a reservation".
    * The form has three fields: "Number of guests", "Date and Time" and "Comment". Only "comment" is not mandatory. Underneath the form is a blue button that says "Book". Should the a validation error be provoked in the form a pink message will appear on top of the form with the error message. When selecting the "Date and Time" field a DateTimePicker will be activated, which makes sure that the correct datetime format is inserted. In the "Number of guests" field the arrow keys, up and down, can also be used to increase the number.
    * This page will show a header "Please log in to make a reservation" if a user arrives, using the URL, without being logged in
    ![Book Table page](/static/images/readme-pictures/landing-page-admin.webp)

* __Upcoming bookings page__:
    * Header says "Upcoming Bookings". If the user is not logged in an error page will show. This view filters all the bookings that are tied to the user logged in, and uses the property is the Booking model "is_past_due" to check if the booking is in the future. Bookings are displayed on Bootstrap cards, and are colored according to their status. Status 0 is pending and will show as a blue card. Blue cards display "pending", "Reservation to be confirmed", date, and guests. Status 1 is accepted and will show as green, "confirmed", then all the tables connected to the booking, then date and guests. Status 2 is declined and will show as red, "Declined", then (if any) the comment tied to the booking, then the date and guests. Underneath each card are actions. If blue or green the user can "cancel" or "Edit comment". "Cancel" links to the DeleteView page, and Edit comment to the UpdateView page, which lets the user update only the comment. The red cards only have one action available which is a link to the book table page "Book another time".
    * On mobile view there is one booking per row, on small two, medium three, and largest as many as fits the width of the screen. It paginates on 6 items, so that is the maximum.
    ![Upcoming bookings page](/static/images/readme-pictures/landing-page-admin.webp)

* __Detele booking page__:
    * The header says "Delete booking". Underneath is a paragraph that says "Are you sure you want to delete the reservation?". Underneath are the details of the booking: Name, Date, Time, and guests. Underneath are two buttons: red button "Delete" and blue button "return". There is no like on the other pages which signifies that it is a serious action that is permanent. The design is narrow and does not change on mobile. If booking is closer than two hours away (booking property latest_cancellation) the page will display "Time limit exceeded. Cancellation is unfortunately no longer possible. Please get in contact with the restaurant if further information is needed"
    ![Delete booking page](/static/images/readme-pictures/landing-page-admin.webp)

* __Update comment page__:
    * Simple design. Header says "Update booking", underneath is a big comment field. Underneath is a blue button "Update". Next to the button is a link to return to the "Upcoming bookings" page "return".

* __Previous bookings page__:
    * Similar set up as "upcoming bookings" page. If the user is not logged in an error page will show. Setup of cards is the same as on the other site only filtering the false of is_due_date with the user. Also, there are no action buttons for the cards.
    ![Previous bookings page](/static/images/readme-pictures/landing-page-admin.webp)

* __Profile page__:
    * Simple design in line with the other sites using forms. Header says "Profile" and underneath is a form. The form has five fields: "Username", "First name", "Last name", "Email", and "Password". All except for password are mandatory. Underneath the form is a paragraph with a link to change the password. Underneath the form is a blue button "Save" which will update the details of the profile. Updating name details here will allow the user to make reservations.
    ![Profile page](/static/images/readme-pictures/landing-page-admin.webp)

* __Log out page__:
    * Very simple design in line with the other allauth pages. Header "Sign out". Underneath a paragraph "Are you sure you want to sign out?". Underneath a blue button "Sign Out".
    ![Log out page](/static/images/readme-pictures/landing-page-admin.webp)

* __Pending bookings page__:
    * Similar design as the "Upcoming bookings" page. If a non-superuser arrives then page will show "You need admin credentials to access this page". Pending reservations (status 0) are filtered to the admin. Admin can see on the booking if tables have been assigned. Underneath the bookings there are two choices: "Cancel" which will take admin to the "Cancel Booking" page, and "Approve/Decline" which takes admin to an extended version of UpdateView. Cards are similarly to the other pages also paginated by six.
    ![Pending bookings page](/static/images/readme-pictures/landing-page-admin.webp)

* __Approve/decline booking page__:
    * Heading reads "Approve or Decline Booking". Underneath are important asterix comments: "* If declining: Add a comment to the customer and remove tables." - this is a chance to explain to the client why the booking was declined. Also, if tables are not removed then they will stay as occupied for other reservations. This can still be changed on the admin site, but it's still good to remember to do it here. Secondly, "* To select/deselect tables, press and hold control/command key when adding/removing" - This is simply to explain how to manage the table-field, if needed.Underneath are two buttons: blue "Update" and under is a white "Return".
    * If status is set to approved and updated an email will be sent:
    Subject: Dre's Diner booking
    From: dresdiner@email.com
    To: {{user.email}}, dresdiner@email.com
    Date: Thu, 23 Dec 2021 20:24:23 -0000
    Message-ID: 
    <164029106357.53006.4891105094604906206@ws-a179a4a9-ce31-4837-8329-6d89e01dd653>

    Hello {{user.first_name}}, your booking is confirmed on {{booking.booking_start}}. Please note that cancellations must be made minimum two hours before. We look forward to seeing you.
    * If status is set to declined a different email will be sent:
    Subject: Dre's Diner booking
    From: dresdiner@email.com
    To: {{user.email}}, dresdiner@email.com
    Date: Thu, 23 Dec 2021 20:27:37 -0000
    Message-ID: 
    <164029125792.53006.11650285119791939862@ws-a179a4a9-ce31-4837-8329-6d89e01dd653>

    Hello {{user.first_name}}. Unfortunately, we are not able to accomodate your booking on {{booking.booking_start}}. For more information please see the comment left by the restaurant or contact us via our website.

    ![Pending bookings page](/static/images/readme-pictures/landing-page-admin.webp)
    ![Email sent approved](/static/images/readme-pictures/landing-page-admin.webp)
    ![Email sent declined](/static/images/readme-pictures/landing-page-admin.webp)
    ![Pending bookings page updated comment](/static/images/readme-pictures/landing-page-admin.webp)

* __Updated Bookings page__:
    * This page shows the admin the future bookings that have been updated in the comments. It filters updated on > created on, and also if there are any comments. The setup is the same as on the other bookings pages with the bookings on cards. Underneath each card the admin has two actions: "Cancel" and "See details". "Cancel" will take the admin to the "Cancel booking" page, and See details will take the admin to another Update booking page. Cards are paginated by 6 as in the other pages.
    ![Updated bookings page](/static/images/readme-pictures/landing-page-admin.webp)

* __Update booking admin page__:
    * This is essentially the same page as the approve/decline bookings, but has a different heading "Update booking". This extra page is created as bookings are likely accepted before they are updated, and another forms feels correct.
    ![Update bookings admin page](/static/images/readme-pictures/landing-page-admin.webp)

* __footer__:
    * Footer is dark grey with centered text. It reads "Made by Dre" Underneath are links to social media: Facebook, Youtube, Github, and Instagram. All links open in a new page. Links simply go to the main pages, except for Github which leads to my personal repository.

### Future features to implement

## Testing
### Django testing
All applications have been tested using TestCase. Forms, models, views, and additional functions have all been tested.
* TestCase
    * When testing the current database was not able to create testing databases, and I had to comment it out and un-comment the other database using sqlite3.
* Applications
    * Contact
        * Test_views - two tests, both pass. One for code 200 and one for email sent.
        * Test_forms - five tests, all pass. Test wrong input and required fields.
    * Homepage
        * Test_views - one test, passes. Tests for code 200.
    * Menu
        * Test_models - two tests, both pass. Test to create objects with both models, Meals and Category.
        * Test_views - one test, passes. Tests for code 200.
    * Reservations
    Every time I tested a booking I had to pass in a datetime object. On the page we pass in a string which is then converted to datetime, but this did not work for certain tests, particularly when testing the model.
        * Test_booking. 29 tests, all pass. Testing each function in reservations.bookings.py. Checking if functions use input from models properly. For many tests I created specific tables to have multiple options to return, checking if correct ones are returned with correct priority. Had to create opening hours, bookings details, users, and tables for most of the tests. For certain tests I started for loops to test function calls with increasing number of guests, and then running self.assert... for each iteration.
        * Test_views - 11 tests, all pass. Tested views for code 200 and correct template use. For many of them I had to create a user, at times a superuser, and log in. For the booking view I logged in and posted a correct form and then checked if a booking had been made.
        * Test_forms - 13 tests, all pass. Tested form for errors for wrong input, all fields should be there, which ones are required, minus values, wrong types, not enough tables, enough tables but one with certain method, opening hours, past booking
        * Test_models - 7 tests, all pass. Tested if object could be made, if default fields are automatically set, if slugs are generated and unique, if model properties work (booking latest_cancellation and is_due_date).
    * Restaurant
        * Test_models - 3 tests, all pass. Test if objects can be created and if default values work.

### Browser Testing

### Media Queries
Media queries have been done using bootstrap's class system.
Chrome Developer Tools was used for testing all media queries.

- Test on Firefox, no problems detected.
- Microsoft Edge, no problems detected.
- Media query tested on my own phone, Samsung Galaxy S9 using Chrome and Firefox, no issues.
- Media query tested on my own tablet, Ipad pro 2018 11" using Safari+Chrome, no issues.
- General testing with my own laptop, Asus 13 inch using Chrome, no issues.
- All links were tested. All external links and internal links work.

### Bugs discovered during testing:
* Update booking doesn't work for some reason. Information is not updated. Gives following error: "POST /bookings/LavaBoy/update/ HTTP/1.1" 302 0 - Was due to view function. 
    * The save() command was in the wrong order
* Cancel function on site doesn't work if there are multiple reservations with the same slug
    * Added random string to every slug due to double slugs if first name + last name is the same as another reservation
* I couldn't add the three hours to booking_start "normally" using timedelta since the datetime input is presented in string form. Therefore, I added four steps to recreate a string with three hours added. 
    * booking_start now uses datetime format and works
* When 12:00 is booked, django writes 12 as "noon", and the function doesn't work because it expects an integer
    * Now uses datetime, is only an issue with strings
* When calculating available seats the system assumes that closing time is on an full-hour mark. Does not calculate properly if e.g. 20:30 is the closing time.
    * No longer uses this feature of showing available times. User is shown validation error in form and uses datetime to calculate available tables
* Need to fix DeleteView and UpdateView to fit new app
    * Turns out I needed to rename the folder where my templates were put in. It was still called "bookings", but is now called "reservations"
* Same user can make many bookings at the same datetime
    * Implemented a check for booking.author in all bookings and test for booking_start. Needed to adjust for length of returns as it always returns one conflicting, which is the booking being made, which is due to double-save.
* Got an error creating the test database: permission denied to create database
    * Need to comment out database in settings and remove commentout for sqlite3 database. Flip back when done testing
* When logged in as user the pagination still thinks that all bookings are there, even though the user only has e.g. 1 booking, so it might show 3 pages to paginate
    * Queryset fixed and now only returns the booking for specific user
* It's possible to create reservations with identical content. However, this makes it impossible to open the details. Console displays: MultipleObjectsReturned at /reservations/xxxxx/ 
    * Slug auto-generated, and there are checks for double booking by same user. First_name and last_name are no longer used, so details from the user is inserted. User must put in details before bookings can be made.
* Django logs user out when following link to reservation_detail.html. User is logged back in when hitting the back button in browser
    * Had to change the render function in ReservationDetail to include "user": User, instead of "user": User.username.
* Implemented authetication check when canceling and updating reservations. The check is already done on the reservation list, but the url can be typed in as long as you know the username, which opens up the possibility for non-users to change the reservation.
    * No longer an issue. user authentication added and random slug.
* Raise validationerror for outside opening hours doesn't show 
    * Fixed - I set crispy fields to only show certain fields thereby hiding messages

### Unfixed Bugs:
* I wanted to have a feature which generated buttons with available times for the date that users put in. I was able to generate the buttons, but not to have them work with a form. This will go in "future implementations"
* Forms are not completely centered, but stick to the left side of the centered box.

### Validator Testing
pep8
- W3 Markup Validation Service completed for all HTML pages with no errors.
- Jigsaw test CSS file completed with no errors.

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

### Icons
Icons and script were taken from https://fontawesome.com/, as well as Google's fonts: https://fonts.google.com/icons?selected=Material+Icons.

### Hosting and Developemtn
GitHub was used to host the repository, GitPot was used for development and version control, and Heroku was used to deploy site.

## Credits
### Pictures
Images were compressed using the webpage https://tinypng.com/ Afterwards they were converted to webp using https://cloudconvert.com/png-to-webp.

Picture credits from freepik

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

### Text content
Content was all formulated by myself, but for the menu I took inspiration from various websites with food, descriptions etc.


### Coding help
- For help with varius issues Django, css etc. I often resorted to https://stackoverflow.com/
- For help with syntax reminders I often used https://www.w3schools.com/, as well as various pages giving advice on Django
- For general best practice I used Code Institute's Slack community.
- For CSS I used Bootstrap Docs a lot.
- General comments from family and peers for what CSS looked the best.
- I looked up other booking system to get inspiration for how it could be set up.

### Design
- For design of the different pages I didn't use other sources of information other than my previous projects.
- No wireframes were used

## User stories
For user stories I used Github's Projects -> User Stories. Kanban board. I created 18 stories and implemented them one by one. Some others were deleted, and some were changed along the way. The ones that are there now are:
- Accept/decline reservation: As a site admin I can approve or reject reservations so that the customer knows if they have a reservation or not
- Choose table assignment method: As an admin I can select a table assignment method so that I can adapt the method to the restaurant setup
- Check opening hours: As a site user I can know if my booking request is within opening hours so that my booking is not falsely accepted
- Avoid double booking: As a site user I can see if no tables are available on the desired datetime so that no double bookings occurs
- Automatic table assignment: As a site user I can have tables automatically assigned to my reservation so that no space is wasted
- Edit reservation: As a site user I can edit the details of my reservation so that the restaurant knows about desired changes
- Log in as user: As a site user I can log in so that I can make reservations
- Book multiple tables: As a site user I can combine tables for a reservation so that a larger party than the table can be accommodated
- Cancel reservation: As a site user I can cancel a reservation so that the restaurant knows of the update
- See list of specific User reservations: As a site user I can see a list of my reservations so that I have an overview of my bookings
- Add special requirements: As a site user I can add notes to my reservation so that the restaurants knows of any needs to accommodate the guests
- See menu: As a site user I can see the menu items so that I can decide whether or not to make a reservation
- See list of reservations: As a site admin I can see the complete list of reservations so that I have an overview of business activity
- Change request status: As a site admin I can change the accepted/declined status of a reservation so that I can fix reply-errors
- See details of reservation: As a site admin I can open a reservation so that see all details of the reservation
- Make reservation: As a site user I can make a reservation so that the restaurant is notified about my request
- Site pagination: As a site user I can view a paginated list of reservations so that I can select which reservation to view
- Send messages to clients: As a site admin I can send messages so that **the customers know reasoning behind e.g. cancellations.

## Strategy
The purpose of this site is to create a simple site for a restaurant that handles reservations. The site should be simple to use, and information should be easy to find with simple and clear design

## Scope
The scope is limtited in functionality, but does implement logic to assign tables with reasonable complexity. It could for sure be more complex and specific. Options for handling bookings are limited but should be completely functional.

## Structure
The flow of the website is simple and should be intuitive for most people. Navbar has everything the user needs to find their way around. In case there is confusion about how the setup works there is a clear path to contact the restaurant both with messages, phones and their address. On the landing page users are shown the call to action divs that encourage them to register.

## Surface

### Design Choices
- Overview: The aim is to provide easy-to-navigate pages that make it easy and clear to navigate around.
- The site should be easy for the eyes, meaning that there should be no overlapping animations that confuse users.
- It should be clear to the user what can be clicked on.
- Information should not be detailed but fast to read and understand, and straight to the point.

### Color Scheme
Dark colors are chosen to give a serious professional vibe. On all pages there is a play between black and white. Black background and white text. Blue is generally used to signal progress and/or pending. Green is used to signal confirmation. Red is used to signal cancellation or declined. The black background resembles dark rocks and gives, in my opinion, a nice constrast with the white text.

### Choice of text

### Pictures/characters

### Languages Used
- HTML
- CSS
- Python
- JavaScript
- Markdown language for readme file

### Accessibility
All non-text elements are marked with aria-labels, and the contrast between background and foreground colors were implemented in color scheme.

## Admin setup
Admin credentials (superuser)
username: admin
password: themagickey

In order for booking logic to work admin must set up the following (This is already set on deployment, but can be changed):
* Under Restaurant:
    - In BookingDetails add one object:
        * Specify Booking Duration - how many minutes each party will occupy the tables
        * Specify Table assign method - how or if the system should assign tables
        * Specify Method Limit - automatically set to 100. This is to set a max-limit of guests to the assign table function. e.g. function will not trigger if number of guests are higher than limit
    * In Opening Hours an object for each day must be added, Monday to Sunday:
        * Specify Weekday, opening time, and closing time

In order for menu to be displayed Admin must add items (This is already set on deployment, but can be changed):
* Under Menu:
    * In Categories add desired number of categories
    * In Meals add objects for each desired category:
        * Specify name, description, price, and for how many people
        * Image must be included
        * Meal must be linked to a category
        * Slug is automatically added

## Setup explanation
* I added a restaurant model to have the restaurant be able to set specific requirements for bookings. Opening hours, booking duration
* Installed Pillow for image upload.
* If a user double books (same user, and duration of booking overlaps) a validation error is not given. Table check is done but tables are not assigned to new booking which is because of the chance that a user may want to use his profile to reserve a table for someone else in the same timeslot. The system sends out an email to the user to notify of the double booking and no tables assigned. The user is then invited to contact the restaurant or delete the double bookings.
* Added property to booking to see if it's in past or not, and also if it's too late to cancel reservation. I set it to two hours, which I believe is reasonable. In case the guests need to cancel anyway they have to call the restaurant.
* I set use_tz to False in settings.py in order to avoid the timezone input from bookings.booking_start
* In order to add the ManyToManyField in the Booking model I had to save the booking first in the view and then afterwards attach the tables, and finally save again. This caused a lot of trouble but it works now.


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


## Additional comments on setup
* In first I included first_name and last_name in the Booking model, but it seemed extensive, especially when a user was already created. Instead, I found it better to require to add contact details before making a booking. This way the same user can easily book again, and the details are taken from the user. The first_name and last_name could be cut from the booking, thus making it more appropriate to book using only a datetime and guests number.
* On booking_list add comment as pop-out to card. - If declined it is there on the card
* Height of body is set to 100 to fill the screen


command used for copying authentication templates to directory. Once copied we can make changes to the styling, and the content
cp -r ../.pip-modules/lib/python3.8/site-packages/allauth/templates/* ./templates

Due to error when creating user I was advised to implement the following in settings.py:
ACCOUNT_EMAIL_VERIFICATION = 'none'
![registration error](/static/images/readme-pictures/registration-error.png "error when registering a user")

## Additional mentions:
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

The following was added in settings.py to work with emails during development, should not be there when submitting:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


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
- Sort out CSS

pip3 freeze > unins.txt && pip3 uninstall -y -r unins.txt && rm unins.txt
pip3 install -r requirements.txt - second