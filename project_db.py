import pymongo
import config

client = pymongo.MongoClient(f"mongodb://localhost:{config.MONGODB_PORT_NO}")
db = client[config.MONGODB_DATABASE_NAME]

collection_user = db["user_details"]
collection_pred = db["model_pred"]

def save_reg_detail(name,mail,mob,password):

    resp = collection_user.find_one({"Email":mail})
    if resp:      
        return "mailID already exist"
    
    resp = collection_user.find_one({"Mob":mob})
    if resp:      
        return "mobile no already exist"


    resp = collection_user.insert_one({"Name":name,
                                "Email":mail,
                                "Mob":mob,
                                "password":password})
   
    return "User register successfully "
def login(mailid,password):
    resp = collection_user.find_one({"Email":mailid})
    if not resp:      
        return "User not exist"
    
    resp = collection_user.find_one({"Email":mailid,
                            "password":password})
    # Check login Postman
    if resp:
        return "user login success"
    
    else :
        return "password Incorrect"
    
def pred_info(age,gender,bmi,children,smoker,region,pred_price):
    resp = collection_pred.insert_one({"age":age,
                                "Gender":gender,
                                "BMI":bmi,
                                "Children":children,
                                "smoker":smoker,
                                "region":region,
                                "Result":pred_price})
   

