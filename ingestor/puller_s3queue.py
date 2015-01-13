#!/usr/bin/env python

import sys
import os
import argparse
import requests

import l8_lib

def build_url(scene_root):
    return 'https://s3-us-west-2.amazonaws.com/landsat-pds/tarq/%s.tar.gz' % (
        scene_root)

def pull(scene_root, scene_dict, verbose=False):
    filename = scene_root + '.tar.gz'

    url = build_url(scene_root)
    if verbose:
        print 'Fetching:', url

    rv = requests.get(url, stream=True)
    rv.raise_for_status()

    with open(filename, 'wb') as f:
        for d in rv.iter_content(chunk_size=1024 * 1024 * 10):
            if d:
                f.write(d)
                if verbose:
                    sys.stdout.write('.')
                    sys.stdout.flush()

    if verbose:
        sys.stdout.write('\n')

    # Confirm this is really a .gz file, not an http error or something.
    if open(filename).read(2) != '\037\213':
        raise Exception('%s does not appear to be a .gz file' % filename)

    if verbose:
        print '%s successfully downloaded (%d bytes)' % (
            filename, os.path.getsize(filename))

    if scene_dict is not None:
        scene_dict['src_url'] = url
        scene_dict['src_md5sum'] = l8_lib.get_file_md5sum(filename)
        
    return filename
