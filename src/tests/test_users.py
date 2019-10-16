import pyunit
from src.actions.users import login

def test_invalid_email():
    with pytest.raises(APIException):
        login('alejo', '23234')

def test_email():
    with pytest.raises(APIException):
        login('alejo', '')