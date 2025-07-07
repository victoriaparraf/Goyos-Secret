from uuid import uuid4
from modules.auth.domain.user import User, UserRole

def test_user_creation_valid_data():
    """
    Test that a User object can be created with valid data.
    """
    user_id = uuid4()
    user = User(
        uuid=user_id,
        name="Test User",
        email="test@example.com",
        hashed_password="hashedpassword123",
        role=UserRole.CLIENT
    )

    assert user.uuid == user_id
    assert user.name == "Test User"
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashedpassword123"
    assert user.role == UserRole.CLIENT

def test_user_creation_admin_role():
    """
    Test that a User object can be created with an ADMIN role.
    """
    user_id = uuid4()
    user = User(
        uuid=user_id,
        name="Admin User",
        email="admin@example.com",
        hashed_password="adminhashedpassword",
        role=UserRole.ADMIN
    )

    assert user.role == UserRole.ADMIN



def test_user_missing_required_field():
    """
    Test that User creation fails when a required field is missing.
    """
    from pydantic import ValidationError
    import pytest

    with pytest.raises(ValidationError):
        User(
            uuid=uuid4(),
            name="Missing Field User",
            email="missing@example.com",
            # hashed_password is intentionally missing
            role=UserRole.CLIENT
        )
