import os
import unittest
from app import db,app
from sqlalchemy import func
from sqlalchemy import create_engine



class BasicTests(unittest.TestCase):
 
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cs162_user:cs162_password@localhost/cs162?port5432'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
     
    def test_add(self):
        response = self.app.post( '/add', data = dict(expression="2*5"), follow_redirects=True)
        self.assertEqual(Expression.query.filter(id == 1), 10)
        
    def test_crapinput(self):
        response = self.app.post( '/add', data = dict(expression="asd"), follow_redirects=True)
        self.assertEqual(response.status_code, 500 )
        
    def test_noaddedrows(self):
        self.assertEqual(Expression.query(func.count(id)) == 1)
        
        
@app.route('/add', methods=['POST'])
def add():
    expression = text = request.form['expression']
    p = Parser(expression)
    value = p.getValue()
    now = datetime.utcnow()

    db.session.add(Expression(text=expression, value=value, now=now))
    db.session.commit()

    return redirect(url_for('index'))
