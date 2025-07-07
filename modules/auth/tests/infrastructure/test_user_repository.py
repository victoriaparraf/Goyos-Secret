import pytest
from unittest.mock import Mock, MagicMock
from uuid import uuid4
from sqlmodel import Session, select

from modules.auth.infrastructure.user_repository import UserRepository
from modules.auth.infrastructure.user_db_model import UserDB
from modules.auth.domain.user import User, UserRole

# Fixture para un mock de la sesión de la base de datos
@pytest.fixture
def mock_db_session():
    return Mock(spec=Session)

# Fixture para el repositorio de usuarios con la sesión mockeada
@pytest.fixture
def user_repository(mock_db_session):
    return UserRepository(db=mock_db_session)

# Fixture para un usuario de ejemplo en formato UserDB
@pytest.fixture
def sample_user_db():
    return UserDB(
        uuid=uuid4(),
        name="Test User",
        email="test@example.com",
        hashed_password="hashedpassword123",
        role=UserRole.CLIENT
    )

# Fixture para un usuario de ejemplo en formato User (dominio)
@pytest.fixture
def sample_user_domain(sample_user_db):
    return User(
        uuid=sample_user_db.uuid,
        name=sample_user_db.name,
        email=sample_user_db.email,
        hashed_password=sample_user_db.hashed_password,
        role=sample_user_db.role
    )

# Tests para get_by_email
def test_get_by_email_found(user_repository, mock_db_session, sample_user_db):
    # Configurar el mock para simular el resultado de una consulta
    mock_exec = MagicMock()
    mock_exec.first.return_value = sample_user_db
    mock_db_session.exec.return_value = mock_exec

    user = user_repository.get_by_email("test@example.com")

    assert user == sample_user_db
    mock_db_session.exec.assert_called_once()

def test_get_by_email_not_found(user_repository, mock_db_session):
    mock_exec = MagicMock()
    mock_exec.first.return_value = None
    mock_db_session.exec.return_value = mock_exec

    user = user_repository.get_by_email("nonexistent@example.com")

    assert user is None
    mock_db_session.exec.assert_called_once()

# Tests para create_user
def test_create_user_success(user_repository, mock_db_session, sample_user_domain):
    user_repository.create_user(sample_user_domain)

    mock_db_session.add.assert_called_once_with(sample_user_domain)
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(sample_user_domain)

# Tests para modify_user
def test_modify_user_success(user_repository, mock_db_session, sample_user_db):
    user_repository.modify_user(sample_user_db)

    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(sample_user_db)

# Tests para get_by_id
def test_get_by_id_found(user_repository, mock_db_session, sample_user_db):
    mock_exec = MagicMock()
    mock_exec.first.return_value = sample_user_db
    mock_db_session.exec.return_value = mock_exec

    user = user_repository.get_by_id(str(sample_user_db.uuid))

    assert user == sample_user_db
    mock_db_session.exec.assert_called_once()

def test_get_by_id_not_found(user_repository, mock_db_session):
    mock_exec = MagicMock()
    mock_exec.first.return_value = None
    mock_db_session.exec.return_value = mock_exec

    user = user_repository.get_by_id(str(uuid4()))

    assert user is None
    mock_db_session.exec.assert_called_once()
