Email Sending Platform
**Overview**
This project is a web-based email sending platform built using Django. The platform allows users to compose and send emails with attachments, view email details, and organize emails into various folders.

**Features**
User Authentication: Sign up and log in with secure authentication.
Compose Email: Create and send emails with text content and file attachments.
Email Details: View detailed information of sent emails, including attachments.
Organize Emails: Categorize emails into folders such as Inbox, Starred, Drafts, Outbox, Important, and Bin.
Attachment Previews: Display image attachments directly in the email details view.

**Installation**
Clone the repository:

**bash**
git clone https://github.com/yourusername/email-sending-platform.git
cd email-sending-platform

Set up a virtual environment:

bash
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`

Install the dependencies:

bash
pip install -r requirements.txt

Set up the database:

bash
python manage.py migrate

Create a superuser:

bash
python manage.py createsuperuser

Run the development server:

bash
python manage.py runserver
Access the application at http://127.0.0.1:8000/.

Usage
Sign Up: Register a new user account.
Log In: Log in with your credentials.
Compose Email: Navigate to the compose email page, fill in the recipient's email, subject, message, and add attachments if necessary.
View Emails: View emails in various folders.
Email Details: Click on an email to view its details and attachments.

Project Structure

email-sending-platform/
├── akmail/
│   ├── migrations/
│   ├── static/
│   │   ├── images/
│   ├── templates/
│   │   ├── email_detail.html
│   │   ├── index.html
│   │   ├── signup.html
│   ├── templatetags/
│   │   ├── custom_filters.py
│   ├── views.py
│   ├── models.py
├── akmailproject/
│   ├── settings.py
│   ├── urls.py
├── manage.py
├── requirements.txt

**Custom Filters**
This project uses custom template filters to handle specific logic in templates. The custom_filters.py file includes a filter to check the file extension of attachments.

**Contributing**
Fork the repository.
Create your feature branch: git checkout -b feature/your-feature
Commit your changes: git commit -m 'Add some feature'
Push to the branch: git push origin feature/your-feature
Open a pull request.

**License**
This project is licensed under the MIT License. See the LICENSE file for details.
