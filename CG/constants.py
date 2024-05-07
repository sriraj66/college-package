PROMPT1 = """
Identify 8 potential career goals and target companies using the Ikigai model, based on My interests and skills.
Consider your passions, such as {0} as well as 
skills like {1} and potential money-making markets 
such as {2}.
For each potential career goal, conduct an exploration of different industries, job roles, and organizations to gain insights into potential career paths.

Your sujestions should be structured and well-organized, with separate div, ul, h4 and 
li elements with class for li for all job roles.
Important Wrap all contents inside <div> element no text should be out of the div.
Dont give prefix Numbers inside <li>
dont use ```html all these. return only single div
Ensure that there are no line breaks present.
Your am response should provide detailed insights into each field,
including potential job roles and companies relevant to me, To identified career goals.
"""

PROMPT2 = """
Based on previous result, I want to Become a {0} 

Currently I am {1} at {2}
Location: {3}
Current: {4} 
Professional Skills: {5}, 
Global Certification: {6},

Set an specific, measurable, achievable, relevant, and time-bound (SMART) 
Short term goal [1-3 Years] and
Long Term Goal [5-10 years] in the following Format

Career Designation:
Location:
Industry:
Compensation Level (Range):
Professional Skills:
Personal Skills (Soft Skills):
Domain:

Based on my Short and Long term Goal, I want to Develop my Skill set and need to succeed in my domain,
Identify the Skill Set and create a plan to acquire or strengthen those skills through coursework,
internships, workshops, or extracurricular activities  and keep it  as a bullet point.
Output Should be in  structured and well-organized, with separate miltiple div inside single div and 
ul,li elements with class for all li for all job roles.
Ensure that there are no line breaks present.
your am response should provide detailed insights.
Important Wrap all contents inside <div> element no text should be out of the div.
dont use ```html all these. return only single div
"""


PROMPT3 = """
My self {0},  Here I attach my Information 
Information : {1},
Output should contain:
 - Linked In Head line minimus of 3 lines
 - About section for LinkedIn Profile with Keywords minimum of 4 lines.
 - Craft me a good message to send to a LinkedIn connection request message for someone to make them a potential mentor, expressing my interest in their guidance. Keep the tone formal and limit the words to 100 maximum.End with Regards.

These Elements are inside a single div containing seperate div inside ul,li,p heading h4 tags with classes.
Ensure that there are no line breaks present.
your response should provide detailed insights.
Important Wrap all contents inside <div> element no text should be out of the div.
dont use ```html all these. return only single div
"""


PROMPT4 = """
Write a 3 line {0} note to {1}
Reciptant Bio :  {2}.
For My Bio : Extract The Headline and Bio For this Context {3}.
These Elements are inside a single div containing seperate div inside ul,li,p heading h4 tags with classes.
Ensure that there are no line breaks present.
your response should provide detailed insights.
Important Wrap all contents inside <div> element no text should be out of the div.
dont use ```html all these. return only single div
"""
