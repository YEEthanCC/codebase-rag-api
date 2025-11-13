import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
import datetime
from app import db
from flask import jsonify
from sqlalchemy import asc, desc

def get_all_users(page, per_page, sort_by, order):
    query = User.query
    if order == "asc" and sort_by:
        query = query.order_by(asc(sort_by))
    elif order == "desc" and sort_by:
        query =  query.order_by(desc(sort_by))
    users = None
    if not page or not per_page:
        users = query.all()
    else:
        users = query.paginate(page=int(page), per_page=int(per_page))
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['fullname'] = user.fullname
        user_data['created_at'] = user.created_at
        user_data['updated_at'] = user.updated_at
        output.append(user_data)
    
    return jsonify({'users': output})

def get_users_by_name(fullname):
    users = User.query.filter_by(fullname=fullname).all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['fullname'] = user.fullname
        user_data['created_at'] = user.created_at
        user_data['updated_at'] = user.updated_at
        output.append(user_data)
    return jsonify({'users': output})

def get_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user found!'}), 404
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['fullname'] = user.fullname
    user_data['created_at'] = user.created_at
    user_data['updated_at'] = user.updated_at
    return jsonify({'user': user_data})

def create_user(fullname, pwd):
    hashed_pwd = generate_password_hash(pwd, method='pbkdf2:sha256')
    new_user = User(public_id=str(uuid.uuid4()), fullname=fullname, pwd=hashed_pwd, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now()) 
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})

def get_public_id(fullname, pwd):
    users = User.query.filter_by(fullname=fullname).all()
    if len(users) == 0:
        return None
    for user in users:
        if check_password_hash(user.pwd, pwd): 
            return user.public_id
    return None

def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user found!'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'The user has been deleted!'}), 200

def udpate_user(public_id, fullname, pwd):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user found!'}), 404
    user.fullname = fullname
    user.pwd = generate_password_hash(pwd, method='pbkdf2:sha256')
    user.updated_at = datetime.datetime.now() 
    db.session.commit()
    return jsonify({'message': 'The user has been updated!'})