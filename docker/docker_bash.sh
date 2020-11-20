#!/usr/bin/env bash

docker run -d --name keet-postgres -e POSTGRES_PASSWORD=epona27 -e PGDATA=/var/lib/postgresql/data/pgdata -v /custom/mount:/var/lib/postgresql/data postgres

