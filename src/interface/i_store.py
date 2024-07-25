"""
    Interface for a Store of files
"""
class IStore():
    """
        add files to store.

        file_paths should be files available on the local filesystem for now.
        you can upload files to local filesystem using the file upload APIs. (see API documentation)
    """
    def add(self, file_paths : list[str]):
        pass

    """
        get id of store
    """
    def get_id():
        pass