#!/usr/bin/env bash

cd ~/Documents/IceStream/log_analysis
/home/ubuntu/anaconda3/bin/python -m main >> ./logs/cron.log 2>&1

