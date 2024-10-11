from flask import Flask
from flask import render_template
from flask import request, session, redirect, url_for
from flask import jsonify
import sqlite_connector as con

app = Flask(__name__)
app.secret_key="f5ds7dsadsf7dg68s7d5"

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
        if email == "saykin.developer@gmail.com" and pw == "Test1234!":
            print(session)
            session['user'] = email
            return redirect(url_for('index'))
            # return redirect(url_for('shop'))
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

# @app.route('/api/v1/user', methods=['GET', 'PUT', 'UPDATE', 'DELETE'])
# def api_v1_user():
#     if request.method == 'GET':
#         return {'user': 'GET'}
#     elif request.method == 'PUT':
#         return {'user': 'PUT'}
#     elif request.method == 'UPDATE':
#         return {'user': 'UPDATE'}
#     elif request.method == 'DELETE':
#         return {'user': 'DELETE'}
#     return {'user': 'POST'}


# PUT Code:
# curl -X PUT http://127.0.0.1:4000/api/v1/supplier -H "Content-Type: application/json" -d '{"name":"deinname","address":"witzig","city":"rofl","zip_code":"68750","country":"flashland","contact_name":"Peter","contact_phone":"46576879087","contact_email":"123@gmail.com"}'
@app.route('/api/v1/supplier', methods=['GET', 'PUT'])
def api_v1_supplier():
    success = False
    if request.method == 'GET':
        result = con.get_supplieres()
        success = True
        return {'success': success, 'result': result}
    elif request.method == 'PUT':
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
            supplier_id = con.create_supplier(name, address, city, zip_code, country, contact_name, contact_phone, contact_email)
            if supplier_id:
                success = True
                return {'success': success, 'id': supplier_id, 'message': 'Supplier added successfully.'}
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

