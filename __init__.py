# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import issue

def register():
    Pool.register(
        issue.IssueCategory,
        issue.Issue,
        module='sale_issue', type_='model')
