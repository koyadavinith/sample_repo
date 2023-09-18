from market import app,db
from flask import render_template,request, url_for,redirect,flash,Request
from market.models import Item,user
from market.register import Register,Login,PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required,current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market',methods = ['POST','GET'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST':
        #purchase Item logic
        purchased_item = request.form.get('purchased_item')
        p_item_obj = Item.query.filter_by(name = purchased_item).first()
        if p_item_obj:
            if current_user.can_purchase(p_item_obj):
                p_item_obj.buy(current_user)
                flash(f'Congratulations! You have purchased {p_item_obj.name} for {p_item_obj.price}₹',category= 'success')
            else:
                flash(f'Unfortunately, You dont have enough money to purchase {p_item_obj.name}',category= 'danger')

        #selling item logic
        sold_item = request.form.get('sold_item')
        s_item_obj = Item.query.filter_by(name = sold_item).first()
        if s_item_obj:
            if current_user.can_sell(s_item_obj):
                s_item_obj.sell(current_user)
                flash(f'Congratulations! You sold {s_item_obj.name} back to market',category='success')
            else:
                flash('Something went wrong with selling {s_item_object.name}',category='danger')
        return redirect(url_for('market_page'))

    if request.method == 'GET':
        items = Item.query.filter_by(owner =None)
        owned_items = Item.query.filter_by(owner = current_user.id)
        return render_template('market.html',items = items, purchase_form = purchase_form,owned_items = owned_items, selling_form = selling_form)


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        barcode = request.form['barcode']
        description = request.form['description']
        item = Item(name=name, price=price, barcode=barcode, description=description)
        db.session.add(item)
        db.session.commit()
        return render_template('add_item.html')
    else:
        return render_template('add_item.html')



@app.route('/register',methods = ['POST','GET'])
def register_page():
    form = Register()
    if form.validate_on_submit():
        with app.app_context():
            user_data = user(username = form.username.data,
                              email_id = form.email_id.data,
                              password = form.password1.data)
            db.session.add(user_data)
            db.session.commit()
            login_user(user_data)
        flash(f'Account created successfully!, Now you are logged in as {user_data.username}',category = 'succes')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating user: {err_msg}',category='danger')
    return render_template('register.html',form = form)

@app.route('/login',methods = ['POST','GET'])
def login_page():
    form = Login()
    if form.validate_on_submit():
        attempted_user = user.query.filter_by(username = form.username.data).first()
        if attempted_user and attempted_user.check_password_match(attempted_password = form.password.data):
            login_user(attempted_user)
            flash(f'Succes! You are logged in as: {attempted_user.username}',category = 'success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again',category = 'danger')
    return render_template('login.html',form = form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have logged out!',category= 'info')
    return redirect(url_for('home_page'))
