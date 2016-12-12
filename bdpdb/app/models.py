from flask.ext.appbuilder import Model
from flask.ext.appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
       
"""
Examples from http://flask-appbuilder.readthedocs.io/en/latest/quickhowto.html
"""

class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

class Contact(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    address = Column(String(564), default='Street ')
    birthday = Column(Date)
    mobile_phone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey('contact_group.id'))
    contact_group = relationship("ContactGroup")

    def __repr__(self):
        return self.name


"""
BDPDB Models
Based on examples from http://flask-appbuilder.readthedocs.io/en/latest/relations.html
"""

class Patient(Model):
    id = Column(Integer, primary_key=True)
    patient_number = Column(Integer, unique=True, nullable=False)
    dob = Column(Date, nullable=False)
    sex = Column(String(1), nullable=False)
    lesion_location = Column(String(50))
    lesion_cause = Column(String(50))
    lesion_date = Column(Date)
    referred_by = Column(String(50))

    def __repr__(self):
        return self.patient_number

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
    acquisition_order = Column(String(25), nullable=False)
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




