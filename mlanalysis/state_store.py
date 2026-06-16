from typing import List, Dict
import numpy as np


class ClaimStore:

    def __init__(self):
        self.claims: List[Dict] = []
        self.embeddings = None

    def add_batch(self, new_claims, new_embeddings):
        """
        Append new claims + embeddings
        """

        if self.embeddings is None:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])

        self.claims.extend(new_claims)

    def get_all(self):
        return self.claims

    def get_embeddings(self):
        return self.embeddings
