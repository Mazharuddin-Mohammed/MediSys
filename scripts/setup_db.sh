#!/bin/bash
psql -U postgres -c "CREATE DATABASE medisys;"
psql -U postgres -d medisys -f src/backend/core/database/schema.sql