# Personal RSSBox fork

This fork keeps upstream bug fixes and adds opt-in features for our local deployment.
The upstream project currently accepts bug fixes rather than new features.

- `main` tracks `versun/RSSBox:main` with fast-forward updates only.
- `personal` is the deployment branch, starting with YouTube caption support.
- Build feature branches from `personal` and merge tested changes back there.
- Build upstream bug-fix branches from `upstream/main`, so upstream PRs contain only
  the fix. Cherry-pick those fixes onto `personal` as needed; reconcile once upstream
  merges them. Do not force-push shared deployment branches.

## Local container builds

```sh
git fetch upstream main
git switch main
git merge --ff-only upstream/main
git push origin main
git switch personal
git merge main
```

Resolve integration and migration conflicts, then run the tests and a migration
rehearsal using a copy of the production database before deployment. Keep `main`
free of personal features. Pin the upstream commit used for each release and record
the personal branch commit in the image tag and OCI revision label.

```sh
docker build -f Dockerfile.personal --build-arg REVISION=<full-commit> -t local/rssbox:<full-commit> .
```

`Dockerfile.personal` reuses the pinned upstream runtime for Python/OS tools, installs
Python dependencies from `uv.lock`, and replaces the application with this checkout.
The personal entrypoint applies committed migrations and stops on initialization
failure. It does not generate migrations at startup. `RSSBOX_RUN_CRON=0` disables
scheduled work for isolated migration rehearsals; production defaults to enabled.

The local deployment harness and private backups are maintained outside this source
checkout under `/home/ianzhao/rssbox/fork`. No databases, credentials, backups, or
machine-specific Compose configuration belong in the GitHub fork. Back up the live
SQLite database with the app stopped before changing images. Restoring a pre-upgrade
database rolls back writes made after that backup; preserve a fresh snapshot first
if later data needs to be recovered.

See [YouTube captions](youtube-captions.md) for the opt-in feature settings. Existing
Windmill YouTube processing can continue independently; enabling this feature does
not automatically migrate its feeds or caches.
