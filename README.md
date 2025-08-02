💼 Odoo Help Desk - CGC Mohali Hackathon Submission
Odoo Help Desk (codenamed QuickDesk) is a simplified, yet powerful ticketing system that enables efficient issue tracking and resolution for users, agents, and administrators. Built for the Odoo x CGC Mohali Hackathon, this solution streamlines the support process while remaining intuitive and responsive.

🌟 Features
✅ End Users
Register/Login securely

Raise support tickets with:

Subject line

Description

Optional file attachments

View their tickets and check statuses

Add comments to ongoing tickets

View full ticket lifecycle (Open → In Progress → Resolved → Closed)

🛠️ Support Agents
View all submitted tickets

Comment on tickets

Update ticket status in real-time

Monitor ticket status history

Role-specific dashboard

🧑‍💼 Admins
Manage user roles

Control ticket categories (easily extendable)

Full access to ticket data for analytics or moderation

📁 Project Structure
csharp
CopyEdit
oddo/
├── app.py                 # Main Flask app
├── support.db             # SQLite3 database
├── templates/             # Jinja2 HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── create_ticket.html
│   └── ticket_detail.html
├── static/
│   └── style.css          # Responsive custom CSS
└── README.md              # This file
⚙️ Technologies Used
Backend: Flask (Python)

Database: SQLite3

Frontend: HTML5, CSS3 (Custom & Responsive)

Templating: Jinja2

Email: Simulated via print() logs for local demo

Deployment: Localhost (Flask debug=True)

🚀 How to Run Locally
1. Clone the repo
bash
CopyEdit
git clone https://github.com/showmi442/Odoo-Hackathon-Quick-Desk
cd oddo-helpdesk
2. Setup virtual environment (optional but recommended)
bash
CopyEdit
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
3. Install dependencies
bash
CopyEdit
pip install flask
4. Run the Flask app
bash
CopyEdit
python app.py
5. Access the web app
Open browser and navigate to http://localhost:5000

📌 Known Limitations
Email functionality is simulated (no SMTP/Gmail integration to avoid credentials exposure)

Notifications are stored but not visualized due to limited hackathon time

No advanced search/filter yet (can be extended post-hackathon)

📽️ Team & Demo Video
👩‍💻 Roles:
Shrowmika (Team Leader): Introduction + Admin functionalities

Sirisha: End User flows (Register, Ticket Raise, Status View)

Preetika: Agent Dashboard, Comments, and Ticket Lifecycle
