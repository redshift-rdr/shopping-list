from flask import render_template, flash, redirect, request, url_for, session, make_response, jsonify
from app import app, db
from app.models import Item

@app.route('/')
@app.route('/index')
def index():
    items = db.session.query(Item).all()
    return render_template("index.html", items=items)

@app.route('/items/add', methods=["POST"])
def add_item():
    data = request.get_json()

    try:
        new_item = Item(name=data.get('name'), brand=data.get('brand', None), quantity=data.get('quantity', None), link=data.get('link', None), note=data.get('note', None), requestor=data.get('requestor', None))
        db.session.add(new_item)
        db.session.commit()
    except:
        return 'Not ok', 400

    return 'OK', 200

@app.route('/items/remove/<id>', methods=["GET"])
def remove_item(id):
    item = db.session.query(Item).filter_by(id=id).first()

    if not item:
        return redirect(url_for('index'))
    
    db.session.query(Item).filter_by(id=id).delete()
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/items/clear', methods=['GET'])
def clear_list():
    db.session.query(Item).delete()
    db.session.commit()

    return 'OK', 200