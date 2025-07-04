# from rag.encoder import Encoder
from torch.nn.functional import embedding


class Retriever:
    def __init__(self, dbmanager, encoder):
        self.dbmanager = dbmanager
        self.encoder = encoder

    def find_relate_data(self, input_data: str):
        """
        This function receives a query input,
        converts it into a vector,
        and finds a similar text in the database that
        will be used as a context for LLM.

        Args:
            input_data: str
                Data in text form, to which need to find the related data.
        Returns:

        """
        emb = self.encoder.conv_text_to_vec([input_data])
        # a part where im doing a request to database and trying to find similar vectors
