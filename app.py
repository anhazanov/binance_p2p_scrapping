from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import MultiDict
import time
import ast

from flask import Flask, render_template, url_for, request, jsonify, redirect, flash, get_flashed_messages, make_response, session, sessions
from flask_session import Session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_parameter

from db import Database
from UserLogin import UserLogin
from main_config import logo_list

app = Flask(__name__)
app.secret_key = 'super secret key'


conn = Database() # connect to DB

login_manager = LoginManager(app) # login Flask
login_manager.login_view = 'singin'
login_manager.login_message = 'Авторизуйтесь для доступа к закрытым разделам'
login_manager.login_message_category = 'success'

MAX_CONTENT_LENGTH = 1024 * 1024
ROWS_PER_PAGE = 20

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id)

@app.route('/')
@app.route('/home')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/singin', methods=['POST', 'GET'])
def singin():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        print('where?')
        user = conn.getUserByEmail(request.form['email'])
        if user and check_password_hash(user[3], request.form['psw']):
            userLogin = UserLogin().creat(user)
            rm = True if request.form.get('remaime') else False
            login_user(userLogin, remember=rm)
            return redirect(request.args.get('next') or url_for('profile'))
        flash('Неверная пара логин/пароль', 'error')

    return render_template('singin.html')

@app.route('/singup', methods=['POST', 'GET'])
def singup():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 and \
            len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            result = conn.addUser(request.form['name'], request.form['email'], hash)
            if result:
                flash("Вы успешно зарегистрированы", "success")
                return redirect('singin')
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля. Логин или пароль менее 5 символов.", "error")

    return render_template('singup.html')


@app.route('/trades', methods=["POST","GET"])
@login_required
def trades():
    # if current_user.getPay() and float(current_user.getPay()) > float(time.time()):
    if True:
        conn = Database()
        exchange = conn.select_row('exchange1')
        bnk1 = conn.select_row('bank1')
        bnk2 = conn.select_row('bank2')
        rl = conn.select_row('role')
        cryptos = set([el[0].split('>')[0] for el in conn.select_row('crypto_path')])
        cryptos = [(el, ) for el in cryptos]
        st_min = [(500, ), (1000, ), (2000, ), (5000, ), (10000, ), (20000, ), (50000, ), (100000, )]
        if request.method == 'POST':
            print(request.form)
            exch1 = f"IN {tuple(request.form.getlist('exchange1[]'))}" if len(request.form.getlist('exchange1[]')) > 1 else f"IN {tuple([el[0] for el in exchange])}" \
                    if len(request.form.getlist('exchange1[]')) != 1 else f"LIKE '{tuple(request.form.getlist('exchange1[]'))[0]}'"
            exch2 = f"IN {tuple(request.form.getlist('exchange2[]'))}" if len(request.form.getlist('exchange2[]')) > 1 else f"IN {tuple([el[0] for el in exchange])}" \
                    if len(request.form.getlist('exchange2[]')) != 1 else f"LIKE '{tuple(request.form.getlist('exchange2[]'))[0]}'"
            bank1 = f"IN {tuple(request.form.getlist('bank1[]'))}" if len(request.form.getlist('bank1[]')) > 1 else f"IN {tuple([el[0] for el in bnk1])}" \
                    if len(request.form.getlist('bank1[]')) != 1 else f"LIKE '{tuple(request.form.getlist('bank1[]'))[0]}'"
            bank2 = f"IN {tuple(request.form.getlist('bank2[]'))}" if len(request.form.getlist('bank2[]')) > 1 else f"IN {tuple([el[0] for el in bnk2])}" \
                    if len(request.form.getlist('bank2[]')) != 1 else f"LIKE '{tuple(request.form.getlist('bank2[]'))[0]}'"
            crypto_from = ' OR '.join([f"crypto_path LIKE '{el}%'" for el in request.form.getlist('crypto_from[]')]) if len(request.form.getlist('crypto_from[]')) > 0 \
                    else "crypto_path LIKE '%'"

            crypto_to = ' OR '.join([f"crypto_path LIKE '%{el}'" for el in request.form.getlist('crypto_to[]')]) if len(request.form.getlist('crypto_to[]')) > 0 \
                    else "crypto_path LIKE '%'"
            role = f"IN {tuple(request.form.getlist('role[]'))}" if len(request.form.getlist('role[]')) > 1 else f"IN {tuple([el[0] for el in rl])}" \
                    if len(request.form.getlist('role[]')) != 1 else f"LIKE '{tuple(request.form.getlist('role[]'))[0]}'"
            print(exch1)
            print(request.form.getlist('crypto_from[]'))
            print(crypto_from)
            start_min = float(request.form.getlist('start_min[]')[0]) if len(request.form.getlist('start_min[]')) > 0 else 500
            args = request.args
            args.to_dict()
            all_trades = conn.select_data(profit_from=0, exchange1=exch1, exchange2=exch2, bank1=bank1, bank2=bank2, role=role, start_min=start_min, crypto_from=crypto_from, crypto_to=crypto_to)
            # page = request.args.get(get_page_parameter(), type=int, default=1)
            page = 1
            pagination = Pagination(page=page, total=len(all_trades), record_name='all_trades', href="?page={0}" + \
                        f'&exchange1={request.form.getlist("exchange1[]")}&exchange2={request.form.getlist("exchange2[]")}'
                        f'&bank1={request.form.getlist("bank1[]")}&bank2={request.form.getlist("bank2[]")}'
                        f'&crypto_from={request.form.getlist("crypto_from[]")}&crypto_to={request.form.getlist("crypto_to[]")}'
                        f'&role={request.form.getlist("role[]")}&start_min={request.form.getlist("start_min[]")}')
            return render_template('trades.html', exchange=exchange, bank1=bnk1, bank2=bnk2, crypto=cryptos, role=rl, start_min=st_min, all_trades=all_trades[:10], logo_list=logo_list, pagination=pagination)
        elif request.args.to_dict().get('exchange1'):
            args = request.args
            args.to_dict()
            exch1 = f"IN {tuple(ast.literal_eval(args.get('exchange1')))}" if len(ast.literal_eval(args.get('exchange1'))) > 1 else f"IN {tuple([el[0] for el in exchange])}" \
                    if len(ast.literal_eval(args.get('exchange1'))) != 1 else f"LIKE '{tuple(ast.literal_eval(args.get('exchange1')))[0]}'"
            exch2 = f"IN {tuple(ast.literal_eval(args.get('exchange2')))}" if len(
                ast.literal_eval(args.get('exchange2'))) > 1 else f"IN {tuple([el[0] for el in exchange])}" \
                if len(
                ast.literal_eval(args.get('exchange2'))) != 1 else f"LIKE '{tuple(ast.literal_eval(args.get('exchange2')))[0]}'"
            bank1 = f"IN {tuple(ast.literal_eval(args.get('bank1')))}" if len(
                ast.literal_eval(args.get('bank1'))) > 1 else f"IN {tuple([el[0] for el in bnk1])}" \
                if len(ast.literal_eval(args.get('bank1'))) != 1 else f"LIKE '{tuple(ast.literal_eval(args.get('bank1')))[0]}'"
            bank2 = f"IN {tuple(ast.literal_eval(args.get('bank2')))}" if len(
                ast.literal_eval(args.get('bank2'))) > 1 else f"IN {tuple([el[0] for el in bnk2])}" \
                if len(ast.literal_eval(args.get('bank2'))) != 1 else f"LIKE '{tuple(ast.literal_eval(args.get('bank2')))[0]}'"
            crypto_from = ' OR '.join(
                [f"crypto_path LIKE '{el}%'" for el in ast.literal_eval(args.get('crypto_from'))]) if len(
                ast.literal_eval(args.get('crypto_from'))) > 0 \
                else "crypto_path LIKE '%'"
            crypto_to = ' OR '.join([f"crypto_path LIKE '%{el}'" for el in ast.literal_eval(args.get('crypto_to'))]) if len(
                ast.literal_eval(args.get('crypto_to'))) > 0 \
                else "crypto_path LIKE '%'"
            role = f"IN {tuple(ast.literal_eval(args.get('role')))}" if len(
                ast.literal_eval(args.get('role'))) > 1 else f"IN {tuple([el[0] for el in rl])}" \
                if len(ast.literal_eval(args.get('role'))) != 1 else f"LIKE '{tuple(ast.literal_eval(args.get('role')))[0]}'"
            start_min = float(ast.literal_eval(args.get('start_min'))[0]) if len(
                ast.literal_eval(args.get('start_min'))) > 0 else 500
            all_trades = conn.select_data(profit_from=0, exchange1=exch1, exchange2=exch2, bank1=bank1, bank2=bank2,
                                          role=role, start_min=start_min, crypto_from=crypto_from, crypto_to=crypto_to)
            page = request.args.get(get_page_parameter(), type=int, default=1)
            pagination = Pagination(page=page, total=len(all_trades), record_name='all_trades', href="?page={0}" + \
                                 f'&exchange1={args.get("exchange1")}&exchange2={args.get("exchange2")}'
                                 f'&bank1={args.get("bank1")}&bank2={args.get("bank2")}'
                                 f'&crypto_from={args.get("crypto_from")}&crypto_to={args.get("crypto_to")}'
                                 f'&role={args.get("role")}&start_min={args.get("start_min")}')
            return render_template('trades.html', exchange=exchange, bank1=bnk1, bank2=bnk2, crypto=cryptos, role=rl,
                                   start_min=st_min, all_trades=all_trades[(int(args.get('page', 1)) * 10 - 10):(
                            int(args.get('page', 1)) * 10)], logo_list=logo_list, pagination=pagination)
        else:
            args = request.args
            args.to_dict()
            all_trades = conn.select_data(profit_from=0,)
            page = request.args.get(get_page_parameter(), type=int, default=1)
            pagination = Pagination(page=page, total=len(all_trades), record_name='all_trades')
            return render_template('trades.html', exchange=exchange, bank1=bnk1, bank2=bnk2, crypto=cryptos, role=rl, start_min=st_min, all_trades=all_trades[(int(args.get('page', 1))*10 - 10):(int(args.get('page', 1))*10)], logo_list=logo_list, pagination=pagination)
    else:
        return render_template('/needpay.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Bы вышли из аккаунта","success")
    return redirect(url_for('singin'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
         return""
    h = make_response(img)
    h.headers['Content-Type'] ='images/png'
    return h

@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
         file = request.files['file']
         if file and current_user.verifyExt(file.filename):
              try:
                   img = file.read()
                   res = conn.updateUserAvatar(img, current_user.get_id())
                   if not res:
                        flash("Ошибка обновления аватара", "error")
                   flash("Aвaтaр обновлен", "success")
              except FileNotFoundError as e:
                   flash("Ошибка чтения файлa", "error")
         else:
              flash("Ошибка обновления аватара", "error")
    return redirect(url_for('profile'))

@app.route('/successful')
@login_required
def successful():
    return render_template('successful.html')

@app.route('/failed')
@login_required
def failed():
    return render_template('failed.html')

@app.route('/pay-responce', methods=['POST', 'GET'])
@login_required
def pay_responce():
    if request.method == 'POST':
        print(request.form)

if __name__ == '__main__':
    app.run(debug=True)
