"""
    Interface for an AI agent. All agents should implement this
"""

class IAgent():
    """
        pass a list of questions and a list of store_ids to get responses to the questions
        using the information available in the stores
    """
    def query(self, questions: list[str], store_ids: list[str]):
        pass