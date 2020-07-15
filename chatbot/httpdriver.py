"""Driver for http/https based web-servers"""

import json

import requests
import urllib3

from chatbot import LOGGER


class HttpDriverException(Exception):
    """Raise this exception when connecting with an HTTP Server"""

    def __init__(self, etype, url, message):
        super().__init__(f'{etype}: ServerURL: {url}\n ERROR: {message}')


class HttpAuthenticationException(Exception):
    """Raise this exception when authentication to http server fails with response code 401"""

    pass


class HttpServerNotFoundException(Exception):
    """Raise this exception when http server not found with response code 404"""

    pass


class HttpDriver:
    """An HttpConnection implementation using the popular requests module.

    Making as generic as possible for connecting to al possible http servers using different
    architectures (SOAP, REST..). Instead of using the get, post methods from request module
    itself we are using the Session object to persist the authentication and session data.
    """

    JSON_HEADERS = {'content-type': 'application/json'}

    def __init__(
        self, host, protocol='http', port=None, auth=None, ssl_verify=False, http_adapter=None
    ):
        """Initialize the connection to an http server

        Args:
            protocol: Protocol to use http/https (str)
            host: a host address/name of the server to connect (str)
            auth: An authentication tuple (username, password) if required or a defined
                  type of authentication (tuple)
            ssl_verify: If the server is on SSL verify certificate or not (bool)
            http_adapter: An adapter for http connection.
        """

        urllib3.disable_warnings()
        self.__protocol = protocol
        self.__host = host
        self.__port = port
        if port:
            self.__base_url = f'{self.__protocol}://{self.__host}:{self.__port}'
        else:
            self.__base_url = f'{self.__protocol}://{self.__host}'
        self.__ssl_verify = ssl_verify
        self.__session = requests.session()
        if auth:
            self.__session.auth = auth
        if http_adapter:
            self.__session.mount(f'{protocol}://', http_adapter)
        self.__session.verify = self.__ssl_verify
        self.__connected = False
        # A default parameter list maintaining for the the request if server always need it,
        # For example in some POST calls, if the server always expects 'ctoken' as a parameter we
        #  can get it and save to default_params, so whenever we make a connection these
        # parameters will be automatically send
        self.__default_params = {}
        # When we create the connection object itself will make sure we can connect to the server
        #  this ensure that we wont go further when the server is not available
        # self.__connect__()
        # self.__session.cookies = None

    @property
    def protocol(self):
        return self.__protocol

    @property
    def host(self):
        return self.__host

    @property
    def base_url(self):
        return self.__base_url

    @base_url.setter
    def base_url(self, base_url):
        self.__base_url = base_url

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port

    @property
    def session(self):
        return self.__session

    @property
    def connected(self):
        return self.__connected

    @property
    def default_params(self):
        return self.__default_params

    @staticmethod
    def __valid_json__(json_var):
        try:
            json.loads(json_var)
        except ValueError as _:
            return False
        return True

    def __connect__(self):
        """Start an HTTP Session to the host, to make sure we can connect to it"""

        try:
            self.Get('', parse_output=False)
            self.__connected = True
        except Exception as e:
            raise HttpDriverException('ConnectionError', self.base_url, str(e))

    def SetDefaultParams(self, params):
        """Set the default params if any

        Args:
            params: Default Parameters to set (dict)
        """

        if params is not None:
            for key, value in params.items():
                self.__default_params[key] = value

    @staticmethod
    def PrettyPrintJson(json_dict):
        """Returns JSON provided in pretty format

        Args:
            json_dict: JSON to convert into pretty format (json)
        """

        return json.dumps(json_dict, sort_keys=True, indent=4)

    def __merge_default_params__(self, params):
        """Merge the given parameters to DefaultParams (private use for HTTP methods)

        Args:
            params: Parameters to merge with default params (dict)
        """

        if params is not None:
            for key, value in self.__default_params.items():
                if key not in params:
                    params[key] = value
            return params
        else:
            return self.__default_params

    @staticmethod
    def GetJsonResponse(response):
        """verify the response code and return json response

        Args:
            response: json response from requests (obj)

        Returns:
            validated json response (json)

        Raises:
            UnknownResponseError if response doesnt have any JSON (HttpDriverException)
        """

        if response.status_code == 200:
            return response.json()
        else:
            raise HttpDriverException(
                'UnknownResponseError', response.url, 'ERROR RESPONSE: %s' % response.status_code
            )

    def Get(self, url, params=None, headers=None, timeout=300, parse_output=True):
        """A wrapper method for sending HTTP GET Requests to the Server

        Args:
            url: A Resource Reference Path to send the request (str)
            params: parameters for the request (dict)
            headers: header information for http requests
            timeout: request timeout value in seconds (int)
            parse_output: parse the JSON output for validity (bool)

        Returns:
            response (object)

        Raises:
            GetRequestError if response doesnt have any JSON (HttpDriverException)
        """

        request_url = self.base_url + url
        params = self.__merge_default_params__(params)
        try:
            response = self.session.get(
                request_url, params=params, headers=headers, timeout=timeout
            )
            LOGGER.debug(f'[GET] Request URL: {response.request.url}')
            LOGGER.debug(f'[GET] Request Headers:\n{response.request.headers}')
            LOGGER.debug(f'[GET] Response Status: {response.status_code}')
            # if parse_output and response.content.decode() is not '' \
            #         and self.__valid_json__(response.text):
            #    LOGGER.debug('[GET] Response Content:\n{}'
            #                 .format(self.PrettyPrintJson(response.json())))
            # if response.status_code == 404:
            #     raise URLRequired('[GET] {} URL path not found !!'.format(request_url))
            return response
        except HttpDriverException as e:
            raise HttpDriverException('[GET] GetRequestError', request_url, str(e))

    def Post(self, url, params=None, data=None, files=None, headers=None, timeout=300):
        """A wrapper method for sending HTTP POST Requests to the Server

        Args:
            url: A Resource Reference Path to send the request (str)
            params: parameters for the request (dict)
            data: payload for the POST request that will be sent either in form-urlencoded encoding
                  if it is a dict, or without any encoding if it is a str. This is to align with the
                  'data' parameter in the underlying session.post() call. (dict or str)
            files: If any file data to be send (obj)
            headers: HTTP Post headers (str)
            timeout: request timeout value in seconds (int)

        Returns:
            response (object)

        Raises:
            PostRequestError if response doesn't have any JSON (HttpDriverException)
        """

        request_url = self.base_url + url
        params = self.__merge_default_params__(params)
        try:
            LOGGER.debug(f'[POST] Payload: {data}')
            response = self.session.post(request_url,
                                         params=params,
                                         data=data,
                                         files=files,
                                         headers=headers,
                                         timeout=timeout,
                                         cookies=self.session.cookies)
            LOGGER.debug(f'[POST] Request URL: {response.request.url}')
            LOGGER.debug(f'[POST] Request Headers:\n{response.request.headers}')
            LOGGER.debug(f'[POST] Response Status: {response.status_code}')
            if response.content.decode() != '':
                if self.__valid_json__(response.text):
                    LOGGER.debug(f'[POST] Response Content:\n'
                                 f'{self.PrettyPrintJson(response.json())}')
                else:
                    LOGGER.debug(f'[POST] Response Content:\n{response.text}')
            return response
        except HttpDriverException as e:
            raise HttpDriverException('PostRequestError', request_url, str(e))

    def Delete(self, url, params=None, data=None, headers=None, timeout=300):
        """A wrapper method for sending HTTP DELETE Requests to the Server

        Args:
            url: A Resource Reference Path to send the request
            params: parameters for the request
            data: payload for the DELETE request, Request will be loading the payload as
                  JSON while sending the call so the format should be in JSON decodable (dict)
            headers: header information for http requests
            timeout: request timeout value in seconds (int)

        Returns:
            response (object)

        Raises:
            DeleteRequestError if response doesnt have any JSON (HttpDriverException)
        """

        request_url = self.base_url + url
        params = self.__merge_default_params__(params)
        try:
            response = self.session.delete(request_url, params=params, json=data,
                                           headers=headers, timeout=timeout)
            return response
        except HttpDriverException as e:
            raise HttpDriverException('DeleteRequestError', request_url, str(e))

    def Put(self, url, params=None, data=None, files=None, headers=None, timeout=300):
        """A wrapper method for sending HTTP PUT Requests to the Server

        Args:
            url: A Resource Reference Path to send the request
            params: parameters for the request (Dict)
            data: payload for the Put request, Request will be loading the payload as JSON
                  while sending the call so the format should be in JSON decodable (Dict)
            timeout: request timeout value in seconds (int)
            files: If any file data to be send (obj)
            headers: HTTP Post headers (str)

        Returns:
            response (object)

        Raises:
            PutRequestError if response doesnt have any JSON (HttpDriverException)
        """

        request_url = self.base_url + url
        params = self.__merge_default_params__(params)
        try:
            LOGGER.debug(f'[PUT] Payload: {data}')
            response = self.session.put(request_url,
                                        params=params,
                                        data=data,
                                        timeout=timeout,
                                        cookies=self.session.cookies,
                                        headers=headers,
                                        files=files)
            LOGGER.debug(f'[PUT] Request URL: {response.request.url}')
            LOGGER.debug(f'[PUT] Request Headers:\n{response.request.headers}')
            LOGGER.debug(f'[PUT] Response Status: {response.status_code}')
            if response.content.decode() != '':
                if self.__valid_json__(response.text):
                    LOGGER.debug(f'[PUT] Response Content:\n'
                                 f'{self.PrettyPrintJson(response.json())}')
                else:
                    LOGGER.debug(f'[PUT] Response Content:\n{response.text}')
            return response
        except HttpDriverException as e:
            raise HttpDriverException('PutRequestError', request_url, str(e))
