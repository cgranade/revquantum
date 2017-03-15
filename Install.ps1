param(
    [switch] $CTAN
)

#region Bootstrap PoShTeX
if (!(Get-Module -ListAvailable -Name posh-tex -ErrorAction SilentlyContinue)) {
    Install-Module posh-tex -Scope CurrentUser
}
Import-Module posh-tex
#endregion

Out-TeXStyle revquantum
Out-TeXStyleDocumentation revquantum

Install-TeXUserResource tex/latex/revquantum revquantum.sty, revquantum.pdf

Install-PandocUserResource templates pandoc/templates/revquantum.latex -ErrorAction Continue

if ($CTAN) {
    Invoke-TeXBuildEngine example.tex
    Export-CTANArchive -ArchiveLayout Simple revquantum.ins, revquantum.pdf, README.md, example.tex, example.pdf, Install.ps1
}