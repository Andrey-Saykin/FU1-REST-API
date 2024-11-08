from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import sqlite_connector as con
from models import db, Base, User, Group, Address

app = Flask(__name__)
app.secret_key="f5ds7dsadsf7dg68s7d5"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite_v01.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

engine = create_engine("sqlite:///sqlite_v01.db", echo=True)
Session = sessionmaker(bind=engine)

with app.app_context():
    Base.metadata.create_all(engine)

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', user=session['user'])
    return render_template('index.html')


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['pw']
        # Hardcoced login for admin and mitarbeiter
        if email == "admin@gmail.com" and pw == "admin1234" \
        or email == "mitarbeiter@gmail.com" and pw == "mitarbeiter1234":
            session['user'] = email
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/admin/dashboard/api', methods=['GET', 'POST'])
def admin_dashboard_api():
    if not 'user' in session:
        return redirect(url_for('login'))
    
    context = {'user': session['user']}
    
    return render_template('admin_dashboard_api.html', **context)


@app.route('/shop')
def shop():
    print(session)
    context = {'member': 'Nicht-Kunden'}
    if 'user' in session:
        context['member'] = 'Kunden'
        context['user'] = session['user']   
    return render_template('shop_member.html', **context)

# API Routes

# curl -X GET http://127.0.0.1:4000/api/v1/user -H "Content-Type: application/json"
# curl -X PUT http://127.0.0.1:4000/api/v1/user -H "Content-Type: application/json" -d '{"first_name":"deinvorname", "last_name":"deinnachname", "email":"deineemail@gmail.com","is_active":true,"is_staff":false,"is_superuser":false,"address_id":null}'
@app.route('/api/v1/user', methods=['GET', 'PUT'])
def api_v1_user():
    print('api_v1_user')
    if request.method == 'GET':
        with Session() as session:
            users = session.execute(select(User)).scalars().all()
            users_list = [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users]
            return jsonify(users_list)
    elif request.method == 'PUT':
        data = request.get_json()
        print(data)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        is_active = data.get('is_active', True)
        is_staff = data.get('is_staff', False)
        is_superuser = data.get('is_superuser', False)
        address_id = data.get('address_id')

        if not first_name or not last_name or not email:
            return jsonify({'message': 'Missing required fields'}), 400
        
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            address_id=address_id
        )

        with Session() as session:
            session.add(new_user)
            session.commit()
            return jsonify({'message': 'User added successfully.'}), 201

    return jsonify({'message': 'Invalid request method.'})

# curl -X GET http://127.0.0.1:4000/api/v1/user/1 -H "Content-Type: application/json"
# curl -X UPDATE http://127.0.0.1:4000/api/v1/user/1 -H "Content-Type: application/json" -d '{"first_name":"newname", "last_name":"newlastname"}'
# curl -X DELETE http://127.0.0.1:4000/api/v1/user/1 -H "Content-Type: application/json"
@app.route('/api/v1/user/<int:user_id>', methods=['GET', 'UPDATE', 'DELETE'])
def api_v1_user_id(user_id):
    if request.method == 'GET':
        with Session() as session:
            user = session.execute(select(User).where(User.id == user_id)).scalar()
            if not user:
                return jsonify({'message': 'User not found.'}), 404
            user_dict = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'address_id': user.address_id
            }
            return jsonify(user_dict)
    elif request.method == 'UPDATE':
        data = request.get_json()
        allowed_fields = ['first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'address_id']
        filtered_data = {key: value for key, value in data.items() if key in allowed_fields}

        if not filtered_data:
            return jsonify({'message': 'No valid fields to update in json.'}), 400
        
        with Session() as session:
            user = session.execute(select(User).where(User.id == user_id)).scalar()
            if not user:
                return jsonify({'message': 'User not found.'}), 404

            for key, value in filtered_data.items():
                setattr(user, key, value)
            session.commit()
            return jsonify({'message': 'User updated successfully.'}), 200
    elif request.method == 'DELETE':
        with Session() as session:
            user = session.execute(select(User).where(User.id == user_id)).scalar()
            if not user:
                return jsonify({'message': 'User not found.'}), 404
            session.delete(user)
            session.commit()
            return jsonify({'message': 'User deleted successfully.'}), 200

# curl -X GET http://127.0.0.1:4000/api/v1/supplier -H "Content-Type: application/json"
# curl -X PUT http://127.0.0.1:4000/api/v1/supplier -H "Content-Type: application/json" -d '{"name":"deinname","address":"witzig","city":"rofl","zip_code":"68750","country":"flashland","contact_name":"Peter","contact_phone":"46576879087","contact_email":"123@gmail.com"}'
@app.route('/api/v1/supplier', methods=['GET', 'PUT'])
def api_v1_supplier():
    success = False
    if request.method == 'GET':
        result = con.get_supplieres()
        success = True
        return {'success': success, 'result': result}
    elif request.method == 'PUT':
        print('PUT')
        data = request.get_json()
        print(data)
        name = data.get('name')
        address = data.get('address')
        city = data.get('city')
        zip_code = data.get('zip_code')
        country = data.get('country')
        contact_name = data.get('contact_name')
        contact_phone = data.get('contact_phone')
        contact_email = data.get('contact_email')

        if name and address and city and zip_code and country and contact_name and contact_phone and contact_email:
            row_count = con.create_supplier(name, address, city, zip_code, country, contact_name, contact_phone, contact_email)
            if row_count:
                success = True
                return {'success': success, 'message': 'Supplier added successfully.'}
            return {'success': success, 'message': 'An error occurred while adding the supplier.'}
        else:
            return {'success': success, 'message': 'Missing required fields.'}
    return {'success': success, 'message': 'Invalid request method.'}


# curl -X UPDATE http://127.0.0.1:4000/api/v1/supplier/1 -H "Content-Type: application/json" -d '{"name":"mein_name","contact_name":"PeterWal"}'
@app.route('/api/v1/supplier/<int:supplier_id>', methods=['GET', 'UPDATE', 'DELETE'])
def api_v1_supplier_id(supplier_id):
    success = False
    if request.method == 'GET':
        result = con.get_supplier(supplier_id)
        success = True
        return {'success': success, 'result': result}
    elif request.method == 'UPDATE':
        data = request.get_json()

        allowed_fields = ['name', 'address', 'city', 'zip_code', 'country', 'contact_name', 'contact_phone', 'contact_email']
        filtered_data = {key: value for key, value in data.items() if key in allowed_fields}

        if not filtered_data:
            return {'success': success, 'message': 'No valid fields to update in json.'}
        
        if filtered_data != data:
            print('Some fields that are not allowed were removed.')

        columns = tuple(filtered_data.keys())
        values = tuple(filtered_data.values())
        changes = con.update_supplier(supplier_id, columns, values)
        if changes:
            success = True
            return {'success': success, 'message': 'Supplier updated successfully.'}
        return {'success': success, 'message': 'No changes applied.'}
        
    elif request.method == 'DELETE':
        result = con.delete_supplier(supplier_id)
        if result:
            success = True
            return {'success': success, 'message': 'Supplier deleted successfully.'}
        return {'success': success, 'result': 'No supplier found with the given id.'}
    return {'success': success, 'message': 'Invalid request method.'}


if __name__ == '__main__':
    app.run(port=4000, debug=True)

