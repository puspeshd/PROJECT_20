import os
import pandas as pd

xyz=os.listdir("uploads/")
def update_max_list(max_list, other_list):
    for i, item in enumerate(other_list):
        if item not in max_list:
            # Find the nearest index to insert the item in max_list
            for j in range(len(max_list)):
                if max_list[j] > item:
                    max_list.insert(j, item)
                    break
            else:
                # If no larger item is found, append the item at the end
                max_list.append(item)

    return max_list

def main(lists):
    # Find the list with the maximum number of items
    max_list = max(lists, key=len)
    
    # Iterate over other lists and update the max_list accordingly
    for lst in lists:
        if lst != max_list:
            max_list = update_max_list(max_list, lst)

    return max_list
def merge_csv_files(csv_files):
    # Read and combine all CSV files
    data_frames = [pd.read_csv("uploads/"+file) for file in csv_files]
    
    master_c1_list=[]
    for x in data_frames:
        row1_columns=list(x[x.columns[0]])
        master_c1_list.append(row1_columns)
    for x in master_c1_list:
        for y in range(len(x)):
            x[y]=x[y].replace(".","").replace("  ","").strip() 
    updated_max_list = main(master_c1_list)
    print(updated_max_list)
    
    combined_list=[]

    count=0           
    for x in master_c1_list:
        for i,y in enumerate(x):
            count=count+1
            x[i]=x[i].strip()
            
            if(x[i] not in combined_list):
                combined_list.append(x[i])
    column_master=[]  
    print(combined_list)
             
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
            i.at[x,i.columns[0]]=i.at[x,i.columns[0]].replace(".","").replace("  ","")
    for x in master_df.index:
        for i in data_frames:
            for y in i.index:
                if(master_df.at[x,master_df.columns[0]]==i.at[y,i.columns[0]]):
                    for z in i.columns:
                        try:
                            master_df.at[x,z]=i.at[y,z] 
                        except:
                            pass    


                            
    


    
    """order = list(data_frames[0].columns[0])


    # Create a categorical type with the specified order
    master_df['A_cat'] = pd.Categorical(master_df['Unnamed: 0'], categories=order, ordered=True)

    # Split the DataFrame into matched and unmatched parts
    matched = master_df[master_df['Unnamed: 0'].isin(order)]
    unmatched = master_df[~master_df['Unnamed: 0'].isin(order)]

    # Sort the matched part by the categorical order
    matched = matched.sort_values('A_cat')

    # Concatenate matched and unmatched parts
    result = pd.concat([matched, unmatched])

    # Drop the auxiliary column used for sorting
    result = result.drop(columns='A_cat')

    print(result)"""

    master_df.to_excel("output1.xlsx",index=False)
            




     

    







merge_csv_files(xyz)