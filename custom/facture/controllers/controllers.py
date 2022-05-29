import json

from odoo import http
from odoo.http import request


class Facture (http.Controller):

    @http.route(['/api/users'], type="http", website=True, method=['GET'], csrf=False)
    def get_invoices(self):
        values = {}

        data = request.env['res.users'].sudo().search([])

        if data:
            books = []
            for book_data in data:
                book = {
                    "name": book_data.name,
                    "login": book_data.login,
                }
                # categories = []
                # for category in book_data.categories:
                #     categories.append(category.name)
                # book["categories"] = categories
                books.append(book)

            # values['success'] = True
            values['data'] = books
        else:
            # values['success'] = False
            # values['error_code'] = 1
            # values['error_data'] = 'No data found!'
            values['data'] = ''

        return json.dumps(books)