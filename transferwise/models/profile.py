from transferwise.models.base import TFModel


class Profile(TFModel):
    _entity = 'profiles'
    type = None  # personal, business
    details = None  # PersonalDetails, BusinessDetails


class PersonalDetails:
    first_name = None
    last_name = None
    date_of_birth = None
    phone_number = None
    avatar = None
    occupation = None
    primary_address = None  # Address model


class BusinessDetails:
    name = None
    registration_number = None
    acn = None
    abn = None
    arbn = None
    company_type = None
    company_role = None
    description_of_business = None
    primary_address = None  # Address model
    webpage = None
