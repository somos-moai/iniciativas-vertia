"""Generate private demo HTTP credentials remotely, without printing secrets.

Preparation only: nginx authentication is activated by a later deployment.
"""
from pathlib import Path
import crypt
import grp
import json
import os
import secrets
import string

root=Path('/root/.config/iniciativas-vertia')
root.mkdir(mode=0o700,parents=True,exist_ok=True)
os.chmod(root,0o700)
access=root/'http-access.json'
if access.exists():
    record=json.loads(access.read_text())
else:
    password=''.join(secrets.choice(string.ascii_letters+string.digits) for _ in range(20))
    record={'url':'https://iniciativasvertia.somosmoai.tech','username':'vertia','password':password}
    access.write_text(json.dumps(record))
    os.chmod(access,0o600)
htpasswd=Path('/etc/nginx/vertia-demo.htpasswd')
if not htpasswd.exists():
    htpasswd.write_text(record['username']+':'+crypt.crypt(record['password'],crypt.mksalt(crypt.METHOD_SHA512))+'\n')
    os.chmod(htpasswd,0o640)
    os.chown(htpasswd,0,grp.getgrnam('www-data').gr_gid)
print('Private access prepared; authentication not activated.')
