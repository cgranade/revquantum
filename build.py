#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

PACKAGE_NAME = 'revquantum'
TEX_DIR = None

import errno
import sys
import os
import tempfile
import shutil
import zipfile
from subprocess import Popen, PIPE

from io import StringIO

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

def is_writable(dir_name):
    # Technique adapted from:
    #     http://stackoverflow.com/a/25868839/267841
    # We modify by not raising on other OSErrors, as
    # we don't care *why* a directory isn't writable,
    # so much as that we need to know that it isn't.
    # We also note that tempfile raises an IOError
    # on Windows if it can't write, so we catch that,
    # too.
    try:
        with tempfile.TemporaryFile(dir=dir_name):
            pass
    except (OSError, IOError) as ex:
        return False
    
    return True

def mkdir_p(path):
    # Copied from http://stackoverflow.com/a/600612/267841,
    # in keeping with the CC-BY-SA 3.0 license on StackOverflow
    # user contributions.
    if os.path.isdir(path):
        return
    try:
        os.makedirs(path)
    except OSError as exc:  # Python > 2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    except WindowsError as exc:
        if exc.errno == 183 and os.path.isdir(path):
            pass
        else:
            raise

def try_until(condition, *fns):
    for fn in fns:
        retval = fn()
        if condition(retval):
            return retval

    # This is likely a terrible error for any poor user,
    # so we should probably catch it. Probably.
    raise RuntimeError("No candidates found matching the given condition.")

def is_miktek():
    # Assume MikTeX if and only if Windows.
    # This is a bad assumption, but we can encapsulate
    # it here and generalize later.
    return os.name == 'nt'

def find_tex_root():
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

def find_tex_user():
    if is_miktek():
        # Use MikTeX's initexmf utility to find the user install
        # dir.
        #     http://tex.stackexchange.com/a/69484/615
        initexmf = Popen(['initexmf', '--report'], stdout=PIPE)
        stdout, stderr = initexmf.communicate()

        for line in stdout.split('\n'):
            try:
                key, value = line.split(':', 1)
                if key.strip().lower() == 'userinstall':
                    return value.strip()
            except:
                continue

        raise RuntimeError("MikTeX did not report a UserInstall directory.")

    else:
        return os.path.expanduser('~/texmf')

def find_tex():
    global TEX_DIR

    if TEX_DIR is None:
        TEX_DIR = try_until(is_writable, 
            find_tex_root,
            find_tex_user
        )

    return TEX_DIR

def copy_to_tex(what, tex_path=['tex', 'latex']):
    tex_root = find_tex()
    where = os.path.join(tex_root, *tex_path)
    full_path = os.path.join(where, what)

    # Check if the directory exists, make it if it doesn't.
    mkdir_p(where)

    print("Installing: {} ---> {}".format(what, full_path))
    shutil.copyfile(what, full_path)

def write_to_zip(zip_file, filename, arcname=None, normalize_crlf=None):
    """
    normalize_crlf = None: automatically detect from filename.
    """

    if normalize_crlf is None:
        root, ext = os.path.splitext(filename)
        if ext in ('.dtx', '.ins', '.txt', '.md', '.py', '.tex'):
            normalize_crlf = True
        else:
            normalize_crlf = False

    if arcname is None:
        arcname = filename

    if not normalize_crlf:
        print("\tPacking: {} ---> {}".format(filename, arcname))
        zip_file.write(filename, arcname=arcname)
    else:
        print("\tPacking: {} ---> {} (normalized line endings)".format(filename, arcname))
        contents = StringIO(newline='\n')
        with open(filename, 'r') as f:
            for line in f:
                contents.write(line.decode('utf-8'))
        zip_file.writestr(
            arcname,
            contents.getvalue()
        )

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
            '{}.dtx'.format(style_name),
            '{}.ins'.format(style_name),
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
            write_to_zip(tds_zip, what, arcname=os.path.join(*where + [what]))

        print("\n\n\n")
        return self

    def build_ctan_zip(self):
        print("Building: {}.zip".format(self.style_name))
        ctan_zip = zipfile.ZipFile('{}.zip'.format(self.style_name), 'w')

        for what in self.ctan_manifest:
            assert os.path.isfile(what)
            write_to_zip(ctan_zip, what, arcname=os.path.join(self.style_name, what))

        print("\n\n\n")
        return self

    def install(self):
        for what, where in self.manifest.items():
            assert os.path.isfile(what)
            copy_to_tex(what, where)

        # Make sure to run texhash if we're not using MikTeX.
        if not is_miktek():
            print("Rehashing...")
            texhash = Popen(['texhash'])
            texhash.wait()

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
            builder.build_ctan_zip()

        else:
            assert False
