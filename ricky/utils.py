# This isn't perfect, but it'll do.

from debian import deb822
from ethel.utils import run_command, tdir, cd

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import datetime as dt
import email.utils
import tarfile
import hashlib
import time
import os


def pool_path(source):
    pfix = ''
    if source.startswith('lib'):
        pfix += source[:4]
    else:
        pfix += source[0]
    pfix += "/" + source
    return pfix


def run(cmd):
    out, err, ret = run_command(cmd)
    if ret != 0:
        print(out, err)
        raise Exception("Stupid")
    return out, err


def fetch_and_upload(dist, source, version):
    from ricky import DEFAULT_MIRROR
    config = configparser.ConfigParser()
    assert config.read(["/etc/ricky.ini"]) != []
    gpg = config.get('config', 'signing-key')

    path = pool_path(source)
    DSC_URL = (
        "http://{mirror}/debian/pool/main/"
        "{path}/{source}_{version}.dsc".format(
            path=path,
            source=source,
            version=version,
            mirror=DEFAULT_MIRROR,
        ))

    with tdir() as pth:
        with cd(pth):
            out, err = run(['dget', '-u', DSC_URL])
            dsc = os.path.basename(DSC_URL)
            changes = write_changes(dsc, dist)
            out, err = run(['debsign', '-k%s' % (gpg), changes])
            out, err = run(['dput', 'debuild', changes])


def file_info(path):
    for algo, name in [
        ('md5', 'Files'),
        ('sha1', 'Checksums-Sha1'),
        ('sha256', 'Checksums-Sha256')
    ]:
        m = getattr(hashlib, algo)()
        buf = open(path, 'rb').read()
        m.update(buf)
        hhash = m.hexdigest()
        fsize = len(buf)
        yield (algo, name, hhash, fsize, path)


def write_changes(fname, dist):
    changes = forge_changes_file(fname, dist)
    path = '{source}_{version}_source.changes'.format(
        source=changes['Source'],
        version=changes['Version']
    )
    changes.dump(fd=open(path, 'wb'))
    return path


def forge_changes_file(fname, dist):
    dsc = deb822.Dsc(open(fname, 'r'))

    changes = deb822.Changes()
    changes['Format'] = '1.8'
    changes['Date'] = email.utils.formatdate(
        time.mktime(dt.datetime.utcnow().timetuple()), usegmt=True
    )

    for key in [
        'Source', 'Version', 'Maintainer',
        'Checksums-Sha1', 'Checksums-Sha256', 'Files'
    ]:
        changes[key] = dsc[key]

    for algo, key, h, s, f in file_info(fname):
        if algo == 'md5':
            algo = 'md5sum'

        entry = deb822.Deb822Dict()
        entry[algo] = h
        entry['size'] = s
        entry['name'] = f

        changes[key].append(entry)

    for entry in changes['Files']:
        entry['section'] = 'not-implemented'
        entry['priority'] = 'not-implemented'

    changes['Distribution'] = dist
    changes['Urgency'] = 'low'
    changes['Changed-By'] = 'Archive Rebuilder <paultag@debian.org>'
    changes['Architecture'] = 'source'
    changes['Binary'] = 'not implemented either'
    changes['Changes'] = """
 {source} ({version}) {dist}; urgency={urgency}
 .
   * This is a fake ChangeLog entry used by ricky to force a rebuild
     on debuild.me.
    """.format(
        source=changes['Source'],
        version=changes['Version'],
        urgency=changes['Urgency'],
        dist=dist,
    )

    changes['Description'] = """This feature is not implemented.
 This is a pretty damn hard to deal with right now. I might write this
 later."""

    return changes
