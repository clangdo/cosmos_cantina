from localization import *

class Link:
    def __init__(self, to, name_key = None, extra_classes=[]):
        if name_key is None:
            name_key = 'link'+to.replace('/', '_')

        self.classes=' '.join(['button'] + extra_classes)
        self.name = localize(name_key)
        self.url = to

def navlinks():
    view_links = [
        Link('/customers'),
        Link('/drinks'),
        Link('/ingredients'),
        Link('/purchases'),
        Link('/tabs')]

    create_links = [
        Link('/customers/create'),
        Link('/drinks/create'),
        Link('/ingredients/create'),
        Link('/purchases/create'),
        Link('/tabs/create')]


    return {
        'view_links': view_links,
        'create_links': create_links}
