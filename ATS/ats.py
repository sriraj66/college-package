from openai import OpenAI
import pdfplumber
import requests
from io import BytesIO
import os, docx
class ATS:
    def __init__(self, api_key, pdf_path,job_description):
        self.key = api_key
        self.jd = job_description

        self.client = OpenAI(api_key=self.key)
        try:
            self.pdf_text = self.extract_pdf_text(pdf_path) if str(pdf_path).split('.')[-1]=='pdf' else self.extract_docx_text(pdf_path)
        except Exception as e:
            self.pdf_text = "Unable to Extract This is not and resume."
            print(e)
        self.messages = []

    def extract_pdf_text(self,pdf_url):
        with requests.get(pdf_url) as response:
            with pdfplumber.open(BytesIO(response.content)) as pdf:
                pdf_text = ""
                for page in pdf.pages:
                    pdf_text += page.extract_text()
        return pdf_text

    def extract_docx_text(self,docx_url):
        text = ""
        with requests.get(docx_url) as response:
            doc = docx.Document(BytesIO(response.content))            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        return text

    def evaluate(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are Going to chat About the PDF[Resume,CV] of the user .if it not look like a resume or cv Try to change the resume if not possible tell not looks like a resume docx.and Rate matching with the job description  Rate out of 10 and give some tips and accurate number. and make an accurate answer."},
                {"role": "system", "content": "The output must be in a json format with max of 400 characters if no error return null [score,tips,error,discription,myfeedback]"},
                {"role": "system", "content": "The output of the tips as a html list elemen. and tips has some emojies."},
                {"role": "user", "content": f"Here is the Resume  context : {self.pdf_text}"},
                {"role": "user", "content": f"Here is the Job Description context : {self.jd}"},
            ]
        )

        answer = response.choices[0].message.content

        return answer


def run(api_key, pdf_path,job_description):
    app = ATS(api_key, pdf_path,job_description)
    return app.evaluate()



jd = """
We are looking for a Python Developer to join our engineering team and help us develop and maintain various software products.

Python Developer responsibilities include writing and testing code, debugging programs and integrating applications with third-party web services. To be successful in this role, you should have experience using server-side logic and work well in a team.

Ultimately, you'll build highly responsive web applications that align with our business needs.

Responsibilities
Write effective, scalable code
Develop back-end components to improve responsiveness and overall performance
Integrate user-facing elements into applications
Test and debug programs
Improve functionality of existing systems
Implement security and data protection solutions
Assess and prioritize feature requests
Coordinate with internal teams to understand user requirements and provide technical solutions
Requirements and skills
Work experience as a Python Developer
Expertise in at least one popular Python framework (like Django, Flask or Pyramid)
Knowledge of object-relational mapping (ORM)
Familiarity with front-end technologies (like JavaScript and HTML5)
Team spirit
Good problem-solving skills
BSc in Computer Science, Engineering or relevant field
"""

if __name__ == "__main__":
    assistant = ATS(os.getenv("key"), "test.pdf",job_description=jd)
    assistant.evaluate()