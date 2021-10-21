# app.py
import random
import json
import nltk
import textwrap
nltk.download('stopwords')
from Questgen import main
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()
class Payload(BaseModel):
    input_text : str
    max_questions : int

#True or False (Yes & No Questions)
qe= main.BoolQGen()
qg = main.QGen()
 
# output.append(qg.predict_mcq(j_object))
# output.append(qe.predict_boolq(j_object))

@app.post("/boolean", status_code=201)
async def post_questions_boolean(payload:Payload):
   #print(json.dumps(payload.input_text))
   completeStr = payload.input_text
   output = []
   #for st in textwrap.wrap(completeStr, int(len(completeStr)/3)):
   for st in textwrap.wrap(completeStr, 1000):
       if len(st) < 100:
           break
       j_object = {"input_text": st, "max_questions": payload.max_questions}
       output.append(qg.predict_mcq(j_object))
       #output.append(qg.predict_shortq(j_object))
   return generate_mcq_final_response(output)
   #return generate_faq_final_response(output)


def generate_mcq_final_response(initial_resp): 
    question_list = []
    for resp in initial_resp:
        for question in resp["questions"]:
            question["question_statement"].strip("/n")
            #removing extra fields
            question.pop("options_algorithm")
            question.pop("extra_options")
            question.pop("context")
            question.pop('id')
            question["options"].append(question["answer"])
            #randomizing options in questions
            random.shuffle(question["options"])
            question_list.append(question)
    return {"mcq_questions" : question_list}


def generate_faq_final_response(initial_resp):
    question_list = []
    for resp in initial_resp:
        for question in resp["questions"]:
            question["Question"].strip("/n").strip()
            #removing extra fields
            question.pop('id')
            question["question"] = question.pop("Question")
            question["short_answer"] = question.pop("Answer")
            question["long_answer"] = question.pop("context")
            question_list.append(question)
    return {"faq_questions" : question_list}











