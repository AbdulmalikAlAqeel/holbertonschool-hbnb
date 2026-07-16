import re
from models.base_model import BaseModel

class User(BaseModel):
    """Represents a user profile in the system."""
    
    def __init__(self, email, first_name, last_name, password, is_admin=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email = self.validate_email(email)
        self.first_name = self.validate_string(first_name, "First name")
        self.last_name = self.validate_string(last_name, "Last name")
        self.password = password  # Plain text for now, can be hashed in later tasks
        self.is_admin = is_admin

    @staticmethod
    def validate_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            raise ValueError("Invalid email format.")
        return email

    @staticmethod
    def validate_string(val, field_name):
        if not val or not isinstance(val, str):
            raise ValueError(f"{field_name} must be a non-empty string.")
        return val
