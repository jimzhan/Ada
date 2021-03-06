# -*- coding: utf-8 -*-
"""
Functions that interact with local file system.
"""
from __future__ import with_statement

import os
import shutil
import logging
import itertools

from rex.core import regex


logger = logging.getLogger(__name__)

#==========================================================================================
#   General/Common Properties
#==========================================================================================
sysroot = os.path.abspath('/')
userdir = os.path.expanduser('~')



def realpath(path):
    """
    Create the real absolute path for the given path.

    Add supports for userdir & / supports.

    Args:
        * path: pathname to use for realpath.

    Returns:
        Platform independent real absolute path.
    """
    if path == '~':
        return userdir

    if path == '/':
        return sysroot

    if path.startswith('/'):
        return os.path.abspath(path)

    if path.startswith('~/'):
        return os.path.expanduser(path)

    if path.startswith('./'):
        return os.path.abspath(os.path.join(os.path.curdir, path[2:]))

    return os.path.abspath(path)



def find(pattern, path=os.path.curdir, recursive=False):
    """
    Find absolute file/folder paths with the given ``re`` pattern.

    Args:
        * pattern: search pattern, support both string (exact match) and `re` pattern.
        * path: root path to start searching, default is current working directory.
        * recursive: whether to recursively find the matched items from `path`, False by default

    Returns:
        Generator of the matched items of Files/Folders.
    """
    root = realpath(path)

    Finder = lambda item: regex.is_regex(pattern) \
                    and pattern.match(item) or (pattern == item)

    if recursive:
        for base, dirs, files in os.walk(root, topdown=True):
            for segment in itertools.chain(filter(Finder, files), filter(Finder, dirs)):
                yield FS(os.path.join(base, segment))

    else:
        for segment in filter(Finder, os.listdir(root)):
            yield(os.path.join(root, segment))



class FS(object):
    """
    Generic file system object.

    Attributes:
        * path: absolute path of the file system object.
    """
    def __init__(self, path, *args, **kwargs):
        self.path = realpath(path)


    def __unicode__(self):
        return self.path


    def __repr__(self):
        return self.path


    @property
    def exists(self):
        return os.path.exists(self.path)


    @property
    def name(self):
        return os.path.basename(self.path)


    def copy(self, dest):
        """
        Copy item to the given `dest` path.

        Args:
            * dest: destination path to copy.
        """
        if os.path.isfile(self.path):
            shutil.copy2(self.path, dest)
        else:
            shutil.copytree(self.path, dest, symlinks=False, ignore=None)


    def create(self):
        """
        Create item under file system with its path.

        Returns:
            True if its path does not exist, False otherwise.
        """
        if os.path.isfile(self.path):
            if not os.path.exists(self.path):
                with open(self.path, 'w') as fileobj:
                    fileobj.write('')
        else:
            os.makedirs(self.path)


    def delete(self):
        """
        Delete the file/folder itself from file system.
        """
        if os.path.isfile(self.path):
            os.remove(self.path)
        else:
            shutil.rmtree(self.path)


    def move(self, dest):
        """
        Move item to the given `dest` path.

        Args:
            * dest: destination path to move.
        """
        shutil.move(self.path, dest)


    def flush(self):
        """
        Commit the marked action, against `revert`.
        """
        raise NotImplementedError


    def revert(self):
        """
        Revert the last action.
        """
        raise NotImplementedError



class File(FS):

    def create(self):
        """
        Create item under file system with its path.

        Returns:
            True if its path does not exist, False otherwise.
        """
        if not os.path.exists(self.path):
            with open(self.path, 'w') as fileobj:
                fileobj.write('')


class Folder(FS):

    def create(self):
        """
        Recursively create the folder using its path.
        """
        os.makedirs(self.path)
