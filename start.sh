#!/bin/bash
exec gunicorn --bind 0.0.0.0:10000 app:app
