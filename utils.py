from jina import DocumentArray, Document
from executors.sentence_encoder import encode_sentences
from git import Repo

second_brain_path = ""

def split_note_into_sentences(note):
    sentences = []
    for line in note.split('\n'):
        line = line.strip()
        sub_sentences = line.split('. ')
        for sub_sentence in sub_sentences:
            if sub_sentence != '':
                sentences.append(sub_sentence.strip())
    return sentences


def get_highlight_with_embedded_notes(highlight, note):
    database = Document(text=highlight)
    children = DocumentArray(storage='annlite', config={'n_dim': 384})
    sentences = split_note_into_sentences(note)
    for s in sentences:
        child = Document(text=s, parent_id=database.id)
        children.append(child)

    encoded_da = encode_sentences(children)
    highlight_embedding = encode_sentences(DocumentArray(
        [database], storage='annlite', config={'n_dim': 384}))
    database.embedding = highlight_embedding[0].embedding
    database.chunks = encoded_da
    return database


def get_list_of_updated_notes():
    r = Repo(second_brain_path)
    #r.git.add('.')
    different = r.head.commit.diff(None)
    #different_2 = r.git.diff(name_only=True)
    files = {}
    for item in different:
        full_path = second_brain_path + item.a_path
        files[full_path] = True if item.change_type == 'M' else False
        #r.index.remove(full_path)

    return files


def commit_file(filepath):
    r = Repo(second_brain_path)
    r.index.add(filepath)
    r.index.commit(f'{filepath} committed')
