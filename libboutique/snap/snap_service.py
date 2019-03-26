import gi
import os
import json
try:
    gi.require_version("Snapd", 1)
    from gi.repository import Snapd
except:
    pass

class SnapService(object):

    def __init__(self):
        pass

    def _connect(self):
        pass
