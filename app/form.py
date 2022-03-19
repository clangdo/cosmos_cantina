from flask import render_template
import mariadb as mdb

from math import trunc
from datetime import datetime

from localization import *
from queries import queries
from sanitize import sanitize
from validate import *
import database as db


class FormField:
    __db_to_input_type = {
        'INT': 'number',
        'LONG': 'number',
        'DECIMAL': 'number',
        'NEWDECIMAL': 'number',
        'TIMESTAMP': 'datetime-local',
        'VAR_STRING': 'text',
        'STRING': 'text',
        'TINY': 'checkbox',
    }
    
    def __init__(
            self, key, db_type, properties=[], locale_key=None,
            required=True, prefill='', disabled=False, options=None,
            submit_value=None, extra_validate=None):
        if locale_key is None:
            locale_key = key

        self.key = key
        self.name = localize(locale_key)
        self.db_type = db_type
        self.input_type = FormField.__db_to_input_type[db_type]
        self.properties = properties
        self.required = required
        self.prefill = int(prefill) if prefill and self.input_type == 'checkbox' else prefill
        self.disabled = disabled
        self.options = options
        self.extra_validate = extra_validate
        if submit_value is not None:
            self.set_value(submit_value)

    def get_value(self):
        return self.__value
            
    def set_value(self, value):
        if value == '':
            value = None

        self.__value = self.validate(value)

    def validate_int(self, submission):
        try:
            float_parse = float(submission)
            if float_parse != trunc(float_parse):
                raise Exception()
            elif float_parse < 0.0:
                raise Exception()

            int_parse = int(submission)
        except:
            raise ValidationException(f'''{self.name} should be a non-negative integer, 
            but it was {submission}.''')

        return int_parse

    def validate_decimal(self, submission):
        try:
            float_parse = float(submission)
        except:
            raise ValidationException(f'''{self.name} should be a decimal value, 
            but it was {submission}.''')

        if (float_parse < 0.0 or float_parse > 99_999.99):
            raise ValidationException(f'''{self.name} should be between 0.0 and
            99,999.00 but it was {submission}.''')

        return float_parse

    def validate_string(self, submission):
        sanitized = sanitize(submission)
        if len(sanitized) > 255:
            raise ValidationException(f'''{self.name} must be less than 256 characters,
            but it was {len(sanitized)} characters.''')

        return sanitized

    def validate_timestamp(self, submission):
        try:
            try:
                ts = datetime.strptime(submission, '%Y-%m-%dT%H:%M:%S')
            except:
                ts = datetime.strptime(submission, '%Y-%m-%dT%H:%M')
        except Exception as e:
            raise ValidationException(f'''{self.name} should be a date but it was {submission}''')

        return mdb.Timestamp(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second)
            
    def validate_type(self, submission):
        if(self.db_type in ('INT', 'LONG')):
            return self.validate_int(submission)

        if(self.db_type == 'TINY'):
            return self.validate_int(1 if submission == 'on' else 0)

        if(self.db_type in('DECIMAL', 'NEWDECIMAL')):
            return self.validate_decimal(submission)

        if(self.db_type in('STRING', 'VAR_STRING')):
            return self.validate_string(submission)

        if(self.db_type == 'TIMESTAMP'):
            return self.validate_timestamp(submission)
        
    def validate(self, submission):
        if submission is None and self.required:
            raise ValidationException(f'''{self.name} was required but no value was given''')

        if submission is not None or self.db_type == 'TINY':
            # This may throw a validation exception
            result = self.validate_type(submission)

            if self.extra_validate is not None:
                error = self.extra_validate(result)
                if error is not None:
                    raise ValidationException(error)

            return result
        return None

class Form:
    def __init__(
            self, fields,
            validate=None,
            submit_url=None,
            cancel_url=None,
            cancel_text=None,
            submit_text=None,
            custom_buttons=None):
        
        if cancel_text is None:
            cancel_text = localize('form_cancel_default')
        if submit_text is None:
            submit_text = localize('form_submit_default')

        self.fields = fields
        self.validate = validate
        self.submit_url = submit_url
        self.cancel_url = cancel_url
        self.cancel_text = cancel_text
        self.submit_text = submit_text
        self.custom_buttons = custom_buttons

    def render(self):
        # Pretty sure there's a better way of doing this (implementing
        # some interface) but for now this works.
        return render_template('form.jinja', form=self)

    @staticmethod
    def _get_dropdown_options(name):
        query = queries[f'{name}_dropdown']
        cursor = db.execute(query);
        options = cursor.fetchall()
        cursor.close()
        return options

    @staticmethod
    def build_form(table, pk = ['id'], prefill_id = None):
        field_validators, form_validate = extra_validations(table, prefill_id is not None)
        fk_map = {
            'customers':[],
            'drinks':[],
            'ingredients':['mixed_drink_id', 'ingredient_drink_id'],
            'purchases':['tab_id','drink_id'],
            'tabs':['customer_id']
        }

        query = queries[f'{table}_form']
        if prefill_id is not None:
            query = ' '.join((query, f'WHERE {pk[0]} = {prefill_id[0]}'))
            for i in range(1, len(pk)):
                query = ' AND '.join((query, f'{pk[i]} = {prefill_id[i]}'))

        query = ' '.join((query, 'LIMIT 1'))
        fields = Form.table_fields(query, pk, table,
                                   prefill_id is not None,
                                   fk_map[table], field_validators)
        return Form(fields, form_validate, cancel_url=f'/{table}/page/1')
    
    @staticmethod
    def table_fields(query, immutable=[], prefix='', prefill=False, fks=[],
                     field_validators={}):
        '''Returns a list of fields suitable for the columns of 'table'

        'immutable' should be a list of specific column names to ignore
        when creating the list of fields.
        '''
        fields = []

        cursor = db.execute(query)
        row = None
        if prefill:
            row = cursor.fetchone()
        description = cursor.description
        cursor.close()
        fieldinfo = mdb.fieldinfo()

        for i in range(len(description)):
            column = description[i]
            db_name = column[0]
            dropdown = None
            disabled = db_name in immutable
            if not prefill and disabled:
                continue

            if db_name in fks:
                options = Form._get_dropdown_options(db_name)
            else:
                options = None
            
            name = f'{prefix}_{db_name}'
            db_type = fieldinfo.type(column)
            nullable = column[6]

            value = '' if row is None or row[i] is None else row[i]
            extra_validate=field_validators.get(db_name)
            required = not nullable and not db_type == 'TINY'
            
            field = FormField(
                db_name,
                db_type,
                locale_key=name,
                required=required,
                prefill=value,
                disabled=disabled,
                options=options,
                extra_validate=extra_validate)
            fields.append(field)

        return fields
    
    def set_values(self, submitted):
        errors = {}
        for field in self.fields:
            # Make sure we have all the required fields submitted
            if field.key not in submitted and field.required:
                errors[field.key] = f'Required value {field.name} not found in submission!'

            # Do further validation on the actual submitted values,
            # including any custom validators we've passed
            try:
                field.set_value(submitted.get(field.key))
            except ValidationException as err:
                errors[field.key] = str(err)

        if len(errors) == 0:
            try:
                if self.validate is not None:
                    self.validate(self)
            except ValidationException as err:
                errors['Form'] = str(err)

        return errors

    def submit(self, table_name, where):
        comma_separate = lambda val: f'{val},'
        enabled_fields = list(filter(lambda field: not field.disabled, self.fields))

        if len(where) > 0:
            setstr = ', '.join((f"{field.key} = ?" for field in self.fields))
            where_clause = ' AND '.join((f"{key} = {value}" for key, value in where.items()))
            query = queries['update'].format(table_name.capitalize(), setstr, where_clause)
        else:
            keystr = ', '.join(str(field.key) for field in self.fields)
            keystr = ''.join(('(', keystr, ')'))
            valuestr = ', '.join('?' for field in self.fields)
            valuestr = ''.join(('(', valuestr, ')'))
            query = queries['create'].format(table_name.capitalize(), keystr, valuestr)

        values = tuple(field.get_value() for field in self.fields)
        cursor = db.execute(query, *values);

    def try_effects(self, effects, description_key):
        errors = {}
        for effect in effects:
            try:
                effect(self)
            except ValidationException as e:
                db.rollback()
                errors['Side Effects'] = str(e)
                description = localize(description_key)
                page_content = render_template(
                    'form_error.jinja',
                    description=description,
                    errors=errors)

                return page_content, False
            
        return None
        
    def validate_and_submit(self, submitted, table_name, update_id={}, pre_effects=[], post_effects=[]):
        values = {}
        values.update(update_id)
        values.update(submitted)
        errors = self.set_values(values)
        operation = 'create' if len(update_id) == 0 else 'update'
        if not len(errors) == 0:
            description = localize(f'{table_name}_{operation}_failure')
            page_content = render_template(
                'form_error.jinja',
                description=description,
                errors=errors)

            # Be very careful this line stays here, the execution
            # below MUST NOT OCCUR if there are validation errors
            return page_content, False


        result = self.try_effects(pre_effects, f'{table_name}_{operation}_failure')
        if result is not None:
            return result;
        
        self.submit(table_name, update_id)

        result = self.try_effects(post_effects, f'{table_name}_{operation}_failure')
        if result is not None:
            return result;

        page_title = localize(f'create_success')
        description = localize(f'{table_name}_{operation}_success')
        page_content = render_template(
            'form_success.jinja',
            description=description)

        return page_content, True

    def get_field(self, key):
        # This is not the best way to do a search...
        # but it will do for now
        return next(filter(lambda field: field.key == key, self.fields))

    # NOTE THIS IS CURRENTLY UNUSED, IT NEEDS TO BE HOOKED UP AS A SIDE EFFECT OF
    # PURCHASE CREATION AND EDITING
    def use_inventory(form):
        to_make_id = form.get_field('drink_id').get_value()
        quantity = form.get_field('quantity').get_value()
        Form.make_drink(to_make_id, quantity)

    def unuse_inventory(form):
        id = form.get_field('id').get_value()
        cursor = db.execute('SELECT drink_id, quantity FROM Purchases WHERE id = ?', id)
        drink_id, quantity = cursor.fetchone()
        cursor.close()
        Form.unmake_drink(drink_id, quantity)

    def unmake_drink(to_unmake_id, quantity):
        query = '''
        SELECT ingredient_drink_id, quantity 
        FROM Ingredients WHERE mixed_drink_id = ?'''
        cursor = db.execute(query, to_unmake_id)
        ingredients = cursor.fetchall()
        cursor.close()

        if len(ingredients) == 0:
            cursor = db.execute('SELECT stock FROM Drinks WHERE id = ?', to_unmake_id)
            stock = cursor.fetchone()[0]
            cursor.close()
            query = '''UPDATE Drinks SET stock = ? WHERE id = ?'''
            cursor = db.execute(query, stock + quantity, to_unmake_id)
            cursor.close()
        else:
            for id, ingredient_quantity in ingredients:
                Form.unmake_drink(id, ingredient_quantity * quantity)
        
    def make_drink(to_make_id, quantity):
        # Deduct the quantity purchased from the quantity on hand. First, determine 
        # whether the drink purchased was a cocktail.
        query = f'''SELECT stock, name FROM Drinks WHERE id = %d LIMIT 1'''
        cursor = db.execute(query, to_make_id)
        stock, name = cursor.fetchone()
        cursor.close()

        if stock >= quantity:
            query = '''UPDATE Drinks SET stock = ? WHERE id = ?'''
            cursor = db.execute(query, stock - quantity, to_make_id)
            cursor.close()
        else:
            query = '''
            SELECT ingredient_drink_id, quantity 
            FROM Ingredients WHERE mixed_drink_id = ?'''
            cursor = db.execute(query, to_make_id)
            ingredients = cursor.fetchall()
            cursor.close()
            if len(ingredients) == 0:
                raise ValidationException(f"You do not have enough {name} in the inventory")

            for id, ingredient_quantity in ingredients:
                Form.make_drink(id, quantity * ingredient_quantity)
