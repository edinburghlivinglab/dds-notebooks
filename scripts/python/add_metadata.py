import nbformat
from nbformat import NotebookNode

test = 'what_is_data_1.ipynb'
out = 'test.ipynb'


data = nbformat.read(test, as_version=nbformat.NO_CONVERT)
new_metadata = data.metadata.copy()

cells = data.cells

document = NotebookNode(dict(author = 'Ewan Klein', licence = 'CC-BY', title="What is Data???"))

new_metadata['document'] = document
data.metadata = NotebookNode(new_metadata)
nbformat.validate(data)

header = cells[0]['source']


title = '# ' + document.title
author = document.author

header_lines = header.split('\n')


if header_lines[0].startswith('#'):
    del header_lines[0]

header_lines = [title, author] + header_lines
header_string = '\n'.join(header_lines)

data.cells[0]['source'] = header_string

with open(out,  encoding='utf-8', mode='w') as fp:
    nbformat.write(data, fp)





