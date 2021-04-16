from openchat.base.envs.base import BaseEnvironment as BaseEnv
from openchat.base.envs.base import BaseAgent as BaseModel
from typing import Dict
from flask import Flask, render_template
from flask_cors import CORS
from flask_ngrok import run_with_ngrok
class WebDemoEnv(BaseEnv):
     def __init__(self):
         super().__init__()
         self.app = Flask(__name__)
         run_with_ngrok(self.app)
         CORS(self.app)
         self.keywords=['exit']
     def start(self, model: BaseModel):
         @self.app.route("/")
         def index():
             return render_template("index.html", title=model.name)
         @self.app.route('/user/<user_id>',methods=['GET'])
         def reg(user_id,):
             self.clear_histories(user_id)
             print("User created")
             return {"success":1}

         @self.app.route('/send/<user_id>/<text>', methods=['GET'])
         def send(user_id, text: str) -> Dict[str, str]:
             if(self.is_empty(user_id)):
               self.clear_histories(user_id)
             if text in self.keywords:
                 # Format of self.keywords dictionary
                 # self.keywords['/exit'] = (exit_function, 'good bye.')
                 _out = self.keywords[text][1]
                 # text to print when keyword triggered
                 self.keywords[text][0](user_id, text)
                 # function to operate when keyword triggered
             else:
                 model_input=self.make_model_input(user_id,text,model)
                 self.add_user_message(user_id, text)
                 _out = model.predict(model_input)
                 self.add_bot_message(user_id,_out['output'])
             return {"output": _out['output']}
         if __name__=='__main__':
             self.app.run() 

from openchat import OpenChat
OpenChat(model="blender.small", env=WebDemoEnv(),device='cpu',environment="webserver")
