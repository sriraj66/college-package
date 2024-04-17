import threading
from embedchain import App
from .models import ChatBot
from core import utils
from dotenv import load_dotenv
from django.conf import settings
import os
load_dotenv()


class Emmbedded(threading.Thread):
    
    def __init__(self, uid, prompt,urls = []):
        super(Emmbedded, self).__init__()
        self.urls = urls
        self.id = str(uid)
        self.prompt = prompt
        self.clg = ChatBot.objects.get(uid=self.id)
        self.key = self.clg.college.api_key
        self.config = {
            "app": {
                "config": {
                "id": self.id,
                "name": self.clg.name,
                }
            },
            "llm": {
                "provider": "openai",
                "config": {
                "model": "gpt-3.5-turbo",
                "temperature": 0.5,
                "max_tokens": 1000,
                "top_p": 1,
                "stream": False,
                "prompt": "$history Use the following pieces of query to answer.\n$context\n\nQuery: $query\n\nHelpful Answer:",
                "system_prompt": (
                "Act as Assistant. Answer the following questions in the style of Helping Assistant.Give the Accurate answers.\n"
                
                ),
                "api_key": self.key
                }
            },
            
            "embedder": {
                "provider": "openai",
                "config": {
                "model": "text-embedding-3-large",
                "api_key": self.key
                }
            },
            "chunker": {
                "chunk_size": 2000,
                "chunk_overlap": 100,
                "length_function": "len",
                "min_chunk_size": 0
            },
            "cache": {
                "similarity_evaluation": {
                    "strategy": "distance",
                    "max_distance": 1.0,
                },
                "config": {
                    "similarity_threshold": 0.8,
                    "auto_flush": 50,
                },
            },
        }
        self.add_db()
        
        self.app = App.from_config(config=self.config)
    
    
    def add_db(self):
        name = f"chat-bot-{str(self.clg.id)}"
        if settings.DEBUG is True:
            db_config = {
                    "provider": "chroma",
                    "config": {
                    "collection_name": name,
                    "dir": 'db',
                    "allow_reset": True
                }
            }
        else:
            db_config = {
                    "provider": "chroma",
                    "config": {
                    "collection_name": name,
                    "host": os.getenv("CHROMA_DB_HOST"),
                    "port":os.getenv("CHROMA_DB_PORT"),
                    "allow_reset": True
                }
            }
            
        self.config['vectordb'] = db_config
        # print(db_config)
        
        return True
        
    def add_sources(self):
        print("Adding SOURCE")
        for i in self.urls:
            try:
                self.app.add(i)
                print("CHUNK : ",i)
            except Exception as e:
                print(e)
        
        self.app.add(self.clg.hints)
        self.app.add(self.clg.desc)
        print("Done Adding urls to the sources list.")
        self.clg.state = True
        self.clg.running = True
        self.clg.save()
        print("State : " , self.clg.state)
        print("Running : " , self.clg.running)
        return True

    def query(self,urls=[]):
        if self.clg.state is False or self.clg.running is False:
            utils.start_page_source(self.clg.id)

            return "The Server is down... Try after some time"
        else:
            return self.app.chat(self.prompt,citations=True)[0].replace(",[object Object]"," ")
        
    def search(self, prompt):
        return self.app.search(prompt)
