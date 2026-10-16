"""Deploy isolated synthetic demos to the authorized MoAI VPS via known SSH key.

No credentials are copied locally. .env remains private on the VPS. Run this
script from any directory; only this project's files and service are updated.
"""
import argparse
from pathlib import Path
import posixpath
import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[1]
REMOTE = '/home/moai/iniciativas-vertia'

parser = argparse.ArgumentParser()
parser.add_argument('--publish', action='store_true', help='Install NEW service/site after tests pass')
parser.add_argument('--tls', action='store_true', help='Provision certificate for verified demo hostname')
parser.add_argument('--private', action='store_true', help='Activate prepared HTTP Basic authentication for real uploads')
args = parser.parse_args()
if args.private and not args.publish:
    parser.error('--private requires --publish')
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.RejectPolicy())
client.connect('217.196.62.58', username='root', key_filename=str(Path.home()/'.ssh/id_ed25519'), look_for_keys=False, allow_agent=False, timeout=15)
sftp = client.open_sftp()

def mkdir(path):
    try:
        sftp.stat(path)
    except FileNotFoundError:
        mkdir(posixpath.dirname(path))
        sftp.mkdir(path, 0o750)

def tree(relative):
    source = ROOT / relative
    if not source.exists():
        return
    for path in source.rglob('*'):
        if path.is_file() and not any(x in {'__pycache__', '.pytest_cache', '.env', 'node_modules', '.venv'} for x in path.parts):
            target = REMOTE + '/' + path.relative_to(ROOT).as_posix()
            mkdir(posixpath.dirname(target))
            sftp.put(str(path), target)

def run(command, timeout=180):
    _, out, err = client.exec_command(command, timeout=timeout)
    output, error = out.read().decode('utf-8','replace'), err.read().decode('utf-8','replace')
    status = out.channel.recv_exit_status()
    print(output, flush=True)
    if error:
        print(error, flush=True)
    if status:
        raise SystemExit(f'Remote command failed ({status}); deployment stopped.')

for relative in ['backend', 'frontend/dist', 'deliverables']:
    tree(relative)
for name in ['iniciativas-vertia.service','nginx-demo.conf','activate-private-access.py']:
    mkdir(REMOTE+'/infra')
    sftp.put(str(ROOT/'infra'/name), REMOTE+'/infra/'+name)
sftp.close()
# Update only this non-secret setting; never print or retrieve the private env.
run(f"sed -i 's|^PROPOSALS_DIR=.*|PROPOSALS_DIR={REMOTE}/deliverables|' {REMOTE}/.env; chmod 600 {REMOTE}/.env; chown -R moai:moai {REMOTE}/backend {REMOTE}/infra {REMOTE}/frontend {REMOTE}/deliverables; sudo -u moai {REMOTE}/.venv/bin/pip install -q -r {REMOTE}/backend/requirements.txt", 240)
run(f"cd {REMOTE} && set -a && . ./.env && set +a && export TEST_DATABASE_URL=\"$DATABASE_URL\" && sudo -u moai --preserve-env=DATABASE_URL,TEST_DATABASE_URL {REMOTE}/.venv/bin/python -m pytest backend/tests -q", 180)
if args.publish:
    if args.private:
        # Protect existing site before starting a version that accepts uploads.
        run(f'python3 {REMOTE}/infra/activate-private-access.py && nginx -t && systemctl reload nginx')
    # Pre-existing matching files are updated only for this project's service.
    run(f'install -m 644 {REMOTE}/infra/iniciativas-vertia.service /etc/systemd/system/iniciativas-vertia.service && systemctl daemon-reload && systemctl enable --now iniciativas-vertia && systemctl restart iniciativas-vertia')
    run('curl --fail --silent --retry 12 --retry-connrefused --retry-delay 1 http://127.0.0.1:8788/api/health')
    # Preserve TLS configuration inserted by certbot on subsequent deployments.
    run(f"test -f /etc/nginx/sites-available/iniciativas-vertia || install -m 644 {REMOTE}/infra/nginx-demo.conf /etc/nginx/sites-available/iniciativas-vertia; sed -i -E 's/client_max_body_size[[:space:]]+[0-9]+m;/client_max_body_size 16m;/; s/proxy_read_timeout[[:space:]]+[0-9]+s;/proxy_read_timeout 120s;/' /etc/nginx/sites-available/iniciativas-vertia; test -L /etc/nginx/sites-enabled/iniciativas-vertia || ln -s /etc/nginx/sites-available/iniciativas-vertia /etc/nginx/sites-enabled/iniciativas-vertia; nginx -t && systemctl reload nginx")
    if args.tls:
        run('certbot --nginx -d iniciativasvertia.somosmoai.tech --non-interactive --agree-tos --register-unsafely-without-email --redirect', 180)
client.close()
