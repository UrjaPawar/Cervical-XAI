from flask import Flask, flash, redirect, render_template, request, session, abort,send_from_directory,send_file,jsonify
import pandas as pd

import json

application= Flask(__name__)

class DataStore():
    model=None
    dataset=None
    result= None
    key = None
data=DataStore()


@application.route("/main",methods=["GET","POST"])

#3. Define main code
@application.route("/",methods=["GET","POST"])
def homepage():
    ds = request.form.get('data','Original')
    mo = request.form.get('model','dtg')
    feature_list = request.form.getlist('check')
    feature_list.append("All Features")
    data.dataset = ds
    data.model = mo
    key="0"
    with open('result.json') as f:
        e = json.load(f)
    for feature_combo in e["features"]:
        if set(feature_combo["val"]) - set(feature_list) == set() and set(feature_list) - set(feature_combo["val"]) == set():
            key = feature_combo["key"]
            break
    data.result=e[key][data.dataset][data.model]
    data.key=key
    return render_template("index.html",acc=data.result["acc"], prec=data.result["prec"], rec=data.result["rec"])


@application.route("/get-data",methods=["GET","POST"])
def returnProdData():
    f=data.result["fi"]
    res=[]
    for obj in f:
        if obj['val']!=0:
            res.append(obj)
    print(jsonify(f))
    return jsonify(res)

@application.route("/music/myaudi.mp3")
def download_file():
    return send_from_directory(r"C:\Users\R00194685\Desktop\XAI-Pro\FAO-FBS-Data-Explorer",'myaudi.mp3')

if __name__ == "__main__":
    application.config["CACHE_TYPE"] = "null"
    application.run(debug=True)



