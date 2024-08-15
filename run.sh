#!/bin/bash
echo "sm-updater init"
rm -vfr sm-updater
rm -vfr src/sm-updater.*
rm -vfr src/sm_updater.*
python3 -m venv sm-updater
source sm-updater/bin/activate
pip install -e .
python main.py
deactivate
echo "sm-updater end"
