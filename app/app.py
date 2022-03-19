# LIMIT 1 in all create queries came from
# https://mariadb.com/docs/clients/mariadb-connectors/connector-python/development/
# (I didn't originally think of that)

from flask import Flask, abort, redirect, render_template, request


app = Flask(__name__)
config_loaded = app.config.from_pyfile('config.py')
if not config_loaded:
    raise Exception("Could not load configuration file.")

from werkzeug.exceptions import *

import database as db
from localization import *
from queries import queries
from table import Table
from form import *
from link import *
from sanitize import sanitize
from validate import *

def page(key, content, error=False):
    return render_template(
        'page.jinja',
        title=localize(key),
        error=error,
        navlinks=navlinks(),
        content=content)

@app.before_request
def before():
    db.connect()

@app.teardown_request
def teardown(err=None):
    db.close_connection()

#TODO update these to be the proper fallthroughs for all 500 errors
@app.errorhandler(InternalServerError)
def server_error(error):
    status = error.get_response().status
    title = 'error_500_title'
    description = localize('error_500_description')
    summary = localize('error_500_summary')
    content = render_template(
        'error.jinja',
        summary=summary,
        description=description,
        status=status)

    return page(title, content, error=True), status

@app.errorhandler(BadRequest)
def bad_request(error):
    status = error.get_response().status
    title = 'error_400_title'
    description = localize('error_400_description')
    summary = localize('error_400_summary')
    content = render_template(
        'error.jinja',
        summary=summary,
        description=description,
        status=400)

    return page(title, content, error=True), status

@app.errorhandler(404)
def not_found(error):
    status = error.get_response().status
    description = localize('error_404_description')
    summary = localize('error_404_summary')
    content = render_template(
        'error.jinja',
        summary=summary,
        description=description,
        status=404)

    return page('error_404_title', content, error=True), 404

@app.route('/')
def index():
    welcome = render_template('welcome.jinja', message=localize('welcome_message'))
    return page('welcome_title', content=welcome)

@app.route('/bibliography')
def view_bibliography():
    bibliography=render_template('bibliography.jinja')
    return page('bibliography', bibliography)

@app.route('/<table>')
def read(table):
    return redirect(f'/{table}/page/1')

@app.route('/<table>/page/<int:pageno>')
def read_page(table, pageno):
    if f'read_{table}' not in queries:
        abort(404)

    num_ids = 1
    num_hidden = 0
    extra_buttons = []
    if table == 'ingredients':
        num_ids = 2
        num_hidden = 2
    if table == 'drinks':
        extra_buttons = [Link('/ingredients/for/', 'ingredients', ['read-button'])]


    query = queries[f'read_{table}']
    if (len(request.args) > 0 and
        not all(value == '' for value in request.args.values())):
        filters = ''

            
        for (submit_key, submit_value) in request.args.items():
            key = sanitize(submit_key)
            value = sanitize(submit_value)
            if value != '':
                filters += f"{key} LIKE '{value}' AND "
        query = f'SELECT * FROM ({query}) AS results WHERE {filters[:-5]}'

    table_obj = Table(query,
                  prefix=table,
                  num_ids=num_ids,
                  num_hidden=num_hidden,
                  extra_buttons=extra_buttons)
    
    return page(table, table_obj.render(pageno))

@app.route('/ingredients/for/<int:drink_id>')
def read_ingredients_for_drink(drink_id):
    try:
        cursor = db.execute(f'''SELECT name FROM Drinks WHERE id = {drink_id}''')
        mixed_drink_name = f'{cursor.fetchone()[0]}'
    except:
        abort(404);
    finally:
        cursor.close()
    
    query = queries['read_ingredients_for'].format(drink_id)
    table = Table(query, prefix='ingredients', num_ids=2, num_hidden=2)

    pagetitle = localize_for_clause('ingredients', mixed_drink_name)
    return page(pagetitle, table.render())

@app.route('/<table>/create', methods=['GET', 'POST'])
def create(table):
    if table not in ['customers', 'drinks', 'purchases', 'tabs', 'ingredients']:
        abort(404)

    immutable = [] if table == 'ingredients' else ['id']
    form = Form.build_form(table, immutable)
    
    if request.method == 'GET':
        return page(f'{table}_create', form.render())
    else:
        # POST
        post_effects = []
        if table == 'purchases':
            post_effects = [Form.use_inventory]
        feedback, ok = form.validate_and_submit(request.form, table, post_effects=post_effects)
        title = 'create_success' if ok else 'create_failure'
        status = 201 if ok else 400
        return page(title, feedback, error=not ok), status


@app.route('/<table>/edit/<int:id>', methods=['GET', 'POST'])
def edit(table, id):
    if table not in ['customers', 'drinks', 'purchases', 'tabs']:
        abort(404)

    form = Form.build_form(table, ['id'], [id])
    if request.method == 'GET':
        return page(f'{table}_edit', form.render())
    else:
        pre_effects = []
        post_effects = []
        if table == 'purchases':
            pre_effects = [Form.unuse_inventory]
            post_effects = [Form.use_inventory]

        feedback, ok = form.validate_and_submit(
            request.form, table,
            update_id={'id': id},
            post_effects=post_effects,
            pre_effects=pre_effects)
        title = 'edit_success' if ok else 'edit_failure'
        status = 200 if ok else 400
        return page(title, feedback, error=not ok), status

@app.route('/ingredients/edit/<int:ingredient_id>/in/<int:mixed_id>', methods=['GET', 'POST'])
def edit_ingredient_form(ingredient_id, mixed_id):
    form = Form.build_form('ingredients', ['ingredient_drink_id', 'mixed_drink_id'],
                           [ingredient_id, mixed_id])
    if request.method == 'GET':
        return page('ingredients_edit', form.render())
    else:
        feedback, ok = form.validate_and_submit(
            request.form, 'ingredients',
            update_id={
                'ingredient_drink_id': ingredient_id,
                'mixed_drink_id': mixed_id
            })
        title = 'edit_success' if ok else 'edit_failure'
        status = 200 if ok else 400
        return page(title, feedback, error=not ok), status

@app.route('/<table>/delete/<int:id>')
def delete_customer(table, id):
    if table not in ['drinks', 'purchases', 'customers', 'tabs']:
        abort(404)

    query = f'DELETE FROM {table.capitalize()} WHERE id = %d'
    db.execute(query, id)

    return redirect(f'/{table}')

@app.route('/ingredients/delete/<int:ingredient_id>/in/<int:mixed_id>')
def delete_ingredient(ingredient_id, mixed_id):
    query = 'DELETE FROM Ingredients WHERE ingredient_drink_id = %s AND mixed_drink_id = %s'
    db.execute(query, ingredient_id, mixed_id)

    return redirect('/ingredients')

# Listener for local testing
if __name__ == "__main__":
    app.run(port=3400, debug=True)
