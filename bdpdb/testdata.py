from app import db
from app.models import DataSource, Etiology, BrainArea


# Auto-fill test values.
def fill_source():
    sources = ['UC Davis', 'UC Berkeley', 'Martinez VA']
    try:
        for i in sources:
            db.session.add(DataSource(name=i))
        db.session.commit()
        print("Populating data sources")
    except:
        db.session.rollback()

def fill_cause():
    causes = ['TBI', 'Ischemic Stroke', 'Hemorrhagic Stroke']
    try:
        for i in causes:
            db.session.add(Etiology(name=i))
        db.session.commit()
        print("Populating etiologies")
    except:
        db.session.rollback()

def fill_area():
    areas = ['Right Thalamus', 'Left Striatum', 'Left OFC']
    try:
        for i in areas:
            db.session.add(BrainArea(name=i))
        db.session.commit() 
        print("Populating brain areas")
    except:
        db.session.rollback()

fill_source()
fill_cause()
fill_area()

