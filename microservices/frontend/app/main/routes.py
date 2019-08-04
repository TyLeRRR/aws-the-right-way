import json
import logging

import requests, os
from flask import render_template, current_app, flash, redirect, url_for
from tenacity import before_log, retry, stop_after_attempt
from app.main import bp
from app.forms.forms import SubmitStockForm

logger = logging.getLogger('routes')


@bp.route('/')
@bp.route('/index', methods=['GET', 'POST'])
def index():
    response = requests.get(current_app.config['STOCK_SYMBOL_SERVICE_URL'])
    data = response.json()
    stock = {'name': data['stock']['name'],
             'logo_url': data['stock']['logo_url']}
    return render_template('index.html', title='Home', stock=stock)


@bp.route('/addstock', methods=['GET', 'POST'])
@retry(stop=stop_after_attempt(5),
       before=before_log(logger, logging.DEBUG))
def add_stock():
    form = SubmitStockForm()
    if form.validate_on_submit():
        save_logo(logo_file=form.logo.data, stock_name=form.stock.data)
        save_stock(form.stock)
        flash('Thank you for submitting a new stock symbol!')
        return redirect(url_for('main.index'))
    return render_template('addstock.html', title='Add New Stock Symbol', form=form)


def save_stock(stock_name):
    data = {'name': stock_name.data}

    requests.post(current_app.config['STOCK_SYMBOL_SERVICE_URL'], json=data)
    return 'OK'


def save_logo(logo_file, stock_name):
    filename = stock_name + '.jpeg'
    logo_file.save('./' + filename)
    file_path = './' + filename

    data = open(file_path, 'rb').read()
    stock_name = {'name': stock_name}

    stock = {
        'name': (None, json.dumps(stock_name), 'application/json'),
        'image': data
    }
    requests.post(current_app.config['LOGO_RESIZER_SERVICE_URL'], files=stock)
    os.remove(file_path)


@bp.route('/api/ping', methods=["GET"])
def ping():
    return 'OK'
