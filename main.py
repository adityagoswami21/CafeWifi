from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cafeName: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    openTime: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    closeTime: Mapped[str] = mapped_column(String(250), nullable=True)
    coffeeRating: Mapped[str] = mapped_column(String(250), nullable=True)
    wifiRating: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    powerRating: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)

with app.app_context():
    db.create_all()

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    maps = URLField('Location', validators=[URL()])
    open = StringField('Opening Time', validators=[DataRequired()])
    close = StringField('Closing Time', validators=[DataRequired()])
    coffee = SelectField('Coffee Rating', validators=[DataRequired()], choices=['✘', '☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️'])
    wifi = SelectField('Wifi Rating', validators=[DataRequired()], choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪️'])
    power = SelectField('Power Outlet Rating', validators=[DataRequired()], choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌'])
    submit = SubmitField('Submit')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET','POST'])
def add():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            cafeName=form.cafe.data,
            location=form.maps.data,
            openTime=form.open.data,
            closeTime=form.close.data,
            coffeeRating=form.coffee.data,
            wifiRating=form.wifi.data,
            powerRating=form.power.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template('add.html',form=form)


@app.route('/cafes', methods=['GET','POST'])
def cafes():
    result = db.session.execute(db.select(Cafe))
    all_cafe = result.scalars().all()
    return render_template('cafes.html',cafes=all_cafe) 

if __name__=="__main__":
    app.run(debug=True, port=5002)
