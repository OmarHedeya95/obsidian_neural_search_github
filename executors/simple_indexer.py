import os
from collections import defaultdict
from docarray import DocumentArray
from jina import Executor, requests


class SimpleIndexer(Executor):
    """Simple indexer class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._docs = DocumentArray(storage='annlite',
                                   config={'data_path': os.path.join(self.workspace, 'index.db'), 'n_dim': 384, 'metric': 'cosine'})

    @requests(on='/duplicate_removal')
    def remove_duplicates(self, **kwargs):
        repeat = dict()

        for i, doc in enumerate(self._docs):
            if not repeat.get(doc.text):
                repeat[doc.text] = {'occurence': 1, 'id': doc.id}
            else:
                original = self._docs[repeat[doc.text]['id']]
                # Due to saving document title as first highlight and not as file name we check if first chunks are equal
                if original.chunks and doc.chunks:
                    if original.chunks[0].text == doc.chunks[0].text:
                        if len(original.chunks) == len(doc.chunks):
                            self._docs.remove(original)
                            original.chunks.clear()
                            self._docs.__delitem__(i)


    @requests(on='/remove_old_note')
    def remove_old_note(self, docs: 'DocumentArray', **kwargs):
        modified_note = docs[0]
        with self._docs:
            for i, old_note in enumerate(self._docs):
                if modified_note.text == old_note.text:
                    self._docs.remove(old_note)
                    old_note.chunks.clear()
                    self._docs.__delitem__(i)
                    break



    @requests(on='/index')
    def index(self, docs: DocumentArray, **kwargs):
        # Stores the index in attribute
        if docs:
            with self._docs:                
                self._docs.append(docs[0])


    @requests(on='/validate')
    def validate(self, **kwargs):
        for doc in self._docs:
            doc.summary()

    @requests(on='/search')
    def search(self, docs: 'DocumentArray', **kwargs):
        """Append best matches to each document in docs"""

        for doc in docs:
            print('Questions')
            print(doc.text)
            doc.match(  # Match query agains the index using cosine similarity
                # self._docs['@c'][...] because we want to match with the chunks
                self._docs['@c'][...],
                metric='cosine',
                # makes the top result 1, lowest result 0
                normalization=(1, 0),
                limit=5,
                traversal_rdarray='c,'
            )
            for match in doc.matches:
                print(f"The matched sentence: {match.text}")
                print(f"Its score: {match.scores['cosine']}")
                print(f"Note title: {self._docs[match.parent_id].text} \n")

            '''results = self._docs['@c'][...].find(doc.embedding, limit=10)
            for result in results:
                print(result.text)
                print(result.scores)'''

        print('-----------------------------------')
