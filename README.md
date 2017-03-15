# revquantum #

This package attempts to solve, or at least mitigate, standard problems with
writing quantum information papers in ``{revtex4-1}``. In particular:

- Includes titles in BibTeX.
- Allows for use of nicer-looking fonts via ``{mathpazo}``.
- Configures ``{hyperref}`` to make nicer-looking links and to correctly use ``\autoref``.
- Sets up ``{listings}`` for common scientific languages and legacy environments (Python, Mathematica and MATLAB).
- Provides notation for quantum information and makes defining new notation easier.
- Reduces boilerplate for author affiliations by providing a (rudimentary) database for a few departments.

A major goal of this package is to reduce the amount of useless crap that needs to be copied and pasted between documents. In particular, a complete document can be written in just a few lines:

```latex
\documentclass[pra,aps,twocolumn,superscriptaddress,10pt]{revtex4-1}
\usepackage[pretty,uselistings]{revquantum}

\begin{document}

\title{Example \textsf{revquantum} Document}

\author{Christopher Granade}
\email{cgranade@cgranade.com}
\affilUSydPhys \affilEQUS

\date{\today}

\begin{abstract}
    \TODO
\end{abstract}

\maketitle

\bibliography{example}
\appendix

\end{document} 
```

## Installing ##

### Install With PowerShell ###

In an attempt to cut down on the pain of LaTeX package installation, ``{revquantum}`` uses [PoShTeX](https://github.com/cgranade/posh-tex/) to automate installation. If you're running PowerShell already, just run ``Install.ps1``:

```powershell
PS> Unblock-File Install.ps1 # Mark the installer as safe to run.
PS> ./Install.ps1
```

PowerShell itself is easy to install on many macOS and Linux systems using the [provided packages](https://github.com/PowerShell/PowerShell#get-powershell).

### Manual Installation ###

I think the following works on Unix-like systems. If not, let me know or pull request with better instructions.

```bash
$ latex revquantum.ins # Makes the actual .sty from the .dtx file.
$ pdflatex revquantum.dtx # Makes documentation, such as it is.
$ mkdir texdir/tex/latex/revquantum # Replace texdir with where you actually installed TeX (e.g. ~/texmf).
$ cp revquantum.sty texdir/tex/latex/revquantum # As with above, replace texdir.
$ texhash
```

Directions for Windows/MikTeX can be found thanks to [this useful StackOverflow answer](http://tex.stackexchange.com/questions/2063/how-can-i-manually-install-a-package-on-miktex-windows).

## Using ##

I'll write more complete documentation later (hopefully), but for now:

- ``{braket}`` is automatically imported, defining ``\ket``, ``\bra`` and ``\braket``.
- The notation commands ``\ii`` and ``\dd`` typeset roman "i" and "d" characters, respectively. More generally, ``\newrm{foo}`` creates a new command ``\foo`` that typesets ``foo`` in math-roman. ``{revquantum}`` comes with ``\e``, ``\TVD`` and ``\T`` predefined using ``\newrm``.
- Similarly, ``\newoperator`` defines new commands which typeset using ``\operatorname``. By default, this is used to define ``\Tr``, ``\Cov``, ``\supp``, ``\diag`` and ``\rank``.
- The commands ``\defeq``, ``\expect`` and ``\id`` define the common notation ``:=``, double-struck E and double-struck 1 (respectively).
- ``\newaffil{NAME}{DESCRIPTION}`` defines a new affiliation command ``\affilNAME``.
- The ``\todo`` command typesets its argument in purple and raises a warning when built. If ``{revquantum}`` is loaded with the ``[final]`` option, this warning is escalated to an error. Similarly, ``\TODO`` takes no argument but inserts the placeholder "TODO" and ``\todolist`` typesets an ``{itemize}`` environment in ``\todo``.

## Known Issues ##

- The BibTeX thing is an unforgivable hack. Thankfully, I'm not asking for anyone's forgiveness.
- ``\autoref`` chokes on appendices, giving nonsense like "Section A". This should be fixable, though.
- The use of the "UW" prefix for the University of Waterloo was probably a bad idea, and will likely change so as to not preclude other universities whose names start with "W".
