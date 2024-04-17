from smcg import constants
from openai import OpenAI
import requests, json
from smcg.models import *
from core.models import *
from django.urls import reverse


def get_past_data(url, uuid, query):
    data = {'uuid': uuid, 'query': "Details about " + query}
    response = requests.post(url, data=data)
    try:
        if response.status_code == 200:
            text = json.loads(response.text)
            
            return text
        else:
            print("POST request failed with status code:", response.status_code)
    except Exception as e:
        print(e)

    return False


class SMCG:

    def __init__(self, key, uid=None,is_past = False):
        self.uid = uid
        self.is_past = is_past
        self.client = OpenAI(api_key=key)
        self.past_data = None
        self.message = []


    def get_past(self,url, query):
        past = get_past_data(url=url,uuid=self.uid,query=query)
        return "No Past Data Found" if past is False else past['response']



    def get_content(self,request,platform,type,goal,topic,desc):
        domain = request.build_absolute_uri('/')
        url_path = reverse('api_get_responce')
        full_url = f'{domain.rstrip("/")}{url_path}'
        print(full_url)
        print(self.uid,self.is_past)
        if self.is_past == True and self.uid != None:
            self.past_data = self.get_past(full_url,f"{goal}  {topic}")
            # self.past_data = "No Past Data Found"
            # print("Past Data Called")

        if len(self.message) == 0:
            self.message = [
        {"role": "system", "content": "You are a Social media content Generator, Generate The description based on the [Data Record] Provided to You. if the record has no data generate own."},
        
        {"role":"user",'content': "[Data Record] : " + self.past_data if self.past_data is not None else "Dont Look at Past Data. No Data found Generate Own."},

        ]
        


        n = constants.PROMPT.format(platform,type,goal,topic,desc)
        self.message.append({
            "role": "user", "content": "if there is not sufficient data or None.  Generate own according to the Query." + n,
        })

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.message,
        )
        out = response.choices[0].message.content
        self.message.append({
                "role" : "system","content":out,
            })
        

        return out
