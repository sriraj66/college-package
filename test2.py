PLATFORM = [
    "Facebook","Twitter","Youtube","Instagram","Linkedin"]

TYPE = [
    "Image","Video","Small Article","Live","Story","Infographic","Testimonial","Quote"]

GOAL = [
    "Convince","Educate","Inspire","Important_days","Holidays"
]

IDEA = {
    "Convince":[
    "Infrastructure","Interior environment","Teachers' qualification","Healthcare Facilities",
    "Fitness Facilities","Hostel facilities","Parking space","Internet facility","Access to class recordings","E-coaching services","Library facility",
    "Virtual Lab Facility","Health and Wellness","Students view of Virtual Learning @our institute"
    ],
    "Educate":[
        "Events you organize","Existing student's portfolio","Fee structure","Psychological support","Ethical standards","Hand-outs and mock tests","Your vision","Your mission",
        "Awareness factor","Trust factor","Meetups","How to write Resume","How to attend Interview","How to use LinkedIn","Tips for Job Searching","Job Opportunities in your Domain",
        "Video Interview Tips","Employability skills","Different between profile and resume","Tips for Writing LinkedIn Summaries","What is Job Description-JD?","What is Application Tracking System",
        "Type of Resume","Normal CV","Visual CV","Video CV (Elevator Pitch)","Match JD with CV","Type of Interview","During Interview","Post Interview","Career Opportunities after +2","Organize Hackathon",
    ],
    "Inspire":[
        "Testimonials","Readerships","Scholarships","Networking opportunities","Leadership Opportunities","Past years' success records","Students placements","Use of technology",
        "Webinars","Awards","Recognitions","Students' achievements","Sports events and achievements","Accreditation","Practical viability","Congratulations Note for Students",
        "Congratulations Note for Faculties","Details of MoU","Alumni Talk","Internship","Curricular opportunities","Extracurricular opportunities","Counselors' behavior and talking"
    ],
    "Important_days":[
        "National Youth Day","National Science Day","International Red Cross Day","National Technology Day","International Women's Day","World Health Day","International Yoga Day",
        "National Doctors Day","World Environment Day","World Population Day","National Sports Day","Teacher's Day","World Tourism Day","United Nations Day","Human Rights' Day","National Voters' Day",
        "National Consumers' Day","International Non-violence Day","Indian Air Force Day","World Food Day","National Education Day","Children's Day","National Integration Day"
    ],
    
    "Holidays":["Republic Day","Independence Day","Gandhi Jayanti","Christmas Day","Diwali","Eid al-Fitr (Ramadan)","Eid al-Adha (Bakrid)","Gandhi Jayanti","Ayudha Pooja",
                "Maha Navami","Dussehra","New Year's Day","Pongal","Thaipusam","Republic Day","Rama Navami","Ambedkar Jayanti","Telugu New Year's Day","Tamil New year's Day","Good Friday",
                "May Day","Muharram","Independence Day","Krishna Jayanthi","Vinayakar Chaturthi","Vijaya Dasami"
    
    ],
    
}



PROMPT = """
write a social media post for the following context.
PLATFORM={0},TYPE = {1},GOAL = {2} ,TOPIC = {3},DESCRIPTION = {4}

use simple and professional way of writing.
add emojies if want

Ruelse:
The size of the output is depends upon the TYPE and PLATFORM

complete the result with related hashtags.

"""

from openai import OpenAI
from constants import key
from template import *


import requests,json

def get_past_data(url,uuid,query):
    data = {'uuid': uuid, 'query': "Details about "+ query}
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



client = OpenAI(api_key = key)
past_rec = get_past_data(url='http://127.0.0.1:8000/api/get_responce',uuid='96dc4f88-e912-4cb5-937a-5a2adb0fdfa5',query="Placement Details")

message = [
    {"role": "system", "content": "You are a Social media content Generator, Refer the past data for more information"},
    {"role":"user",'content': "Past record : " + past_rec["response"]},
    
    {"role": "user", "content": qus1},
    {"role": "system", "content": res1},
 
    {"role": "user", "content": QUERY},
    {"role": "system", "content": RESPONCE},
 
  ]


while 1:

    plat = input("Platform : ")
    type = input("Type : ")
    goal = input("Goal : ")
    topic = input("Topic : ")
    desc = input("Description : ")
    
    past_rec = get_past_data(url='http://127.0.0.1:8000/api/get_responce',uuid='96dc4f88-e912-4cb5-937a-5a2adb0fdfa5',query=topic)
    message.append({
        "role" : "user","content":"Past record : " + past_rec["response"],
    })
    n = PROMPT.format(plat, type, goal, topic,desc)
    
    message.append({
        "role" : "user","content":"if there is not sufficient data make over the data, for the questions ."+n,
    })
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages= message,
    )
    
    out = response.choices[0].message.content
    
    
    message.append({
        "role" : "system","content":out,
    })
    print(out)