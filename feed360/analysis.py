from openai import OpenAI
from .models import Form,Analysis_with_exel


PROMPT = """
Conduct a comprehensive sentiment analysis on the given data frame, comprising feedback records from srudents or Users.
Identify and categorize the positive and negative comments from the feedback, while also suggesting improvements. and give positive persentage and negative percentage.
Organize this information using div elements exclusively.
Your analysis should be structured and well-organized, with separate div, ul, h4 and li elements with class for li for positive comments, negative comments, and improvement suggestions.
Important Wrap all contents inside <div> element no text should be out of the div.
dont use ```html all these. return only single div.
Ensure that there are no line breaks present. For each category of feedback, provide specific and relevant insights, offering actionable suggestions for improvement. 
Your analysis should have the flexibility to accommodate diverse types of feedback.

"""

class Analysis:
    
    def __init__(self,id,df,file=False):
        if file is False:
            self.form = Form.objects.get(id=id)
        else:
            self.form = Analysis_with_exel.objects.get(id=id)

        self.api_key = self.form.staff.college.api_key            
        self.client = OpenAI(api_key=self.api_key)
        self.messages = [
            {"role": "system", "content": "You are a data_scientist. and do Sentimntal analysis for the given Data Frame."},
            {"role": "user", "content": f"Here is the Data Frame {str(df)}"},
            {"role": "system", "content": PROMPT},
        ]
    
    def analysis(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        output =  response.choices[0].message.content
        return output