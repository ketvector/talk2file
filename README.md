**1. What does the code do ?:**

- APIs to support question answering from files. (Supports only PDF for now, will add support for other files later)
- Also supports sending the responses to a target. (Supports sending to slack for now)

**2. Core Interfaces:**

The main interfaces in the project are Agents and Stores. Agents are AI agents that answer questions, and stores host the information base. See [./src/interface](./src/interface/) for more.

**3. Implementations:**

There are two implementations I have provided for the interfaces:

1. [Langchain Implementation](./src/langchain/) : 
   - Custom RAG implementation including indexing, ingestion to vector database (chroma), retrieval from database, and prompt to AI model (gpt-4o-mini for now). 
   - Used langchain helpers but created the chain myself. 
   - Also hosting chromadb separetely with persistence, and not using the default Chroma.from_docs helper from langchain
  
2. [Open AI Assistant Implementation](./src/openai_assistants/):
   
   - Used the [OpenAI assistants API](https://platform.openai.com/docs/assistants/overview) to implement the file search features.

**4. API:**
  
  - Used FastAPI to provide file upload, adding files to vector store, asking question and posting to slack functions.
  - You can view the APIs with examples in Postman :
  
     [<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/7638829-4199003a-6846-4c9b-96cb-749e743c9b95?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D7638829-4199003a-6846-4c9b-96cb-749e743c9b95%26entityType%3Dcollection%26workspaceId%3D695166a5-a212-4b07-8aab-781842a14dff)
  - To run the server locally,
      - install dependencies using `pip3 install -r requirements.txt` from the root folder.
      - create a `.env` file in the root folder. You can copy the contents of `.env.example` and fill in the variables. You can use defaults and just change the keys.
      - if hitting the `/langchain` apis, also start the chroma server using `chroma run --path ./ --port 8001`. Here I am assuming you are using port 8001 from `.env`
      - run `fastapi dev main.py` from inside the `src` folder. this is for dev mode. i have only tested with this.


**5. Proposed Improvements:**

**5.1: Infra**
- A lot of the computation is time consuming so a synchronous GET/POST for asking questions or ingesting files is not the best approach. A better approach would be to design asynchronous APIs using a combination of databases (MongoDB) and queues (RabbitMQ).

- As an example of the previous point, the query routes could be designed as:
   
   - 1: Client posts questions using a simple POST API.
   - 2: The backend takes questions from step 1 and adds it to queue. To the client it provides a request-id for this request. The client can use the request-id to poll for when the answer becomes available.
   - 3: A different service picks the questions from queue, gets the answers and posts it back to queue
   - 4: A different service picks up the answers and posts to slack
   - 5: The client can get the status of all the tasks using polling on the request-id it was given.

- We can also think about streaming the answers. The openAI and langchain sdks support streaming out of the box and I can use them
 
**5.2: RAG Quality**

- experiment with different `chunk size` and `chunk overlap` values in the `document splitter`.
- experiment with `similarity search threshold` instead of `top-k` for the `vector store retriver`.
- try retrievers other than `VectorStore` like `ParentDocument` , `MultiVector`  or `MultiQuery`.
- In the langchain implementation, also return `sources` or `citations`
like the `openai-assistants` file search implementation does. 

**5.3: Benchmarking/Metrics**

- Option 1: Create a test dataset and use a traditional metric like `ROGUE` or `BLEU` . (Too effort intensive ?)
- Option 2: Use [RAGAS](https://docs.ragas.io/en/stable/) to evaluate retriver and llm. ( Seems faster )
- Option 3: Something custom made ? [G-Eval](https://arxiv.org/abs/2303.16634)
 
**5.4: Code Quality**
- Resolve all the TODOs
- Better error handling at some places
- modify apis to support files being added to store in one call (services already support this)
- better API responses to clients in upload to store apis (instead of simple "success")

**6. Known Issues**
- File upload from postman intermittently errors due to what is most likely a Postman bug. [Bug](https://stackoverflow.com/questions/64972165/fastapi-error-uploading-files-bigger-than-100kb)
  











