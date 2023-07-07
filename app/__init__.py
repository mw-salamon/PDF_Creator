from flask import Flask, render_template, request, redirect, flash, jsonify, session, send_file, after_this_request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from werkzeug.utils import secure_filename
import io
from app.pdf_creator import PDF
import tempfile
from PIL import Image

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://admin:rpumk123@pdf-creator-db.crso7vjacfgq.eu-central-1.rds.amazonaws.com:3306/pdf_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = '33352a946f0c2b8629d29b59f61535f41334c32243a2410b50ea9290ecc756c6'
# Session(app)
db.init_app(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Models
class CurrencyEntity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(30), nullable=False)
    short = db.Column(db.String(3), nullable=False)
    flag = db.Column(db.BLOB, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/curr-add', methods=['GET', 'POST'])
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
                new_curr = CurrencyEntity(file_name=filename, short=curr_short, flag=flag_data)
                db.session.add(new_curr)
                db.session.commit()
                return redirect('/curr-opt')
        except Exception as e:
            print(f"Kod błędu: {e}")
            return redirect(request.url)
    else:
        return render_template('curr_add.html')


@app.route('/curr-opt')
def currOpt():
    return render_template('curr_options.html')

@app.route('/curr-opt/from-list', methods=['GET', 'POST'])
def currency():
    if request.method == 'POST':
        pass
    else:
        currencies = CurrencyEntity.query.all()
        return render_template('currency.html', currencies=currencies)

    return '', 200

@app.route('/create-curr-pdf', methods=['POST'])
def createPdf():
    data = request.form['currencies']
    return render_template('create_curr_pdf.html', currencies = data.split(','), currencies_input = data)
    

@app.route('/download', methods=['POST'])
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