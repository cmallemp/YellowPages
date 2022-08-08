from decimal import ROUND_HALF_DOWN
from operator import inv
import os
from re import L
from click import edit
from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func,  and_, or_, not_

from sympy import comp, content

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class companies(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    cname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mobile = db.Column(db.String(100))
    address = db.Column(db.String(200))

    def __init__(self, cname, email, mobile, address):
        self.cname = cname
        self.email = email
        self.mobile = mobile
        self.address = address


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/", methods=['POST', 'GET'])
def index():
    coms = db.session.query(companies).all()

    if(request.method == 'POST'):
        val = request.form['type']
        if(val == 'additem'):
            cname = request.form['cname']
            emailid = request.form['emailid']
            mobile = request.form['mobile']
            address = request.form['address']
            com = companies(cname, emailid, mobile, address)
            db.session.add(com)
            db.session.commit()
            coms = db.session.query(companies).all()
            return render_template('home.html', content=[coms])

        elif(val == 'search'):
            term = request.form['sea_trm']
            term = "%" + term + "%"
            res = db.session.query(companies).filter(
                or_(
                    companies.cname.like(term),
                    companies.mobile.like(term),
                    companies.email.like(term),
                    companies.address.like(term)
                )
            ).all()
            coms = db.session.query(companies).all()
            return render_template('home.html', content=[coms, "", res])

        elif(val == 'delete'):
            id = request.form['id']
            db.session.query(companies).filter(companies.id == id).delete()
            db.session.commit()
            coms = companies.query.all()
            return render_template("home.html", content=[coms])

        elif(val == 'edit'):
            ed_id = request.form['id']
            coms = companies.query.all()
            return render_template('home.html', content=[coms, ed_id])

        elif(val == 'edit_id'):
            id = request.form['id']
            cname = request.form['cname']
            email = request.form['emailid']
            mobile = request.form['mobile']
            db.session.query(companies).filter(companies.id == id).update(
                {'cname': cname,
                 'email': email,
                 'mobile': mobile
                 })
            db.session.commit()

            coms = companies.query.all()
            return render_template("home.html", content=[coms, ""])

    return render_template('home.html', content=[coms, ""])


if __name__ == '__main__':
    app.run(debug=True)
