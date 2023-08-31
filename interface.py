from flask import Flask, request, jsonify,render_template
from utils import MedicalInsurance
import config
import pymongo
import project_db

client = pymongo.MongoClient(f"mongodb://localhost:{config.MONGODB_PORT_NO}")
db = client[config.MONGODB_DATABASE_NAME]

collection_user = db["user_details"]
collection_pred = db["model_pred"]

app = Flask(__name__)
@app.route("/reg",methods = ["GET","POST"])
def reg():
    if request.method == "POST":
        data = request.form
        print("Data",data)

        name = data["name"]
        mail = data["emailid"]
        mob = int(data["mobileno"])
        password = data["password"]
        resp = project_db.save_reg_detail(name,mail,mob,password)
        
    return jsonify({"Result": resp})

@app.route("/login")
def login():
    data = request.form
    mail = data["mailid"]
    password = data["password"]

    #resp = collection_user.find_one({"Email":mail,
                         #   "password":password})

    resp= project_db.login(mail,password)

    return jsonify({"Result": resp})


@app.route("/")
def home():
    
    #return jsonify("Home Page of medical insurance Prediction")
    return render_template("index.html")


@app.route("/predict_charges",methods = ["GET","POST"])
def predict_charges():

    if request.method == "POST":
        data = request.form

        age = int(data["age"])
        gender = data["gender"]
        bmi = eval(data["bmi"])
        children = int(data["children"])
        smoker = data["smoker"]
        region = data["region"]


        obj = MedicalInsurance(age,gender,bmi,children,smoker,region)
        pred_price = obj.get_predicted_price()[0]

        project_db.pred_info(age,gender,bmi,children,smoker,region,pred_price)

        return jsonify({"Result": f"Predicted Charges {pred_price}"})
        return render_template("index.html",result=pred_price)
    
    elif request.method == "GET":

        data = request.args.get

        age = int(data('age'))
        gender = data('gender')
        bmi = eval(data('bmi'))
        children = int(data('children'))
        smoker = data('smoker')
        region = data('region')

        obj = MedicalInsurance(age,gender,bmi,children,smoker,region)
        pred_price = obj.get_predicted_price()[0]

        resp = project_db.pred_info(age,gender,bmi,children,smoker,region,pred_price)
        
        return render_template("index.html", result = pred_price)
        return jsonify({"Insurence Charges":chrg})

    
    return jsonify({"GG":"PP"})


if __name__ == "__main__":
    app.run(host="0.0.0.0" ,port=config.PORT_NO,debug= True)
