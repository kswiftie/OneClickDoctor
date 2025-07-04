from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F


class Encoder:
    def __init__(self, model_name: str):
        """

        Args:
            model_name: str
                Name of the model from huggingface.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(
            model_name
        )  # 'sentence-transformers/all-MiniLM-L6-v2'

    def conv_text_to_vec(self, text_blocks: list[str]) -> torch.Tensor:
        """

        Args:
             text_blocks: list[str]
                List of a texts to be converted to vectors.
                count of a text_blocks == count of vectors.
        """

        # Mean Pooling - Take attention mask into account for correct averaging
        def mean_pooling(model_output, attention_mask):
            token_embeddings = model_output[
                0
            ]  # First element of model_output contains all token embeddings
            input_mask_expanded = (
                attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            )
            return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
                input_mask_expanded.sum(1), min=1e-9
            )

        # Tokenize blocks
        encoded_input = self.tokenizer(
            text_blocks, padding=True, truncation=True, return_tensors="pt"
        )

        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)

        # Get the embeddings
        sentence_embeddings = mean_pooling(
            model_output, encoded_input["attention_mask"]
        )

        # And Normalize them
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

        return sentence_embeddings
