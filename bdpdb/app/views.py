from flask import render_template
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder import ModelView, AppBuilder, expose, BaseView, has_access
from app import appbuilder, db

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

    #from flask import render_template

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

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()


