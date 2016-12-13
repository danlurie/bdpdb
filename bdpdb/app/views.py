from flask import render_template, flash
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder import ModelView, expose, BaseView, has_access, SimpleFormView
from app import appbuilder, db
from wtforms import StringField
from wtforms.validators import DataRequired
from flask.ext.appbuilder.fieldwidgets import BS3TextFieldWidget
from flask.ext.appbuilder.forms import DynamicForm

from .compute import coordinate_search
from .models import Patient

"""
Coordinate Search Form
"""

class CoordSearch(DynamicForm):
    field_x = StringField(('X'),
              validators=[DataRequired()],
              widget=BS3TextFieldWidget())
    field_y = StringField(('Y'),
              validators=[DataRequired()],
              widget=BS3TextFieldWidget())
    field_z = StringField(('Z'),
              validators=[DataRequired()],
              widget=BS3TextFieldWidget())

class CoordSearchView(SimpleFormView):
    form = CoordSearch
    form_title = "MNI Coordinate Search"
    
    def form_get(self, form):
        # pre-process form
        pass
        
    def form_post(self, form):
        # post-process form
        patients = coordinate_search(
        flash( str(foo))

appbuilder.add_view(CoordSearchView, "MNI Coordinate Search", icon='fa-search', label='Search',
        category='Search', category_icon='fa_cogs')

"""
BDPDB Views
"""
class Home(BaseView):
    
    default_view = 'view_overlap'

    @expose('/view_overlap/')
    @has_access
    def view_overlap(self):
        self.update_redirect()
        return self.render_template('view_overlap.html')
     
appbuilder.add_view(Home, 'View Overlap', category='Home')


class PatientView(ModelView):
    datamodel = SQLAInterface(Patient)

    list_columns = ['patient_number', 'dob', 'sex', 'lesion_location', 'lesion_cause']

    add_columns = ['patient_number', 'dob', 'sex', 'lesion_location', 'lesion_cause',
            'lesion_date', 'referral_site', 'mask_path']
    edit_columns = ['patient_number', 'dob', 'sex', 'lesion_location', 'lesion_cause',
            'lesion_date', 'referral_site', 'mask_path']


    show_fieldsets = [
            ('Patient Info', {'fields':['patient_number', 'dob', 'sex', 'lesion_location',
                'lesion_cause', 'lesion_date', 'referral_site', 'mask_path']})
            ]

db.create_all()
appbuilder.add_view(PatientView, "List Patients", icon='fa-users',category='Patients')

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()


