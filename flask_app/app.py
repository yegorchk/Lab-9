from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///steps.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Модель пользователя
class Steps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steps = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "steps": self.steps, "date": self.date}


# Создание базы данных
with app.app_context():
    db.create_all()


# Главная страница (фронтенд)
@app.route("/")
def index():
    return render_template("index.html")


# Получение всех пользователей
@app.route("/api/steps", methods=["GET"])
def get_steps():
    info = Steps.query.all()
    return jsonify([steps.to_dict() for steps in info])


# Добавление пользователя
@app.route("/api/steps", methods=["POST"])
def add_steps():
    data = request.get_json()
    new_info = Steps(steps=data["steps"], date=data["date"])
    db.session.add(new_info)
    db.session.commit()
    return jsonify(new_info.to_dict()), 201


# Удаление пользователя
@app.route("/api/steps/<int:info_id>", methods=["DELETE"])
def delete_info(info_id):
    info = Steps.query.get(info_id)
    if not info:
        return jsonify({"error": "Information not found"}), 404
    db.session.delete(info)
    db.session.commit()
    return jsonify({"message": "Information deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
