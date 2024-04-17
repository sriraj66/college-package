PLATFORM = [
    "Facebook", "Twitter", "Instagram", "Linkedin"]

TYPE = [
     "Small Article", "Description","Image", "Story", "Infographic", "Testimonial", "Quote"]

GOAL = [
    "Convince", "Educate", "Inspire", "Important_days", "Holidays"
]

IDEA = {
    "Convince": [
        "Infrastructure", "Interior environment", "Teachers' qualification", "Healthcare Facilities",
        "Fitness Facilities", "Hostel facilities", "Parking space", "Internet facility", "Access to class recordings",
        "E-coaching services", "Library facility",
        "Virtual Lab Facility", "Health and Wellness", "Students view of Virtual Learning @our institute"
    ],
    "Educate": [
        "Events you organize", "Existing student's portfolio", "Fee structure", "Psychological support",
        "Ethical standards", "Hand-outs and mock tests", "Your vision", "Your mission",
        "Awareness factor", "Trust factor", "Meetups", "How to write Resume", "How to attend Interview",
        "How to use LinkedIn", "Tips for Job Searching", "Job Opportunities in your Domain",
        "Video Interview Tips", "Employability skills", "Different between profile and resume",
        "Tips for Writing LinkedIn Summaries", "What is Job Description-JD?", "What is Application Tracking System",
        "Type of Resume", "Normal CV", "Visual CV", "Video CV (Elevator Pitch)", "Match JD with CV",
        "Type of Interview", "During Interview", "Post Interview", "Career Opportunities after +2",
        "Organize Hackathon",
    ],
    "Inspire": [
        "Testimonials", "Readerships", "Scholarships", "Networking opportunities", "Leadership Opportunities",
        "Past years' success records", "Students placements", "Use of technology",
        "Webinars", "Awards", "Recognitions", "Students' achievements", "Sports events and achievements",
        "Accreditation", "Practical viability", "Congratulations Note for Students",
        "Congratulations Note for Faculties", "Details of MoU", "Alumni Talk", "Internship", "Curricular opportunities",
        "Extracurricular opportunities", "Counselors' behavior and talking"
    ],
    "Important_days": [
        "National Youth Day", "National Science Day", "International Red Cross Day", "National Technology Day",
        "International Women's Day", "World Health Day", "International Yoga Day",
        "National Doctors Day", "World Environment Day", "World Population Day", "National Sports Day", "Teacher's Day",
        "World Tourism Day", "United Nations Day", "Human Rights' Day", "National Voters' Day",
        "National Consumers' Day", "International Non-violence Day", "Indian Air Force Day", "World Food Day",
        "National Education Day", "Children's Day", "National Integration Day"
    ],

    "Holidays": ["Republic Day", "Independence Day", "Gandhi Jayanti", "Christmas Day", "Diwali",
                 "Eid al-Fitr (Ramadan)", "Eid al-Adha (Bakrid)", "Gandhi Jayanti", "Ayudha Pooja",
                 "Maha Navami", "Dussehra", "New Year's Day", "Pongal", "Thaipusam", "Republic Day", "Rama Navami",
                 "Ambedkar Jayanti", "Telugu New Year's Day", "Tamil New year's Day", "Good Friday",
                 "May Day", "Muharram", "Independence Day", "Krishna Jayanthi", "Vinayakar Chaturthi", "Vijaya Dasami"

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

QUERY = """
write a social media post for the following context.
PLATFORM=Linkedin,TYPE = Small Article,GOAL = Educate ,TOPIC = Video Interview Tips

use simple and professional way of writing.
add emojies if want

Ruelse:
The size of the output is depends upon the TYPE and PLATFORM

complete the result with related hashtags.
"""


RESPONCE = """

🎥 Mastering Video Interviews: Top Tips for Success 🎬

As virtual interviews become increasingly common, it's essential to sharpen your skills to stand out from the crowd. Here are some key tips to help you ace your next video interview:

1️⃣ Dress professionally: Just because you're at home doesn't mean you can't dress the part. Opt for professional 
attire to make a strong first impression.

2️⃣ Test your tech: Ensure your internet connection is stable, and your camera and microphone are working correctly. Test them in advance to avoid any last-minute technical issues.

3️⃣ Choose the right setting: Find a quiet, well-lit space for your interview. Make sure your background is clean and 
clutter-free to maintain a professional appearance.

4️⃣ Practice makes perfect: Practice answering common interview questions in front of the camera. This will help you feel more comfortable and confident during the actual interview.

5️⃣ Pay attention to body language: Maintain good posture, make eye contact, and smile to convey confidence and enthusiasm. Remember, nonverbal cues are just as important in a virtual setting.

6️⃣ Follow up: Don't forget to send a thank-you email after the interview to express your gratitude and reiterate your interest in the position.

With these tips in mind, you'll be well-prepared to excel in your next video interview! 💼✨ #VideoInterviewTips #JobSearch #CareerAdvice #InterviewSuccess #ProfessionalDevelopment

"""

qus1 = """
write a social media post for the following context.
PLATFORM=linked in,TYPE = POST,GOAL = Inspire ,TOPIC = PLACEMENT DERAILS,DESCRIPTION = ""

use simple and professional way of writing.
add emojies if want

Ruelse:
The size of the output is depends upon the TYPE and PLATFORM

complete the result with related hashtags.
"""
res1  = """🎓 Celebrating Success! 🌟

We're thrilled to share the latest placement details from our talented pool of individuals:

🚀 Naveen has secured a prestigious role at TCS, marking a significant milestone in his career journey. His dedication and determination have led him to this remarkable achievement.

💼 Meanwhile, Ajay has embraced a new chapter at Infosys, where his skills and expertise will undoubtedly shine bright.

👏 Join us in congratulating Naveen and Ajay on their well-deserved successes! Their achievements serve as a testament to the limitless possibilities that await those who pursue their dreams with passion and perseverance.

#SuccessStory #CareerGrowth #Inspiration #TCS #Infosys #Congratulations #LinkedInSuccess #DreamBig"""



IMAGE_PROMPT = """

THEME : {0}

Text : Generate a Text from the Theme content

Font: according to the Text.

EXTRAS : {1}

Rules:
    If the Text is given. It should be present in the image.

Style: Minimalist, Clean, Classic.

"""
