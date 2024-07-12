import traceback
from flask import Flask, request, jsonify,render_template,send_file
import os
import tabula
import pandas as pd
import requests
import json
import datetime
def remove_files():
    f_t_r=os.listdir("uploads")
    
    for i in f_t_r:
        #check if it is a directory
        if os.path.isdir("uploads/"+i):
            #remove all files in the directory
            for j in os.listdir("uploads/"+i):
                os.remove("uploads/"+i+"/"+j)
            #remove the directory
            
        os.remove("uploads"+i)

app = Flask(__name__)
def main(lists):
    # Find the list with the maximum number of items
    max_list = max(lists, key=len)
    
    # Iterate over other lists and update the max_list accordingly
    for lst in lists:
        if lst != max_list:
            max_list = update_max_list(max_list, lst)

    return max_list
def update_max_list(max_list, other_list):
    for i, item in enumerate(other_list):
        if item not in max_list:
            # Find the nearest index to insert the item in max_list
            for j in range(len(max_list)):
                if j > i:
                    max_list.insert(j, item)
                    break
            else:
                # If no larger item is found, append the item at the end
                max_list.append(item)

    return max_list
def merge_csv_files(csv_files,merged_path,folder_name):
    
    data_frames = [pd.read_csv("uploads/"+folder_name+"/"+file) for file in csv_files]
    
    master_c1_list=[]
    for x in data_frames:
        row1_columns=list(x[x.columns[0]])
        master_c1_list.append(row1_columns)
    for x in master_c1_list:
        for y in range(len(x)):
            try:
                x[y]=x[y].replace(".","").replace("  ","").strip() 
            except:
                pass    
    updated_max_list = main(master_c1_list)
    print(updated_max_list)
    
    combined_list=[]

    count=0           
    for x in master_c1_list:
        for i,y in enumerate(x):
            count=count+1
            try:
                x[i]=x[i].strip()
            except:
                pass     
            
            if(x[i] not in combined_list):
                combined_list.append(x[i])
    column_master=[]  
    #print(combined_list)
             
    for i in data_frames:
        list(i.columns)
        for x in i.columns:
            
            if(x not in column_master):
                column_master.append(x)
    #column_master=sorted(column_master,reverse=True)
    master_df=pd.DataFrame(columns=column_master)
    master_df["Unnamed: 0"]=updated_max_list
    
    for i in data_frames:
        

        for x in i.index:
            try:
                i.at[x,i.columns[0]]=i.at[x,i.columns[0]].replace(".","").replace("  ","")
            except:
                pass    
    for x in master_df.index:
        for i in data_frames:
            for y in i.index:
                if(master_df.at[x,master_df.columns[0]]==i.at[y,i.columns[0]]):
                    for z in i.columns:
                        try:
                            master_df.at[x,z]=i.at[y,z] 
                        except:
                            pass    


                            
    


    
    

    master_df.to_excel(merged_path,index=False)
        
os.makedirs('pdfs', exist_ok=True)
@app.route("/")
def dashboard():
    return render_template("dashboard.html")
@app.route('/process_pdfs', methods=['POST'])
def process_pdfs():
    try:
        remove_files()
    except:
        pass    
    files = request.files.getlist('files')
    form_data = request.form.to_dict(flat=False)
    
    csv_files=[]

    # Ensure 'uploads' directory exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    company_name=""
    for file in files:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        cash_flow = form_data[f'data[{file.filename}][cashFlow]'][0]
        balance_sheet = form_data[f'data[{file.filename}][balanceSheet]'][0]
        income_statement = form_data[f'data[{file.filename}][incomeStatement]'][0]
        company_name = form_data[f'data[{file.filename}][companyName]'][0]
        
        csv_file_path_cash_flow = os.path.join('uploads',"cash_flow", f"{os.path.splitext(file.filename)[0]}.csv")
        csv_file_path_balance_sheet = os.path.join('uploads',"balance_sheet", f"{os.path.splitext(file.filename)[0]}.csv")
        csv_file_path_income_statement = os.path.join('uploads',"income_statement", f"{os.path.splitext(file.filename)[0]}.csv")
        tabula.convert_into(file_path, csv_file_path_cash_flow, output_format="csv", pages=int(cash_flow))
        tabula.convert_into(file_path, csv_file_path_balance_sheet, output_format="csv", pages=int(balance_sheet))
        tabula.convert_into(file_path, csv_file_path_income_statement, output_format="csv", pages=int(income_statement)) 
        #csv_files.append(csv_file_path)
    datetimestamp=str(datetime.datetime.now()).replace("-","").replace(":","").replace(".","").replace(" ","")    
    merged_csv_path = f"{company_name}_{datetimestamp}.xlsx"
    cash_flow_files=os.listdir("uploads/cash_flow/")
    for i in cash_flow_files:     
        x=os.path.getsize(f"uploads/cash_flow/{i}")
        if(x==0):
            os.remove(f"uploads/cash_flow/{i}")
    cash_flow_files=os.listdir("uploads/cash_flow/")
    balance_sheet_files=os.listdir("uploads/balance_sheet/")
    for i in balance_sheet_files:     
        x=os.path.getsize(f"uploads/balance_sheet/{i}")
        if(x==0):
            os.remove(f"uploads/balance_sheet/{i}")
    balance_sheet_files=os.listdir("uploads/balance_sheet/")        
    income_statement_files=os.listdir("uploads/income_statement/")
    for i in income_statement_files:     
        x=os.path.getsize(f"uploads/income_statement/{i}")
        if(x==0):
            os.remove(f"uploads/income_statement/{i}")
    income_statement_files=os.listdir("uploads/income_statement/")
    print(cash_flow_files,balance_sheet_files,income_statement_files)
    try:
        if(len(cash_flow_files)>1):
            merge_csv_files(cash_flow_files, "cash_flow_"+merged_csv_path,"cash_flow")
            cash_flow_file_path="cash_flow_"+merged_csv_path
        else:
            pass    
    except:
        cash_flow_file_path="NOT ABLE TO GEGNERATE"
        traceback.print_exc()
    try:
        if(len(balance_sheet_files)>1):
            merge_csv_files(balance_sheet_files, "balance_sheet_"+merged_csv_path,"balance_sheet")
            balance_sheet_file_path="balance_sheet_"+merged_csv_path
    except:
        balance_sheet_file_path="NOT ABLE TO GEGNERATE"
        traceback.print_exc()
    try:
        if(len(income_statement_files)>1):
            merge_csv_files(income_statement_files, "income_statement_"+merged_csv_path,"income_statement")
            income_statement_file_path="income_statement_"+merged_csv_path
    except:
        income_statement_file_path="NOT ABLE TO GEGNERATE"
        
        traceback.print_exc()       

    data={"cash_flow_file_path":cash_flow_file_path, "balance_sheet_file_path":balance_sheet_file_path, "income_statement_file_path":income_statement_file_path}
    try:
        remove_files()    
    except:
        pass
        

    return render_template("success.html",data=data)

    
@app.route('/csv_ops/<filename>')
def csv_ops(filename):
    return send_file(filename)
    
    
if __name__ == '__main__':
    app.run()




