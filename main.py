from flask import Flask, render_template,request
from datetime import date
import pickle

app=Flask(__name__)

model=pickle.load(open('modfile1.pkl','rb'))

@app.route('/')
def fun():
    return render_template('index_page.html')

@app.route('/getprice', methods=['POST'])
def getPrice():
    price=int(request.form['curprice'])
    kms=int(request.form['kms'])
    own=int(request.form['owners'])
    year=int(request.form['year'])
    fuel=request.form['fuel']
    if(fuel=="diesel"):
        fu_diesel=1
        fu_petrol=0
    elif(fuel=="petrol"):
        fu_diesel=0
        fu_petrol=1
    else:
        fu_diesel=0
        fu_petrol=0
    seller=request.form['seller']
    if(seller=="individual"):
        sel_ind=1
    else:
        sel_ind=0
    tran=request.form['trans']
    if(tran=='manual'):
        tr_man=1
    else:
        tr_man=0
    
    to=date.today()
    ye=to.year
    year=ye-year
    prediction=model.predict([[price,kms,own,year,fu_diesel,fu_petrol,sel_ind,tr_man]])
    prediction=prediction[0]
    if(prediction<0):
        return render_template("index_page.html",text='Sorry, you cant sell the car')
    else:
        return render_template("index_page.html",text='You can sell the car for {}'.format(prediction))
    

if __name__=="__main__":
    app.run(debug=True)
