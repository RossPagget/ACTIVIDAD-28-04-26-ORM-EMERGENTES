from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///products.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELO ---
class Product(db.Model):
    __tablename__ = "products"
    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String,  nullable=False)
    price = db.Column(db.Float,   nullable=False)
    stock = db.Column(db.Integer, default=0)

# --- RUTAS ---

@app.route('/')
def index():
    # READ ALL
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/create', methods=['POST'])
def create():
    # CREATE
    name = request.form.get('name')
    price = float(request.form.get('price'))
    stock = int(request.form.get('stock'))
    
    new_product = Product(name=name, price=price, stock=stock)
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # READ ONE & UPDATE
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', product=product)

@app.route('/delete/<int:id>')
def delete(id):
    # DELETE
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)