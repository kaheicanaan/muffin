from actions.user_registration import UserRegistration
from data_models.users import UserCreate


def test_create_user(db, sample_user):
    action = UserRegistration(db)
    sample_user_model = UserCreate(**sample_user)
    db_user = action.create_user(sample_user_model)
    assert db_user.id
