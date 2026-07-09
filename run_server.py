#!/usr/bin/env python
"""
Railway production entrypoint.
Runs migrations, collects static files, then starts gunicorn.
"""
import os
import subprocess
import sys


def run(cmd):
    """Run a command and exit if it fails."""
    print(f">>> {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, check=True)


def main():
    port = os.getenv('PORT', '8080')
    print(f"=== Dalal Platform Startup (port {port}) ===", flush=True)

    # Run migrations
    run([sys.executable, 'manage.py', 'migrate', '--noinput'])

    # Collect static files
    run([sys.executable, 'manage.py', 'collectstatic', '--noinput'])

    # Read gunicorn configuration from environment
    workers = os.getenv('GUNICORN_WORKERS', '1')
    log_level = os.getenv('GUNICORN_LOG_LEVEL', 'info')
    timeout = os.getenv('GUNICORN_TIMEOUT', '120')

    print(f"Starting gunicorn with workers={workers}, log_level={log_level}, timeout={timeout}", flush=True)

    # Start gunicorn
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

