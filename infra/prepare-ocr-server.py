"""Add bounded local OCR dependencies without restarting existing applications.

Run remotely as root on the authorized demo VPS. No external AI API credentials
are used; uploaded documents stay in this project's private directory.
"""
from pathlib import Path
import importlib.util
import os
import pwd
import subprocess

ROOT=Path('/home/moai/iniciativas-vertia')
uploads=ROOT/'uploads'
account=pwd.getpwnam('moai')

def run(args, **kw):
    subprocess.run(args,check=True,**kw)

env=os.environ.copy()
env.update(DEBIAN_FRONTEND='noninteractive',NEEDRESTART_MODE='l')
# --no-install-recommends limits installation to the OCR engine and languages.
run(['apt-get','install','-y','--no-install-recommends','tesseract-ocr','tesseract-ocr-spa','tesseract-ocr-eng'],env=env)
run(['sudo','-u','moai',str(ROOT/'.venv/bin/pip'),'install','pypdf>=5,<7','pypdfium2>=4.30,<6','Pillow>=11,<13','python-multipart>=0.0.20,<1'])
uploads.mkdir(mode=0o700,exist_ok=True)
os.chmod(uploads,0o700)
os.chown(uploads,account.pw_uid,account.pw_gid)
private_env=ROOT/'.env'
lines=private_env.read_text().splitlines()
lines=[line for line in lines if not line.startswith('UPLOAD_DIR=')]
lines.append(f'UPLOAD_DIR={uploads}')
private_env.write_text('\n'.join(lines)+'\n')
os.chmod(private_env,0o600)
os.chown(private_env,account.pw_uid,account.pw_gid)
run(['tesseract','--list-langs'])
run(['systemctl','is-active','iniciativas-vertia','nginx','postgresql'])
print('Private uploads directory and non-secret setting prepared. Current service was not restarted.')
