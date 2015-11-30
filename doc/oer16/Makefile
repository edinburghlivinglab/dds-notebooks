ABSTRACT := jupyter_oer_abstract_v2.md
OUTPUT := jupyter_oer_abstract_v2.pdf
BIBTEX := abstract.bib

doc:
	pandoc --filter pandoc-citeproc $(ABSTRACT) --biblio $(BIBTEX) -o $(OUTPUT)