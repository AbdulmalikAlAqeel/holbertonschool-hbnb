import uuid
from datetime import datetime

class BaseModel:
    """
    Base class that defines all common attributes and methods 
    for other domain models in the HBnB application.
    """
    def __init__(self):
        """
        Initializes a new BaseModel instance with a unique UUID string,
        and sets the creation and modification timestamps.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Updates the 'updated_at' timestamp to the current time.
        This method should be triggered whenever an object is modified.
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Updates the attributes of the instance dynamically based on the provided data dictionary.
        
        Args:
            data (dict): A dictionary containing attribute names and their new values.
        """
        # Protect read-only system attributes from being modified by external inputs
        protected_keys = ['id', 'created_at', 'updated_at']
        
        for key, value in data.items():
            if key not in protected_keys and hasattr(self, key):
                setattr(self, key, value)
        
        # Automatically update the timestamp after applying modifications
        self.save()
