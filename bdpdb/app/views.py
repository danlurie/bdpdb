from flask import render_template, flash
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, expose, BaseView, has_access, SimpleFormView
from app import appbuilder, db
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
#from flask_appbuilder.models.sqla.filters import FilterRelationOneToManyEqual

#from .compute import coordinate_search
from .models import Patient, Cause, DataSource, BrainArea, Sex, Hemisphere, ScanModality, Scan

"""
BDPDB Views
"""
# Group overlap view
class Home(BaseView):
    
    default_view = 'view_overlap'

    @expose('/view_overlap/')
    @has_access
    def view_overlap(self):
        self.update_redirect()
        return self.render_template('view_overlap.html')
     
appbuilder.add_view(Home, 'View Overlap', category='Home')

# Scan view
class ScanView(ModelView):
    datamodel = SQLAInterface(Scan)
    add_columns = ['patient_number','modality', 'scan_date', 'filename']
    edit_columns = ['patient_number','modality', 'scan_date', 'filename']
    show_columns = ['patient_number','modality', 'scan_date', 'filename']
    list_columns = ['patient_number','modality', 'scan_date', 'filename']

db.create_all()
appbuilder.add_view(ScanView, "Scans", icon='fa-file-image-o',category='Browse')


# PatientScanView
class PatientScanView(ModelView):
    datamodel = SQLAInterface(Scan)
    add_columns = ['patient_number','modality', 'scan_date', 'filename']
    edit_columns = ['modality', 'scan_date', 'filename']
    show_columns = ['modality', 'scan_date', 'filename']
    list_columns = ['modality', 'scan_date', 'filename']

appbuilder.add_view_no_menu(PatientScanView, "PatientScanView")


# Patient view
class PatientView(ModelView):
    datamodel = SQLAInterface(Patient)

    add_columns = ['patient_number','dob','sex','lesion_location','lesion_hemisphere',
            'lesion_cause','lesion_date','data_source','patient_notes']
    edit_columns = ['patient_number','dob','sex','lesion_location','lesion_hemisphere',
            'lesion_cause','lesion_date','data_source','patient_notes']
    list_columns = ['patient_number','dob','sex','lesion_location','lesion_hemisphere',
            'lesion_cause']
    
    show_fieldsets = [
            ('Patient Info', {'fields':['patient_number','dob','sex','lesion_location',
                'lesion_hemisphere','lesion_cause','lesion_date','data_source','patient_notes']})
            ]

    related_views = [PatientScanView]
    show_template = 'appbuilder/general/model/show_cascade.html'

db.create_all()
appbuilder.add_view(PatientView, "Patients", icon='fa-users',category='Browse')

"""
# PatientFilter View
class PatientFilter(ModelView):
    datamodel = SQLAInterface(Patient)
    search_form_query_rel_fields = {'patient_scans':[['modality', FilterRelationOneToManyEqual, True]]}

db.create_all()
appbuilder.add_view(PatientFilter, "Search Patients", icon='fa-users',category='Patients')

# ScanFilter View
class ScanFilter(ModelView):
    datamodel = SQLAInterface(Scan)
    related_views = [PatientView]
    #search_form_query_rel_fields = {'':[['modality', FilterRelationOneToManyEqual, True]]}

db.create_all()
appbuilder.add_view(ScanFilter, "Search Scans", icon='fa-users',category='Patients')
"""

# Cause view
class CauseView(ModelView):
    datamodel = SQLAInterface(Cause)
    related_views = [PatientView]
    add_columns = ['name']
    edit_columns = ['name']
    show_columns = ['name']
    list_columns = ['name']

db.create_all()
appbuilder.add_view(CauseView, 'Manage Causes', icon='fa-ambulance', category='Manage')

# BrainArea view
class BrainAreaView(ModelView):
    datamodel = SQLAInterface(BrainArea)
    related_views = [PatientView]
    add_columns = ['name']
    edit_columns = ['name']
    show_columns = ['name']
    list_columns = ['name']


db.create_all()
appbuilder.add_view(BrainAreaView, 'Manage Brain Areas', icon='fa-globe', category='Manage')

# DataSource view
class DataSourceView(ModelView):
    datamodel = SQLAInterface(DataSource)
    related_views = [PatientView]
    add_columns = ['name']
    edit_columns = ['name']
    show_columns = ['name']
    list_columns = ['name']


db.create_all()
appbuilder.add_view(DataSourceView, 'Manage Data Sources', icon='fa-institution', category='Manage')

# ScanModality view
class ScanModalityView(ModelView):
    datamodel = SQLAInterface(ScanModality)
    related_views = [PatientView]
    add_columns = ['name']
    edit_columns = ['name']
    show_columns = ['name']
    list_columns = ['name']


db.create_all()
appbuilder.add_view(ScanModalityView, 'Manage Scan Types', icon='fa-file-image-o', category='Manage')


# Auto-fill values for Sex and Hemisphere
def fill_sex():
    try:
        db.session.add(Sex(name='Male'))
        db.session.add(Sex(name='Female'))
        db.session.add(Sex(name='Intersex'))
        db.session.commit()
        print('#####----####--SEX----####---####----')
    except:
        db.session.rollback()

def fill_hemi():
    try:
        db.session.add(Hemisphere(name='Left'))
        db.session.add(Hemisphere(name='Right'))
        db.session.commit()
        print('#####----####--HEMI----####---####----')
    except:
        db.session.rollback()

fill_sex()
fill_hemi()

# Auto-fill test values.
def fill_source():
    sources = ['UC Davis', 'UC Berkeley', 'Martinez VA']
    try:
        for i in sources:
            db.session.add(DataSource(name=i))
        db.session.commit()
        print('#####----####--SOURCE----####---####----')
    except:
        db.session.rollback()

def fill_cause():
    causes = ['TBI', 'Ischemic Stroke', 'Hemorrhagic Stroke']
    try:
        for i in causes:
            db.session.add(Cause(name=i))
        db.session.commit() 
    except:
        db.session.rollback()

def fill_area():
    areas = ['Thalamus', 'Striatum', 'OFC']
    try:
        for i in areas:
            db.session.add(BrainArea(name=i))
        db.session.commit() 
    except:
        db.session.rollback()

fill_source()
fill_cause()
fill_area()



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
        #patients = coordinate_searc(
        flash("hello")
        pass

appbuilder.add_view(CoordSearchView, "MNI Coordinate Search", icon='fa-search', label='Search',
        category='Search', category_icon='fa_cogs')

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()


