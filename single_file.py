import tabula
import json
xxx=tabula.read_pdf(f"pdfs/2023.pdf",pages=61,output_format="json",output_path="kkok.json")

"""with open("kkk.json","r") as json_file:
     json_f=json.load(json_file)
json_f= json_f[0]["data"]

#let one list is there superlist of all tops [[],[]]
#another list, superlist of all lefts
left_main=[]
text=""
for i in json_f:
     temp_list=[]
     for x in i:
         for y in i:
                if(x.top==y.top or abs(x.top-y.top)<11):
                                
     print(text)
     print("\n\n\n\n\n")   """ 