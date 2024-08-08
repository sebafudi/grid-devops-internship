import requests
import json
import argparse

# Function to create a survey
def create_survey(survey_data, headers):
    # Extract survey name and pages
    survey_name = list(survey_data.keys())[0]
    pages = survey_data[survey_name]

    # Create survey
    survey_payload = {
        'title': survey_name,
    }
    
    response = requests.post(f'{BASE_URL}/surveys', headers=headers, json=survey_payload)
    survey = response.json()
    survey_id = survey['id']
    
    print(f'Survey "{survey_name}" created with ID: {survey_id}')

    # Create pages and questions
    for page_name, questions in pages.items():
        page_payload = {
            'title': page_name,
        }
        response = requests.post(f'{BASE_URL}/surveys/{survey_id}/pages', headers=headers, json=page_payload)
        page = response.json()
        page_id = page['id']
        
        print(f'Page "{page_name}" created with ID: {page_id}')

        for question_name, details in questions.items():
            question_payload = {
                'headings': [{'heading': question_name}],
                'family': 'multiple_choice',
                'subtype': 'vertical',
                'answers': {
                    'choices': [{'text': ans} for ans in details['Answers']]
                }
            }
            
            response = requests.post(f'{BASE_URL}/surveys/{survey_id}/pages/{page_id}/questions', headers=headers, json=question_payload)
            question = response.json()
            question_id = question['id']
            
            print(f'Question "{question_name}" created with ID: {question_id}')
    
    return survey_id

# Function to create a collector
def create_collector(survey_id, headers):
    collector_payload = {
        'type': 'email',
        'name': 'Email Collector'
    }
    response = requests.post(f'{BASE_URL}/surveys/{survey_id}/collectors', headers=headers, json=collector_payload)
    collector = response.json()
    print(collector)
    collector_id = collector['id']
    
    print(f'Collector created with ID: {collector_id}')
    
    return collector_id

# Function to add recipients to the collector
def add_recipients(collector_id, emails, headers):
    recipients_payload = {
        'contacts': [{'email': email} for email in emails]
    }
    response = requests.post(f'{BASE_URL}/collectors/{collector_id}/messages', headers=headers, json=recipients_payload)
    message = response.json()
    message_id = message['id']
    
    print(f'Recipients added, Message ID: {message_id}')

# Main function
def main(access_token, survey_json_file, email_file):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    with open(survey_json_file, 'r') as f:
        survey_data = json.load(f)
    
    with open(email_file, 'r') as f:
        emails = [line.strip() for line in f.readlines()]

    survey_id = create_survey(survey_data, headers)
    collector_id = create_collector(survey_id, headers)
    add_recipients(collector_id, emails, headers)

# Command-line argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a survey and add recipients using SurveyMonkey API.")
    parser.add_argument('-t', '--token', required=True, help="SurveyMonkey API access token")
    parser.add_argument('-s', '--survey', required=True, help="Path to the JSON file containing the survey questions")
    parser.add_argument('-e', '--emails', required=True, help="Path to the text file containing the email addresses of recipients")

    args = parser.parse_args()

    BASE_URL = 'https://api.surveymonkey.com/v3'

    main(args.token, args.survey, args.emails)
