from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from wtforms import Form, IntegerField, validators
"""
BDPDB Models
Based on examples from http://flask-appbuilder.readthedocs.io/en/latest/relations.html
"""

# What caused the damage
class Cause(AuditMixin, Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

# Where is the patient from
class DataSource(AuditMixin, Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

# Patient Sex
class Sex(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(10), unique=True, nullable=False)

    def __repr__(self):
        return self.name

# Which hemispheres have damage
class Hemisphere(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(10), unique=True, nullable=False)

    def __repr__(self):
        return self.name

assoc_hemi_patient = Table('hemi_patient', Model.metadata,
        Column('id', Integer, primary_key=True),
        Column('hemi_id', Integer, ForeignKey('hemisphere.id')),
        Column('patient_id', Integer, ForeignKey('patient.id'))
        )

# Which brain areas are damaged
class BrainArea(AuditMixin, Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(75), unique=True, nullable=False)

    def __repr__(self):
        return self.name

assoc_area_patient = Table('area_patient', Model.metadata,
        Column('id', Integer, primary_key=True),
        Column('area_id', Integer, ForeignKey('brainarea.id')),
        Column('patient_id', Integer, ForeignKey('patient.id'))
        )

class Patient(AuditMixin, Model):
    id = Column(Integer, primary_key=True)
    patient_number = Column(Integer, unique=True, nullable=False)
    dob = Column(Date, nullable=False)
    sex_id = Column(Integer, ForeignKey, 'sex.id', nullable=False)
    sex = relationship("Sex")
    lesion_location = relationship("BrainArea", secondary=assoc_area_patient, backref='patient')
    lesion_hemisphere = relationship("Hemisphere", secondary=assoc_hemi_patient, backref='patient')
    cause_id = Column(Integer, ForeignKey, 'cause.id')
    lesion_cause = relationship("Cause")
    lesion_date = Column(Date)
    data_source_id = Column(Integer, ForeignKey, 'datasource.id')
    data_source = relationship("DataSource")
    patient_notes = Column(String(500))

    def __repr__(self):
        return self.patient_number

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


"""
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



