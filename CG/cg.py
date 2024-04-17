from openai import OpenAI
from CG.constants import *


class MAP:
    
    def __init__(self,api_key) -> None:
        self.prompt = ""
        self.key = api_key
        
        self.client = OpenAI(api_key=self.key) 
        self.messages = [
            {"role": "system", "content": "You are a helpful mentor to provide guidance for my career."},
            {"role": "system", "content": f"Output should be like a structured Json in this format {ft}"},
        ]
        

    def set_prompt(self,name,year,deg,branch,sd,dur,jd,loc,se,skills):
        self.prompt = f"""
                personal Info : 
                name : {name}
                I am studing {year}th Year in {deg} and {branch}.
                Short Description : {sd}

                These are all my personal information and my expectation.
                Give me a Career Guidance road map for my next {dur} Years to achive my
                dream job {jd} with my expected Salary {se} (Currency depends on Location) in {loc}.

                I am good at these skils:{skills} .
                
                Give me a road map for my Career with Duration.
                please give some courses in youtube,udemy,coursera and others platforms.
                And Give me atleat 5 and atmost 10 Indian or Tamilnadu Linked profiles to get mentorships and to connect to achive my job.
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