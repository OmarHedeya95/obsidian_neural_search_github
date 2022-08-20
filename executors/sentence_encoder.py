from docarray import Document, DocumentArray
import pprint


def encode_sentences(da, endpoint='jinahub+sandbox://TransformerSentenceEncoder/latest'):
    '''
    Encode sentences using the given endpoint.
    '''
    r = da.post(endpoint)
    return r
