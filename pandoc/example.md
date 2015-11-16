---
title: Pandoc Example 
author: Christopher Granade
date: 16 November 2015
bibliography: example.bib
pretty: true
...

# Test Section #

This is an example section, demonstrating a few different ``revquantum``
features working in Markdown. For instance, familiar math-mode commands like $\Tr$ and $\id$ work.

# Those BibTeX Hacks #

The BibTeX hacks work, too, so that we can happily cite our favorite papers like @aloupis_classic_2012. We have to compile on our own, though. For example:

```
$ pandoc --natbib --filter pandoc-citeproc --template=revquantum example.md -o example.tex --standalone
$ latexmk --pdf example.tex
```

This is currently a pain point, but hopefully should be fixed in future versions.
