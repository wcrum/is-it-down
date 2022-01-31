#!/bin/bash
python3 database-tools.py tables create
python3 database-tools.py import file data/data.txt
python3 worker.py