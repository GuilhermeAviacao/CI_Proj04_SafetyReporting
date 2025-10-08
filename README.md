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
  - 🔵 Blue: Waiting investigation
  - 🟡 Yellow: Under investigation
  - ⚫ Grey: Investigation closed
  - ⚫ Dark: Dismissed
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
- GitHub Projects & Issues

![User Stories](documentation/User_Stories.jpg)

---

## Testing

Full documentation on [TESTING.md](TESTING.md)

---

## Credits

Code and troubleshooting assistance with Anthropic Claude (Sonnet 4.1 and 4.5 models).
Especially for the AJAX real-time drop-down page update solution. https://claude.ai/

Read-me inspired by former Code Institute student - Adam Shaw. 
https://github.com/adamshaw90/Trip-easy?tab=readme-ov-file