from flask import Flask, request, make_response
import db
from werkzeug.exceptions import InternalServerError

app = Flask(__name__)

conn = db.get_connection()
cursor = conn.cursor()

def __get_product_by_id(product_id):
    sql = """select * from t_product where id=%s"""
    params = (product_id)
    cursor.execute(sql, params)
    return cursor.fetchone()


def __insert_order(product, order_request):
    username = order_request['username']
    quantity = order_request['quantity']
    product_id = product[0]
    price = product[2]
    sql = """insert into t_order(username, product_id, quantity, price) values(%s, %s, %s, %s)"""
    params = (username, product_id, quantity, price)
    cursor.execute(sql, params)


def __update_product_stock(product, order_request):
    quantity = order_request['quantity']
    product_id = product[0]
    sql = """update t_product set stock = stock - %s where id = %s"""
    params = (quantity, product_id)
    cursor.execute(sql, params)


@app.route('/order', methods=['POST'])
def order():
    order_request = request.get_json()
    product_id = order_request['product_id']

    product = __get_product_by_id(product_id)

    try:
        __insert_order(product, order_request)
        __update_product_stock(product, order_request)
        conn.commit()
        msg = 'Berhasil order'
    except Exception as e:
        conn.rollback()
        msg = 'Gagal order ' + str(e)
        raise InternalServerError(msg)

    return make_response({'message': msg}), 201


if __name__ == '__main__':
    app.run(debug=True)