from abc import ABC, abstractmethod

class Repository(ABC):
    """
    Abstract Base Class defining the interface for data persistence.
    All repository types (e.g., In-Memory, Database-backed) must implement these methods.
    """
    @abstractmethod
    def add(self, obj):
        """
        Add a new object to the persistence layer.
        """
        pass

    @abstractmethod
    def get(self, id):
        """
        Retrieve an object by its unique ID.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Retrieve all objects in the persistence layer.
        """
        pass

    @abstractmethod
    def update(self, id, data):
        """
        Update an existing object's attributes.
        """
        pass

    @abstractmethod
    def delete(self, id):
        """
        Delete an object by its unique ID.
        """
        pass


class InMemoryRepository(Repository):
    """
    In-memory implementation of the Repository interface.
    Uses a dictionary for fast, temporary data storage during Part 2.
    """
    def __init__(self):
        """
        Initializes the storage as an empty dictionary.
        """
        self._storage = {}

    def add(self, obj):
        """
        Saves an object in memory using its unique ID as the key.
        Returns the saved object.
        """
        self._storage[obj.id] = obj
        return obj

    def get(self, id):
        """
        Retrieves an object from memory by its ID.
        Returns None if the object does not exist.
        """
        return self._storage.get(id)

    def get_all(self):
        """
        Returns a list of all objects currently stored in memory.
        """
        return list(self._storage.values())

    def update(self, id, data):
        """
        Updates an object's attributes based on its ID and a dictionary of new values.
        Returns the updated object, or None if the object is not found.
        """
        obj = self.get(id)
        if obj:
            obj.update(data)
            return obj
        return None

    def delete(self, id):
        """
        Deletes an object from memory by its ID.
        Returns True if successfully deleted, False otherwise.
        """
        if id in self._storage:
            del self._storage[id]
            return True
        return False
