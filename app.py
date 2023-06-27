# Import Flask, jsonify, and requests
import jwt
from flask import Flask, jsonify, request, session
import requests, json
from flask_sqlalchemy import SQLAlchemy

# Create a Flask app and an API with Connexion
app = Flask(__name__)
app.config['SECRET_KEY'] = "my-secret-key"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/order_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Sapat1925@52.66.216.101:3309/order_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


# import connexion
# api = connexion.App(__name__, specification_dir="./")
# api.add_api("app_b.yaml")

# Order Model
class Order(db.Model):
    id = db.Column('order_id', db.Integer, primary_key=True)
    food_name = db.Column('food_name', db.String(300))
    food_price = db.Column('food_price', db.Float)
    order_by = db.Column('order_by', db.String(300))


print('Order Table is Created...')
db.create_all()


# Define a resource for the /hello endpoint
@app.route("/")
def hello():
    # Return a greeting message
    return jsonify({"message": "Hello!! Welcome to Order App! Order Service is Working."})


# Define a resource for the /call_app_a endpoint
@app.route("/create/<fname>/<fprice>")  # DONE
def create_order(fname, fprice):
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split()[1]
    except:
        return jsonify({"error": "Token missing, Please login again orderapp.order/create"})
    try:
        isvalid = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except:
        return jsonify({"error": "token is invalid, Please login again orderapp.order/create"})
    ordr = Order(food_name=fname, food_price=fprice, order_by=isvalid['email'])
    db.session.add(ordr)
    db.session.commit()
    # print("order saved :", ordr)
    final_result = []
    order_dict = {"food_name": fname, "food_price": fprice, "order_by": isvalid['email']}
    final_result.append(order_dict)
    # print("final_result is:", final_result)
    return json.dumps(final_result)  # [{ },{ }]  json


# Define a resource for the /call_app_b endpoint
@app.route("/history")  # DONE
def get_history():
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split()[1]
    except:
        return jsonify({"error": "Token missing, Please login again orderapp.order/history"})
    try:
        isvalid = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except:
        return jsonify({"error": "token is invalid, Please login again orderapp.order/history"})
    result = Order.query.all()
    # print("result is:", result)
    # if no products in db -- return -- simple message --
    if not result:
        return json.dumps({"ERROR": "No Order Details...!"})
    else:
        final_result = []
        for o in result:
            order_dict = {'order_id': o.id, 'food_name': o.food_name, 'food_price': o.food_price, 'order_by': o.order_by}
            # print("food dict is:", food_dict)
            # add that dict every time inside final list
            final_result.append(order_dict)
        # print("final :", final_result)
        return json.dumps(final_result)  # [{ },{ }] json

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
