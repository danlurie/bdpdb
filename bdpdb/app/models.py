import os
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from flask_appbuilder.models.generic import GenericModel, GenericSession, GenericColumn
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
#from wtforms import Form, IntegerField, validators

"""
Metadata Models
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

"""
Patient Models
"""

class PatientNote(AuditMixin, Model):
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    #patient_label = relationship('Patient')
    note_title = Column(String(25), nullable=False)
    note_text = Column(String(1000), nullable=False)

"""
class PatientMask(AuditMixin, Model):
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    patient = relationship('Patient', back_populates='mask')
    mask_path = Column(String(200), nullable=False)
"""

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
   
    #mask = relationship('PatientMask', uselist=False, back_populates='patient')
    mni_mask_path = Column(String(200), unique=True, nullable=False)

    patient_notes = relationship('PatientNote', backref='patient')
    patient_scans = relationship("Scan", backref='patient')

    def __repr__(self):
        return self.patient_label

"""
Scan information tables
"""
class ScanModality(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Scan(AuditMixin, Model):
    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    #patient_label = relationship('Patient')

    modality_id = Column(Integer, ForeignKey('scan_modality.id'), nullable=False)
    modality = relationship("ScanModality")

    scan_date = Column(Date, nullable=False)

    filename = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return self.filename

class PSModel(GenericModel):
    UID = GenericColumn(str)
    PID = GenericColumn(int, primary_key=True)
    PPID = GenericColumn(int)
    C = GenericColumn(int)
    STIME = GenericColumn(str)
    TTY = GenericColumn(str)
    TIME = GenericColumn(str)
    CMD = GenericColumn(str)

class PSSession(GenericSession):
    regexp = "(\w+) +(\w+) +(\w+) +(\w+) +(\w+:\w+|\w+) (\?|tty\w+) +(\w+:\w+:\w+) +(.+)\n"

    def _add_object(self, line):
        import re

        group = re.findall(self.regexp, line)
        if group:
            model = PSModel()
            model.UID = group[0][0]
            model.PID = int(group[0][1])
            model.PPID = int(group[0][2])
            model.C = int(group[0][3])
            model.STIME = group[0][4]
            model.TTY = group[0][5]
            model.TIME = group[0][6]
            model.CMD = group[0][7]
            self.add(model)

    def get(self, pk):
        self.delete_all(PSModel())
        out = os.popen('ps -p {0} -f'.format(pk))
        for line in out.readlines():
            self._add_object(line)
        return super(PSSession, self).get(pk)


    def all(self):
        self.delete_all(PSModel())
        out = os.popen('ps -ef')
        for line in out.readlines():
            self._add_object(line)
        return super(PSSession, self).all()



"""
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
"""


