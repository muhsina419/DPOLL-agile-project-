# 🗳️ DPOLL: Decentralized Voting System

> A secure, scalable, and user-friendly web application designed to modernize and safeguard the electoral process.

---

## 📌 Project Overview

`dpoll` is a decentralized digital voting platform built using Django and PostgreSQL with a modern frontend stack. The system is engineered to deliver secure, transparent, and accessible elections for institutions, organizations, or governments. It is cloud-deployment ready and follows agile methodologies for easy scalability, extensibility, and maintenance.

---

## 🌟 Key Features

### 🔐 Voter Registration
- **Two-Factor Verification**: Password and OTP verification for secure sign-up.
- **Identity Uploads**: Aadhaar card, photo, and phone number for validation.
- **Unique Voter ID**: Auto-generated unique ID for all interactions.
- **SMS Notifications**: Real-time updates via Twilio.

### 🔓 Voter Login
- **Two-Factor Authentication (2FA)**: Voter ID + password + OTP via SMS.

### 🧾 Voters & Candidates List
- **Admin View**: List of all verified voters.
- **Candidate Details**: Profiles and manifestos displayed for voters.

### 📝 Update Voter Details
- **Edit Options**: Voters can update address, phone number, etc.
- **SMS Alerts**: Confirmation via SMS for all updates.
- **Audit Logs**: Tracks all changes for transparency.

### 🗳️ Polling System
- **Anonymous Voting**: Prevents double voting, maintains voter privacy.
- **Blockchain Integration**: Immutable vote storage for verification and trust.

### 📊 Live Updates
- **Real-Time Histograms**: Visual polling data for voters and admins.

### 🏆 Results Page
- **Interactive Results**: Final outcomes displayed clearly post-voting.

### 🛠️ Admin Dashboard
- **Centralized Management**: 
  - Approve/reject voter registrations.
  - Add/remove candidates.
  - Monitor polling.
  - Manage election phases.
  - Generate audit and voting reports.

---

## 🧰 Tech Stack

| Layer       | Technologies Used                          |
|-------------|---------------------------------------------|
| Frontend    | HTML, CSS, JavaScript                      |
| Backend     | Python Django, Django REST Framework       |
| Database    | PostgreSQL                                 |
| Auth/SMS    | Twilio (OTP, SMS notifications)            |
| Environment | dotenv (.env for secret keys)              |
| Agile       | jira , trello , Google workspace           |
| Deployment  | AWS-ready (EC2, RDS, etc.)                 |
| Extras      | Blockchain module, Biometric integration (planned) |

---

## 📁 Project Structure

```bash
agile-project/
│
├── dpoll/                  # Django project configurations
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── myprojectdpoll/         # Main Django app logic
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── ...
│
├── templates/              # HTML Templates
├── static/                 # Static Assets (CSS, JS, Images)
├── media/                  # Uploaded files (photos, docs)
├── requirements.txt        # Python Dependencies
└── manage.py               # Django CLI Entry Point
```
## 🌀 Agile Workflow

- 🔁 **Modular Iterations**: New features and improvements are added via sprints.
- 🔧 **Extensibility First**: Biometric login, advanced analytics, or regional voting rules can be added easily.
- 📋 **Jira Board**: [View Our Agile Board](https://muhsinamohammedkutty2003.atlassian.net/jira/software/projects/DPOL/boards/4/backlog)

---

## 💻 Installation & Setup

### 🔧 Prerequisites

- Python 3.x  
- PostgreSQL  
- Node.js (for advanced frontend features)  
- Twilio account (for OTP/SMS)

---

### 🧪 Local Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/dpoll.git
cd dpoll

# Create a virtual environment
python -m venv env
source env/bin/activate  # On Windows use: .\env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Start development server
python manage.py runserver
## 🎥 Project Demo
```
📺 **Video Demo**: 
[Watch Here]()  

---

## 👥 Team DPOLL

A couple of aspiring innovators from the **Department of Computer Science CUSAT**.

### 👩‍💼 Member 1: Muhsina Beegum  
**Contributions**: Designing, Documentation, Backend Integration, GitHub, Deployment, Product Management, and more.

### 👩‍💻 Member 2: Abhinandana T U  
**Contributions**: Frontend development (HTML/CSS/JS), Database Logic & Integration, Initial Project Setup.

---

## 🤝 Contribution

Contributions, issues, and feature requests are welcome!  
Feel free to **fork** the repository, **create a new branch**, and **submit a pull request**.

---

## ❤️ Acknowledgements

Special thanks to:

- Our mentors and peers for their constant support, guidance, and feedback.

> “Let your vote count – securely, anonymously, and forever immutable.”

---

**Made with 🖤 by Team DPOLL**
