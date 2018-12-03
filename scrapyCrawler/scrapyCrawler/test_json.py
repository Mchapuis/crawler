import json
#from Py.QtCore import QLibraryInfo

paths = [x for x in dir(QLibraryInfo) if x.endswith('Path')]
location = {x: QLibraryInfo.location(getattr(QLibraryInfo, x))
            for x in paths}
try:
    version = QLibraryInfo.version().segments()
except AttributeError:
    version = None
print(str(json.dumps({
    'isDebugBuild': QLibraryInfo.isDebugBuild(),
    'version': version,
    'location': location,
})))