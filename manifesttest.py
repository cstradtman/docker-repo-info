import docker_registry_client.reposession as repo
import docker_registry_client.manifest_utils as utils

requestlist = [
    {"repo": "mcr.microsoft.com", "repopath": "dotnet/core/sdk", "tag": "latest"},
    {"repo": "index.docker.io", "repopath": "library/hello-world", "tag": "latest"},
    # {"repo": "index.docker.io", "repopath": "library/hello-world", "tag": "latest"  #,
    #     "username": "repousername", "password": "repopassword"},
    # {"repo": "index.docker.io", "repopath": "dockeraccountname/privaterepo",
    #    "tag": "latest", "username": "repousername", "rpassword": "repopassword"} #,
    # {"repo": "index.docker.io", "repopath": "cstradtman/test", "tag": "latest"} ##!!!!!!! this one SHOULD fail do to no credentials
]

for request in requestlist:
    print("===================================")
    if "username" in request:
        mysession = repo.RepoSession(
            request["repo"], request["username"], request["password"])
    else:
        mysession = repo.RepoSession(request["repo"])
    mysession.ConnectToRepository(request["repopath"])
    manifest = mysession.GetManifest("latest")
    print("Repo="+request["repo"])
    print("Repo Path="+request["repopath"])
    print("Repo tag="+request["tag"])
    print("")
    print("Etag="+utils.getManifestEtag(manifest))
    print("Type="+utils.getManifestType(manifest))
    print("ApiVersion="+utils.getManifestApiVersion(manifest))
    print("RetrievalDate="+utils.getManifestRetrievalDate(manifest))
    print("SchemaVersion="+str(utils.getManifestSchemaVersion(manifest)))
    print("Name="+utils.getManifestName(manifest))
    print("Tag="+utils.getManifestTag(manifest))
    print("Architecture="+utils.getManifestArchitecture(manifest))
    print("***********************************************************")
    print("")
    print("")
    print("")
