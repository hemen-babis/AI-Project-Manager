from flask import request, jsonify, render_template
from app import app, mongo
from .gemini_integration import GeminiAPI
import requests, json
import csv, re
from io import TextIOWrapper

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    try:
        file = request.files['team_csv']
        if not file:
            raise ValueError("No CSV file uploaded.")

        # Read the CSV file
        csv_file = TextIOWrapper(file, encoding='utf-8')
        reader = csv.DictReader(csv_file)

        team_members = []
        for row in reader:
            name = row.get('Name')
            email = row.get('Email')
            if not name or not email:
                raise ValueError("CSV format is incorrect. Ensure it contains 'Name' and 'Email' columns.")
            team_members.append({'name': name, 'email': email})

        # Insert team members into the project or send an email
        # For now, let's assume you're storing them and can return success
        return jsonify({'status': 'success', 'team_members': team_members})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Initialize the API
gemini_api = GeminiAPI(api_key=app.config['GEMINI_API_KEY'])

@app.route('/')
def index():
    return render_template('create_project.html')

# Helper function to send emails with Mailjet
def send_mailjet_email(recipient_email, recipient_name, subject, content):
    mailjet_api_key = app.config['MAILJET_API_KEY']
    mailjet_secret_key = app.config['MAILJET_SECRET_KEY']
    sender_email = app.config['MAIL_DEFAULT_SENDER']

    # Email data payload
    data = {
        "Messages": [
            {
                "From": {
                    "Email": sender_email,
                    "Name": "Project Manager"
                },
                "To": [
                    {
                        "Email": recipient_email,
                        "Name": recipient_name
                    }
                ],
                "Subject": subject,
                "HTMLPart": content
            }
        ]
    }

    try:
        response = requests.post(
            "https://api.mailjet.com/v3.1/send",
            auth=(mailjet_api_key, mailjet_secret_key),
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )
        response.raise_for_status()
        print(f"Email sent successfully to {recipient_name} ({recipient_email}). Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending email to {recipient_email}: {e}")

# Helper function to parse CSV for team members/clients
def parse_csv(file):
    team_list = []
    csv_reader = csv.reader(TextIOWrapper(file, encoding='utf-8'))
    for row in csv_reader:
        if len(row) == 2:
            team_list.append((row[0].strip(), row[1].strip()))  # (name, email)
    return team_list

@app.route('/start_project', methods=['POST'])
def start_project():
    try:
        data = request.form
        project_goal = data.get('goal')
        deadline = data.get('deadline')
        milestones = data.get('milestones').split(',')

        # Collect team members and clients from form or CSV
        team_list = []
        client_list = []

        # Process manually added team members
        for i in range(1, 100):  # Assuming a max of 100 members for now
            team_name = data.get(f'team_name_{i}')
            team_email = data.get(f'team_email_{i}')
            if team_name and team_email:
                team_list.append({'name': team_name, 'email': team_email})

        # Process uploaded team CSV
        team_csv = request.files.get('team_csv')
        if team_csv:
            team_list.extend(parse_csv(team_csv))

        # Process manually added clients
        for i in range(1, 100):
            client_name = data.get(f'client_name_{i}')
            client_email = data.get(f'client_email_{i}')
            if client_name and client_email:
                client_list.append({'name': client_name, 'email': client_email})

        # Process uploaded client CSV
        client_csv = request.files.get('client_csv')
        if client_csv:
            client_list.extend(parse_csv(client_csv))

        # Send emails to team members
        for team_member in team_list:
            team_email_subject = f"Your Involvement: {project_goal} - Deadline {deadline}"
            team_email_content = f"""
            <h1>Project Update</h1>
            <p>Dear <strong>{team_member['name']}</strong>,</p>

            <p>We are making progress on the project "<strong>{project_goal}</strong>". Here are the key updates:</p>

            <ul>
                <li><strong>Project Goal:</strong> {project_goal}</li>
                <li><strong>Deadline:</strong> {deadline}</li>
                <li><strong>Milestones:</strong> {', '.join(milestones)}</li>
            </ul>

            <p>Your contribution is crucial for the successful completion of this project. If you have any questions or need support, feel free to reach out.</p>

            <p>Best regards,<br>
            <strong>Project Manager</strong><br></p>
            """
            send_mailjet_email(team_member['email'], team_member['name'], team_email_subject, team_email_content)

        # Send emails to clients
        for client in client_list:
            client_email_subject = f"Project Update: {project_goal} - Progress and Milestones"
            client_email_content = f"""
            <h1>Project Update</h1>
            <p>Dear <strong>{client['name']}</strong>,</p>

            <p>We are excited to provide you with an update on the project "<strong>{project_goal}</strong>". Here are the current details:</p>

            <ul>
                <li><strong>Project Goal:</strong> {project_goal}</li>
                <li><strong>Deadline:</strong> {deadline}</li>
                <li><strong>Milestones:</strong> {', '.join(milestones)}</li>
            </ul>

            <p>We are committed to ensuring the success of this project. If you have any questions or require further clarification, please do not hesitate to reach out.</p>

            <p>Best regards,<br>
            <strong>Project Manager</strong><br></p>
            """
            send_mailjet_email(client['email'], client['name'], client_email_subject, client_email_content)

        # Insert project data into MongoDB
        project = {
            'goal': project_goal,
            'deadline': deadline,
            'team_members': team_list,
            'clients': client_list,
            'milestones': milestones
        }
        mongo.db.projects.insert_one(project)

        return jsonify({'status': 'success', 'message': 'Project created and emails sent successfully!'})

    except Exception as e:
        print(f"Error while creating the project: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    try:
        # Get the user's question
        question = request.form.get('question')

        # Fetch the most recent project from MongoDB (assuming there's a project context to include)
        project = mongo.db.projects.find_one(sort=[('_id', -1)])  # Get the latest project

        # Add context to the AI question if a project exists
        if project:
            industry = project.get('industry', 'general')  # Adding more context around the industry, if available
            # Context for the AI
            context = f"""
            You are a highly experienced project manager working in the {industry} industry. The project you're managing is called "{project['goal']}". 
            It has a deadline set for {project['deadline']}, with {len(project['team_members'])} team members working towards achieving key milestones, which include {', '.join(project['milestones'])}.
            Now, based on this project context, here's the question:
            """
            # Combine context with the user's question
            question_with_context = f"{context} {question}"
        else:
            # General prompt if no project is found
            question_with_context = f"I'm a project management expert. Let's get started. Here's the question: {question}"

        # Use Gemini API to get the response
        answer = gemini_api.ask_question(question_with_context)

        # Ensure the AI response doesn’t use unwanted characters like ** (bold markers)
        cleaned_answer = re.sub(r'\*', '', answer)
        cleaned_answer = cleaned_answer.replace('\n', '<br>')  # Replace new lines with HTML line breaks
        cleaned_answer = cleaned_answer.replace('•', '-')  # Replace bullet points with dashes
        

        # Ensure the response is professional and in a conversational tone
        humanized_answer = f"""
            <p>{cleaned_answer}</p>
            <p>Is there anything else you’d like help with? Feel free to ask me anything, and I’ll assist you to the best of my ability!</p>
        """
        
        # Return the more human-like response to the user
        return jsonify({'answer': humanized_answer})

    except Exception as e:
        # Log any exceptions and provide a meaningful error message
        print(f"Error in AI interaction: {e}")
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/projects')
def projects():
    try:
        projects = list(mongo.db.projects.find())
        return jsonify(projects)
    except Exception as e:
        print(f"Error retrieving projects: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to retrieve projects'})
