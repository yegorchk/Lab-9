from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask("Furniture store")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# products = [
#     {'prod_name': 'sofa',
#      'price': 12000,
#      'in_stock': False,
#      'id': 0},
#     {'prod_name': 'table',
#      'price': 6000,
#      'in_stock': True,
#      'id': 1},
#     {'prod_name': 'chair',
#      'price': 8000,
#      'in_stock': False,
#      'id': 2},
#
# ]


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(300))
    price = db.Column(db.Integer)
    in_stock = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Product{self.id}. {self.prod_name} - {self.price} rub."


@app.route("/")
def main():
    products = Product.query.all()
    return render_template("index.html", products_list=products)


@app.route("/in_stock/<product_id>", methods=["PATCH"])
def modify_product(product_id):
    product = Product.query.get(product_id)
    product.in_stock = request.json["in_stock"]
    db.session.commit()
    # global products
    # in_stock = request.json['in_stock']
    # for product in products:
    #     if product['id'] == product_id:
    #         product.update({'in_stock': in_stock})
    # return 'OK'


@app.route("/add", methods=["POST"])
def add_product():
    data = request.json
    product = Product(**data)
    db.session.add(product)
    db.session.commit()

    # id_last = products[-1]['id']
    # id_new = id_last + 1
    # data['id'] = id_new
    # products.append(data)
    return "OK"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
