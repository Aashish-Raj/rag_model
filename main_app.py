#  import the  require  pakages
from PIL import Image
import pytesseract as tess
from  pytesseract import image_to_string
from pdf2image import convert_from_path
import os
from  dotenv import load_dotenv
from openai import OpenAI
import json

# load env
load_dotenv()

# setup open ai
client=OpenAI()


# update the 
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'


# set teh  propeller path
poppler_path=os.getenv("POPPLER_PATH")
tess.pytesseract.tesseract_cmd=os.getenv("PROPELLER_PATH")



#  extract  text  from  the  pdf image
def  extract_text_from_image(file_path):
    print("file path---->",file_path)
    chunk=[]

    #  currenty it   read the  10  pages data
    pages=convert_from_path(file_path,first_page=1,last_page=10,poppler_path=poppler_path)
    for i,page in enumerate(pages):
        chunk.append(image_to_string(page))
    return chunk
 
    

#  create respose from  open  ai
def open_ai_quiz_generate(number=10,extracted_texts=None):

    try:
        print("working to  geberate the  quiz........")

        if not extracted_texts:
            return False
        
        # shuffel the extraacted text data 

        ## total number of questin
        total_question=number
        
        #### pass the  prompt to the open ai  fro response
        response = client.chat.completions.create(temperature=0.3,
        model="gpt-4o-mini",
        response_format={ "type": "json_object" }, 
        messages=[{
                    "role": "system",
                    "content": f"""
                    You are a quiz generator designed to output JSON. Generate exactly {total_question} quiz questions based on the following criteria:

                    1. **Question Types**: Provide a mix of mcq, true_false, fill_ups, and short_answer questions. Group questions by type in the 'quiz_questions' dictionary.
                    2. **Format**:
                        - **mcq**: Include 4 options with one correct answer. Do not number the options.
                        - **true_false**: Provide a statement and indicate if it is true or false. Use string values "true" and "false".
                        - **fill_ups**: Provide a question with a blank to be filled.
                        - **short_answer**: Provide a question requiring a brief explanatory answer.
                    3. Each question must include 'question', 'options' (if applicable), 'answer', and 'explanation'.
                    4. Ensure all questions are relevant to the provided data.
                    5. Ensure the total number of questions is exactly {total_question}. If the number of generated questions does not meet this requirement, regenerate the questions until the count is accurate.
                    
                    Begin generating the questions based on the provided data: {extracted_texts}.
                    """
                }
                ]

        )
        
        #  Begin generating the questions now based on  the following data: {extracted_texts}

        res=response.choices[0].message.content
        
        response_dict=json.loads(res)
        print('\n\n\n\n--->>>>>>resposne---------->\n\n\n',response_dict)

        #   store resposne in json
        with open('res.json','w') as json_file:
            json.dump(response_dict,json_file,indent=4)

    # print('open ai response-->', res)
    except Exception as e:
        print(e)
    





if __name__ == "__main__":

    # extract text from  ocr
    text=extract_text_from_image('pdf/aqa-gcse-maths-higher-textbook.pdf')
    print('------>\n\n\n',text,'----->')


    # call the  open ai  funtion to genrate the response
    open_ai_quiz_generate(number=10,extracted_texts=text)