from app.schemas.user import UserCreate, UserLogin, UserResponse


def test_user_create_schema():
    user = UserCreate(email="user@example.com", password="123")
    assert user.email == "user@example.com"
    assert user.password == "123"


def test_user_login_schema():
    login = UserLogin(email="user@example.com", password="abc")
    assert login.email == "user@example.com"
    assert login.password == "abc"


def test_user_response_schema():
    user = UserResponse(id=1, email="test@example.com")
    assert user.id == 1
    assert user.email == "test@example.com"
