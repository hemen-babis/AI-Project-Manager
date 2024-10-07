import google.generativeai as genai

class GeminiAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)

    def ask_question(self, question):
        try:
            # Initialize the Gemini model
            model = genai.GenerativeModel('gemini-pro')

            # Generate a response to the question
            response = model.generate_content(question)
            return response.text  # Returns the response from the Gemini API
        except Exception as e:
            return str(e)  # Return the error message if something goes wrong

def ask_question(self, question):
    print(f"Asking the question: {question}")
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-pro')

        # Generate a response to the question
        response = model.generate_content(question)
        print(f"Response: {response.text}")
        return response.text  # Returns the response from the Gemini API
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return str(e)  # Return the error message if something goes wrong
