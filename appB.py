# Import Flask, jsonify, and requests
from flask import Flask, jsonify, request
import requests, json
from flask_sqlalchemy import SQLAlchemy

# Create a Flask app and an API with Connexion
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/order_db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Sapat1925@192.168.0.103:3310/order_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

# import connexion
# api = connexion.App(__name__, specification_dir="./")
# api.add_api("app_b.yaml")

# Order Model
class Order(db.Model):
    id = db.Column('order_id',db.Integer,primary_key=True)
    food_name = db.Column('food_name',db.String(300))
    food_price = db.Column('food_price', db.Float)
    order_by = db.Column('order_by', db.String(300))
print('Order Table is Created...')
db.create_all()

# Define a resource for the /hello endpoint
@app.route("/")
def hello():
    # Return a greeting message
    return jsonify({"message": "Hello from App B!"})

# Define a resource for the /call_app_a endpoint
@app.route("/create/<fid>/<fname>/<fprice>")
def create_order(fid,fname,fprice):
    # Make a GET request to App B's /hello endpoint
    id = int(fid)
    ord = Order(food_name=fname, food_price=fprice, order_by="Rishabh")
    db.session.add(ord)
    db.session.commit()
    result = Order.query.all()
    # if no products in db -- return -- simple message --
    if not result:
        return json.dumps({"ERROR": "No Order Details...!"})

    final_result = []
    # iterate one by and prepare dict -
    for f in result:
        food_dict = {}
        food_dict['foodid'] = f.id
        food_dict['foodname'] = f.food_name
        food_dict['foodprice'] = f.food_price
        food_dict['orderby'] = f.order_by
        # add that dict every time inside final list
        final_result.append(food_dict)
    # print(final_result)
    return json.dumps(final_result)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5002)
