# AI Project Manager

AI Project Manager is a web-based tool designed to help manage projects with AI-powered assistance. This application allows users to create projects, track milestones, and interact with an AI assistant to handle project management queries. Additionally, it features automatic email notifications to team members and clients.

## Features

- **Project Creation & Management:** Add project goals, deadlines, milestones, team members, and clients.
- **AI Assistance:** Interact with the AI to get insights and advice related to your project.
- **Email Notifications:** Automatically send updates via Mailjet to team members and clients.
- **Chat with AI:** Chat interface to query project details or ask for management assistance.
- **CSV Uploads:** Easily manage large teams or clients by uploading their details via CSV.

## Installation

### Clone the repository:

```bash
git clone https://github.com/yourusername/ai-project-manager.git
```

### Navigate to the project directory:

```bash
cd ai-project-manager
```

### Set up and activate the virtual environment:

- On macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
- On Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

### Install the required packages:

```bash
pip install -r requirements.txt
```

### Set up environment variables:

Create a `.env` file in the project root and configure the following environment variables:

```
MAILJET_API_KEY=your_mailjet_api_key
MAILJET_SECRET_KEY=your_mailjet_secret_key
GEMINI_API_KEY=your_gemini_api_key
FLASK_APP=run.py
FLASK_ENV=development
```

### Run the application:

```bash
flask run
```

The application will be available at `http://127.0.0.1:5000/`.

## Usage

### Creating a Project

1. Navigate to the project creation form.
2. Fill out the project goal, deadlines, milestones, team members, and clients (manually or via CSV upload).
3. Click "Start Project" to create the project and trigger email notifications.

### Interacting with the AI

1. In the chat section, ask any project management-related question.
2. The AI will respond with information related to the project context.

## Project Structure

```
ai_project_manager/
│
├── app/
│   ├── __init__.py               # Flask app initialization
│   ├── routes.py                 # Routes for the application
│   ├── gemini_integration.py      # Integration with Gemini AI
│   └── templates/                # HTML templates for the frontend
│
├── static/                       # Static files (CSS, JS, images)
│
├── tests/                        # Unit tests
│
├── config.py                     # Application configuration
├── .env                          # Environment variables (not in version control)
├── .gitignore                    # Files to be ignored in git commits
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
└── run.py                        # Flask application entry point
```

## Technologies Used

- **Flask:** Backend framework to build and serve the application.
- **Mailjet API:** Email notifications to team members and clients.
- **Gemini API:** AI assistant to manage and answer project-related queries.
- **MongoDB:** Database used to store project information.
- **HTML/CSS (Bootstrap):** Frontend styling and responsive design.
- **JavaScript (AJAX):** Real-time interaction with the AI for a chat-like experience.
```
