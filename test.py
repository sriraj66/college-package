s = """ [
        {"role": "system", "content": "You are a Social media content Generator, Refer the past data for more information"},
        {"role":"user",'content': "Past record : " + self.past_data},

        {"role": "user", "content": constants.qus1},
        {"role": "system", "content": constants.res1},

        {"role": "user", "content": constants.QUERY},
        {"role": "system", "content": constants.RESPONCE},
        ]"""

print()