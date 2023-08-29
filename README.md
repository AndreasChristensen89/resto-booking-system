# Resto-Booking

The idea behind this project is to create a site for a restaurant that can manage reservations.
On deployment all the restaurant details, including contact details, openings hours, booking details, meals, and categories have already been set up, however this can be edited as the admin wants thus making the content changeable.
Much of the content is auto generated on the pages, and the admin can set up their preferred criteria.

The development rationale for this project is to create an application that meets a real-life need, which is the need for restaurant owners to digitalise the process of taking orders, sorting tables, and avoiding double bookings. Much of it should be automatic, including emails.


# Table of contents
- [Resto-Book](#resto-book)
- [Table of contents](#table-of-contents)
- [Features](#features)
  * [Existing Features:](#existing-features-)
  * [Future features to implement](#future-features-to-implement)
- [Testing](#testing)
  * [Django testing](#django-testing)
  * [Browser Testing](#browser-testing)
  * [Media Queries](#media-queries)
  * [Bugs discovered during testing:](#bugs-discovered-during-testing-)
  * [Unfixed Bugs:](#unfixed-bugs-)
  * [Validator Testing](#validator-testing)
- [Starting Django project](#starting-django-project)
  * [Deployment](#deployment)
    + [Heroku](#heroku)
    + [Cloudinary](#cloudinary)
    + [Last settings](#last-settings)
  * [Create a local clone](#create-a-local-clone)
- [Technologies Used](#technologies-used)
  * [Icons](#icons)
  * [Datetime Picker](#datetime-picker)
- [Hosting and Development](#hosting-and-development)
- [Credits](#credits)
  * [Pictures](#pictures)
  * [Text content](#text-content)
  * [Coding help](#coding-help)
  * [Design](#design)
- [User stories](#user-stories)
- [UX](#ux)
  * [User acceptance criteria](#user-acceptance-criteria)
  * [Strategy](#strategy)
  * [Scope](#scope)
  * [Structure](#structure)
  * [Surface](#surface)
    + [Design Choices](#design-choices)
    + [Color Scheme](#color-scheme)
    + [Choice of text](#choice-of-text)
    + [Pictures](#pictures-1)
    + [Accessibility](#accessibility)
- [Languages Used](#languages-used)
- [CRUD](#crud)
  * [Create](#create)
  * [Reading](#reading)
  * [Updating](#updating)
  * [Deteion](#deteion)
- [Email](#email)
- [Admin Access](#admin-access)
  * [Must have settings](#must-have-settings)
  * [Setup explanation](#setup-explanation)
- [Booking Logic](#booking-logic)
  * [Table sorting methods](#table-sorting-methods)
    + [Any tables](#any-tables)
    + [Same zone tables](#same-zone-tables)
    + [Limitations of table sort logic](#limitations-of-table-sort-logic)
- [Django](#django)
  * [Django Apps](#django-apps)
  * [Django models](#django-models)
  * [Django forms](#django-forms)
  * [Additional mentions:](#additional-mentions-)


# Features

## Existing Features:
* Note:
All pages have been tested to work down until width 280px, which is the smallest device on Google Chrome Devtools.

* __Navigation Bar__
    * The navigation bar is found on all pages. It is dark grey with white text and changes according to if the user is logged in, and also whether the user is a superuser or not. The design is Bootstrap's own design (https://getbootstrap.com/docs/4.3/components/navbar/), which I have set to collapse when reaching mobile displays.
        * For non-users there are five links: "Home", "Menu", "Contact Information", "Sign-up", and "Login"
            * ![Nav Bar - logged out large](/static/images/readme-pictures/navbar-logged-out-large.JPG)
            * ![Nav Bar - collapsed mobile](/static/images/readme-pictures/navbar-mobile-collapsed.JPG)
            * ![Nav Bar - logged out mobile](/static/images/readme-pictures/navbar-mobile-open-logged-out.JPG)
        * For users there are more options: "Home", "Menu", a drop-down box "Booking" with three links ("New Booking", "Upcoming Bookings", "Previous Bookings"), "Profile", "Contact Information", and "logout" 
            * ![Nav Bar - user](/static/images/readme-pictures/navbar-logged-in-medium.JPG)
            * ![Nav Bar - user dropdown box](/static/images/readme-pictures/navbar-logged-in-dropbox-medium.JPG)
            * ![Nav Bar - user mobile](/static/images/readme-pictures/navbar-mobile-open-user-login.JPG)
            * ![Nav Bar - user dropdown box mobile](/static/images/readme-pictures/navbar-mobile-open-user-login-dropbox.JPG)
        * For superusers there are different options: "Home", "Menu", drop-down box "Admin Actions" with three links ("Pending Bookings", "Accepted Booking", "Updated Bookings", "Book Table"), "Admin Profile", and "Logout"
            * ![Nav Bar - superuser mobile](/static/images/readme-pictures/navbar-mobile-open-superuser-login.JPG)
            * ![Nav Bar - superuser mobile dropdown box](/static/images/readme-pictures/navbar-mobile-open-superuser-login-dropbox.JPG)
            * ![Nav Bar - superuser](/static/images/readme-pictures/navbar-logged-in-superuser-medium.JPG)
            * ![Nav Bar - superuser dropdown box](/static/images/readme-pictures/navbar-logged-in-superuser-dropbox-medium.JPG)
        * All user have the webpage icon that leads to the landing page
    * Navbar sticks to the top, using Bootstrap's "fixed-top" class. This does however cover the top part, so extra margins had to be created for headings.

* __Landing page__:
    * The landing page has bright themed hero picture of a wooden bar desk. This picture is used in all main pages of the site. There is a welcome message being generated according to who is logged in, and the details of the user. The main title "Welcome to Dre's Diner" is animated going from 0 to 100 opacity and moving 50px up when coming into view. If the user is not logged in it will display the standard welcome message. If logged in, but with no name details added in profile, it will greet the user by username underneath the welcome message "Good to see you, (inserts name)". If name details are provided it will use the provided first name in the greeting. The greeting appears into view after a second and a half, changing opacity from 0 to 100. If user is not logged in the message will read "Log in to make a reservation"

        * ![Landing page - logged out large](/static/images/readme-pictures/index-logged-out-large.JPG)
        * ![Landing page - logged in large](/static/images/readme-pictures/index-logged-in-large.JPG)
        * ![Landing page - logged in only username](/static/images/readme-pictures/index-logged-in-no-details.JPG)
        * ![Landing page - logged out mobile](/static/images/readme-pictures/index-logged-out-mobile.JPG)
        * ![Landing page - logged in mobile](/static/images/readme-pictures/index-logged-in-mobile.JPG)
    
    * On the bar desk area of the hero image are three links. These also change when logged in/out.
        * If not logged in there are two white call-to-action icons that link to the sign-up page and the login page. They move 10px upwards when hovering over them, thus giving an interactive feeling.
        * If logged in there are three links side by side with white borders around them: "New Booking" linking to the booking page, "Menu", linking to the menu page, and "My Bookings", linking to the upcoming bookings for the user. All these divs also move 10px upwards when hovering over them.
        * If logged in as superuser the three links will be "Pending Bookings", "Accepted Bookings", and "Updated Bookings".

* __Menu page__:
    * The menu page shares the index hero-image and has the title "Menu coming right up below" and is animated in the same style as the index titles. This page is the same regardless of user.
        * ![Menu page - large](/static/images/readme-pictures/menu-large.JPG)
        * ![Menu page - mobile top](/static/images/readme-pictures/menu-top-mobile.JPG)
        * ![Menu page - mobile category and items](/static/images/readme-pictures/menu-category-and-item-mobile.JPG)
    * Underneath the main title is an introductory message that reads "Everything served has been put through a rigorous process to ensure optimal quality and flavour"
    * Underneath the site auto generates the categories added by the admin, followed by all the meals connected to this category.
    The category is on a row of its own, and underneath the pictures of the meals are displayed along with title, price, and description. Corners of the pictures are slightly rounded. On mobile view one meal occupies a full column. On large there are two meals side by side, which consists of the image to the left and the descriptions on the right. All text is white.

* __Sign-up page__:
    * Sign up page has a simple design, just showing a heading "Sign Up". Underneath is a paragraph that shows a link to the login page in case the user already has an account. Underneath comes the form, which consists of four fields: "Username", "E-mail", "Password", "Password(again)", and then a blue "Sign Up" button underneath. All fields except for E-mail are mandatory and marked with an "*".
        * ![Sign up page - large](/static/images/readme-pictures/signup-page-large.JPG)
        * ![Sign up page - mobile ](/static/images/readme-pictures/signup-page-mobile.JPG)

* __Log-in page__:
    * Log in page has the same simple design as the sign-up page, just showing a heading "Log in". Underneath is a paragraph that shows a link to the login page in case the user has not already created an account. Underneath comes the form, which consists of two fields: "Username" and "Password", and then a blue "Sign in" button underneath, and right under is a check-box which the phrase "Remember Me" so the system will remember the user. Underneath the button is a link to reset the password in case the user has forgotten. All fields are mandatory and marked with an "*".
        * ![Log in page - large](/static/images/readme-pictures/login-page-large.JPG)
        * ![Log in page - mobile ](/static/images/readme-pictures/login-page-mobile.JPG)

* __Contact Information__:
    * The contact information page has the same design as the index and menu pages. The content is the same regardless of user. Underneath the heading "Contact Information" is a paragraph that reads "Don't hesitate to send us a message if you have any questions or feedback". Below is the form for the user to send a message. On top of the form it reads "Scroll down further for more details", notifying the user of the opening hours and address below the form. There are three fields in the form: "Name", "Email Address", and "Message". All fields are mandatory. Below is a blue send button.
    * Underneath is a section which holds two divs, one with the opening hours - these are generated from the OpeningHours model - and the other with the contact details of the establishment (made up). For mobile views these two divs are not side by side but stacked on top of each other.
        * ![Contact page - top large](/static/images/readme-pictures/contact-top-large.JPG)
        * ![Contact page - bottom large](/static/images/readme-pictures/contact-bottom-large.JPG)
        * ![Contact page - top mobile](/static/images/readme-pictures/contact-top-mobile.JPG)
        * ![Contact page - middle mobile](/static/images/readme-pictures/contact-middle-mobile.JPG)
        * ![Contact page - bottom mobile](/static/images/readme-pictures/contact-bottom-mobile.JPG)

* __Contact Information Logged In__:
    * Same design as contact information but has a more personal message for the user "Don't hesitate to send us a message, {user}". A different shorter form is used, so that the user does not need to put in name and email.
    * ![Contact page logged in - top large](/static/images/readme-pictures/contact-logged-in-top-large.JPG)
    * ![Contact page logged in - bottom large](/static/images/readme-pictures/contact-logged-in-bottom-large.JPG)
    * ![Contact page logged in - top mobile](/static/images/readme-pictures/contact-logged-in-top-mobile.JPG)
    * ![Contact page logged in - bottom mobile](/static/images/readme-pictures/contact-logged-in-bottom-mobile.JPG)

* __Book Table page__:
    * Has the same hero-image as the before-mentioned pages. The heading reads "A Reservation"? which is followed by a phrase underneath "Scroll down and let's see what we can do". Underneath the hero-image is a form with the opening hours next to it. On mobile the opening hours will appear underneath. The opening hours are there for convenience when making a booking. The opening hours are auto generated from the OpeningHours model. If the user has not updated their name details, then the page will only display "Please fill in your name in the (link to profile section) before making a reservation".
    * The form has three fields: "Number of guests", "Date and Time" and "Comment". Only "comment" is not mandatory. Underneath the form is a blue button that says "Book". Should a validation error be provoked in the form a pink message will appear on top of the form with the error message. When selecting the "Date and Time" field a DateTimePicker will be activated, which makes sure that the correct datetime format is inserted. In the "Number of guests" field the arrow keys, up and down, can also be used to increase the number.
    * This page will show a header "Please log in to make a reservation" if a user arrives, using the URL, without being logged in
    * When user has made a reservation, they will be redirected to the "upcoming bookings" page.

        * ![Book Table - large](/static/images/readme-pictures/book-table-large.JPG)
        * ![Book Table - top mobile](/static/images/readme-pictures/book-table-top-mobile.JPG)
        * ![Book Table - middle mobile](/static/images/readme-pictures/book-table-middle-mobile.JPG)
        * ![Book Table - bottom mobile](/static/images/readme-pictures/book-table-bottom-mobile.JPG)

* __Upcoming bookings page__:
    * Same hero-image as before-mentioned pages. Header says, "Your Upcoming Bookings". If the user is not logged in an error page will show. This view filters all the bookings that are tied to the user logged in and are in the future. Bookings are displayed on top of each other, the datetime being shown in white text, 0.2 opacity background, and white borders. Status 0 is pending and will show as a grey background. Status 1 is accepted and will give a green background. Status 2 is declined and will show as red background. Each booking links to a booking details page.
    * The booking paginates by three
        * ![Upcoming bookings page](/static/images/readme-pictures/upcoming-bookings-large.JPG)
        * ![Upcoming bookings page](/static/images/readme-pictures/upcoming-bookings-mobile.JPG)

* __Booking details page__:
    * Same hero-image. Heading reads "Booking Details". Underneath the details of the booking are shown. According to status it displays "To be confirmed", "Accepted", or "Declined". Underneath is the full name of the user, the datetime, the number of guests, the comment (if any), and two buttons; red for Cancel booking and blue for Edit comment. If the booking has been declined there will be a blue button linking to the booking page, urging the user to book another time.
        * ![Booking Details large](/static/images/readme-pictures/booking-details-large.JPG)
        * ![Booking Details declined large](/static/images/readme-pictures/booking-details-declined-large.JPG)
        * ![Booking Details declined mobile](/static/images/readme-pictures/booking-details-declined-mobile.JPG)

* __Delete booking page__:
    * The header says "Delete booking". Underneath is a paragraph that says, "Are you sure you want to delete the reservation?". Underneath are the details of the booking: Name, Date, Time, and guests. Underneath are two buttons: red button "Delete" and blue button "return". There is no like on the other pages which signifies that it is a serious action that is permanent. The design is narrow and does not change on mobile. If booking is closer than two hours away (booking property latest_cancellation) the page will display "Time limit exceeded. Cancellation is unfortunately no longer possible. Please get in contact with the restaurant if further information is needed".

        * ![Delete booking page](/static/images/readme-pictures/cancel-booking-mobile.JPG)

* __Update comment page__:
    * Simple design. Header says, "Update booking", underneath is a big comment field. Underneath is a blue button "Update". Next to the button is a link to return to the "Upcoming bookings" page "return".
        * ![Update comment page large](/static/images/readme-pictures/edit-comment-large.JPG)
        * ![Update comment page mobile](/static/images/readme-pictures/edit-comment-mobile.JPG)

* __Previous bookings page__:
    * Similar set up as "upcoming bookings" page. If the user is not logged in an error page will show. Queryset is set to previous from datetime.now(). 
        * ![Previous bookings large](/static/images/readme-pictures/previous-bookings-large.JPG)
        * ![Previous bookings mobile](/static/images/readme-pictures/previous-bookings-mobile.JPG)

* __Previous bookings details page__:
    * Similar design as the booking details, but since the booking is past time, the user does not have the option to edit or cancel the booking.
        * ![Previous bookings details large](/static/images/readme-pictures/previous-bookings-details-large.JPG)
        * ![Previous bookings details mobile](/static/images/readme-pictures/previous-bookings-details-mobile.JPG)

* __Profile page__:
    * Design in line with the other sites. Header says "Profile" and underneath the image is a form. The form has five fields: "Username", "First name", "Last name", "Email", and "Password". All except for password are mandatory. Underneath the form is a paragraph with a link to change the password. Underneath the form is a blue button "Save" which will update the details of the profile. Updating name details here will allow the user to make reservations.
        * ![Profile page - large](/static/images/readme-pictures/profile-large.JPG)
        * ![Profile page - top mobile](/static/images/readme-pictures/profile-mobile.JPG)

* __Log out page__:
    * Very simple design in line with the other allauth pages. Header "Sign out". Underneath a paragraph "Are you sure you want to sign out?". Underneath a blue button "Sign Out".
        * ![Log out page - large](/static/images/readme-pictures/logout-large.JPG)
        * ![Log out page - mobile](/static/images/readme-pictures/logout-mobile.JPG)

* __Pending bookings page__:
    * Page does not share the design of the other pages as this is an "extra" page for the admin. Admin has the capabilities in the admin panel, and technically does not need this page. If a non-superuser arrives then page will show "You need admin credentials to access this page". Pending reservations (status 0) are filtered to the admin. Bookings are displayed using Bootstrap cards. Admin can see on the booking if tables have been assigned. Underneath the bookings there are two choices: "Cancel" which will take admin to the "Cancel Booking" page, and "Approve/Decline" which takes admin to an extended version of UpdateView. Cards/bookings are paginated by six.
        * ![Pending bookings page - large](/static/images/readme-pictures/pending-bookings-large.JPG)
        * ![Pending bookings page - mobile](/static/images/readme-pictures/pending-bookings-mobile.JPG)

* __Accepted bookings page__:
    * Follows the admin design style. Upcoming accepted bookings are displayed here in the same manner as on the Pending page. Cards are green to signal accepted, and admin has two choices; update the booking, or cancel the booking.
        * ![Accepted bookings page - large](/static/images/readme-pictures/accepted-bookings-admin-large.JPG)

* __Approve/decline booking page__:
    * Heading reads "Approve or Decline Booking". Underneath are important asterix comments: "* If declining: Add a comment to the customer and remove tables." - this is a chance to explain to the client why the booking was declined. Also, if tables are not removed then they will stay as occupied for other reservations. This can still be changed on the admin site, but it's still good to remember to do it here. Secondly, "* To select/deselect tables, press and hold control/command key when adding/removing" - This is simply to explain how to manage the table-field, if needed. Also, there is a link for the admin to see all current available tables for this booking, should they wish to assign/add any. Underneath the form are two buttons: blue "Update" and under is a white "Return".
    * If status is set to approved and updated an email will be sent:
    Subject: Dre's Diner booking
    From: dresdiner@email.com
    To: {{user.email}}
    Date: Thu, 23 Dec 2021 20:24:23 -0000

    Hello {{user.first_name}}, your booking is confirmed on {{booking.booking_start}}. Please note that cancellations must be made minimum two hours before. We look forward to seeing you.

    * If status is set to declined a different email will be sent:
        Subject: Dre's Diner booking
        From: dresdiner@email.com
        To: {{user.email}}
        Date: Jan 2, 2022, 9:11 AM

        Hello {{user.first_name}}. Unfortunately, we are not able to accommodate your booking on {{booking.booking_start}}. For more information, please see the comment left by the restaurant or contact us via our website.

        * ![Approve/Decline bookings - large](/static/images/readme-pictures/approve-decline-large.JPG)
        * ![Approve/Decline bookings - mobile](/static/images/readme-pictures/approve-decline-mobile.JPG)

* __Updated Bookings page__:
    * This page shows the admin the future bookings that have been updated in the comments. It filters updated on > created on, and also if there are any comments. The setup is the same as on the other admin page with the bookings on cards. Underneath each card the admin has two actions: "Cancel" and "See details". "Cancel" will take the admin to the "Cancel booking" page and "See details" will take the admin to another Update booking page. Cards are paginated by 6.
        * ![Updated bookings page - large](/static/images/readme-pictures/updated-bookings-large.JPG)
        * ![Updated bookings page - mobile](/static/images/readme-pictures/updated-bookings-mobile.JPG)

* __Update booking details admin page__:
    * This is essentially the same page as the approve/decline bookings but has a different heading "Update booking". This extra page is created as bookings are likely accepted before they are updated, and another form feels correct.
        * ![Update bookings details admin page - large](/static/images/readme-pictures/update-booking-details-large.JPG)
        * ![Update bookings details admin page top - mobile](/static/images/readme-pictures/update-booking-details-top-mobile.JPG)
        * ![Update bookings details admin page bottom - mobile](/static/images/readme-pictures/update-booking-details-bottom-mobile.JPG)

* __Available Tables admin page__:
    * Page follows the admin styling. Header reads "Available tables". Underneath is another header "Booking for (first name + last name)", and underneath the number of guests are mentioned.
    * All available tables for this booking are displayed one by one, mentioning all fields from the model: Table number, number of seats, and which zone.
        * ![Available tables - large](/static/images/readme-pictures/available-tables-admin.JPG)

* __footer__:
    * Footer is dark grey with centered text. It reads "Made by Dre" Underneath are links to social media: Facebook, Youtube, Github, and Instagram. All links open in a new page. Links simply go to the main pages, except for Github which leads to my personal repository.
        * ![Footer - large](/static/images/readme-pictures/footer-large.JPG)
        * ![Footer - mobile](/static/images/readme-pictures/footer-mobile.JPG)

## Future features to implement
* I wanted to have a feature which generated buttons with available times for the date that users put in. I was able to generate the buttons, but not to have them work with forms.
* Opening hours could include national holidays
* Restaurant could be able to specify latest cancel time

# Testing
## Django testing
All applications have been tested using TestCase. Forms, models, views, and additional functions have all been tested.
* TestCase
    * When testing the current database was not able to create testing databases, and I had to comment it out and un-comment the other database using sqlite3 in settings.py
* Applications
    * Contact
        * Test_views - 2 tests, both pass. One for code 200.
        * Test_forms - 7 tests, all pass. Test wrong input and required fields.
    * Homepage
        * Test_views - 2 tests, passes. Tests for code 200.
    * Menu
        * Test_models - 2 tests, both pass. Test to create objects with both models, Meals and Category.
        * Test_views - 2 test, passes. Tests for code 200.
    * Reservations
        * When I tested a booking, I had to pass in a datetime object. On the website we pass in a string which is then converted to datetime, but this did not work for certain tests or when testing the model.
        * Test_booking. 29 tests, all pass. Testing each function in reservations.bookings.py. Checking if functions use input from models properly. For many tests I created specific tables to have multiple options to return, checking if correct ones are returned with correct priority. Had to create opening hours, bookings details, users, and tables for most of the tests. For certain tests I started for loops to test function calls with increasing number of guests, and then running self.assert... for each iteration.
        * Test_views - 15 tests, all pass. Tested views for code 200 and correct template use. For many of them I had to create a user, at times a superuser, and log in. For the booking view I logged in and posted a correct form and then checked if a booking had been made.
        * Test_forms - 18 tests, all pass. Tested forms for errors for wrong input, all fields should be there, which ones are required, minus values, wrong types, not enough tables, enough tables but one with certain method, opening hours, past booking
        * Test_models - 7 tests, all pass. Tested if object could be made, if default fields are automatically set, if slugs are generated and unique, if model properties work (booking latest_cancellation and is_due_date).
    * Restaurant
        * Test_models - 3 tests, all pass. Test if objects can be created and if default values work.

## Browser Testing

## Media Queries
Media queries have been done using bootstrap's class system.
Chrome Developer Tools was used for testing all media queries for additional CSS.

- Test on Firefox, no problems detected.
- Microsoft Edge, no problems detected.
- Avast secure browser, no problems detected
- A user using "Brave" browser said that content was blurry on his browser due to hero-image being loaded differently. I have not been able to fix this.
- Media query tested on my own phone, Samsung Galaxy S9 using Chrome and Firefox, no issues.
- Media query tested on my own tablet, Ipad pro 2018 11" using Safari+Chrome, no issues.
- General testing with my own laptop, Asus 13 inch using Chrome, no issues.
- All links were tested. All external links and internal links work.

## Bugs discovered during testing:
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
    * Implemented a check for booking.author in all bookings and test for booking_start. Needed to adjust for length of returns as it always returns one conflicting: the one returned is the booking being made because I need to double-save it to add the ManytoManyField.
* Got an error creating the test database: permission denied to create database
    * Need to comment out database in settings and remove comment out for sqlite3 database. Flip back when done testing
* When logged in as user the pagination still thinks that all bookings are there, even though the user only has e.g. 1 booking, so it might show 3 pages to paginate
    * Queryset fixed and now only returns the booking for specific user
* It's possible to create reservations with identical content. However, this makes it impossible to open the details. Console displays: MultipleObjectsReturned at /reservations/xxxxx/ 
    * Slug auto-generated, and there are checks for double booking by same user. First_name and last_name are no longer used, so details from the user is inserted. User must put in details before bookings can be made.
* Django logs user out when following link to reservation_detail.html. User is logged back in when hitting the back button in browser
    * Had to change the render function in ReservationDetail to include "user": User, instead of "user": User.username.
* Implemented authentication check when cancelling and updating reservations. The check is already done on the reservation list, but the url can be typed in as long as you know the username, which opens up the possibility for non-users to change the reservation.
    * No longer an issue. user authentication added and random slug.
* Raise validationerror for outside opening hours doesn't show 
    * Fixed - I set crispy fields to only show certain fields thereby hiding messages
* Had many problems loading the static files from Cloudinary to Heroku. Heroku would generate a wrong URL and could not retrieve CSS and pictures. My mentor and I were unable to resolve the issue after two meetings, which caused me to miss the first deadline.
    * I created a new Cloudinary account which fixed the CSS problem. However, it did not want to load pictures. I eventually solved it by loading the static to every template that had to use images from Cloudinary. Static was already loaded in base.html but did not extend. Also, I was unable to have it load css backgrounds from style.css - the url to cloudinary would be wrong - so I instead used inline styling. This was later removed as I redesigned the page to only used hero-image.

## Unfixed Bugs:
* Due to problems with loading static images I need to import {% load static %} in all of the files using the hero image. I was not able to set a background-image in css as the image would not load properly from Cloudinary. I could not resolve this issue and resorted to my mentor, who was equally unable to understand the cause.
* If a user does not enter email on registration then no confirmation email is sent. If user then updates profile with email, as is required to make a booking, then no email-confirmation is sent. It is only sent on registration.

## Validator Testing
* PEP8 validator for python:
    * I have "Line too long" e501 errors and I am aware of them. I was advised to let them be as they do not impact my code.
        * 2 in reservations.booking.py
        * 10 in reservations.forms.py
        * 10 in reservations.models.py
        * 12 in reservations.views.py
        * 19 in reservations.test_booking.py
        * 5 in reservations.test_forms.py
        * 25 in reservations.test_views.py
        * 1 in menu.models.py
        * 1 in contact.views.py
        * 1 in contact.test_forms.py
        * 3 in restaurant.test_models.py
        * 2 in restaurant.models.py

* W3 Markup Validation Service completed for all HTML pages with no errors.
    - Admin accepted page
        - ![Admin accepted page test](/static/images/readme-pictures/test-admin-accepted.JPG)
    - Admin pending page
        - ![Admin pending page test](/static/images/readme-pictures/test-admin-pending.JPG)
    - Admin updated page
        - ![Admin updated page test](/static/images/readme-pictures/test-admin-updated.JPG)
    - Book table page
        - ![Book table page test](/static/images/readme-pictures/test-book-table.JPG)
    - Contact page nouser
        - ![Contact page nouser test](/static/images/readme-pictures/test-contact-nouser.JPG)
    - Contact page logged in
        - ![Contact page logged in test](/static/images/readme-pictures/test-contact-login.JPG)
    - Homepage
        - ![Homepage test](/static/images/readme-pictures/test-homepage.JPG)
    - Login page
        - ![Login page test](/static/images/readme-pictures/test-login.JPG)
    - Logout page
        - ![Logout page test](/static/images/readme-pictures/test-logout.JPG)
    - Menu page
        - ![Menu page test](/static/images/readme-pictures/test-menu.JPG)
    - Password page
        - ![Password page test](/static/images/readme-pictures/test-password.JPG)
    - Profile page
        - ![Profile page test](/static/images/readme-pictures/test-profile.JPG)
    - Signup page
        - ![Signup page test](/static/images/readme-pictures/test-sigup.JPG)
    - User previous bookings page
        - ![User previous bookings page test](/static/images/readme-pictures/test-user-previous-bookings.JPG)
    - User upcoming bookings page
        - ![User upcoming bookings page test](/static/images/readme-pictures/test-user-upcoming-bookings.JPG)
* Jigsaw test CSS file completed with no errors.

# Starting Django project
* I used the Code Institute full-stack template for this project: https://github.com/Code-Institute-Org/gitpod-full-template
* Create new workspace install the following:
    * Django and gunicorn: pip3 install django gunicorn
    * Supporting libraries: pip3 install dj_database_url psycopg2
    * Cloudinary Libraries: pip3 install dj3-cloudinary-storage
    * Create requirements file: pip3 freeze --local > requirements.txt
    * Create Project: django-admin startproject project .
    * Create App(s): python3 manage.py startapp reservations
    * Add to installed apps in settings.py: 'reservations'
    * Migrate to database: python3 manage.py migrate
    * Now the project can open by typing python3 manage.py runserver

## Deployment
### Heroku
* On dashboard on Heroku create new app, name it and set to EU
* To to resources tab -> search for "postgres" -> add Heroku Postgres
* Go to settings tab -> reveal config vars -> copy-paste the value of DATABASE_URL
* Back to Gitpod -> in the env.py file and add the following
    * import os
    * os.environ['DATABASE_URL'] = 'copy-paste it here'
    * os.environ['SECRET_KEY'] = 'whateveryouwanttocallit'
* copy the secret key value
* On heroku config vars add a new variable "SECRET_KEY", and in value paste your key
* On gitpod in settings.py:
    * import os underneath pathlib
    * add the following underneath:
        * import dj_database_url
        * if os.path.isfile("env.py"):
        *   import env
    * Remove the value of secret key, add instead os.environ.get('SECRET_KEY')
    * Comment out the DATABASE using sqlite3, add underneath:
        * DATABASES = {'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))}
* Migrate changes to new database: python3 manage.py migrate

### Cloudinary
* Create new Cloudinary account
* On the dashboard copy paste the API Environment Variable
* Back to gitpod env.py -> add: os.environ['CLOUDINARY_URL'] = 'here goes the copy-pasted variable'
    * Remove the "CLOUDINARY_URL=" from the beginning of the URL, keep the rest
* Copy the value from CLOUDINARY_URL (now with no "CLOUDINARY_URL=")
* Back to Heroku Config vars
    * Add a variable: CLOUDINARY_URL and paste in the value
    * Add another variable: DISABLE_COLLECTSTATIC, and set the value to 1
* Back to gitpod settings.py, add in installed apps:
    * Over 'django.contrib.staticfiles' add 'cloudinary_storage'
    * Underneath 'django.contrib.staticfiles' add 'cloudinary'
    * Under STATIC_URL = '/static/' add the following:
        * STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
        * STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
        * STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
        * MEDIA_URL = '/media/'
        * DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

### Last settings
* In Gitpod under settings.py:
    * Underneath BASE_DIR = Path(__file__).resolve().parent.parent add:
            * TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
        * In the TEMPLATES variable change DIRS to point to ['TEMPLATES']:
            * TEMPLATES = [
            {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [TEMPLATES_DIR],.....
    * Go to ALLOWED_HOSTS and add localhost and the heroku app name:
        * ALLOWED_HOSTS = ["name-of-the-app.herokuapp.com", "localhost"]
* Create three directories (folders) on the top level next to the manage.py file:
    * Static
    * Media
    * Templates
* Create a Procfile (remember capital P), content should be:
    * web: gunicorn project.wsgi
        * web: tells heroku that this is a process that should accept http traffic
        * gunicorn: the server that we installed
        * wsgi: standard that allows python services to integrate with web servers
* Commit and push to repository
* Back to Heroku Dashboard -> deploym -> choose GitHub -> search for the repository name and connect -> deploy branch


## Create a local clone
1.	Open GitHub and navigate to repository here (https://github.com/AndreasChristensen89/resto-booking-system).
2.	Click the Code drop-down menu.
3.	Options:
•	Download the ZIP file, unpack locally and open with IDE.
•	Copy git URL from HTTPS dialogue box.
4.	Open your chosen IDE and open the terminal in a directory.
5.	Use the "git clone" command with the copied git URL after.
6.	Clone of the project is created locally on your machine.


# Technologies Used

## Icons
Icons and script were taken from https://fontawesome.com/, as well as Google's fonts: https://fonts.google.com/icons?selected=Material+Icons.

## Datetime Picker
A Javascript datetime picker, XDSoft DateTimePicker, was used on the booking page. It was found on this page:
* https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html
    * Followed instructions for install, which included implementation of a script in the head and at the bottom of the html page.
    * Was inserted into base.html

# Hosting and Development
* GitHub was used to host the repository
* GitPod was used for development and version control
* Heroku was used to deploy site
* Cloudinary was used as cloud service

# Credits
## Pictures
Image was compressed using the webpage https://tinypng.com/ Afterwards it was converted to webp using https://cloudconvert.com/png-to-webp.

Picture credits from freepik

hero-pic:
<a href="https://www.freepik.com/photos/background">Background photo created by tirachard - www.freepik.com</a>


## Text content
Content was all formulated by myself, but for the menu I took inspiration from various websites with food, descriptions etc.


## Coding help
- For help with various issues Django, css etc. I often resorted to https://stackoverflow.com/ as well as the official documentation for Django.
- For help with syntax reminders I often used https://www.w3schools.com/, as well as various pages giving advice on Django
- For general best practice I used Code Institute's Slack community.
- For CSS and Bootstrap I used https://stackoverflow.com/ as well as Bootstrap Documentation.
- General comments from family and peers for what CSS looked the best.
- I looked up other booking system to get inspiration for how it could be set up.

## Design
- For design of the different pages I didn't use other sources of information other than my previous projects.
- I decided to redesign the entire site thus making it a lot more minimal. Inspiration came from my family.
- No wireframes were used

# User stories
For user stories I used Github's Projects -> User Stories. Kanban board. I created 18 stories and implemented them one by one. Some others were deleted, and some were changed along the way. The ones that are there now are:
- Accept/decline reservation: As a site admin I can approve or reject reservations so that the customer knows if they have a reservation or not
- Choose table assignment method: As an admin I can select a table assignment method so that I can adapt the method to the restaurant setup
- Check opening hours: As a site user I can know if my booking request is within opening hours so that my booking is not falsely accepted
- Avoid double booking: As a site user I can see if no tables are available on the desired datetime so that no double bookings occur
- Automatic table assignment: As a site user I can have tables automatically assigned to my reservation so that no space is wasted
- Edit reservation: As a site user I can edit the details of my reservation so that the restaurant knows about desired changes
- Log in as user: As a site user I can log in so that I can make reservations
- Book multiple tables: As a site user I can combine tables for a reservation so that a larger party than the table can be accommodated
- Cancel reservation: As a site user I can cancel a reservation so that the restaurant knows of the update
- See list of specific User reservations: As a site user I can see a list of my reservations so that I have an overview of my bookings
- Add special requirements: As a site user I can add notes to my reservation so that the restaurants know of any needs to accommodate the guests
- See menu: As a site user I can see the menu items so that I can decide whether or not to make a reservation
- See list of reservations: As a site admin I can see the complete list of reservations so that I have an overview of business activity
- Change request status: As a site admin I can change the accepted/declined status of a reservation so that I can fix reply-errors
- See details of reservation: As a site admin I can open a reservation so that see all details of the reservation
- Make reservation: As a site user I can make a reservation so that the restaurant is notified about my request
- Site pagination: As a site user I can view a paginated list of reservations so that I can select which reservation to view
- Send messages to clients: As a site admin I can send messages so that the customers know reasoning behind e.g. cancellations.

# UX
## User acceptance criteria
What are the goals for a first-time visitor? 
* Quickly understand that the page is about and make sense of the setup
    * This is indicated by the welcome message and the clear white call-to-action icon
* Be captivated by the content and the imagery
    * Bright and inviting colors are used. It's simple and easy for the eyes.
* Be able to navigate effortless through the pages
    * Navigation bar is always available and the index page has call-to-action links depending on user
    * Interactive element move when users hover over them.
* Easily understand how to get started and to set up
    * Message on index tell them to log in to make a reservation. The call to action links are easy to see and takes them directly to sign-up or login
* Easily understand how to make a booking
    * If user has not entered details they are guided to the profile page to fill them in
    * Afterwards if their screen on the booking site is too small to show the form the message tells them to scroll down
    * If info is wrong, validation error will be raised with clear messages of what went wrong.
* Understand how to access bookings
    * When a booking is made the user is redirected to the upcoming bookings page.
    * Additionally, the nav bar has a dropdown called "booking" which has clear links to upcoming/previous bookings
* Give good feedback
    * Messages are incorporated and gives feedback for account activity and email.
* Have the application work on all devices.
    * Using bootstrap as a mobile first tool made sure that it works properly. Additional styling was made by custom CSS and is tested to work on all devices.

What are the goals for a returning visitor?
* Instantly/easily remember how to navigate the content
    * I estimate this to be intuitive
* Easily remember how to access relevant pages
    * Index has call to action for most common pages, and navbar is always present
    * In case user has questions there is also the contact page, which makes it easy to send messages
* Easily be able to contact the developer with questions, feedback, any other inquiries
    * Contact page is clearly displayed in the navbar, and there is also a link at the bottom of the menu
    * User has the option of sending a message, but also to phone the restaurant (made up number), or to visit them at their address

## Strategy
The purpose of this site is to create a simple site for a restaurant that handles reservations. The site should be simple to use, and information should be easy to find with simple and clear design

## Scope
The scope is limited in functionality but does implement logic to assign tables with reasonable complexity. It could for sure be more complex and specific. Options for handling bookings are limited but should be completely functional.

## Structure
The flow of the website is simple and should be intuitive for most people. Navbar has everything the user needs to find their way around. In case there is confusion about how the setup works there is a clear path to contact the restaurant both with messages, phones, and their address. On the landing page users are shown the call-to-action links that encourage them to register, and if logged in they are directed to the most common pages.

## Surface

### Design Choices
- Overview: The aim is to provide easy-to-navigate pages that make it easy and clear to navigate around.
- The site should be easy for the eyes, meaning that there should be no overlapping animations that confuse users.
- It should be clear to the user what can be clicked on.
- Information should not be detailed but fast to read and understand, and straight to the point.
- All pages should share design

### Color Scheme
There is a play between bright and dark, and the colors are centered around brown. Bright restaurant background with a wooden feel. White is used to for choices and grey, red, and white signal status. Green is used to signal confirmation. Red is used to signal cancellation or declined. Grey is used for pending. The dark brown background resembles and gives, in my opinion, a nice contrast to the hero-image.

### Choice of text
Lato was the choice. I experimented with a lot of fonts from Google, but in the end Lato was the best in my opinion.

### Pictures
There is only one picture used, which is a wooden bar desk with a blurry background. It is bright and has a brown/wood based theme. I find it relaxing and simple, and hope that others will feel the same way.

### Accessibility
All non-text elements are marked with aria-labels, and the contrast between background and foreground colors were implemented in color scheme.

# Languages Used
- HTML
- CSS
- Python
- JavaScript
- Markdown language for readme file

# CRUD
## Create
Users and admin can create objects in the Booking model via the booking form + booking view code on the booking page. Admin can additionally create objects via the admin panel.

## Reading
Users can find their past (previous bookings page) and future booking (upcoming bookings page) object on their site and see the booking details (booking details page). Admin can see all bookings in admin panel, or filtered bookings on the pending bookings page, accepted bookings page, and the updated bookings page.

## Updating
Users can update their future bookings on the upcoming bookings page using the UpdateView class. It is limited in that they can only alter the comment. However, admin is able to alter every aspect of the booking objects, done in the admin panel, pending bookings, updated bookings, and accepted bookings, and can alter bookings from any time.

## Deletion
Users can delete their future bookings on the upcoming bookings page. Admin can delete bookings via the pending bookings, updated bookings, accepted bookings, and can delete all bookings from any time.


# Email
* During development the following was used in settings.py:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
* Post-production a Gmail was implemented with the following settings:
    - EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    - EMAIL_HOST = 'smtp.gmail.com'
    - EMAIL_HOST_USER = 'dresdiner.notice@gmail.com'
    - EMAIL_HOST_PASSWORD = os.environ.get('APP_KEY')
    - EMAIL_PORT = 587
    - EMAIL_USE_TLS = True
    - DEFAULT_FROM_EMAIL = 'dresdiner.notice@gmail.com'
    * This sends live emails from a gmail I created for this project
    * Password in stored in env.py
        * variable is also added to Heroku config variables
* Email is sent when registering to confirm the email.
* Email is sent when resetting password
* Email is sent when a booking is accepted or declined
* Email is sent when a message is sent on the contact page
    * Host email is set as CC
* Email is sent when a User double books, meaning that two or more bookings are overlapping

* Email may arrive in spam folder, so be sure to check that.


# Admin Access
Admin credentials given on submission
* In url add "/admin" (https://resto-booking-system.herokuapp.com/admin)

## Must have settings
In order for booking logic to work admin must set up the following (This is already set on deployment, but can be changed):
* Under Restaurant:
    - In BookingDetails add one object:
        * Specify Booking Duration - how many minutes each party will occupy the tables
        * Specify Table assign method - how or if the system should assign tables
        * Specify Method Limit - automatically set to 100, on deployment set to 12. This is to set a max-limit of guests to the assign table function. e.g. function will not trigger if number of guests are higher than limit
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

* Under Reservation:
    * In Tables add desired number of tables
        * Technically you can make it work without tables, but no tables are available, and it will therefore think that the restaurant is fully booked and will not accept bookings. Admin can make reservations manually though.

* Warning: Admin can rely on booking logic to not conflict tables and bookings, but Admin is able to manually assign the same tables to concurrent bookings. Admin is advised to rely on the logic, or to make sure to use the Available Tables site when updating and accepting bookings (if sorting is turned off). If the admin wants to create a booking, then it is best done from the site, as the logic does not work in the Admin administration system.

## Setup explanation
* I added a restaurant application with models to have the restaurant be able to set specific requirements for bookings. Opening hours, booking duration
* If a user double books (same user, and duration of booking overlaps) a validation error is not given. Table check is done but tables are not assigned to new booking which is because of the chance that a user may want to use his profile to reserve a table for someone else in the same timeslot. The system sends out an email to the user to notify of the double booking and no tables assigned. The user is then invited to contact the restaurant or delete the double booking(s).
* Added property to booking to see if it's in past or not, and also if it's too late to cancel reservation. I set it to two hours, which I believe is reasonable. In case the guests need to cancel anyway they have to call the restaurant.
* I set use_tz to False in settings.py in order to avoid the time zone input from bookings.booking_start
* In order to add the ManyToManyField in the Booking model I had to save the booking first in the view and then afterwards attach the tables, and finally save again. This caused a lot of trouble but it works now.


# Booking Logic
1. User must create a profile in order to make reservations. Profile must include first name and last name.
2. User specifies number of guests and datetime, comment can be made but is not needed
3. Form validates opening hours, datetime (past), number of available tables, number of people and gives validation errors if any conflicts exist
4. View code checks which sorting method/if sorting method is on, uses the method to extract tables, returns best combination, and assigns table(s) to booking.
5. Booking is displayed on users "upcoming bookings" - color indicates status - is also displayed on admin's "pending bookings" as booking is automatically set to status 0 (pending)
6. User can access booking details, cancel booking, or update the comment - User cannot cancel the booking if booking is less than two hours away. If user updates booking it will appear on admin's "updated bookings" site, but only if a comment is present (it's possible to update without leaving a comment)
7. Admin can see booking details, as well as the current tables assigned to the booking. Admin is able to cancel booking directly or accept/decline. In accept/decline admin is able to change tables, status, and comments.
8. If Admin accepts the booking will turn green and give a confirmed message as well as an email. if Admin declines the booking will turn red and send a different email. It's possible for Admin to change a declined to an accepted and vice versa. After action the booking will disappear from the pending page.


## Table sorting methods
In the BookingDetails model Admin can change sorting method or turn it off completely. There are three choices:
* Off
* Tables from same zone
* Any Tables

### Any tables

1. Firstly, the function seeks to bring an exact match with table-size/number of people. 
    - If there are no exact matches it will look for table-size minus one (e.g. table size 6 for 5 people)
    - This is done to keep groups at the same table, and also to preserve other tables (smaller tables are valuable for smaller groups)
    - If there are no matches it will store the best option for 1 table
2. Follows to find best option (fewest seat losses) when combining any two tables
3. Follows to find best option (fewest seat losses) when combining any three tables
4. All options are then compared to each other to find best match
    - fewest tables are prioritised, meaning if losses are equal, it will pick the option with the fewest tables
        - 1-table-option is only compared to 2-table-option. If a single table can fit a group, and with fewer or equal losses than a two-table option, then a 3-table option is not worth considering due to loss of smaller tables. As mentioned above, smaller tables are valuable and should be kept for smaller groups.
            - e.g. if available tables' sizes are [2, 2, 4, 10], a group of 8 will be given a table of 10, even though the total-seat loss of 2+2+4 == 0. If only the table for 10 is used, then three tables remain for a potential of more groups, compared to only a table of 10.
    - fewer losses are then prioritised
        - 2-table option and 3-table option are compared
5. If three tables are not sufficient then tables will be added one by one, largest to smallest.
    - If sum of seats exceeds number of guests, then last table will not be added, and it, along with the following smaller tables, is checked for which one gives fewest losses.
    - Seeks to only add one table to preserve tables
6. Once tables are assigned Admin is still free to change tables.

### Same zone tables
1. Method uses a list of all available tables
2. Creates lists of each zone's tables.
3. Loops through each zone-list and checks if sum of seats >= guests
4. If sum passes then each zone-list is run through same logic as any-tables logic
5. The result with the fewest losses is returned.

### Limitations of table sort logic
* The logic is limited in that it does not factor in moveable tables, as well as overlapping zones, but is only able to go by zone. Zones may not be easy to handle in real life, depending on the restaurant setup, and the logic may end up not finding what would be an obvious solution.
    * In this I am mostly referring to larger parties that require multiple tables. Tables may be in the same zone, but not optimal to put next to each other. Also, tables from two zones may be easily put together in real life but should not in general be in the same zone and thus not able to be sorted with the current logic.


# Django

## Django Apps
* project - main
* reservations - contains the booking and table models as well as the booking and profile form. Contains all the views related to booking, both for admin and users. Also contains all the booking logic in a separate file booking.py.
* homepage - simply contains the view for the index page and the 404 view code.
* contact - contains the view codes for the contact pages as well as the forms
* menu - contains the view for the menu page as well as the two models; Category and Meals.
* restaurant - contains two models: OpeningHours and BookingDetails

## Django models
Six models
* Booking - stores object for each reservation.
    - Has an autogenerated slug field with random chars, User logged in is added, takes number of guests and a booking start. Booking end is automatically generated in view code according to the BookingDetails model. Updated on, and created on are created and uses current datetime. Status has three options,1: "Pending", 2: "Approved", and 3: "Declined", is automatically set to 0. Comment is optional.
    Table is a ManyToManyField and can have multiple tables attached from the Table model.
        - In first I included first_name and last_name in the Booking model, but it seemed extensive, especially when a user was already created. Instead, I found it better to require adding contact details before making a booking. This way the same user can easily book again, and the details are taken from the user. The first_name and last_name could be cut from the booking, thus making it more appropriate to book using only a datetime and guests number.
* Table - store object for each table
    - Needs a unique table number, number of seats, and a zone. Seats and zone are used in booking logic.
* OpeningHours - stores objects for each weekday.
    Takes in weekday, opening time and closing time, which uses timefields.
* Bookings details - should only store one object for booking details.
    - Takes in booking duration, meaning how long time each booking should occupy in the system. Next is table assign method, which has three options: 0 - "Off - admin assigns tables", 1 - "Assign any tables in same zone", 2 - "Assign any tables". Finally assign method limit, which is automatically set to 100. Admin can specify if they want the system to not sort automatically if the number of guests for a single reservation is more than this number.
* Category - stores an object for each food category.
    - One field; name. Connects to meal.
* Meals - stores an object for each meal.
    - Name must be unique. Takes in description. Uses foreignkey to connect to a Category object. Takes in number specifying how many people it is meant for. Price is a decimal field with max 4 digits and two decimal places. Image must be included, which will be uploaded to cloud via Pillow (installed). Slug is auto generated from the name field.

## Django forms
Four forms
* BookTableForm - form for creating booking on the booking page
    * Has three fields: Number of guests, Date and Time, and Comment.
    * Checks if sum of seats (from available tables) are greater or equal to number of guests.
    * Checks if Date and Time is in future
    * Check if number of guests are at least 1
    * Checks if Date and time is within closing time minus booking duration. E.g. if closing time is 22:00 and booking duration is 120 mins, then latest time is 20:00
* ProfileForm - form for the profile page
    * Fields: username, first name, last name, email, and password. Only password is not mandatory.
* ContactForm - form for the contact page
    * Fields: name, email, and message.
* ContactFormLoggedIn - form for the contact page for registered users
    * One field: message. View code handles the rest.

## Additional mentions:
New postgres:
https://www.elephantsql.com/
Not Heroku anymore:
render.com
Due to message on the 06-12-2021, Gitpod had new dependencies. 
I Followed the instructions:
    * find -name "deps.txt" - no results, which meant that I had the older version
    * ran pip3 freeze > unins.txt && pip3 uninstall -y -r unins.txt && rm unins.txt
    * pip3 install django gunicorn
    * pip3 install dj_database_url psycopg2
    * pip3 install dj3-cloudinary-storage
    * pip3 install django-allauth
    * pip3 freeze --local > requirements.txt
    * saved, commited, and pushed
    * pip3 install Pillow
    * pip3 freeze --local > requirements.txt
From here onwards, whenever I (re)started my workspace, I needed to do two things:
* First:
    - pip3 freeze > unins.txt && pip3 uninstall -y -r unins.txt && rm unins.txt
* Second:
    - pip3 install -r requirements.txt

command used for copying authentication templates to directory. Once copied we can make changes to the styling, and the content
cp -r ../.pip-modules/lib/python3.8/site-packages/allauth/templates/* ./templates
