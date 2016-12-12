from flask import render_template, flash
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder import ModelView, AppBuilder, expose, BaseView, has_access, SimpleFormView
from app import appbuilder, db
from wtforms import Form, StringField
from wtforms.validators import DataRequired
from flask.ext.appbuilder.fieldwidgets import BS3TextFieldWidget
from flask.ext.appbuilder.forms import DynamicForm
#from flask.ext.babelpkg import lazy_gettext as _

from .models import ContactGroup, Contact

"""
    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(MyModelView, "My View", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
"""

"""
Example views from http://flask-appbuilder.readthedocs.io/en/latest/views.html
"""
class MyView(BaseView):
    
    default_view = 'method1'

    @expose('/method1/')
    @has_access
    def method1(self):
        # return param1
        return "Hello, authorized user."
    
    @expose('/method2/<string:param1>')
    @has_access
    def method2(self, param1):
        # render param1
        param1 = "Goodbye, {}.".format(param1)
        return param1

    @expose('/method3/<string:param1>')
    @has_access
    def method3(self, param1):
        # render param1 in the template
        param1 = "Then {} said: 'Hey there, good looking.'".format(param1)
        self.update_redirect()
        return self.render_template('method3.html', param1=param1)

appbuilder.add_view(MyView, 'Method1', category='My View')
appbuilder.add_link("Method2", href='/myview/method2/Dan', category='My View')
appbuilder.add_link("Method3", href='/myview/method3/Dan', category='My View')

class MyForm(DynamicForm):
    field1 = StringField(('Field1'),
            description=("We're number one!"),
            validators=[DataRequired()],
            widget=BS3TextFieldWidget())
    field2 = StringField(('Field2'),
            description=("We're number two! (And we're optional)"),
            widget=BS3TextFieldWidget())

class MyFormView(SimpleFormView):
    form = MyForm
    form_title = "Form View MKI"
    message = "It worked!"

    def form_get(self, form):
        # pre-process form
        form.field1.data = 'I dunno man, I just woke up here.'

    def form_post(self, form):
        # post-process form
        flash(self.message, 'info')

appbuilder.add_view(MyFormView, "My Form View", icon='fa-group', label='My form View',
        category='My Forms', category_icon='fa_cogs')

"""
Examples from http://flask-appbuilder.readthedocs.io/en/latest/quickhowto.html
"""

class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)

    label_columns = {'contact_group':'Contacts Group'}
    list_columns = ['name', 'mobile_phone', 'birthday', 'contact_group']
    
    show_fieldsets = [
            ('Summary', {'fields':['name', 'address', 'contact_group']}),
            ('Personal Info', {'fields':['birthday', 'mobile_phone'], 'expanded':False}),
            ]

class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]

   
db.create_all()
appbuilder.add_view(GroupModelView, "List Groups", icon='fa-folder-open-o', category='Contacts',
        category_icon='fa-envelope')
appbuilder.add_view(ContactModelView, "List Contacts", icon='fa-envelope', category='Contacts')

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()


