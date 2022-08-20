![screen-gif](./obsidian_neural_search.gif)

# Setting up the repository
1. Install conda and create a new environment using python 3.7 -> `conda create -n <env-name> python=3.7`
2. Install jina ai -> `conda install jina -c conda-forge`
3. Install annlite -> `pip install "docarray[annlite]"`
4. Install tqdm -> `conda install tqdm`
5. Initialize a git repository at the folder of your second brain
6. `conda install gitpython`
7. Inside `utils.py`-> add the path of your second brain at `second_brain_path`


# How to use
1. To index your data first -> `python easiest_search.py --indexed False --search False`
2. To search your data -> `python easiest_search.py --indexed True --search True``

# How does it work?
- First we get a list that has been updated in our second brain since the last time we indexed our second brain, here we differentiate between new and modified files. For modified files we delete the old file from the index and add the new file by calling the `remove_old_note` function through our flow
- In the `add_highlight` method, we divide the note into "title" and "body". The title is the name of the file and the body starts after the first heading (we usually have a note that starts with '# <Title>')
- The `get_highlight_with_embedded_notes` creates a jina document type which has as text the title of the note, and it would have multiple "chunks" representing the content of the note. Every sentence is considered its own "chunk". Later, when we are searching in our second brain we search against these sentences for a match
- After files have been indexed, they are comitted in the repo we established in the second brain folder
- For each sentence we create an embedding (vector representation) in 384 dimensions using the method `encode_sentences`this takes place on the jina cloud to speed up the process
- Your indexed database lives on your machine under `workspace` only the embedding would happen on the cloud but all your information lives locally on your own machine
- When you are searching, your query gets turned into a vector, and matched to the nearest neighbout under the function `search`






