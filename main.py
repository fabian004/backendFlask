import os

from flask import Flask, render_template, request, Response, jsonify,redirect,url_for
import database as dbase

import numpy as np
import pandas as pd 
import torch
db= dbase.dbConnection()
app = Flask(__name__)

@app.route("/")
def hello_world():

    products = db['products']
    productsReceived=products.find()
    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)



#Add
@app.route('/products',methods=['POST'])
def addProduct():
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']


    if name and price and quantity:
        mydict = { "name": name, "price": price, "quantity": quantity }
        products.insert_one(mydict)
        response = jsonify({
            'name':name,
            'price':price,
            'quantity':quantity
        })
        return redirect(url_for('home'))
    else:
        return notFound()


#Delete
@app.route('/delete/<string:product_name>')
def delete(product_name):
    products = db['products']
    products.delete_one({'name':product_name})
    return redirect(url_for('home'))


#Edit
@app.route('/edit/<string:product_name>',methods=['GET','POST'])
def edit(product_name):
    
        products = db['products']
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']

        if name and price and quantity:
            myquery = { "name": product_name }
            newvalues = { "$set": { "name": name, "price": price, "quantity": quantity } }
            products.update_one(myquery, newvalues)
            response = jsonify({
                'message':'Producto' + product_name + 'Actualizado'
            })
            name = os.environ.get("NAME", "World")
            return "Hello {}!".format(name)
        else:
            return notFound()
    



@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message':'No encontrado: ' + request.url,
        'status':'404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response


#Machine
@app.route('/machine',methods=['GET','POST'])
def machine():
    return 'hola'


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))