# -*- coding: utf-8 -*-
# @Author: eromoe|mithril

from __future__ import unicode_literals, absolute_import, print_function

from six import text_type, binary_type
import re
import os
import PixivConfig
import pdb


configfile = 'config.ini'
__config__ = PixivConfig.PixivConfig()
__config__.loadConfig(path=configfile)


def text(string, encodings=['utf8', 'gbk']):
    """
    Make sure string is unicode type, decode with given encoding if it's not.

    If parameter is a object, object.__str__ will been called
    """
    if isinstance(string, text_type):
        return string
    elif isinstance(string, binary_type):
        for encoding in encodings:
            try:
                return string.decode(encoding)
            except UnicodeDecodeError:
                pass
        else:
            raise Exception('Can not decode with %s' % encodings)

    else:
        return text_type(string)


def gen_abs_path(parent, *rel_path):
    return [os.path.join(parent, p) for p in rel_path]

def get_sub_folders(folder):
    try:
        return gen_abs_path(folder, *os.walk(folder).next()[1])
    except StopIteration:
        return []

def get_folder_name(folder):
    return text(os.path.basename(folder))

class StorageManager(object):
    def __init__(self, root, filenameformat=None):
        self.root = root
        self._id2folder = {}
        self._folder2id = {}
        if filenameformat:
            foldername_re = filenameformat.split('\\', 1)[0]
            foldername_re = foldername_re.replace('%member_id%', '(\d+)')
            foldername_re = re.sub(r'%[^%]+%', '.+', foldername_re)
            self.foldername_pt = re.compile(foldername_re)
        else:
            self.foldername_pt = re.compile(r'.+\((\d+)\)$')

        self.refresh()

    def folder2id(self, foldername):
        # pdb.set_trace()
        print('folder2id', foldername)
        m = self.foldername_pt.search(foldername)
        if m:
            return m.group(1)
        else:
            None

    def update(self, foldername=None, id=None):

        if foldername and not id:
            id = self.folder2id(foldername)
            if not id:
                print('%s do not contain id' % foldername)
                return

        if id and not foldername:
            raise Exception('Invalid input')

        self._id2folder[id] = foldername
        self._folder2id[foldername] = id

    def update_foldername_by_id(self, id, foldername):
        pass

    def update_id_by_foldername(self, foldername, id):
        pass

    def artist_folders(self):
        if not self._folder2id:
            self.refresh()

        return self._folder2id.keys()

    def refresh(self):
        folders = get_sub_folders(self.root)
        for x in folders:
            self.update(foldername=get_folder_name(x))

        # can't use pathlib here, it has unicode error when `x.is_dir()`
        # for x in self.root.iterdir():
        #     if x.is_dir():
        #         self.update(foldername=text(x.parts[1]))
        
    def get_foldername_by_artistId(self, id, scan_flag=False):
        if scan_flag:
            self.refresh()

        return self._id2folder.get(str(id))


    def get_artistId_by_foldername(self, foldername):
        return self._folder2id.get(foldername)


# print('##### root dir', __config__.rootDirectory)

storageManager = StorageManager(__config__.rootDirectory, __config__.filenameFormat)


if __name__ == '__main__' :
    storageManager.refresh()
    storageManager.get_artistId_by_foldername(66760)