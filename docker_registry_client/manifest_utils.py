"""Utilities for use with the manifest structure returned by GetManifest
"""

__author__ = "Chris Stradtman"
__license__ = "MIT"
__version__ = "1.0"


def getManifestEtag(manifest):
    """ returns Etag hash for manifest"""
    return manifest["Etag"]


def getManifestType(manifest):
    """ returns manifest type for manifest"""
    return manifest["Content-Type"]


def getManifestApiVersion(manifest):
    """ returns Api Version for for manifest"""
    return manifest["Docker-Distribution-Api-Version"]


def getManifestRetrievalDate(manifest):
    """ returns datestring of data retrieval for manifest"""
    return manifest["Date"]


def getManifestSchemaVersion(manifest):
    """ returns manifest schema version for manifest"""
    return manifest["manifest"]["schemaVersion"]


def getManifestName(manifest):
    """ returns name of manifest"""
    return manifest["manifest"]["name"]


def getManifestTag(manifest):
    """ returns tag for manifest"""
    return manifest["manifest"]["tag"]


def getManifestArchitecture(manifest):
    """ returns system architecture for manifest"""
    return manifest["manifest"]["architecture"]


def getManifestFsLayers(manifest):
    """ returns hashes pointing to layers for manifest"""
    return manifest["manifest"]["fsLayers"]


def getManifestHistory(manifest):
    """ returns hist for manifest raw data unparsed"""
    return manifest["manifest"]["history"]


def getManifestSignatures(manifest):
    """ returns signature for manifest unparsed"""
    return manifest["manifest"]["signatures"]
