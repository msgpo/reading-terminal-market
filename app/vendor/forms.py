import imghdr
from flask.ext.wtf import Form
from flask.ext.login import current_user
from wtforms.fields import StringField, DecimalField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, URL
from wtforms import ValidationError
from ..models import Category, Listing
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

    def validate_listing_name(self, field):
        is_same_name = Listing.name == field.data
        is_diff_id = Listing.id != self.listing_id
        if current_user.listings.filter(is_same_name, is_diff_id).first():
            raise ValidationError('You already have an item with name {}.'.format(field.data))


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
                                 validators=[DataRequired(message=PRICE_MESSAGE)])
    submit = SubmitField('Create New Item')

    def validate_listing_name(self, field):
        if current_user.listings.filter_by(name=field.data).first():
            raise ValidationError('You already have an item with this name.')


class EditProfileForm(Form):
    image = FileField('Image File')
    bio = TextAreaField('Bio')
    address = StringField('Address')
    phone_number = StringField('Phone Number')
    website = StringField('Website (http://www.example.com)',
                          validators=[URL('This URL is invalid. Please enter a valid website name')])
    email = StringField('Email', validators=[Email('Please enter a valid email address')])
    featured1 = StringField('Featured Item 1')
    description1 = StringField('Description Item 1')
    featured2 = StringField('Featured Item 2')
    description2 = StringField('Description Item 2')
    featured3 = StringField('Featured Item 3')
    description3 = StringField('Description Item 3')
    featured4 = StringField('Featured Item 4')
    description4 = StringField('Description Item 4')
    submit = SubmitField('Save')
