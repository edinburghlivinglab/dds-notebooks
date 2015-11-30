ABSTRACT := jupyter_oer_abstract_v2.md
PDF := jupyter_oer_abstract_v2.pdf
TEXT := jupyter_oer_abstract_v2.txt

BIBTEX := abstract.bib

pdf:
	pandoc --filter pandoc-citeproc $(ABSTRACT) --biblio $(BIBTEX) -o $(PDF)


text:
	pandoc --filter pandoc-citeproc $(ABSTRACT) --biblio $(BIBTEX) -o $(TEXT)