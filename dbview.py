from flask import Flask, render_template
import psycopg2
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    # Подключние к базе данных
    train_number = request.args.get("q", default=None, type=str)
    conn = psycopg2.connect(database="practic",
                            user="postgres",
                            password="12345",
                            host="localhost",
                            port="5432")

    cur = conn.cursor()
    # создание курсора для вывода и поиска нужной информации с помощью SQL запросов
    if train_number is None:
        cur.execute("SELECT * FROM trains")
    else:
        cur.execute("SELECT * FROM trains WHERE train_number = (%s)", (train_number,))

    # Получение данных

    data = cur.fetchall()

    # закрыть курсор и соединение
    cur.close()
    conn.close()
    return render_template("index.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)
