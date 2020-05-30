from requests.auth import HTTPBasicAuth
import requests
import pprint
import os
import logging
import json
__author__ = "Chris Stradtman"
__license__ = "MIT"
__version__ = "1.0"


# From: https://stackoverflow.com/questions/10588644/how-can-i-see-the-entire-http-request-thats-being-sent-by-my-python-application
# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
if os.environ.get("LOGLEVEL") == "DEBUG":
    http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.propagate = True
log = logging.getLogger(__name__)


class RepoSession:
    """ 
    A class use to create a session to a docker repository
    ...

    Attributes
    ----------
    username : str (optional)
        username for authenticated public and private repositories
    password : str (optional)
        password for authenticated public and private repositories

     Methods
        -------
        ConnectToRepository(repository)
            Creates connection to repository
        GetTagList()
            Retrieves Tag list for repo
        GetManifest(tag)
            Retrieves select header and body information for Manifest described by "tag"
    """

    # From https://docs.docker.com/registry/spec/auth/token/
    def __init__(self, registry_base, username=None, password=None):
        """
        Parameters
        ----------
        username : str (optional)
            username for authenticated public and private repositories
        password : str (optional)
            password for authenticated public and private repositories       
        """

        self.username = username
        self.password = password
        # 1 Attempt to begin a push/pull operation with the registry.
        self.registry_url = "https://" + registry_base + "/v2/"
        ####### from https://docs.docker.com/registry/spec/auth/token/ ########
        # The token server should first attempt to authenticate the client
        # using any authentication credentials provided with the request
        if username:
            paramdict = {"account": username}
            response_one = requests.get(self.registry_url, auth=(
                username, password), params=paramdict)
        else:
            response_one = requests.get(self.registry_url)
        logging.debug(pprint.pformat(response_one.json()))
        if response_one.status_code == 200:
            logging.info("initial query successful without authorization")
        elif response_one.status_code == 401:
            # 2 If the registry requires authorization it will return a 401 Unauthorized HTTP response with information on how to authenticate.
            self.bearerinfodict = {}
            bearerinfo = response_one.headers["WWW-Authenticate"]
            bearerinfolist = bearerinfo.split(',')
            for item in bearerinfolist:
                fields = item.split("=")
                self.bearerinfodict[fields[0]] = fields[1].strip("\"")
        else:
            logging.error("Bad initial registry query response=" +
                          str(response_one.status_code))
            logging.error(pprint.pformat(response_one.headers))
            logging.error(pprint.pformat(response_one.url))
            logging.error(pprint.pprint(response_one.json()))
            raise Exception("invalid intial request response=")

    def ConnectToRepository(self, repository):
        """
        Parameters
        ----------
        repository : str 
            hostname for repository (example: index.docker.io)
        """

        logging.debug("Connecting to repository")
        self.repository = repository
        paramdict = {}
        paramdict["scope"] = "repository:" + repository + ":pull"
        if hasattr(self, 'bearerinfodict'):
            paramdict["service"] = self.bearerinfodict["service"]
        if self.username:
            paramdict["account"] = self.username
        self.session = requests.Session()
        self.session.params.update(paramdict)

        # 3 The registry client makes a request to the authorization service for a Bearer token.
        if self.username and self.bearerinfodict:
            #self.session.auth = (self.username, self.password)
            token_response = requests.get(self.bearerinfodict["Bearer realm"], auth=(
                self.username, self.password), params=paramdict)
        elif hasattr(self, 'bearerinfodict'):
            # if self.bearerinfodict:
            token_response = requests.get(
                self.bearerinfodict["Bearer realm"], params=paramdict)
        else:
            return
        body = token_response.json()
        logging.debug(pprint.pformat(body))
        # 4 The authorization service returns an opaque Bearer token representing the client’s authorized access.
        self.session.headers.update(
            {'Authorization': 'Bearer ' + body["token"]})

    def GetTagList(self):
        """
        Parameters
        ----------
        None
        """
        # get list of tags
        # 5 The client retries the original request with the Bearer token embedded in the request’s Authorization header.
        # 6 The Registry authorizes the client by validating the Bearer token and the claim set embedded within it and begins the push/pull session as usual.
        logging.debug("Getting TagList")
        TagListResponse = self.session.get(
            self.registry_url+self.repository+"/tags/list")
        if TagListResponse.status_code == 200:
            logging.debug(pprint.pformat(TagListResponse.json()))
            return TagListResponse.json()["tags"]
        else:
            logging.error("Bad TagList Respose from registry=" +
                          str(TagListResponse.status_code))
            logging.error(pprint.pformat(TagListResponse.headers))
            logging.error(pprint.pformat(TagListResponse.url))
            logging.error(pprint.pprint(TagListResponse.json()))
            raise Exception("invalid tag list response")

    def GetManifest(self, tag):
        """
        Parameters
        ----------
        tag : str 
            Manifest tag for repo
        """
        logging.debug("Getting Manifest")
        # get list of manifest information
        ManifestResponse = self.session.get(
            self.registry_url+self.repository+"/manifests/"+tag)
        if ManifestResponse.status_code == 200:
            logging.debug(pprint.pformat(ManifestResponse.json()))
            fullResponse = ManifestResponse.headers
            del fullResponse["Strict-Transport-Security"]
            del fullResponse["Docker-Content-Digest"]
            fullResponse["manifest"] = ManifestResponse.json()
            return fullResponse
        else:
            logging.error(str(ManifestResponse.status_code))
            logging.error(pprint.pformat(ManifestResponse.headers))
            logging.error(pprint.pformat(ManifestResponse.url))
            logging.error(pprint.pprint(ManifestResponse.json()))
            raise Exception("invalid Manifest response")
