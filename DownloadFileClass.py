#!/usr/bin/python3


from API_Caller import CallAPI


class Download:

    def __init__(self, Credentials, Syncpoint_ID='', file_id=''):
        self.AppKey = Credentials.AppKey
        self.AccessToken = Credentials.AccessToken
        self.AsUser = Credentials.AsUser
        self.vtoken = str(Syncpoint_ID) + "-" + str(file_id)

    def Download(self):
        Method = "GET"
        url = "retrieveFile.php?vToken=%s" % self.vtoken
        request = CallAPI(url, self.AppKey, self.AccessToken, Method, AdditionalHeaders='', data='', base_url='https://data.syncplicity.com/').MakeRequest()
        open('downloaded_file', 'wb').write(request.content)
        return request
