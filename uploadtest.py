import os
import pandas as pd
from flask import *
from flask import request 
from werkzeug.utils import secure_filename

app = Flask(__name__)  
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
 
@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files.getlist('files[]')
        target = os.path.join(APP_ROOT,'data/')
        print(target)
        
        if not os.path.isdir(target):
            os.mkdir(target)
        
        df = []
        for file in request.files.getlist("file"):
            print(file)
            filename = file.filename
            destination = "/".join([target,filename])
            file.save(destination)  
            current_directory = os.getcwd()
            final_directory = os.path.join(current_directory, r'data')
            
        arr = os.listdir('data/')
        print('arr is',arr)
        df1=pd.read_csv('data/'+arr[0], delimiter=',')
        df_temp=[]
        flag=0
        for i in arr:
            if flag==0:
                flag=1
                continue
            df_temp=pd.read_csv('data/'+i, delimiter=',') 
            df1=df1.append(df_temp,ignore_index=True)
        
        df1["Total MarketPlace Charges"] = df1["Commission"] + df1["Payment Gateway"] + df1["PickPack Fee"]
        df1["Profit/Loss"] = df1["Sale Amount"] - (df1["Total MarketPlace Charges"] + df1["Cost Price"])
        final_df = df1.iloc[:,[0,8,3,7]]
        print(df1,final_df)
        df1.to_csv('Final.csv')
        final_df.to_csv('Final1.csv')     
        return render_template('success.html',  tables=[final_df.to_html(classes='data')], titles=final_df.columns.values)  

  
if __name__ == '__main__':  
    app.run(debug = True)  
