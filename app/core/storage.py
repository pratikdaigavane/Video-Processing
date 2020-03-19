import os
from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):
    """
    Changing the default behaviour of django to allow overwrite files
    """
    def get_available_name(self, name, max_length=None):
        """If the file already exists then overwriting it"""
        if self.exists(name):
            os.remove(os.path.join(self.location, name))
            return super(OverwriteStorage,
                         self).get_available_name(name, max_length)
