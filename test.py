__author__ = "Chris Stradtman"
__license__="MIT"
__version__ = "1.0"

import docker_registry_client.reposession as repo
import docker_registry_client.manifest_utils as utils

requestlist = [
    {"repo": "mcr.microsoft.com", "repopath": "dotnet/core/sdk"},
    {"repo": "index.docker.io", "repopath": "library/hello-world"} 
]

for request in requestlist:
    if "username" in request:
        mysession = repo.RepoSession(
            request["repo"], request["username"], request["password"])
    else:
        mysession = repo.RepoSession(request["repo"])
    mysession.ConnectToRepository(request["repopath"])
    taglist = mysession.GetTagList()
    assert isinstance(taglist,list)
    manifest = mysession.GetManifest('latest')
    etag=utils.getManifestEtag(manifest)
    assert isinstance(etag,str)


