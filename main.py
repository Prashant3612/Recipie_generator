import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import requests
import streamlit as st
import json
import os 
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

st.title("Recipie Generator")
input=st.text_input("Enter the ingredients you have")

def recipie_suggester(input):
  prompt='''
  You are an intellegent ai assistant. You have to suggest what recipie can be made from {list}. Only suggest most relevant recipie. Give the ingredients and cooking istructions( lable them as 'Cooking Instructions') also and remove any symbols.
  Only tell one recipie'''
  
  prompt_temp=PromptTemplate(input_varibles=['list'],template=prompt)
  llm=ChatGoogleGenerativeAI(model='gemini-pro')
  chain=prompt_temp | llm | StrOutputParser()
  
  
  output = chain.invoke({"list": input})
  return output


def food_images(food):
  base_url='https://api.edamam.com/api/recipes/v2?type=public'
  app_key='835f96d91f23fdc262577f144bab6a37'
  app_id='7caa4aab'

  print(food)
  uri=base_url+'&q='+food+'&app_id=7caa4aab&app_key=835f96d91f23fdc262577f144bab6a37&imageSize=REGULAR'
  response=requests.get(uri)
  data = json.loads(response.text)
  # print(data)
  default_image='https://drive.google.com/file/d/19QXK3ozgBwwdUJ47ttcCz2pSX59uU-qC/view?usp=drive_link'
  image_urls = []
  try:
    image_url = data['hits'][0]['recipe']['image']
    return image_url
  except (KeyError, IndexError):
    print("Error: Could not extract image URL")
    return default_image
    

if st.button('Submit'):
  text=recipie_suggester(input)
  

  split=text.splitlines()
  st.title(split[0])
  st.subheader(split[2])
  for i in split[3:]:
    if 'Cooking Instruction' not in i:
      st.write(i)
    else:
      st.subheader(i)

  st.image(food_images(split[0]))
  

  st.write("\n\n\n Shot of ingredients? \n Order it from here")

  st.markdown("[Blinkit](https://blinkit.com/)")

  




  