"""Protect the dedicated Vertia nginx location using a pre-generated htpasswd.

Execute only as part of the approved final deployment. Existing unrelated auth
configuration is never overwritten. No credential value is read or printed.
"""
from pathlib import Path

site=Path('/etc/nginx/sites-available/iniciativas-vertia')
password_file=Path('/etc/nginx/vertia-demo.htpasswd')
snippet=Path('/etc/nginx/snippets/iniciativas-vertia-auth.conf')
include='include /etc/nginx/snippets/iniciativas-vertia-auth.conf;'
if not site.is_file() or not password_file.is_file():
    raise SystemExit('Private access prerequisites are missing; aborting.')
text=site.read_text()
if 'auth_basic' in text and include not in text:
    raise SystemExit('Existing authentication configuration requires review; preserved.')
if include not in text:
    marker='location / {'
    if text.count(marker)!=1:
        raise SystemExit('Unexpected site structure; preserved.')
    text=text.replace(marker,marker+'\n        '+include,1)
    site.write_text(text)
snippet.write_text('auth_basic "Vertia - Acceso privado";\nauth_basic_user_file /etc/nginx/vertia-demo.htpasswd;\n')
snippet.chmod(0o644)
print('Private access configured for the dedicated demo site; validate nginx before reload.')
