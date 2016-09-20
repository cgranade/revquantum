#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

PACKAGE_NAME = 'revquantum'

import sys
import os
import shutil
import zipfile
from subprocess import Popen, PIPE

def print_usage():
    print("""
Usage:
------

python build.py tds
    Builds a *.tds.zip file for this package.

python build.py install
    Installs this package into the main TeX directory.
    May require administrator privileges.
""")
    sys.exit(1)

def find_tex():
    proc = Popen(['kpsewhich', 'article.cls'], stdout=PIPE)
    stdout, stderr = proc.communicate()

    head, tail = os.path.split(stdout.strip())

    # Note that kpsewhich returns with / characters, even
    # under Windows, so we must use str.split to override
    # os.path's behavior.
    head_parts = head.split('/')

    # If we're on Windows, then that destroyed the drive
    # part of the pathspec.
    if os.name == 'nt':
        head_parts = [head_parts[0] + '\\'] + head_parts[1:]

    # Remove "tex/latex/base" from head_parts, since that's where
    # article.cls should live.
    tex_root = os.path.join(*head_parts[:-3])

    return tex_root

def copy_to_tex(what, tex_path=['tex', 'latex']):
    tex_root = find_tex()
    where = os.path.join(tex_root, *tex_path)

    print("Installing: {} ---> {}".format(what, where))
    shutil.copyfile(what, where)

def yes_proc(args, yes="yes"):
    proc = Popen(args, stdin=PIPE)
    while proc.returncode is None:
        proc.communicate(yes)
        proc.poll()

    return proc.returncode == 0

class LaTeXStyleBuilder(object):
    """
    Builds a DocStrip-formatted LaTeX style by running
    the LaTeX processor on the appropriate *.dtx file.
    """
    style_name = None
    manifest = {}
    ctan_manifest = {}

    def __init__(self, style_name):
        self.style_name = style_name

        self.manifest = {
            '{}.{}'.format(style_name, ext):
                path + [style_name]
            for ext, path in
            {
                'sty': ['tex', 'latex'],
                'pdf': ['doc', 'latex']
            }.items()
        }

        self.ctan_manifest = [
            '{}.tds.zip'.format(style_name),
            '{}.dtx'.format(style_name),
            '{}.pdf'.format(style_name),
            'build.py',
            'README.md'
        ]

    def build_sty(self):
        print("Building: {}.sty".format(self.style_name))
        if not yes_proc(['latex', '{}.ins'.format(self.style_name)]):
            raise RuntimeError
        print("\n\n\n")
        return self

    def build_doc_pdf(self):
        print("Building: {}.pdf".format(self.style_name))
        if not yes_proc(['pdflatex', '{}.dtx'.format(self.style_name)]):
            raise RuntimeError
        print("\n\n\n")
        return self

    def build_tds_zip(self):
        print("Building: {}.tds.zip".format(self.style_name))
        tds_zip = zipfile.ZipFile('{}.tds.zip'.format(self.style_name), 'w')

        for what, where in self.manifest.items():
            assert os.path.isfile(what)
            print("\tPacking: {} ---> {}".format(what, os.path.join(*where)))
            tds_zip.write(what, arcname=os.path.join(*where + [what]))

        print("\n\n\n")
        return self

    def build_ctan_zip(self):
        print("Building: {}.zip".format(self.style_name))
        ctan_zip = zipfile.ZipFile('{}.zip'.format(self.style_name), 'w')

        for what in self.ctan_manifest:
            assert os.path.isfile(what)
            print("\tPacking: {}".format(what))
            ctan_zip.write(what)

        print("\n\n\n")
        return self

    def install(self):
        for what, where in self.manifest.items():
            assert os.path.isfile(what)
            copy_to_tex(what, where)

        return self

if __name__ == "__main__":
    print("""
WARNING: This installer is still in alpha, and is provided
         as a convenience only. That said, this installer
         may cause you to say unkind words in frustration
         instead of providing the intended convenience.
""")

    if len(sys.argv) < 2:
        print_usage()

    else:
        subcommand = sys.argv[1]
        if subcommand not in ('tds', 'install', 'ctan'):
            print("No such command {}, try either 'tds', 'install' or 'ctan'.")
            print_usage()

        builder = LaTeXStyleBuilder(PACKAGE_NAME)
        builder.build_sty().build_doc_pdf()

        if subcommand == 'tds':
            builder.build_tds_zip()

        elif subcommand == 'install':
            builder.install()

        elif subcommand == 'ctan':
            builder.build_tds_zip().build_ctan_zip()

        else:
            assert False
