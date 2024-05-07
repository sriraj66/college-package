from openai import OpenAI
from CG.constants import *

class Career_Tool:
    def __init__(self,request,api_key) -> None:
        self.prompt = ""
        self.request = request
        self.key = api_key
        self.client = OpenAI(api_key=self.key)
        if "ct_message" not in self.request.session:
            self.messages = []
        else:
            self.messages = self.request.session["ct_message"]
    
    def self_assement(self,s,ts,fr):
        self.prompt = PROMPT1.format(s,ts,fr)
        
        self.messages = [
            {"role": "system", "content": "You are a Career Guide to the Students. You have to Suject the Job Titles and Help the student to build their skills and optimize the linked in profile"},
            {"role": "user", "content": self.prompt},
        ]
        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=self.messages
        )
        output =  response.choices[0].message.content
        
        self.messages.append({"role":"assistant","content":output})
        self.request.session["ct_message"] = self.messages
        return output
    
    def generate_final(self,ipic,role,workspace,loc,ps,gc):
        print('Final')
        self.prompt = PROMPT2.format(ipic,role,workspace,role,loc,ps,gc)
        self.messages.append({"role": "user", "content": self.prompt})
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        output =  response.choices[0].message.content
        
        self.messages.append({"role":"assistant","content":output})
        # print(self.messages)
        self.request.session["ct_message"] = self.messages

        return output
    
    def generate_linked_in(self,name,bio):
        print("Linked IN")
        self.prompt = PROMPT3.format(name,bio)
        self.messages.append({"role": "user", "content": self.prompt})
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        output =  response.choices[0].message.content
        
        self.messages.append({"role":"assistant","content":output})
        
        self.request.session["ct_message"] = self.messages

        return output
    
    def write_modes(self,name,bio,mode,con):
        self.prompt = PROMPT4.format(mode,name,bio,con)
        self.messages.append({"role": "user", "content": self.prompt})
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        output =  response.choices[0].message.content
        
        self.messages.append({"role":"assistant","content":output})
        
        self.request.session["ct_message"] = self.messages

        return output
    
    