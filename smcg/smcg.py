from smcg import constants
from openai import OpenAI
import requests, json
from smcg.models import *
from core.models import *
from django.urls import  reverse
def get_past_data(url, uuid, query):
    data = {'uuid': uuid, 'query': "Details about " + query}
    response = requests.post(url, data=data)
    try:
        if response.status_code == 200:
            text = json.loads(response.text)
            print(text["response"])
            return text
        else:
            print("POST request failed with status code:", response.status_code)
    except Exception as e:
        print(e)

    return False


class SMCG:

    def __init__(self, uid,):
        self.uid = uid
        self.clg = College.objects.get(uid=uid)
        self.client = OpenAI(api_key=self.clg.api_key)
        self.past_data = ""
        self.message = []


    def get_past(self,url, query):
        past = get_past_data(url=url,uuid=self.uid,query=query)
        return "No Past Data Found" if past is False else past['response']



    def get_content(self,request,platform,type,goal,topic,desc):
        domain = request.build_absolute_uri('/')
        url_path = reverse('api_get_responce')
        full_url = f'{domain.rstrip("/")}{url_path}'
        print(full_url)
        self.past_data = self.get_past(full_url,f"{goal}  {topic}")

        if len(self.message) == 0:
            self.message = [
        {"role": "system", "content": "You are a Social media content Generator, Refer the past data for more information"},
        {"role":"user",'content': "Past record : " + self.past_data},

        {"role": "user", "content": constants.qus1},
        {"role": "system", "content": constants.res1},

        {"role": "user", "content": constants.QUERY},
        {"role": "system", "content": constants.RESPONCE},
        ]


        n = constants.PROMPT.format(platform,type,goal,topic,desc)
        self.message.append({
            "role": "user", "content": "if there is not sufficient data make over the data, for the questions ." + n,
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
