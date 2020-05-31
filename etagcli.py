import docker_registry_client.manifest_utils as utils
import docker_registry_client.reposession as repo
import sys

__author__ = "Chris Stradtman"
__license__ = "MIT"
__version__ = "1.0"

if len(sys.argv) == 4 or len(sys.argv) == 6:
    request={}
    request["repo"] = sys.argv[1]
    request["repopath"] = sys.argv[2]
    request["tag"] = sys.argv[3]
    if len(sys.argv) == 5:
        request["username"] = sys.argv[4]
        request["password"] = sys.argv[5]
else:
    print("Usage: etagcli.py repo repopath tag [username password]")
    print("Example: etagcli.py index.docker.io library/hello-world latest")
    print("")
    print("repo=repo FQDN")
    print("repopath=path to actual container repository inside repo")
    print("tag=tag assigned to the container of interest")
    print("username=repo username credential (optional)")
    print("password=repo password credential (optional)")
    exit()


if "username" in request:
    mysession = repo.RepoSession(
        request["repo"], request["username"], request["password"])
else:
    mysession = repo.RepoSession(request["repo"])
mysession.ConnectToRepository(request["repopath"])
etag = mysession.GetManifestHead(request["tag"])["Etag"].strip("\"")
print(etag)