from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app=Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#create engine
engine=create_engine('sqlite:///restaurantmenu.db?check_same_thread=False')
Base.metadata.bind=engine
#create session
DBSession = sessionmaker(bind=engine)
session=DBSession()


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id,menu_id):
    menuItem = session.query(MenuItem).filter_by(
        id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    items=session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('menu.html',restaurant=restaurant,items=items)                       
    

@app.route('/restaurant/<int:restaurant_id>/new/',methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/',methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
            editedItem.description = request.form['description']
            editedItem.price = request.form['price']
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        flash("Menu Item has been edited!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, item=editedItem)
    

# Task 3: Create a route for deleteMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/',methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method =='POST':
        session.delete(deletedItem)
        session.commit()
        flash("Menu Item has been deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))        

    else:
        return render_template(
            'deletemenuitem.html', item=deletedItem)    
    


if __name__ == '__main__':
    app.secret_key='super_user_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)