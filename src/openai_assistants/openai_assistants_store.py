from ..interface.i_store import IStore
class OpenAIAssistantsStore(IStore):
    def __init__(self, client, id = "None", name="OpenAIAssistantsStore"):
        self.client = client
        if id == None:
            self.vector_store = client.beta.vector_stores.create(name=name)
        else:
            self.vector_store = client.beta.vector_stores.retrieve(id)
    
    def add(self, file_paths):
        file_streams = [open(path, "rb") for path in file_paths]

        print("starting upload")
 
        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id= self.vector_store.id, files=file_streams
        )

        print("upload done")
 
        # You can print the status and the file counts of the batch to see the result of this operation.
        # TODO: proper error handling
        print(file_batch.status)
        print(file_batch.file_counts)
    
    def get_id(self):
        return self.vector_store.id
 