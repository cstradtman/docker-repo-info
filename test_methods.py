import docker_registry_client.manifest_utils as utils
import docker_registry_client.reposession as repo
__author__ = "Chris Stradtman"
__license__ = "MIT"
__version__ = "1.0"

def test_methods():
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
        assert isinstance(taglist, list)
        manifest = mysession.GetManifest('latest')
        etag = utils.getManifestEtag(manifest)
        assert isinstance(etag, str)

if __name__ == "__main__":
    # execute only if run as a script
    test_methods()