from flask import current_app, render_template

from localization import *
import database as db

class Table:
    DEFAULT_PAGE_SIZE=10
    
    def __init__(self, query, header_keys=None,
                 prefix = '',
                 link_prefix=None,
                 page_size=DEFAULT_PAGE_SIZE,
                 add_buttons=True, extra_buttons=None, num_ids=1,
                 num_hidden=0):

        if header_keys is None:
            cursor = db.execute(query)
            # Extract the name from each column descriptor
            header_keys = [prefix + '_' + col[0] for col in cursor.description]
            cursor.close()

        if link_prefix is None:
            if len(prefix) > 0:
                link_prefix = prefix
            else:
                link_prefix = ''
            
            
        if add_buttons:
            header_keys += ['row_controls']

        header_keys = header_keys[num_hidden:]

        self.config = current_app.config
        self.num_hidden = num_hidden
        self.num_ids = num_ids
        self.prefix = prefix
        self.add_buttons = add_buttons
        self.query = query
        self.page_size = page_size
        self.extra_buttons = extra_buttons
        self.link_prefix = link_prefix

    def render(self, page=1):
        header = self.header(page)
        rows = self.rows(page)
        pager_prefix = self.link_prefix + '/page/'
        prev_url = None
        next_url = None
        if page > 1:
            prev_url = '/' + pager_prefix + str(page - 1)
        if len(rows) == self.page_size:
            next_url = '/' + pager_prefix + str(page + 1)

        return render_template(
            'table.jinja',
            header=header,
            rows=rows,
            prev_url=prev_url,
            next_url=next_url)
        
    def rows(self, page):
        if(page < 1):
            page = 1
        cursor = db.execute(self.query)
        rows = []
        for i in range(page):
            rows = cursor.fetchmany(self.page_size)

        if self.add_buttons:
            rows = [row + (self.buttons(row[:self.num_ids]),) for row in rows]

        rows = [row[self.num_hidden:] for row in rows]
        cursor.close()
        return rows

    def header(self, page):
        cursor = db.execute(self.query)
        columns = cursor.description
        cursor.close()
        header = []

        visible_column_indices = range(self.num_hidden, len(columns))
        for column in visible_column_indices:
            name = columns[column][0]
            cursor = db.execute(f'''
            SELECT DISTINCT {name} FROM ({self.query}) 
            AS results ORDER BY results.{name}''')
            localname = localize(f'{self.prefix}_{name}')
            options = [row[0] for row in cursor.fetchall()]
            header.append(render_template(
                'header_cell.jinja',
                name=name,
                localname=localname,
                options=options))
            cursor.close()

        if self.add_buttons:
            header.append(render_template(
                'header_cell.jinja',
                localname=localize('row_controls')))
        cursor.close()
        return header
        
    def buttons(self, ids):
        suffix = f'{ids[0]}'
        for id in ids[1:]:
            suffix += f'/in/{id}'
        return render_template(
            'buttons.jinja',
            extra_buttons=self.extra_buttons,
            link_prefix=self.link_prefix,
            link_suffix=suffix)
