# Campsite Alert Bot

Planning a last minute vacation to Big Sur, I found myself continously checking the Reserve California website for a campsite availability. I decided to automate the process and built this campsite alert bot. This bot programmatically checks the Reserve California site and sends out a text (via Twilio) if a campsite was found. I ended up getting the campsite! :)

Currently this is hard-coded to Pfieffer Big Sur for 07/26/2019. With a little bit of code modification, you can reconfigure this for your desired park and date.

### Usage
------------
1. Download and clone repo
2. 'pip install -r requirements.txt'
3. Add twilio credentials to a 'config.py' file 
4. Reconfigure to your desired park and date
5. Run main.py

** Instead of manually launching the script everytime, it's best to schedule your tasks with Cron Jobs (Linux,Mac)
  - I scheduled this script to run every hour on a RPiZW