#!/usr/bin/env python
"""Railway production entrypoint: migrate, collectstatic, then gunicorn."""
import os
import subprocess
import sys


def run(cmd):
    print(f">>> {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, check=True)


def main():
    port = os.getenv('PORT', '8080')
    print(f"=== Dalal Platform Startup (port {port}) ===", flush=True)

    run([sys.executable, 'manage.py', 'migrate', '--noinput'])
    run([sys.executable, 'manage.py', 'collectstatic', '--noinput'])

    # Read workers and log level from environment
    workers = os.getenv('GUNICORN_WORKERS', '1')
    log_level = os.getenv('GUNICORN_LOG_LEVEL', 'info')
    timeout = os.getenv('GUNICORN_TIMEOUT', '120')

    print(f"Starting gunicorn with workers={workers}, log_level={log_level}, timeout={timeout}", flush=True)

    os.execvp(
        'gunicorn',
        [
            'gunicorn',
            'dalal_project.wsgi:application',
            '--bind', f'0.0.0.0:{port}',
            '--workers', workers,
            '--timeout', timeout,
            '--log-level', log_level,
            '--access-logfile', '-',
            '--error-logfile', '-',
        ],
    )


if __name__ == '__main__':
    main()

