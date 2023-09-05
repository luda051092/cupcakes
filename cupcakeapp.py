"""Flask app for Cupcakes"""
from flask import Flask, json, redirect, render_template, jsonify, request, abort, url_for
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'COFFEE_CAKE'

connect_db(app)
db.create_all()


@app.route('/')
def index():
    """displays all cupcakes, appends new cupcakes """

    return render_template('cupcakeindex.html')

@app.route('/api/cupcakes', methods=['GET'])
def get_from_all():

    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def get_from_id(cupcake_id):
    """handler for returning a cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    if cupcake:
        json_format = cupcake.serialize()

        return jsonify(cupcake=json_format)
    else: 
        abort(404)

@app.route('/api/cupcakes', methods=['POST'])
def post_to_all():
    """Handler to add a cupcake"""

    json_cupcake = request.json

    cupcake = Cupcake(flavor=json_cupcake['flavor'],
                      rating=json_cupcake['rating'],
                      size=json_cupcake['size'],
                       image=json_cupcake['image'] or None)
    
    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', method=['PATCH'])
def patch_from_id(cupcake_id):
    """Updating cupcakes"""

    json_cupcake = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    if cupcake:
        cupcake.flavor = json_cupcake['flavor']
        cupcake.rating = json_cupcake['rating']
        cupcake.size = json_cupcake['size']
        cupcake.image = json_cupcake['image']

        db.session.add(cupcake)
        db.session.commit()

        return jsonify(cupcake=cupcake.serialize())
    else: 
        abort(404)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_from_id(cupcake_id):
    """deleting a cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    if cupcake:
        db.session.delete(cupcake)
        db.session.commit()

        return (jsonify(message='deleted'), 202)
    else: 
        abort(404)


@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404