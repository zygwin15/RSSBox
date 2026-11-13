#!/bin/sh
set -eu

# Match upstream's cron environment, but replace rather than append each startup.
printenv | grep -Ev '^(BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID)=' > /etc/environment
/opt/venv/bin/python -m scripts.personal_init

if [ "${RSSBOX_RUN_CRON:-1}" = "1" ]; then
    cron -n &
fi

attempt=0
until python -c 'import os,redis; redis.Redis.from_url(os.environ.get("REDIS_URL", "redis://rssbox_redis:6379/0"), socket_connect_timeout=3, socket_timeout=3).ping()' 2>/dev/null; do
    attempt=$((attempt+1))
    if [ "$attempt" -ge 10 ]; then
        echo 'Redis is unavailable; refusing to start RSSBox.' >&2
        exit 1
    fi
    sleep 2
done
exec "$@"
