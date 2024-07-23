from openai import OpenAI

class OpenAIAssistantsAgent:
    def __init__(self, client, id=None,  name="OpenAIAssistantsAgent"):
        self.client = client


        if id == None:
            self.assistant = self.client.beta.assistants.create(
                name=name,
                instructions="You are an expert pdf reader. Use your knowledge base to answer the questions asked to you",
                model="gpt-3.5-turbo-0125",
                tools=[{"type": "file_search"}],
            )
        else:
            self.assistant = self.client.beta.assistants.retrieve(
                id
            )
        

    
    def query(self, questions, store_ids):
        question = "" 
        for idx, q in enumerate(questions):
            question = question + f"{idx}.{q}\n"
        
        self.assistant = self.client.beta.assistants.update(
            assistant_id=self.assistant.id,
            tool_resources={"file_search": {"vector_store_ids": store_ids}},
        )

        thread = self.client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": question,
                }
            ]
        )

        # Use the create and poll SDK helper to create a run and poll the status of
        # the run until it's in a terminal state.

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=self.assistant.id
        )

        messages = list(self.client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

        answer = ""

        if len(messages) > 0:
            message_content = messages[0].content[0].text
            annotations = message_content.annotations
            citations = []
            for index, annotation in enumerate(annotations):
                message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
                if file_citation := getattr(annotation, "file_citation", None):
                    cited_file = self.client.files.retrieve(file_citation.file_id)
                    citations.append(f"[{index}] {cited_file.filename}")

            answer = answer + message_content.value
            answer = answer + "\n".join(citations)

        return answer


    