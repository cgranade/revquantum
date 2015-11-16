#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os, sys, shutil

MANIFEST = [
    'templates/revquantum.latex'
]

DIR_STRUCTURE = set([''] + [
    os.path.dirname(filename)
    for filename in MANIFEST
])

if __name__ == "__main__":
    # Find what OS we're running on and use that to define
    # the data-dir for Pandoc.
    data_dir = os.path.expanduser(
        os.path.join("~", ".pandoc")
        if sys.platform in ('linux2', 'darwin', 'cygwin')
        else
        os.path.join("~", "AppData", "Roaming", "pandoc")
        if sys.platform in ('win32', )
        else
        None
    )

    # Ensure that the directory structure exists.
    for dirname in DIR_STRUCTURE:
        try:
            os.makedirs(os.path.join(data_dir, dirname))
            print("Created {}".format(os.path.join(data_dir, dirname)))
        except:
            pass

    for filename in MANIFEST:
        src = os.path.join(os.path.dirname(__file__), filename)
        dest = os.path.join(data_dir, filename)
        print("{} → {}".format(filename, dest))
        shutil.copyfile(
            src, dest
        )

    print(
        "\n"
        "Pandoc template installed sucessfully. To use the new template, run "
        "with the '--template=revquantum' option."
        "\n"
    )