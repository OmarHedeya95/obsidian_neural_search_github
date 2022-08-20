from operator import index
from pprint import pprint
from executors.sentence_encoder import encode_sentences
from jina import DocumentArray, Document, Flow
from executors.simple_indexer import SimpleIndexer
from extract_info import add_highlight
from utils import get_highlight_with_embedded_notes, get_list_of_updated_notes, commit_file
from tqdm import tqdm
import argparse




if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Control variable for indexing and searching")
    parser.add_argument('--indexed', type=str,
                        help='Is your data already indexed?', required=True)
    parser.add_argument('--search', type=str,
                        help='Should I search your data?', required=True)
    parser.add_argument('--duplicate', type=str,
                        help='Should I remove duplicates from database?', required=False)
    args = parser.parse_args()
    is_indexed = True if args.index == "True" else False
    to_search = True if args.search == "True" else False
    remove_duplicates = True if args.duplicate == "True" else False
    
    if remove_duplicates:
        print("Removing Duplicates from database....")
        duplicate_flow = Flow.load_config('./flow_simple.jina.yml')
        with duplicate_flow:
            duplicate_flow.post(on='/duplicate_removal')

    if is_indexed == False:

        files = get_list_of_updated_notes()
        for file, is_modified in tqdm(files.items()):
            try:
                note, highlight = add_highlight(file)
            except Exception as e:
                continue

            if note and highlight:
                # Create a document with the note title as text and all (embedded) sentences as chunks
                try:
                    embedded_note = get_highlight_with_embedded_notes(
                        highlight, note)
                except Exception as e:
                    print(f'This file is too long: {file}')
                    pass

                docs = DocumentArray(storage='annlite', config={
                    'n_dim': 384, 'metric': 'cosine'})
                docs.append(embedded_note)

                # If file is modified and already indexed
                duplicate_flow = Flow.load_config('./flow_simple.jina.yml')
                if is_modified:
                    with duplicate_flow:
                        duplicate_flow.post(on='/remove_old_note', data=docs)

                indexing_flow = Flow.load_config('./flow_simple.jina.yml')

                with indexing_flow:
                    # This way we index the note and we have the sentences as chunks within the note, when we search we can find the sentence and easily figure out to which note it belongs
                    indexing_flow.post(on='/index', data=docs)

                    # commit this file
                    commit_file(file)

    searching_flow = Flow.load_config(source='./flow_simple.jina.yml')
    with searching_flow:
        if to_search:
            query = input('Please enter your search query: ')
            query = DocumentArray([Document(text=query)], storage='annlite', config={
                'n_dim': 384, 'metric': 'cosine'})
            encoded_query = encode_sentences(query)
            searching_flow.post(on='/search', data=encoded_query)
        else:
            #searching_flow.post(on='/validate')
            pass
