# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from utils.cutom_exception import RequestFailException, AuthenticationFailureException
from utils.file_utils import get_api_public_key

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


class CheckStatusCode:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        if 'timeout' not in kwargs:
            kwargs["timeout"] = 5
        need_raw_content = kwargs.pop("need_raw_content", False)
        # print("upload", kwargs)
        result = self.func(*args, **kwargs)
        if result.status_code == 401:
            raise AuthenticationFailureException("authentication failed")
        elif result.status_code // 100 == 5 or result.status_code // 100 == 4:
            # TODO： 结果中含有中文不知何种编码
            error_message = {"status_code": result.status_code, "reason": result.content.decode("utf-8")}
            raise RequestFailException(error_message)
        else:
            if need_raw_content:
                return result.content
            return result.json()


class CustomSession(object):
    def __init__(self):
        self.session = requests_retry_session()
        self.get = CheckStatusCode(self.session.get)
        self.put = CheckStatusCode(self.session.put)
        self.post = CheckStatusCode(self.session.post)
        self.delete = CheckStatusCode(self.session.delete)
        self.options = CheckStatusCode(self.session.options)


class RequestHandler:

    def __init__(self):
        self.session = CustomSession()
        self.host = 'https://api.remove.bg/v1.0/removebg'

    def remove_bg(self, file_path):
        files = {'image_file': open(file_path, 'rb')}
        data = {'size': 'auto'}
        headers = {'X-Api-Key': get_api_public_key()}
        return self.session.post(self.host, files=files, data=data, headers=headers, need_raw_content=True)


def main():
    pass


if __name__ == "__main__":
    main()
