#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
module: markuman.nextcloud.file_info
short_description: info about files in nextcloud
description:
  - collect informations about files and folders in nextcloud
version_added: "8.0.0"
author:
  - "Markus Bergholz"
requirements:
  - requests python module
options:
  api_token:
    description:
      - Nextcloud App Password.
      - Can also be set as ENV variable.
    required: false
    type: str
    aliases: ['access_token']
  user:
    description:
      - Nextcloud user who (will) owns the file.
      - Can also be set as ENV variable.
    required: false
    type: str
  host:
    description:
      - Nextcloud tld host.
      - Can also be set as ENV variable.
    required: false
    type: str
  mode:
    description:
      - Weather the file should be downloaded (get), uploaded (put) or deleted (delete).
    required: true
    type: str
  source:
    description:
      - file or folder in nextcloud
    required: true
    aliases:
      - src
    type: str
  ssl_mode:
    description:
      - ability to use http:// for integration tests
      - ability to skip ssl verification
      - Possible values `https` (default https), `http` (http), `skip` (https) 
    required: false
    type: str
    default: https
    version_added: 3.0.3
'''

EXAMPLES = '''
    - name: fetch file from nextcloud
      markuman.nextcloud.file_info:
        source: anythingeverything.jpg
'''

from ansible.module_utils.basic import *
from ansible_collections.markuman.nextcloud.plugins.module_utils.nextcloud import NextcloudHandler
import os.path
import hashlib

def write_file(destination, content):
    with open(destination,'wb') as FILE:
        FILE.write(content)

def main():
    module = AnsibleModule(
        argument_spec = dict(
            source = dict(required=True, type='str', aliases=['src']),
            host = dict(required=False, type='str'),
            user = dict(required=False, type='str'),
            api_token = dict(required=False, type='str', no_log=True, aliases=['access_token']),
            ssl_mode = dict(required=False, type='str', default='https', choices=['https', 'http', 'skip'])
        )
    )

    nc = NextcloudHandler(module.params)

    source = module.params.get("source")

  
    change = False
    r = nc.propfind("remote.php/dav/files/{USER}/{SRC}".format(USER=nc.user(), SRC=source))

    if r != {}:
        r['source'] = source

    module.exit_json(changed = change, file_info={'source': r})
    

if __name__ == '__main__':
    main()