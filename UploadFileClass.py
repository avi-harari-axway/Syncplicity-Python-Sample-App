#!/usr/bin/python3


from API_Caller import CallAPI
import hashlib
import os
import platform
import datetime


class Upload:

    def __init__(self, Credentials, filename=''):
        self.AppKey = Credentials.AppKey
        self.AccessToken = Credentials.AccessToken
        self.AsUser = Credentials.AsUser
        self.filename = filename

    def sha256_checksum(self, block_size=65536):
        sha256 = hashlib.sha256()
        with open(self.filename, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()

    def creation_date(self):
        if platform.system() == 'Windows':
            return datetime.datetime.fromtimestamp(os.path.getctime(self.filename)).isoformat()
        else:
            stat = os.stat(self.filename)
            try:
                return datetime.datetime.fromtimestamp(stat.st_ctime).isoformat()
            except AttributeError:
                return datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()

    def Upload(self, Syncpoint_ID, Path):
        Method = "POST"
        login_headers = {'As-User': '%s' % self.AsUser, "User-Agent": "API_Application", "Content-Range": "0-*/*"}
        files = [('fileData', ('%s' % self.filename, open('%s' % self.filename, 'rb'), 'application/octet-stream')), ('sha256', (None, self.sha256_checksum(), None)), ('sessionKey', (None, 'Bearer ' + self.AccessToken, None)), ('virtualFolderId', (None, '%s' % Syncpoint_ID, None)), ('creationTimeUtc', (None, self.creation_date(), None)), ('lastWriteTimeUtc', (None, datetime.datetime.fromtimestamp(os.path.getmtime(self.filename)).isoformat(), None)), ('fileDone', (None, '', None))]
        url = "saveFile.php?filepath=" + Path
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, login_headers, data='', file=files, base_url="https://data.syncplicity.com/").MakeRequest()
        return request
