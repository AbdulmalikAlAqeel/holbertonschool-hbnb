"""Repository interfaces and in-memory implementation."""

from abc import ABC, abstractmethod


class Repository(ABC):
    """Define the common persistence interface."""

    @abstractmethod
    def add(self, obj):
        """Add an object to the repository."""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by ID."""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieve all objects."""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object."""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object."""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by one of its attributes."""
        pass


class InMemoryRepository(Repository):
    """Store objects temporarily in memory."""

    def __init__(self):
        """Initialize empty storage."""
        self._storage = {}

    def add(self, obj):
        """Add an object using its ID as the key."""
        self._storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        """Retrieve an object by ID."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Return all stored objects."""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update an object using a dictionary of values."""
        obj = self.get(obj_id)

        if not obj:
            return None

        obj.update(data)
        return obj

    def delete(self, obj_id):
        """Delete an object by ID."""
        if obj_id not in self._storage:
            return False

        del self._storage[obj_id]
        return True

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve the first object matching an attribute."""
        for obj in self._storage.values():
            if getattr(obj, attr_name, None) == attr_value:
                return obj

        return None
