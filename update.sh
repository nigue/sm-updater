#!/bin/bash
echo "sm-updater update"
rm -fr sm-updater main.py run.sh setup.py src update.sh
unzip -P qwer sm-updater.zip
rm sm-updater.zip
echo "sm-updater updated"