#!/bin/bash

set -e

cmd="$@"

echo "Starting the Python application..."

uwsgi --ini uwsgi.ini

echo "Python application has started."