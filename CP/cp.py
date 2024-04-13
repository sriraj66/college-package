from openai import OpenAI
from CP.constants import *
from CP.models import College


class CMAP:
    
    def __init__(self,uid) -> None:
        self.prompt = ""
        self.clg = College.objects.get(uid=uid)
        
        self.client = OpenAI(api_key=self.clg.api_key) 
        self.messages = [
            {"role": "system", "content": "You are a helpful mentor to provide guidance for my career."},
            {"role": "system", "content": f"Output should be like a structured Json in this format {ft}"},
        ]
        

    def set_prompt(self,name,major,branch,sBranch,subject,syllbus,tp,pd):
        self.prompt =  f"""
            Lecturer info:
            Name : {name}
            Major : {major} {branch}

            Student Branch : {sBranch}.


            Subject : {subject}.

            Syllabus : {syllbus}
            Total Periods of classes : {tp}.
            Period Duration : {pd} min

            Give me a  road map to complete the syllabus to the students in a given Class periods and hints to take the class Efectively.

            Add atleast one for each topics some youtube,corsera and other to learn the concepts.
            and Give atleast one Linked in profiles related to the topics.
            """
        self.messages.append({"role": "user", "content": self.prompt})
                    
        return True

    def generate(self):
        print("Generating...")
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                response_format={ "type": "json_object" },
                messages=self.messages,
                )
            
            return response.choices[0].message.content
        except Exception as e:
            return str(e)