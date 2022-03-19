import database as db

from datetime import datetime

class ValidationException(Exception):
    pass

def drink_ingredients(drink_id, quantity):
    query = f'''SELECT ingredient_drink_id, mixed_drink_id, quantity * {quantity} as quantity
    FROM Ingredients WHERE mixed_drink_id = {drink_id}'''
    cursor = db.execute(query)
    ingredients = cursor.fetchall()
    cursor.close()
    return ingredients

def drink_in_stock(drink_id, quantity):
    query = f'''SELECT stock FROM Drinks WHERE id = {drink_id}'''
    cursor = db.execute(query)
    stock = cursor.fetchone()[0]
    cursor.close()
    return quantity <= stock

def verify_acyclic(mixed_id, ingredient_id, marked, down=True, up=True):
    print(f'Verifying mixed: {mixed_id} and ingredient: {ingredient_id} are acyclic (down {down})')
    if ((ingredient_id in marked and down) or
        (mixed_id in marked and up) or
        ingredient_id == mixed_id):
        raise ValidationException(f'''
        You have a cyclic ingredient reference.''')

    marked.add(mixed_id)
    marked.add(ingredient_id)
    
    # Technically we could pass the ingredients down and filter them
    # to avoid the need for db communication, but let's just start
    # with this

    # Propagate down down the ingredient tree looking for duplicates
    # We may have say...lime juice as an ingredient twice if a sub
    # cocktail uses lime juice, and this drink adds more...this should allow
    # for that
    down_marked = []
    if down:
        cursor = db.execute('''
        SELECT mixed_drink_id, ingredient_drink_id 
        FROM Ingredients 
        WHERE mixed_drink_id = %d
        ''', ingredient_id)
        sub_ingredients = cursor.fetchall()
        cursor.close()
        for ingredient in sub_ingredients:
            result = verify_acyclic(ingredient[0], ingredient[1], set(marked), up=False)
            down_marked.append(result)

    for down_mark in down_marked:
        marked.update(down_mark)

    if up:
        # Propagate up the ingredient tree looking for duplicates
        cursor = db.execute('''
        SELECT mixed_drink_id, ingredient_drink_id 
        FROM Ingredients 
        WHERE ingredient_drink_id = %d
        ''', mixed_id)
        mixed_products = cursor.fetchall()
        cursor.close()
        for drink in mixed_products:
            marked = verify_acyclic(drink[0], drink[1], marked, down=False)

    return marked

def extra_validations(table, update=False):
    # Our extra validation functions... 
    field_validators = {}
    form_validators = {
        'ingredients_create': validate_ingredient,
        'ingredients_update': validate_ingredient_edit,
        'purchases_create': validate_purchase,
        'tabs_create': validate_tab
    }
    
    if table == 'customers':
        field_validators['uba'] = lambda uba: None if len(uba) == 20 else '''
        UBA must be a 20 character string'''
    elif table == 'purchases':
        field_validators['date'] = lambda date: None if date <= datetime.now() else '''
        Cannot create a purchase in the future'''

    update_str = 'update' if update else 'create'
    form_validate = form_validators.get(f'{table}_{update_str}')

    return field_validators, form_validate

def validate_ingredient(form):
    ingredient_id = form.get_field('ingredient_drink_id').get_value()
    mixed_id = form.get_field('mixed_drink_id').get_value()
    cursor = db.execute('''
    SELECT mixed_drink_id, ingredient_drink_id FROM Ingredients 
    WHERE mixed_drink_id = %d AND ingredient_drink_id = %d
    LIMIT 1''', mixed_id, ingredient_id)
    ingredients = cursor.fetchall()
    cursor.close()

    if (mixed_id, ingredient_id) in ingredients:
        raise ValidationException('''You already have that drink
        in your cocktail, you should edit the existing ingredient
        instead.''')

    verify_acyclic(mixed_id, ingredient_id, set())

def validate_ingredient_edit(form):
    ingredient_id = form.get_field('ingredient_drink_id').get_value()
    mixed_id = form.get_field('mixed_drink_id').get_value()

    verify_acyclic(mixed_id, ingredient_id, set())

def validate_purchase(form):
    purchase_time = form.get_field('date').get_value()
    tab_id = form.get_field('tab_id').get_value()

    cursor = db.execute('SELECT due FROM Tabs WHERE id = %d', tab_id)
    tab_due = cursor.fetchone()[0]
    cursor.close()

    if purchase_time > tab_due:
        raise ValidationException('''
        Cannot add a purchase to a tab after the due date of that tab''')

def validate_tab(form):
    customer_field = filter(lambda field: field.key == 'customer_id', form.fields)
    fk_customer = next(customer_field).get_value()
    cursor = db.execute('SELECT * FROM Tabs WHERE customer_id = %d AND ISNULL(paid)', fk_customer)
    value = cursor.fetchone()
    cursor.close()
    if value != None:
        raise ValidationException('Cannot open a tab for a customer with a tab unpaid.')
