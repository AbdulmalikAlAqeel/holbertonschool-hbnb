"""User-specific SQLAlchemy repository."""

from app.extensions import db
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """Handle database operations specific to User."""

    def __init__(self):
        """Initialize the repository for User."""
        super().__init__(User)

    def get_user_by_email(self, email):
        """Retrieve a user by email address."""
        return User.query.filter(User._email == email).first()

    def update(self, user_id, data):
        """Update a user and commit the changes."""
        user = self.get(user_id)

        if not user:
            return None

        user.update(data)
        db.session.commit()
        return user
