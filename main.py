import schedule
import time
import subprocess


def run_chatgpt_and_telegram_bots():
    subprocess.run(['sh', 'run_bots.sh'])


def run_hourly_script():
    subprocess.run(['sh', 'run_project.sh'])


run_chatgpt_and_telegram_bots()
schedule.every().hour.do(run_hourly_script)

while True:
    schedule.run_pending()
    time.sleep(1)
