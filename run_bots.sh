#!/bin/sh
python3 spiders/myspider1.py
python3 data_processing/Ready_posts/send2tg.py
python3 data_processing/process_data.py
