import os

class OpenAIAssistantsAgent:
    def __init__(self, client, id=None,  name="OpenAIAssistantsAgent"):
        self.client = client


        if id == None:
            model = os.environ["OPENAI_ASST_MODEL"]
            self.assistant = self.client.beta.assistants.create(
                name=name,
                instructions="You are an expert pdf reader. Use your knowledge base to answer the questions asked to you",
                model=model,
                tools=[{"type": "file_search"}],
            )
        else:
            self.assistant = self.client.beta.assistants.retrieve(
                id
            )
        

    # TODO: Batching questions
    def query(self, questions, store_ids):        
        self.assistant = self.client.beta.assistants.update(
            assistant_id=self.assistant.id,
            tool_resources={"file_search": {"vector_store_ids": store_ids}},
        )

        json_response_array = []
        
        for question in questions:

            messages = [
                {
                    "role": "user",
                    "content" : question
                } 
            ]

            thread = self.client.beta.threads.create(
                messages=messages
            )

            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread.id, assistant_id=self.assistant.id
            )

            answers = list(self.client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    

            if len(answers) > 0:
                answer_content = answers[0].content[0].text
                annotations = answer_content.annotations
                citations = []
                for index, annotation in enumerate(annotations):
                    answer_content.value = answer_content.value.replace(annotation.text, f"[{index}]")
                    if file_citation := getattr(annotation, "file_citation", None):
                        cited_file = self.client.files.retrieve(file_citation.file_id)
                        citations.append(f"[{index}] {cited_file.filename}")
                json_response_array.append(
                    {
                        "question": question,
                        "answer": answer_content.value,
                        "citations": citations
                    }
                )

        return {
            "responses" : json_response_array 
        }


    