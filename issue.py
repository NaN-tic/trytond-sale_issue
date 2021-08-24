#The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta
from trytond.transaction import Transaction
from trytond.modules.product import price_digits
from trytond.modules.currency.fields import Monetary

__all__ = ['IssueCategory', 'Issue', 'Sale', 'Party']


class IssueCategory(ModelSQL, ModelView):
    'Issue Category'
    __name__ = 'sale.issue.category'
    name = fields.Char('Name', translate=True)


class Issue(ModelSQL, ModelView):
    'Issues'
    __name__ = 'sale.issue'

    sale = fields.Many2One('sale.sale', 'Sale', required=True)
    company = fields.Function(fields.Many2One('company.company', 'Company'),
        'on_change_with_company', searcher='search_sale')
    subject = fields.Char('Subject', required=True)
    category = fields.Many2One('sale.issue.category', 'Category',
        required=True)
    currency = fields.Function(
        fields.Many2One('currency.currency', 'Currency'),
        'on_change_with_currency')
    cost = Monetary('Cost', digits=price_digits, currency='currency')
    sale_party = fields.Function(fields.Many2One('party.party', 'Sale Party'),
        'on_change_with_sale_party', searcher='search_sale')
    causing_party = fields.Many2One('party.party', 'Causing Party')
    description = fields.Text('Description')

    @staticmethod
    def default_company():
        return Transaction().context.get('company')

    @fields.depends('sale')
    def on_change_with_company(self, name=None):
        if self.sale:
            return self.sale.company.id

    @fields.depends('sale')
    def on_change_with_sale_party(self, name=None):
        if self.sale:
            return self.sale.party.id

    @fields.depends('sale', '_parent_sale.currency')
    def on_change_with_currency(self, name=None):
        if self.sale and self.sale.currency:
            return self.sale.currency.id

    @classmethod
    def search_sale(cls, name, clause):
        if name == 'sale_party':
            name = 'party'
        return [('sale.' + name,) + tuple(clause[1:])]


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'
    issues = fields.One2Many('sale.issue', 'sale', 'Issues')


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'
    sale_issues = fields.One2Many('sale.issue', 'sale_party', 'Sale Issues')
    caused_issues = fields.One2Many('sale.issue', 'causing_party',
        'Caused Issues')
