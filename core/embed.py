import threading
from embedchain import App
from .models import College

class Emmbedded(threading.Thread):
    
    def __init__(self, uid, prompt,urls = []):
        super(Emmbedded, self).__init__()
        self.urls = urls
        self.id = str(uid)
        self.prompt = prompt
        self.clg = College.objects.get(uid=self.id)
        self.key = self.clg.api_key
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
                "temperature": 0.7,
                "max_tokens": 1000,
                "top_p": 1,
                "stream": False,
                "prompt": "Use the following pieces of context to answer the query at the end.\nIf you don't know the answer, just say that you don't know.\n$context\n\nQuery: $query\n\nHelpful Answer:",
                "system_prompt": (
                "Act as Assistant. Answer the following questions in the style of Professional Assistant.\n"
                
                ),
                "api_key": self.key
                }
            },
            "vectordb": {
                "provider": "chroma",
                "config": {
                "collection_name": "full-stack-app",
                "dir": "db",
                "allow_reset": True
                }
            },
            "embedder": {
                "provider": "openai",
                "config": {
                "model": "text-embedding-ada-002",
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
        self.app = App.from_config(config=self.config)
        
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
        return True

    def query(self,urls=[]):
        if self.clg.state == False:
            t = threading.Thread(target=self.add_sources,args=(urls,))
            t.start()
            return "The Server is down... Try after some time"
        else:
            return self.app.chat(self.prompt,citations=True)[0].replace(",[object Object]"," ")
        
    def search(self, prompt):
        return self.app.search(prompt)
