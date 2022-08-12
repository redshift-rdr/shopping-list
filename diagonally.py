from app import app, db
from app.models import ShoppingList, ShoppingListItem

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'ShoppingList': ShoppingList, 'ShoppingListItem': ShoppingListItem}