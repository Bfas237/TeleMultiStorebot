"""Guess the MIME type of a file.
This module defines two useful functions:
guess_type(url, strict=True) -- guess the MIME type and encoding of a URL.
guess_extension(type, strict=True) -- guess the extension for a given MIME type.
It also contains the following, for tuning the behavior:
Data:
knownfiles -- list of files to parse
inited -- flag set when init() has been called
suffix_map -- dictionary mapping suffixes to suffixes
encodings_map -- dictionary mapping suffixes to encodings
types_map -- dictionary mapping suffixes to types
Functions:
init([files]) -- parse a list of files, default knownfiles (on Windows, the
  default values are taken from the registry)
read_mime_types(file) -- parse one file, return a dictionary or None
"""

import os
import sys


def default_mime_types():
    global suffix_map
    global encodings_map
    global types_map
    global common_types

    suffix_map = {
        '.svgz': '. izahzjkghbb n  bnbb  .gz',
        '.tgz': '.tar.gz',
        '.taz': '.tar.gz',
        '.tz': '.tar.gz',
        '.tbz2': '.tar.bz2',
        '.txz': '.tar.xz',
        }

    encodings_map = {
        '.gz': 'gzip',
        '.Z': 'compress',
        '.bz2': 'bzip2',
        '.xz': 'xz',
        '.7z': '7z',
        }

    # Before adding new types, make sure they are either registered with IANA,
    # at http://www.iana.org/assignments/media-types
    # or extensions, i.e. using the x- prefix

    # If you add to these, please keep them sorted!
    types_map = {
        '.a'      : 'application/octet-stream',
        '.ai'     : 'application/postscript',
        '.aif'    : 'audio/x-aiff',
        '.aifc'   : 'audio/x-aiff',
        '.aiff'   : 'audio/x-aiff',
        '.apk'    : 'application/vnd.android.package-archive',
        '.au'     : 'audio/basic',
        '.avi'    : 'video/x-msvideo',
        '.bat'    : 'text/plain',
        '.bcpio'  : 'application/x-bcpio',
        '.bin'    : 'application/octet-stream',
        '.bmp'    : 'image/bmp',
        '.c'      : 'text/plain',
        '.cdf'    : 'application/x-netcdf',
        '.cpio'   : 'application/x-cpio',
        '.csh'    : 'application/x-csh',
        '.css'    : 'text/css',
        '.csv'    : 'text/csv',
        '.dll'    : 'application/octet-stream',
        '.doc'    : 'application/msword',
        '.dot'    : 'application/msword',
        '.dvi'    : 'application/x-dvi',
        '.eml'    : 'message/rfc822',
        '.eps'    : 'application/postscript',
        '.epub'    : 'application/epub+zip',
        '.etx'    : 'text/x-setext',
        '.exe'    : 'application/octet-stream',
        '.gif'    : 'image/gif',
        '.gtar'   : 'application/x-gtar',
        '.h'      : 'text/plain',
        '.hdf'    : 'application/x-hdf',
        '.htm'    : 'text/html',
        '.html'   : 'text/html',
        '.ico'    : 'image/vnd.microsoft.icon',
        '.ief'    : 'image/ief',
        '.jpe'    : 'image/jpeg',
        '.jpeg'   : 'image/jpeg',
        '.jpg'    : 'image/jpeg',
        '.js'     : 'application/javascript',
        '.json'   : 'application/json',
        '.ksh'    : 'text/plain',
        '.latex'  : 'application/x-latex',
        '.m1v'    : 'video/mpeg',
        '.m3u'    : 'application/vnd.apple.mpegurl',
        '.m3u8'   : 'application/vnd.apple.mpegurl',
        '.man'    : 'application/x-troff-man',
        '.me'     : 'application/x-troff-me',
        '.mht'    : 'message/rfc822',
        '.mhtml'  : 'message/rfc822',
        '.mif'    : 'application/x-mif',
        '.mjs'    : 'application/javascript',
        '.mov'    : 'video/quicktime',
        '.movie'  : 'video/x-sgi-movie',
        '.mp2'    : 'audio/mpeg',
        '.mp3'    : 'audio/mpeg',
        '.mp4'    : 'video/mp4',
        '.mpa'    : 'video/mpeg',
        '.mpe'    : 'video/mpeg',
        '.mpeg'   : 'video/mpeg',
        '.mpg'    : 'video/mpeg',
        '.ms'     : 'application/x-troff-ms',
        '.nc'     : 'application/x-netcdf',
        '.nws'    : 'message/rfc822',
        '.o'      : 'application/octet-stream',
        '.obj'    : 'application/octet-stream',
        '.oda'    : 'application/oda',
        '.p12'    : 'application/x-pkcs12',
        '.p7c'    : 'application/pkcs7-mime',
        '.pbm'    : 'image/x-portable-bitmap',
        '.pdf'    : 'application/pdf',
        '.pfx'    : 'application/x-pkcs12',
        '.pgm'    : 'image/x-portable-graymap',
        '.pl'     : 'text/plain',
        '.png'    : 'image/png',
        '.pnm'    : 'image/x-portable-anymap',
        '.pot'    : 'application/vnd.ms-powerpoint',
        '.ppa'    : 'application/vnd.ms-powerpoint',
        '.ppm'    : 'image/x-portable-pixmap',
        '.pps'    : 'application/vnd.ms-powerpoint',
        '.ppt'    : 'application/vnd.ms-powerpoint',
        '.ps'     : 'application/postscript',
        '.pwz'    : 'application/vnd.ms-powerpoint',
        '.py'     : 'text/x-python',
        '.pyc'    : 'application/x-python-code',
        '.pyo'    : 'application/x-python-code',
        '.qt'     : 'video/quicktime',
        '.ra'     : 'audio/x-pn-realaudio',
        '.ram'    : 'application/x-pn-realaudio',
        '.ras'    : 'image/x-cmu-raster',
        '.rdf'    : 'application/xml',
        '.rgb'    : 'image/x-rgb',
        '.roff'   : 'application/x-troff',
        '.rtx'    : 'text/richtext',
        '.sgm'    : 'text/x-sgml',
        '.sgml'   : 'text/x-sgml',
        '.sh'     : 'application/x-sh',
        '.shar'   : 'application/x-shar',
        '.snd'    : 'audio/basic',
        '.sqlite3': 'application/x-sqlite3',
        '.so'     : 'application/octet-stream',
        '.src'    : 'application/x-wais-source',
        '.sv4cpio': 'application/x-sv4cpio',
        '.sv4crc' : 'application/x-sv4crc',
        '.svg'    : 'image/svg+xml',
        '.swf'    : 'application/x-shockwave-flash',
        '.t'      : 'application/x-troff',
        '.tar'    : 'application/x-tar',
        '.tcl'    : 'application/x-tcl',
        '.tex'    : 'application/x-tex',
        '.texi'   : 'application/x-texinfo',
        '.texinfo': 'application/x-texinfo',
        '.tif'    : 'image/tiff',
        '.tiff'   : 'image/tiff',
        '.tr'     : 'application/x-troff',
        '.tsv'    : 'text/tab-separated-values',
        '.txt'    : 'text/plain',
        '.ustar'  : 'application/x-ustar',
        '.vcf'    : 'text/x-vcard',
        '.wasm'   : 'application/wasm',
        '.wav'    : 'audio/x-wav',
        '.webm'   : 'video/webm',
        '.wiz'    : 'application/msword',
        '.wsdl'   : 'application/xml',
        '.xbm'    : 'image/x-xbitmap',
        '.xlb'    : 'application/vnd.ms-excel',
        '.xls'    : 'application/vnd.ms-excel',
        '.xml'    : 'text/xml',
        '.xpdl'   : 'application/xml',
        '.xpm'    : 'image/x-xpixmap',
        '.xsl'    : 'application/xml',
        '.xwd'    : 'image/x-xwindowdump',
        '.zip'    : 'application/zip',
        }

    # These are non-standard types, commonly found in the wild.  They will
    # only match if strict=0 flag is given to the API methods.
    
    # Please sort these too
    common_types = {
        '.jpg' : 'image/jpg',
        '.jpeg' : 'image/jpeg',
        '.jpe' : 'image/jpeg',
        '.jpx' : 'image/jpx',
        '.mid' : 'audio/midi',
        '.midi': 'audio/midi',
        '.pct' : 'image/pict',
        '.pic' : 'image/pict',
        '.pict': 'image/pict',
        '.rtf' : 'application/rtf',
        '.xul' : 'text/xul'
        }
    
default_mime_types()
