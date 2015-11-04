# revquantum #

This package attempts to solve, or at least mitigate, standard problems with
writing quantum information papers in ``{revtex4-1}``. In particular:

- Includes titles in BibTeX.
- Allows for use of nicer-looking fonts via ``{mathpazo}``.
- Configures ``{hyperref}`` to make nicer-looking links and to correctly use ``\autoref``.
- Sets up ``{listings}`` for common scientific langauges and legacy environments (Python, Mathematica and MATLAB).
- Provides notation for quantum information and makes defining new notation easier.
- Reduces boilerplate for author affiliations by providing a (rudimentary) database for a few departments.

## Installing ##

Installing LaTeX packages outside of CTAN is a pain, and this is no exception. I'll submit there at some point to remove that difficulty. In the meantime, I think the following works on Unix-like systems. If not, let me know or pull request with better instructions.

```bash
$ latex revquantum.ins # Makes the actual .sty from the .dtx file.
$ pdflatex revquantum.dtx # Makes documentation, such as it is.
$ mkdir texdir/tex/latex/revquantum # Replace texdir with where you actually installed TeX (e.g. ~/texmf).
$ cp revquantum.sty texdir/tex/latex/revquantum # As with above, replace texdir.
$ texhash
```

Directions for Windows/MikTeX can be found thanks to [this useful StackOverflow answer](http://tex.stackexchange.com/questions/2063/how-can-i-manually-install-a-package-on-miktex-windows).
