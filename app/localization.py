locale_strings = {
    'bibliography': 'Bibliography',
    'create_success': 'Successfully Created',
    'create_failure': 'Failed to Create',
    'edit_success': 'Successfully Edited',
    'edit_failure': 'Failed to Edit',
    'customers': 'Customers',
    'customers_edit': 'Edit Customer Information',
    'customers_id': 'Customer Number',
    'customers_create': 'Create Customer',
    'customers_create_success': 'Successfully added customer to database',
    'customers_create_failure': 'There was a problem adding the customer to the database',
    'customers_update_success': 'Successfully edited that customer',
    'customers_update_failure': 'There was a problem editing the customer that way',
    'customers_name': 'Customer Full Name',
    'customers_last_name': 'Last Name',
    'customers_first_name': 'First Name',
    'customers_name': 'Customer',
    'customers_uba': 'UBA Number',
    'drinks': 'Inventory',
    'drinks_edit': 'Edit Drink Information',
    'drinks_id': 'Drink Number',
    'drinks_name': 'Drink Name',
    'drinks_price': 'Price Per Shot',
    'drinks_stock': 'Shots in Stock',
    'drinks_serving': 'Shots Per Serving',
    'drinks_signature': 'Signature Cocktail',
    'drinks_ingredients': 'Ingredients',
    'drinks_create': 'Add Drink to Menu',
    'drinks_create_success': 'Successfully added drink to database',
    'drinks_create_failure': 'There was a problem adding the drink to the database',
    'drinks_update_success': 'Successfully edited that drink',
    'drinks_update_failure': 'There was a problem editing the drink that way',
    'form_submit_default': 'Submit',
    'form_cancel_default': 'Cancel',
    'ingredients_name': 'Ingredient',
    'ingredients_edit': 'Edit Ingredient Quantity',
    'ingredients_quantity': 'Shots to Include',
    'ingredients_ingredient_drink_id': 'Ingredient',
    'ingredients_mixed_drink_id': 'Cocktail',
    'ingredients_ingredient_drink_name': 'Ingredient',
    'ingredients_mixed_drink_name': 'Mixed Drink',
    'ingredients_create': 'Add New Ingredient',
    'ingredients_create_success': 'Successfully added ingredient relationship to database',
    'ingredients_create_failure': 'There was a problem adding the ingredient relationship to the database',
    'ingredients_update_success': 'Successfully edited that ingredient',
    'ingredients_update_failure': 'There was a problem editing the ingredient that way',
    'ingredients': 'Ingredients',
    'ingredients_cocktail': 'Cocktail',
    'ingredients_component': 'Component',
    'ingredients_quantity': 'Quantity',
    'link_customers': 'View Customers',
    'link_customers_create': 'Create Customer',
    'link_drinks': 'View Inventory',
    'link_drinks_create': 'Add Drink to Menu',
    'link_ingredients': 'View All Ingredients',
    'link_ingredients_create': 'Add New Ingredient',
    'link_purchases': 'View Purchases',
    'link_purchases_create': 'Record Purchase',
    'link_tabs': 'View Tabs',
    'link_tabs_create': 'Open a Tab',
    'not_found': 'Page Not Found (404)',
    'purchases': 'Purchases',
    'purchases_edit': 'Edit Purchase',
    'purchases_id': 'Purchase Number',
    'purchases_customer': 'Customer',
    'purchases_create': 'Record Purchase',
    'purchases_create_success': 'Successfully recorded purchase and removed ingredients from inventory',
    'purchases_create_failure': 'There was a problem recording the purchase',
    'purchases_update_success': 'Successfully edited that purchase and adjusted inventory as if it never occurred differently',
    'purchases_update_failure': 'There was a problem editing the purchase that way',
    'purchases_drink': 'Drink',
    'purchases_drink_id': 'Drink',
    'purchases_tab_id': 'Tab',
    'purchases_date': 'Purchase Time',
    'purchases_quantity': 'Shots Ordered',
    'purchases_total': 'Total',
    'row_controls': 'Actions',
    'tabs': 'Tabs',
    'tabs_create': 'Open a Tab',
    'tabs_create_success': 'Successfully opened the tab',
    'tabs_create_failure': 'There was a problem opening the tab',
    'tabs_update_success': 'Successfully edited that tab',
    'tabs_update_failure': 'There was a problem editing the tab that way',
    'tabs_edit': 'Edit Tab',
    'tabs_id': 'Tab Number',
    'tabs_customer': 'Customer',
    'tabs_customer_id': 'Customer',
    'tabs_due': 'Due',
    'tabs_paid': 'Paid',
    'tabs_total': 'Tab Total',
    'error_500_title': '''Server Error''',
    'error_500_summary': '''Something has gone wrong on our end''',
    'error_500_description': '''If you're receiving this error it means we did something wrong. So
    we can fix it, please let us know what you were doing when the
    error occured, and try to tell us exactly when you received the
    error.''',
    'error_400_title': '''Bad Request''',
    'error_400_summary': '''Something was wrong with your request''',
    'error_400_description': '''You requested a page in an unexpected way, if you submitted a form
    maybe something was not in the proper format, try double checking
    that all form values are correct. Make sure there were no negative
    numbers or decimal points where they wouldn't make sense.''',
    'error_404_title':'Not Found',
    'error_404_summary': '''There isn't a page at this URL''',
    'error_404_description': '''This error means the page you're trying to get can't be found on\
    the webserver. In essence our server doesn't know how to handle
    your request. You're probably receiving this error because of a
    faulty link. Please let us know which one you clicked to get here,
    and we'll update it as soon as possible. If you typed the URL by
    hand, check your spelling carefully.''',
    'welcome_title':"Cosmo's Cantina POS System",
    'welcome_message':'''
<p>
    Welcome to the Cosmo's Cantina POS system. With this technological
    marvel, patented by Andromitech®, you can easily manage customer
    orders and your inventory.
</p>
<p>
    There are four kinds of operations
    you can do on the database, and links are colored according to
    what they do, their four colors as follows
    <span class="read">reading data</span>, <span class="create">creating
    data</span>, <span class="edit">editing data</span>,
    and <span class="delete">deleting data</span>. Always
    be careful about deleting data, as the operation is permanant.
</p>
<p>
    Please use this system responsibly. Unauthorized use may result in
    security turret malfunctions, uncontrolled electrical surges,
    financial liability of up to 40,000,000 galactic credits, and
    other minor inconveniences.
</p>'''
}

locale_table_headers = {
    'Customers': ('Customer Number', 'First Name', 'Last Name', 'UBA Number'),
}

def localize(string):
    try:
        return locale_strings[string]
    except:
        return string

def localize_table_header(prefix, header):
    return [localize(prefix+'_'+key) for key in header]

def localize_list(keys):
    return [localize(key) for key in keys]

def localize_for_clause(something, for_what):
    return f'{localize(something)} for {localize(for_what)}'
