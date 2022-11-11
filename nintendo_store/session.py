from typing import Optional

from requests import Session, Response, RequestException
from requests.auth import AuthBase

from nintendo_store.config import NintendoStoreConfig

URL = 'https://store.nintendo.es/'
USER_AGENT = 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'


def absolute_url(path):
    return  '{}/{}'.format(URL.rstrip('/'), path.lstrip('/'))


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = f"Bearer {self.token}"
        return r


class NintendoStoreSession:
    def __init__(self, username: str, password: str, config: NintendoStoreConfig):
        self.username = username
        self.password = password
        self.initial_referrer = "/"
        self.session = Session()

        self.config = config


    def request(self, path: str, method: str = 'get', json=None, params: Optional[dict] = None, referrer=None,
                validate=True, accept: str= 'application/json', reauthenticate_on_logout: bool = True,
                **kwargs) -> Response:
        referrer = absolute_url(referrer or self.initial_referrer)
        url = absolute_url(path)
        headers = {
            'Referer': referrer,
            'User-Agent': USER_AGENT,
            'Accept': accept,
        }
        response = self.session.request(method, url, json=json, params=params, headers=headers, **kwargs)
        try:
            if validate:
                response.raise_for_status()
        except RequestException as exc:
            response: Optional[Response] = getattr(exc, "response", None)
            if reauthenticate_on_logout and response is not None and response.status_code == 401:
                self.login()
                return self.request(path, method, json, params, referrer, validate, accept, False, **kwargs)
            raise
        return response
