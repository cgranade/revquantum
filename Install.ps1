# bootstrap posh-tex
if (!(Get-Module -ListAvailable -Name posh-tex -ErrorAction SilentlyContinue)) {
    Install-Module posh-tex
}
Import-Module posh-tex
# /bootstrap posh-tex

Out-TeXStyle revquantum
Out-TeXStyleDocumentation revquantum

Install-TeXUserResource tex/latex/revquantum revquantum.sty, revquantum.pdf

Install-PandocUserResource templates pandoc/templates/revquantum.latex -ErrorAction Continue
