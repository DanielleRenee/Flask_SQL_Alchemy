"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?
# a list of Brand objects, in this case, only one object
# <flask_sqlalchemy.BaseQuery object at 0x7fc2baa29d90>



# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?
# An association table is a table in the middle of a data model which only serves
# to glue other tables together. The table itself does not actually contain any
# important fields, but it does contain foreign keys from tables on either side
# of it. Many-to-many relationships are all over the place, and are not able to 
# stored in relationship databases without the help of association tables 
# (an intermediary).




# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries


# Get the brand with the brand_id of ``ram``.
q1 = Brand.query.filter_by(brand_id='ram').one()

# Get all models with the name ``Corvette`` and the brand_id ``che``.
q2 = Model.query.filter_by(brand_id='che', name='Corvette').all()

# Get all models that are older than 1960.
q3 = Model.query.filter(Model.year > 1960).all()

# Get all brands that were founded after 1920.
q4 = Brand.query.filter(Brand.founded > 1920).all()

# Get all models with names that begin with ``Cor``.
q5 = Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
q6 = Brand.query.filter(Brand.founded==1903, Brand.discontinued.is_(None)).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
q = Brand.query
q7 = q.filter( db.or_(Brand.discontinued.isnot(None), Brand.founded < 1950) )

# Get all models whose brand_id is not ``for``.
q8 = Model.query.filter(Model.brand_id != 'for').all()



# -------------------------------------------------------------------
# Part 4: Write Functions


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""


    b = db.session.query(Model, Brand).join(Brand).all()
    #default is an innter join

    for mod, bran in b:
        if mod.year == year:
            print mod.name, bran.name, bran.headquarters



def get_brands_summary():
    """Prints out each brand name (once) and all of that brand's models,
    including their year, using only ONE database query."""

    #refrencing http://docs.sqlalchemy.org/en/rel_1_0/orm/query.html#sqlalchemy.orm.query.Query.offset
    # qx = db.session.query(Brand, Model).join(Model).group_by(Brand.name)
    q = db.session.query(Brand, Model).join(Model).all()

    #not sure about this one, continue to get sqlalchemy.exc.ProgrammingError: (psycopg2.ProgrammingError)
    #add brands as keys in the dictionary, and value as list of tuples containing model and year

    for bran, mod in q:
        summary = { bran.name : (mod.name, mod.year) for bran.name in q }


def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    d = Brand.query.filter(Brand.name.like("%mystr%")).all()

    names = []
    for item in d:
        names.append(item)

    return names


def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    
    e = Model.query.filter(Model.year >= start_year, Model.year < end_year).all()

    models = []
    for item in e:
        models.append(item)

    return models

