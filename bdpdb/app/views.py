from flask import render_template, flash, redirect, request
import re
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.sqla.filters import get_field_setup_query
from flask_appbuilder.models.filters import BaseFilter
#from flask_appbuilder import ModelView, expose, BaseView, has_access, SimpleFormView
from flask_appbuilder import ModelView, BaseView, expose, SimpleFormView
from app import appbuilder, db
from flask_appbuilder.widgets import ListLinkWidget, ShowWidget
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from .models import (Patient, PatientNote, Etiology, DataSource, BrainArea,
        Laterality, Scan, ScanModality, Sex)

class PapayaWidget(ShowWidget):
    template = 'papaya_widget.html'

class OverlapPage(BaseView):
    
    default_view = 'view_overlap'

    @expose('/view_overlap/')
    def view_overlap(self):
        self.update_redirect()
        return self.render_template('view_overlap.html')
     
appbuilder.add_view(OverlapPage, 'Overlap Heatmap',
        icon='fa-database', category='Browse')

class PatientPage(BaseView):
    
    default_view = 'view_patient'

    @expose('/view_patient/')
    def view_patient(self):
        self.update_redirect()
        return self.render_template('view_patient.html')
     
appbuilder.add_view(PatientPage, 'View Patient',
        icon='fa-database', category='Browse')


class ViewSingle(ModelView):
    datamodel = SQLAInterface(Patient)
    show_template = 'single.html'

appbuilder.add_view(ViewSingle, "View Single", category='My View')


class MyView(BaseView):
    
    default_view = 'method1'

    @expose('/method1/')
    #@has_access
    def method1(self):
        # do something with param1
        # and return to previous page or index
        return 'Hello'

    @expose('/method2/<string:param1>')
    #@has_access
    def method2(self, param1):
        # do something with param1
        # and render template with param
        param1 = 'Goodbye %s' % (param1)
        return param1

    @expose('/method3/<string:param1>')
    #@has_access
    def method3(self, param1):
        # do something with param1
        # and render template with param
        #param1 = 'Goodbye %s' % (param1)
        self.update_redirect()
        return self.render_template('method3.html',
                               param1 = param1)

appbuilder.add_view(MyView, "Method1", category='My View')
appbuilder.add_link("Method2", href='/myview/method2/john', category='My View')
appbuilder.add_link("Method3", href='/myview/method3/john', category='My View')


class ScanView(ModelView):
    datamodel = SQLAInterface(Scan)
    list_widget = ListLinkWidget

    add_columns = ['patient','filename','modality','scan_date']
    edit_columns = ['patient','filename','modality','scan_date']
    show_columns = ['filename','modality','scan_date']
    list_columns = ['filename','modality','scan_date']

appbuilder.add_view_no_menu(ScanView, "ScanView")


class PatientNoteView(ModelView):
    datamodel = SQLAInterface(PatientNote)
    list_widget = ListLinkWidget

    add_columns = ['patient', 'note_title', 'note_text']
    edit_columns = ['patient', 'note_title', 'note_text']
    list_columns = ['note_title', 'created_by', 'created_on']
    show_columns = ['created_by', 'created_on','note_title', 'note_text']

appbuilder.add_view_no_menu(PatientNoteView, 'PatientNoteView')


class CustomShowWidget(ShowWidget):
    template = 'show_widget.html'

class PatientView(ModelView):
    datamodel = SQLAInterface(Patient)
    list_widget = ListLinkWidget
    show_widget = CustomShowWidget
    
    add_columns = ['patient_label','dob','sex','damaged_areas','laterality',
            'insult_date','etiology','data_source','mni_mask_path']
    edit_columns = ['dob','sex','damaged_areas','laterality',
            'insult_date','etiology','data_source', 'mni_mask_path']
    list_columns = ['patient_label','dob','sex','damaged_areas','laterality']

    show_fieldsets = [
            ('Patient Information',{
                'fields':['patient_label','sex','dob','damaged_areas',
                    'laterality','insult_date','etiology','data_source',
                    'mni_mask_path']})]
   
    related_views = [ScanView, PatientNoteView] 
    show_template = 'patient_cascade.html'  
    
    extra_args = {'foo': 'bar'}

    @expose('/coord_search/', methods=['GET','POST'])
    def coord_search(self):
        patients = []
        for arg in request.args:
            re_match = re.findall('search_(.*',arg)
            if re_match:
                patients.append(str(request.args.get(arg)))
        base_filters = [['patient_label', FilterIsIn, patients]]
        return base_filters
        

appbuilder.add_view(PatientView, "List Patients",
        icon='fa-users',category='Browse')



"""
Coordinate Search
"""

class FilterIsIn(BaseFilter):
    name = "Filter items that appear in a list."

    def apply(self, query, item_list):
        query, field = get_field_setup_query(query, self.model, self.column_name)
        return query.filter(field.in_(item_list))
          

class CoordinateSearchResults(PatientView):
    datamodel = SQLAInterface(Patient)

     
    
    #base_filters = [['patient_label', FilterIsIn, ['101', '103']]]
    #list_template = 'results.html'

appbuilder.add_view(CoordinateSearchResults, "Coordinate Search Results")

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
        redirect_url = 'http://www.google.com'
        return redirect(redirect_url)

        #patients = coordinate_searc(
        flash("hello", 'info')

    
appbuilder.add_view(CoordSearchView, "MNI Coordinate Search", icon='fa-search', label='Search',
        category='Foo', category_icon='fa_cogs')




"""
Metadata Model Views
"""

class EtiologyView(ModelView):
    datamodel = SQLAInterface(Etiology)
    related_views = [PatientView]
    add_columns = ['name']
    edit_columns = ['name']
    show_columns = ['name']
    list_columns = ['name']

appbuilder.add_view(EtiologyView, 'Manage Etiologies',
        icon='fa-ambulance', category='Manage')

class BrainAreaView(ModelView):
    datamodel = SQLAInterface(BrainArea)
    related_views = [PatientView]
    add_columns = ['name']
    edit_columns = ['name']
    show_columns = ['name']
    list_columns = ['name']

appbuilder.add_view(BrainAreaView, 'Manage Brain Areas',
        icon='fa-globe', category='Manage')

class DataSourceView(ModelView):
    datamodel = SQLAInterface(DataSource)
    related_views = [PatientView]
    add_columns = ['name']
    edit_columns = ['name']
    show_columns = ['name']
    list_columns = ['name']

appbuilder.add_view(DataSourceView, 'Manage Data Sources',
        icon='fa-institution', category='Manage')

class ScanModalityView(ModelView):
    datamodel = SQLAInterface(ScanModality)
    related_views = [ScanView]
    add_columns = ['name']
    edit_columns = ['name']
    show_columns = ['name']
    list_columns = ['name']

appbuilder.add_view(ScanModalityView, 'Manage Scan Types',
        icon='fa-file-image-o', category='Manage')


"""
Register views
"""

# Auto-fill values for Sex and Hemisphere
def fill_sex():
    try:
        db.session.add(Sex(name='Male'))
        db.session.add(Sex(name='Female'))
        db.session.add(Sex(name='Intersex'))
        db.session.commit()
    except:
        db.session.rollback()

def fill_hemi():
    try:
        db.session.add(Laterality(name='Left'))
        db.session.add(Laterality(name='Right'))
        db.session.add(Laterality(name='Bilateral'))
        db.session.commit()
    except:
        db.session.rollback()

fill_sex()
fill_hemi()



    
# Application wide 404 error handler

@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()


