from flask.ext.appbuilder import Model
from flask.ext.appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, String,  Date
from wtforms import Form, IntegerField, validators
# from sqlalchemy.orm import relationship
"""
BDPDB Models
Based on examples from http://flask-appbuilder.readthedocs.io/en/latest/relations.html
"""

class Patient(AuditMixin, Model):
    id = Column(Integer, primary_key=True)
    patient_number = Column(Integer, unique=True, nullable=False)
    dob = Column(Date, nullable=False)
    sex = Column(String(1), nullable=False)
    lesion_location = Column(String(50))
    lesion_cause = Column(String(50))
    lesion_date = Column(Date)
    referral_site = Column(String(50))
    mask_path = Column(String(250))

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



