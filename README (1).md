New website theme - Match Your Major
This is a platform where Yale students can find other Yale students that are studying or intending to study the same major as them. We offer students the chance to contact those other students either by phone or by email, such that students who are unsure about what they want to study can clear these doubts.

Launching the website:
The website just requires the "flask run" command-line to be launched.

Website layout when not logged in:
When a user is not logged in, the only options they'll have on our website are to view our mission statement, our homepage, create an account (through the register button), and log into their account (via the log in button)

Website layout when logged in:
When logged in, a user can acces their "My Profile" page, our mission statement, the "Find Matching majors" page, or logout.

Homepage (route="/"):
This will be the homepage which will be showed to anyone who accesses the website but is not logged in. It shows a welcome message. From here, a student may create an account, log into their existing account, or view our mission statement

Mission statement (route="/statement"):
This shows the website's mission statement i.e. what effects we wish to have on the Yale community and why this platform is a positive addition to life at Yale.

Register (route="/register"):
We allow Yale students to create an account with all the information we require to show on their profile pages (i.e. class year, residential college, major, Yale email, phone number, etc)

Login (route="/login"):
Allows users to login with their Yale email and passwords. They are then redirected to their profile page.

Profile page (route="/profile"):
Once students are logged in, they are redirected to their profile page where they can see their information. They can alter their profile information by clicking on the "Edit profile" button.

Find matching majors (route="/browse"):
When a student clicks on the "Find matching majors" link on the top bar, they'll be redirected to a page wherein they can select the major they want to be matched with. They'll then see a table with all the students (their name, college, class year, and contact information) that are also studying that major. From there, they can contact the other students by email or by phone with any questions or discussion topics they have on their major chocies.

Youtube link: https://youtu.be/jYH2bMNE3Mc