from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
#from wtforms import Form, IntegerField, validators

"""
Patient information tables
"""
class Sex(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(10), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class BrainArea(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(75), unique=True, nullable=False)

    def __repr__(self):
        return self.name


assoc_patient_area = Table('assoc_patient_area', Model.metadata,
        Column('patient_id', Integer, ForeignKey('patient.id')),
        Column('area_id', Integer, ForeignKey('brain_area.id'))
        )


class Laterality(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(10), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Etiology(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class DataSource(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class PatientNote(AuditMixin, Model):
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    note_title = Column(String(25), nullable=False)
    note_text = Column(String(1000), nullable=False)

class Patient(AuditMixin, Model):
    id = Column(Integer, primary_key=True)

    patient_label = Column(String(25), unique=True, nullable=False)

    dob = Column(Date, nullable=False) 

    sex_id = Column(Integer, ForeignKey('sex.id'), nullable=False)
    sex = relationship('Sex')

    damaged_areas = relationship('BrainArea',
            secondary=assoc_patient_area,
            backref='patients')
    
    laterality_id = Column(Integer, ForeignKey('laterality.id'))
    laterality = relationship('Laterality')

    insult_date = Column(Date)
    
    etiology_id = Column(Integer, ForeignKey('etiology.id'))
    etiology = relationship('Etiology')

    data_source_id = Column(Integer, ForeignKey('data_source.id'))
    data_source = relationship("DataSource")
    
    patient_notes = relationship('PatientNote', backref='patient')
    #patient_scans = relationship("Scan")

    def __repr__(self):
        return self.patient_label

"""

# What scans does the patient have?

# Scan Modality (based on BIDS spec)
class ScanModality(AuditMixin, Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

# Scan object
class Scan(AuditMixin, Model):
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    patient_number = relationship("Patient")
    modality_id = Column(Integer, ForeignKey('scan_modality.id'), nullable=False)
    modality = relationship("ScanModality")
    scan_date = Column(Date, nullable=False)
    filename = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return self.filename

# The Patient entity


# Coordinate search form
class CoordSearchForm(Form):
    x = IntegerField(
            label='x',
            validators=[validators.InputRequired()])
    y = IntegerField(
            label='y',
            validators=[validators.InputRequired()])
    z = IntegerField(
            label='z',
            validators=[validators.InputRequired()])



class Sequence(Model):
    id = Column(Integer, primary_key=True)
    sequence_name = Column(String(50), nullable=False)
    repetition_time = Column(Integer, nullable=False)
    echo_time = Column(Integer, nullable=False)
    flip_angle = Column(Integer, nullable=False)
    pixel_spacing = Column(String(25), nullable=False)
    num_slices =  Column(Integer, nullable=False)
    slice_thickness = Column(Float, nullable=False)
    slice_spacing = Column(Float, nullable=False)
    acquisition_order = Column(String(25))
    volumes = Column(Integer, nullable=False)
    scanner = Column(String(25), nullable=False)

    def __repr__(self):
        return self.sequence_name

class Scan(Model):
    id = Column(Integer, primary_key=True)
    scan_type = Column(String(25), nullable=False)
    scan_date = Column(Date, nullable=False)
    scan_site = Column(String(25), nullable=False)
    file_path = Column(String(250), nullable=False)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    patient = relationship('Patient')
    sequence_id = Column(Integer, ForeignKey('sequence.id'), nullable=False)
    sequence = relationship('Sequence')

    def __repr__(self):
        return self.scan_type

"""


