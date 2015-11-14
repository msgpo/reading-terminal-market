from flask.ext.wtf import Form
from wtforms.fields import StringField, DecimalField, BooleanField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length
from ..models import Category
from .. import db


PRICE_MESSAGE = "This value needs to be filled and needs to be a number"


class ChangeListingInformation(Form):
    category_id = QuerySelectField('Category',
                                   validators=[DataRequired()],
                                   get_label='name',
                                   query_factory=lambda: db.session.query(Category).order_by('id'))
    listing_name = StringField('Item Name', validators=[DataRequired(), Length(1, 1000)])
    listing_description = TextAreaField('Item Description',
                                        validators=[DataRequired(), Length(1, 2500)])
    listing_price = DecimalField('Item Price', places=2,
                                 validators=[DataRequired(message=PRICE_MESSAGE)])
    listing_available = BooleanField('Available?')
    submit = SubmitField('Update Item Information')


class NewItemForm(Form):	
    category_id = QuerySelectField('Category',
                                   validators=[DataRequired()],
                                   get_label='name',
                                   query_factory=lambda: db.session.query(Category).order_by('id'))
    listing_name = StringField('Item Name',
                               validators=[DataRequired(), Length(1, 1000)])
    listing_description = TextAreaField('Item Description',
                                        validators=[DataRequired(), Length(1, 2500)])
    listing_price = DecimalField('Item Price', places=2,
                                 validators=[DataRequired(message=[PRICE_MESSAGE])])
    submit = SubmitField('Create New Item')
