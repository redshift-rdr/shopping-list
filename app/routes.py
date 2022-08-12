from flask import render_template, flash, redirect, request, url_for, session, make_response, jsonify
from app import app, db
from app.models import ShoppingList, ShoppingListItem

@app.route('/')
@app.route('/index')
def index():
    lists = db.session.query(ShoppingList).filter_by(archived=False).all()

    return render_template('index.html', lists=lists)

@app.route('/item/add', methods=['POST'])
def item_add():
    list_id = request.form.get('list_id')
    item_name = request.form.get('name')

    slist = db.session.query(ShoppingList).filter_by(id=list_id).first()
    if not slist:
        flash('that is not a valid list')
        return redirect(url_for('index'))

    if not item_name.isalnum():
        flash('that is not a valid name for an item')
        return redirect(url_for('index'))

    item = ShoppingListItem(name=item_name, slist=slist)

    try:
        db.session.add(item)
        db.session.commit()
    except Exception as e:
        flash(f'there was an error: {e}')
        return redirect(url_for('index'))

    return redirect(url_for('index'))

@app.route('/item/remove/<item_id>', methods=['GET'])
def item_remove(item_id):
    item = db.session.query(ShoppingListItem).filter_by(id=item_id).first()

    if not item:
        flash('that item doesn\'t exist')
        return redirect(url_for('index'))

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        flash(f'there was an error: {e}')
        return redirect(url_for('index'))

    return redirect(url_for('index'))

@app.route('/item/recurring/<item_id>', methods=['GET'])
def item_recurring(item_id):
    item = db.session.query(ShoppingListItem).filter_by(id=item_id).first()

    if not item:
        flash('that item doesn\'t exist')
        return redirect(url_for('index'))

    item.recurring = not item.recurring

    try:
        db.session.add(item)
        db.session.commit()
    except Exception as e:
        flash(f'there was an error: {e}')
        return redirect(url_for('index'))

    return redirect(url_for('index'))

@app.route('/item/query/<query>', methods=['GET'])
def item_query(query):
    query = f'{query}%'
    items = ShoppingListItem.query.filter(ShoppingListItem.name.like(query)).all()#db.session.query(ShoppingListItem.name.like(query)).all()

    # set comprehension to make sure only unique items returned, cast to list to be json serializable
    return jsonify(list({item.name for item in items}))

@app.route('/list/complete/<list_id>', methods=['GET'])
def list_complete(list_id):
    slist = db.session.query(ShoppingList).filter_by(id=list_id).first()

    if not slist:
        flash('that list doesnt exist')
        return redirect(url_for('index'))

    slist.archived = True

    try:
        db.session.add(slist)
        db.session.commit()
    except Exception as e:
        flash(f'there was an error: {e}')
        return redirect(url_for('index'))

    newlist = ShoppingList()
    recurring_items = db.session.query(ShoppingListItem).filter_by(recurring=True).all()
    for item in recurring_items:
        item.slist = newlist

    try:
        db.session.add(newlist)
        db.session.add_all(recurring_items)
        db.session.commit()
    except Exception as e:
        flash(f'there was an error: {e}')
        return redirect(url_for('index'))

    return redirect(url_for('index'))


