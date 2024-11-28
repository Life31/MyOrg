import os
import zipfile
def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


zipf = zipfile.ZipFile('static.zip', 'w', zipfile.ZIP_DEFLATED)
zipdir('static', zipf)
zipf.close()
