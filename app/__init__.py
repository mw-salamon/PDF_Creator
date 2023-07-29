from flask import Flask, jsonify, render_template, request, redirect, flash, send_file, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from werkzeug.utils import secure_filename
from app.pdf_creator import PDF
from PIL import Image
from dotenv import load_dotenv
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash
import os, io, tempfile, json


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

dotenv_path = Path('app/static/env_var/.env')
load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.getenv('SECRET')
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Models
class UserEntity(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)
    role = db.Column(db.String(8),
                     nullable=False)
    exchanges_owned = db.relationship('ExchangeEntity', backref='user')

class CurrencyEntity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(30), nullable=False)
    short = db.Column(db.String(3), nullable=False)
    flag = db.Column(db.BLOB, nullable=False)

class ExchangeEntity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_entity.id'))
    currencies = db.relationship('CurrencyEntity', secondary='currency_exchange', backref='exchanges')

currency_exchange = db.Table('currency_exchange',
                    db.Column('currency_id', db.Integer, db.ForeignKey('currency_entity.id'), primary_key=True),
                    db.Column('exchange_id', db.Integer, db.ForeignKey('exchange_entity.id'), primary_key=True)
                    )

@app.route('/')
def index():
    return render_template('index.html')

@login_manager.user_loader
def loader_user(user_id):
    return UserEntity.query.get(user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = UserEntity.query.filter_by(username=username).first()

        if user:
            flash("User with this username already exists")
            return render_template("register.html")
        
        user = UserEntity(username=username, 
                          password=generate_password_hash(password=password, method='scrypt'),
                          role="user")

        db.session.add(user)
        db.session.commit()

        return render_template('index.html')

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = UserEntity.query.filter_by(username=request.form.get("username")).first()

        if not user or not check_password_hash(user.password, request.form.get('password')):
                return render_template("login.html")

        login_user(user)
        return render_template('index.html')
        
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('index.html')

@app.route("/admin-panel")
@login_required
def adminPanel():
    return render_template('admin_panel.html')

@app.route('/curr-add', methods=['GET', 'POST'])
@login_required
def currAdd():
    if request.method=='POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        curr_short = request.form['short']
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        try:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                flag_data = file.read()

                curr = CurrencyEntity.query.filter_by(short=curr_short).first()

                if curr:
                    return redirect('/curr-opt')

                new_curr = CurrencyEntity(file_name=filename, short=curr_short, flag=flag_data)
                db.session.add(new_curr)
                db.session.commit()
                return redirect('/curr-opt')
        except Exception as e:
            print(f"Kod błędu: {e}")
            return redirect(request.url)
    else:
        return render_template('curr_add.html')
    
@app.route('/exchange-add', methods=['GET', 'POST'])
@login_required
def exchangeAdd():
    if request.method=='POST':
        name = request.form['exchange']

        exchange = ExchangeEntity.query.filter_by(name=name, user_id=current_user.id).first()

        if exchange:
            return redirect('/curr-opt')

        new_exchange = ExchangeEntity(name=name, user_id=current_user.id)
        db.session.add(new_exchange)
        db.session.commit()
        return redirect('/curr-opt')
    else:
        return render_template('exchange.html')
    
@app.route('/add-to-exchange', methods=['GET', 'PUT'])
@login_required
def addToExchange():
    if request.method == 'PUT':
        data = request.get_json()
        selected_exchanges = data.get('selected_exchanges', [])
        selected_currencies = data.get('selected_currencies', [])

        user_exchanges = ExchangeEntity.query.filter_by(user_id=current_user.id).all()

        for exchange in user_exchanges:
            if exchange.name in selected_exchanges:
                exchange.currencies = CurrencyEntity.query.filter(CurrencyEntity.short.in_(selected_currencies)).all()
            else:
                exchange.currencies = []

        db.session.commit()
        return jsonify({'message': 'Exchange data updated successfully'})
    elif request.method == 'POST':
        currencies = CurrencyEntity.query.all()
        return render_template('curr_exchange.html', currencies=currencies)
    else:
        currencies = CurrencyEntity.query.all()
        return render_template('curr_exchange.html', currencies=currencies)


@app.route('/curr-opt')
@login_required
def currOpt():
    return render_template('curr_options.html')

@app.route('/curr-opt/from-list', methods=['GET', 'POST'])
@login_required
def currency():
    if request.method == 'POST':
        pass
    else:
        currencies = CurrencyEntity.query.all()
        exchanges = ExchangeEntity.query.filter_by(user_id=current_user.id)
        return render_template('currency.html', currencies=currencies, exchanges=exchanges)
    return '', 200

@app.route('/create-curr-pdf', methods=['POST'])
@login_required
def createPdf():
    exchange = request.form['currencies']
    entity = ExchangeEntity.query.filter_by(name=exchange, user_id=current_user.id).first()
    currency_list = []
    if exchange:
        currencies = entity.currencies
        currency_list = [currency.short for currency in currencies]
    return render_template('create_curr_pdf.html', currencies = currency_list, currencies_input = currency_list)
    
@app.route('/download', methods=['POST'])
@login_required
def download_pdf():
    currencies = []
    data = request.form['currencies']
    curr_to_add = []
    curr_dict = {}

    for item in data.split(","):
        curr_entity = CurrencyEntity.query.filter(CurrencyEntity.short == item).first()
        dict = entity_to_dict(curr_entity)
        curr_to_add.append(dict)

    currencies = curr_to_add

    for curr in currencies:
        flag_data = curr['flag']
        flag_image = Image.open(io.BytesIO(flag_data))
        flag_image = flag_image.convert("RGB")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file_path = temp_file.name
            flag_image.save(temp_file_path, format='JPEG')
            key = f'{curr["short"]}'
            curr_dict[key] = []
            curr_dict[key].append(temp_file_path)
            curr_dict[key].append(request.form[f'{key}-sk'])
            curr_dict[key].append(request.form[f'{key}-sp'])

    pdf_creator = PDF('P', 'mm', 'A4')
    pdf_name = pdf_creator.create(curr_dict)
    return send_file(pdf_name, as_attachment=True)
    
def open_flag(file_name):
    with open(file_name, 'rb') as file:
        return file.read()
    
def entity_to_dict(entity):
    if entity is None:
        return None
    columns = [column.key for column in inspect(entity.__class__).columns]
    return {column: getattr(entity, column) for column in columns}

with app.app_context():
        db.create_all()