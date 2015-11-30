ABSTRACT := jupyter_oer_abstract_v2.md
PDF := jupyter_oer_abstract_v2.pdf
HTML := jupyter_oer_abstract_v2.html

BIBTEX := abstract.bib

pdf:
	pandoc --filter pandoc-citeproc $(ABSTRACT) --biblio $(BIBTEX) -o $(PDF)

html:
	pandoc --filter pandoc-citeproc $(ABSTRACT) --biblio $(BIBTEX) -t html -o $(HTML)