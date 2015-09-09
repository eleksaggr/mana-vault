from flask import Blueprint, flash, redirect, render_template, request, session, \
    url_for
from wtforms.fields.html5 import DecimalRangeField
from bson.objectid import ObjectId

from app import logger
from app.mod_budget.form import AddEntryForm, EditBudgetForm
from app.mod_budget.model import Category, CategoryBudget, Expense, Income
from app.mod_auth.helper import requireAuth
from app.mod_auth.model import User

budget = Blueprint('budget', __name__, template_folder = 'templates')

@budget.route('/')
@requireAuth()
def default():
    return "Hello World!"

@budget.route('/income/add', methods = ['GET', 'POST'])
@requireAuth()
def addIncome():
    form = AddEntryForm(request.form)
    # Load the categories from the DB into the SelectField
    form.loadCategories()

    if request.method == 'POST' and form.validate():
        income = Income()
        form.populate_obj(income)

        # Insert category into the ReferenceField.
        income.category = Category.objects(id = ObjectId(income.category)).first()
        # Insert owner into the ReferenceField.
        userId = ObjectId(session.get('user')['_id']['$oid'])
        income.owner = User.objects(id = userId).first()
        income.save()

        logger.debug('{0} added Income({1}, {2}, {3})'.format(
            session.get('user')['username'], income.amount, income.description,
                income.category))

        flash('Your income has been added.')
        return redirect(url_for('budget.default'))
    return render_template('budget/income/add.html', form = form)

@budget.route('/expense/add', methods = ['GET', 'POST'])
@requireAuth()
def addExpense():
    form = AddEntryForm(request.form)
    # Load the categories from the DB into the SelectField
    form.loadCategories()

    if request.method == 'POST' and form.validate():
        expense = Expense()
        form.populate_obj(expense)

        # Insert category into the ReferenceField.
        expense.category = Category.objects(id = ObjectId(expense.category)).first()
        # Insert owner into the ReferenceField.
        userId = ObjectId(session.get('user')['_id']['$oid'])
        income.owner = User.objects(id = userId).first()
        expense.save()

        flash('Your income has been added.')
        return redirect(url_for('budget.default'))
    return render_template('budget/expense/add.html', form = form)
