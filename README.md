# Aviation Safety Reporting Application

![Responsive Mockup](documentation/amIresponsive.jpg)

Aviation Safety Reporting is a Django-based web application designed to improve aviation safety through voluntary, non-punitive incident reporting. Aviation professionals can submit safety reports, track investigation statuses, and collaborate through comments, fostering a culture of continuous safety improvement.

The system provides role-based access control, allowing regular users to submit and view reports, while investigators can manage investigation statuses and track safety trends through comprehensive dashboards.

**Live Site:** [Aviation Safety Reporting Application](https://aviation-safety-reporting-82b23530b80a.herokuapp.com/)

**Repository:** [GitHub Repository](https://github.com/GuilhermeAviacao/CI_Proj04_SafetyReporting)

---
## Features

The Aviation Safety Reporting System provides a comprehensive platform for safety incident reporting and investigation management. Below are the main features of the application:

### Home / About Page
![Home / About Page](documentation/Page_About.jpg)
![Home / About Page2](documentation/Page_About_2.jpg)
The landing page introduces users to the Aviation Safety Reporting System and its mission.

**Key Features:**
- **Non-Punitive Philosophy**: Clearly communicates the voluntary, confidential nature of safety reporting
- **Aviation Safety Context**: Explains the importance of incident reporting in improving aviation safety
- **Call-to-Action**: Prominent links to register, login, or view safety reports
- **Professional Design**: Clean, aviation-themed layout with responsive navigation
- **User-Friendly Navigation**: Easy access to all key sections (Board, Investigations, Create Report)

### Board Page (Latest Safety Reports)
![Board Page](documentation/Page_Board.jpg)
The central hub displaying all submitted safety reports in an organized, searchable format.

**Key Features:**
- **Card-Based Layout**: Each report displayed in a visually distinct card with key information
- **Color-Coded Status Badges**:
  - Blue: Waiting investigation
  - Yellow: Under investigation
  - Grey: Investigation closed
  - Dark: Dismissed
- **Search Functionality**: Real-time search to filter reports by location, description, or status
- **Pagination**: Displays 6 reports per page for optimal viewing experience
- **Quick Information**: Each card shows:
  - Report location (airport/airspace)
  - Incident date and time
  - Report author
  - Investigation status
  - Creation timestamp
- **Responsive Grid**: 3-column layout on desktop, automatically stacks on mobile devices
- **Click-Through Access**: Click any card to view full report details

### Report Detail Page
![ReportDetail Page](documentation/Page_ReportDetail.jpg)
![ReportDetail Page 2](documentation/Page_ReportDetail_2.jpg)
Comprehensive view of individual safety reports with collaboration features.

**Key Features:**
- **Complete Report Information**:
  - Full incident description
  - Location, date, and time details
  - Report author information
  - Creation and last update timestamps
- **Investigation Status Management** (Role-Based):
  - Regular users see status as a badge (read-only)
  - Investigators can update status via dropdown menu
  - AJAX-powered updates without page reload
- **Collaborative Comments Section**:
  - Real-time discussion thread for each report
  - Comment authorship tracking with timestamps
  - Edit/Delete controls (only for comment authors)
  - Inline comment form for seamless interaction
- **Ownership Controls**:
  - Authors can edit/delete their own comments
  - Visual indicators for user's own comments
- **Update Notifications**: Alert banner shows when report status was last modified
- **Responsive Layout**: Optimized for desktop, tablet, and mobile viewing

### Create Report Page
![Create Report Page](documentation/Page_CreateReport.jpg)
Secure, user-friendly form for submitting new safety incidents.

**Key Features:**
- **Authentication Required**: Only logged-in users can submit reports
- **Structured Form Fields**:
  - **Place**: Location of incident (airport code, airspace, etc.)
  - **Date**: Calendar picker for incident date
  - **Time**: Time picker for precise incident timing
  - **Description**: Large text area for detailed incident narrative
  - **Image Upload** (Optional): Attach supporting visual evidence
- **Form Validation**:
  - Required field indicators (*)
  - Real-time client-side validation
  - Server-side validation for data integrity
  - Clear error messages for invalid inputs
- **Helper Text**: Guidance prompts to help users provide complete information
- **Confidentiality Notice**: Reassurance about non-punitive nature and data privacy
- **Cancel/Submit Controls**: Clear action buttons with confirmation
- **Automatic Attribution**: Report automatically linked to authenticated user
- **Success Redirect**: Upon submission, redirects to the new report detail page

### Investigation Dashboard Page
![Investigations Page](documentation/Page_Investigations.jpg)
- Visual statistics with Chart.js doughnut chart
- Status distribution breakdown
- Total report count and percentages
- Quick overview of investigation workload

### Additional Features

**Role-Based Access Control:**
- **Regular Users**: Submit reports, view all reports, comment, manage own comments
- **Investigators**: All regular user permissions + update investigation status + access dashboard
- **Administrators**: Full system access including user management

**User Authentication:**
- Secure registration and login via Django Allauth
- Password reset functionality
- Session management
- Profile management

---

## Wireframes

The wireframes were created using Balsamiq to plan the structure and user flow before development.

### Key Pages:

#### 1. Board Page (Report Listings)
![Latest Safety Reports Wireframe](documentation/1%20-%20Balsamiq%20-%20Latest%20Safety%20Reports.jpg)

- Card-based layout for easy scanning of safety reports
- Color-coded status badges for quick visual identification
- Search functionality for filtering reports
- Responsive grid layout (3 columns on desktop, stacks on mobile)

#### 2. Report Detail Page
![Safety Report Details Wireframe](documentation/2%20-%20Balsamiq%20-%20Safety%20Report%20Details.jpg)

- Clear hierarchy: Report details → Comments → Action area
- Status management (dropdown for investigators, badge for users)
- Inline comment form for seamless collaboration
- Edit/Delete controls restricted to comment authors

#### 3. Investigations Dashboard
![Investigation Status Overview Wireframe](documentation/3%20-%20Balsamiq%20-%20Investigation%20Status%20Overview.jpg)

- Summary banner showing total report count
- Status cards with counts and percentages
- Visual distribution via Chart.js doughnut chart
- Color-coded progress indicators

#### 4. Create Report Form
![Create Safety Report Wireframe](documentation/4%20-%20Balsamiq%20-%20Create%20Safety%20report.jpg)

- Structured form with clear field labels
- Helper text to guide users
- Confidentiality notice to encourage reporting
- Bootstrap validation styling


---

## Database Design

The database schema was designed to support role-based access control, investigation tracking, and collaborative commenting. The system uses Django's built-in User model extended with a custom UserProfile for role management.

### Entity Relationship Diagram

#### Overview of Relationships
![ERD Relationships Overview](documentation/ERD_0_Relationships.jpg)

The database consists of four main entities:

#### 1. User Authentication
![User Model ERD](documentation/ERD_Detailed_1_Auth.jpg)

- Django's built-in User model handles authentication
- Stores username, email, password (hashed), and account status

#### 2. User Roles & Profiles
![UserProfile Model ERD](documentation/ERD_Detailed_2_Roles.jpg)

- One-to-One relationship with User model
- Role choices: Regular User, Investigator, Administrator
- Auto-created via Django signals on user registration

#### 3. Safety Reports
![SafetyReport Model ERD](documentation/ERD_Detailed_3_Report.jpg)

- Many-to-One relationship with User (author)
- Stores incident details: location, date, time, description
- Investigation status tracking: Waiting, Investigating, Closed, Dismissed
- Timestamps for audit trails (created_at, updated_at)

#### 4. Comments
![Comment Model ERD](documentation/ERD_Detailed_4_Comment.jpg)

- Many-to-One relationship with SafetyReport
- Many-to-One relationship with User (author)
- Enables collaborative discussion on reports
- Edit/delete permissions restricted to comment authors

---

## Agile Development Process
- Link to [Git Hub Project Management](https://github.com/users/GuilhermeAviacao/projects/3)
- Usage of GitHub Projects & Issues to store the User Stories and assign their progress in a Kanban style progress tracker. 
![User Stories](documentation/User_Stories.jpg)

---

## Testing

Full documentation on [TESTING.md](TESTING.md)

---

## Known Issues

Due to scope limitation, this project deliberately didn't add the option for a user to recover a forgotten password, as it would require some e-mail service to send it. 

---

## Deployment

This section covers the deployment process, including Cloudinary API setup, Heroku deployment, and local development options.

### Cloudinary API Setup

This project uses the [Cloudinary API](https://cloudinary.com/) to store media assets online, as Heroku doesn't persist uploaded images and files.

**Configuration Steps:**
1. Create a free account at [Cloudinary](https://cloudinary.com/)
2. Select **Programmable Media** for images and video API
3. Optionally customize your cloud name
4. Navigate to your Dashboard and copy the **API Environment Variable**
5. Remove the `CLOUDINARY_URL=` prefix from the copied value - you only need the portion after the equals sign

---

### Heroku Deployment

The application is deployed on [Heroku](https://www.heroku.com/), a cloud platform for hosting web applications.

#### Initial Setup

1. Log in to your Heroku account
2. Click **New** in the top-right corner of the dashboard
3. Select **Create new app**
4. Enter a unique app name (e.g., `aviation-safety-reporting`)
5. Choose your region (Europe or United States)
6. Click **Create app**

#### Environment Variables Configuration

1. Navigate to the **Settings** tab of your Heroku app
2. Click **Reveal Config Vars**
3. Add the following environment variables:

| Key | Value |
|-----|-------|
| `CLOUDINARY_URL` | Your Cloudinary API URL (without the `CLOUDINARY_URL=` prefix) |
| `DATABASE_URL` | Automatically added by Heroku Postgres addon |
| `SECRET_KEY` | Your Django secret key (generate a secure random string) |
| `DISABLE_COLLECTSTATIC` | `1` (temporary, can be removed after first deployment) |

**Note:** Never commit sensitive keys to your repository. Always use environment variables.

#### Required Files

Ensure your repository contains:
- **requirements.txt**: Lists all Python dependencies
- **Procfile**: Tells Heroku how to run your application
  ```
  web: gunicorn your_project_name.wsgi
  ```

#### Deployment Methods

**Option 1: Automatic Deployment (Recommended)**
1. Navigate to the **Deploy** tab in your Heroku app
2. Select **GitHub** as the deployment method
3. Connect to your GitHub repository
4. Enable **Automatic Deploys** from your main branch
5. Click **Deploy Branch** for the initial deployment

**Option 2: Heroku CLI**
1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Open your terminal and navigate to your project directory
3. Log in to Heroku:
   ```bash
   heroku login -i
   ```
4. Connect your local repository to the Heroku app:
   ```bash
   heroku git:remote -a your-app-name
   ```
5. Deploy your code:
   ```bash
   git push heroku main
   ```

For additional deployment documentation, refer to the [Heroku Dev Center](https://devcenter.heroku.com/categories/deployment).

---

### Local Deployment

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

#### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GuilhermeAviacao/CI_Proj04_SafetyReporting.git
   cd CI_Proj04_SafetyReporting
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Create environment file:**
   Create a file named `env.py` at the root level of your project with the following content:
   ```python
   import os

   os.environ['CLOUDINARY_URL'] = 'your_cloudinary_url_here'
   os.environ['DATABASE_URL'] = 'your_database_url_here'
   os.environ['SECRET_KEY'] = 'your_secret_key_here'
   os.environ['DEBUG'] = 'True'  # Only for local development
   ```

   **Important:** Ensure `env.py` is listed in your `.gitignore` file to prevent committing sensitive data.

4. **Run initial server test:**
   ```bash
   python3 manage.py runserver
   ```
   Stop the server with `CTRL+C`

5. **Apply database migrations:**
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

6. **Create superuser account:**
   ```bash
   python3 manage.py createsuperuser
   ```
   Follow the prompts to set up your admin account.

7. **Load initial data (if applicable):**
   ```bash
   python3 manage.py loaddata fixtures_file_name
   ```

8. **Start the development server:**
   ```bash
   python3 manage.py runserver
   ```

   Access the application at `http://127.0.0.1:8000/`

---

### Forking the Repository

Forking creates a personal copy of the repository in your GitHub account.

1. Navigate to the [repository](https://github.com/GuilhermeAviacao/CI_Proj04_SafetyReporting)
2. Click the **Fork** button in the top-right corner
3. Select your GitHub account as the destination
4. You now have a complete copy to experiment with

---

### Cloning the Repository

Cloning downloads the repository to your local machine.

**Using HTTPS:**
```bash
git clone https://github.com/GuilhermeAviacao/CI_Proj04_SafetyReporting.git
```

**Using SSH:**
```bash
git clone git@github.com:GuilhermeAviacao/CI_Proj04_SafetyReporting.git
```

**Using GitHub CLI:**
```bash
gh repo clone GuilhermeAviacao/CI_Proj04_SafetyReporting
```




---
## Credits

Code and troubleshooting assistance with Anthropic Claude (Sonnet 4.1 and 4.5 models).
Especially for the AJAX real-time drop-down page update solution. https://claude.ai/

Read-me inspired by former Code Institute student - Adam Shaw. 
https://github.com/adamshaw90/Trip-easy?tab=readme-ov-file

### Media

Images sourced from [Pixabay](pixabay.com). 
All are open source and free for use under the Pixabay [content license](https://pixabay.com/service/license-summary/).

| Legend                      | Link                                                                          |
|-----------------------------|-------------------------------------------------------------------------------|
| Car in a runway             | https://pixabay.com/sv/photos/runway-flygf%C3%A4lt-flygplats-landning-1227526/|
| Cockpit view of PAPI lights | https://pixabay.com/photos/cockpit-aircraft-runway-flying-4598188/            |
| Airside Vehicle             | https://pixabay.com/photos/bird-watch-vehicle-schiphol-airport-9102           |
| Runway Lights               | https://pixabay.com/photos/green-laser-light-rays-light-games-1757807/        |
| Drone                       | https://pixabay.com/photos/aerial-aeroplane-aircraft-airplane-8334932/        |
| Airport Tower               | https://pixabay.com/photos/airport-radar-airport-radar-tower-6599447/         |
| Aircraft Accident           | https://pixabay.com/photos/plane-crash-accident-bad-landing-514783/           |
| Helicopter Rescue           | https://pixabay.com/photos/pzl-w-3-sok%C3%B3%C5%82-czech-air-force-8274644/   |
| Fighter Aircraft            | https://pixabay.com/photos/helicopter-agustawestland-aw189-7485942/           |
| Aircraft Cabin              | https://pixabay.com/photos/aircraft-cabin-airplane-cabin-5535467/             |
| Glider                      | https://pixabay.com/photos/glider-aviation-cabin-aircraft-613205/             |

## Acknowledgements
I would like to thank the Code Institute team for the feedback that led to the final version of this project.