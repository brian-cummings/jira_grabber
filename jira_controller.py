import datetime
import pytz
import math
import get_jira_issues
import jira_model
import get_jira_worklog
import argparse
import logging
from logging.handlers import TimedRotatingFileHandler

log_file = "../logs/jira.log"
logger = logging.getLogger("jiraLogger")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler(log_file, when="D", interval=1, backupCount=7)
handler.doRollover()
logger.addHandler(handler)

parser = argparse.ArgumentParser(__file__)
parser.add_argument('-t',metavar='hours', dest='hours', help='Time in hours to retrieve', type=int)
parser.add_argument('-i',metavar='issue key', dest='issue_key', help='Jira issue key', type=str)
args = parser.parse_args()
user_hours = args.hours
user_issue_key = args.issue_key

utc_datetime = pytz.utc.localize(datetime.datetime.utcnow())
curr_datetime = utc_datetime.astimezone(pytz.timezone("America/New_York"))
if user_hours is None:
    user_hours = -1
    logger.info("Retrieving most recent updates from db")
    last_updated = jira_model.return_last_update()
    hours_since_update = math.ceil((curr_datetime - last_updated).total_seconds() / 3600)

else:
    logger.info("Received user input of {} hours".format(user_hours))
    hours_since_update = user_hours


logger.info("Looking for updates in the past {} hours".format(hours_since_update))

if user_issue_key is None:
    if hours_since_update > 0:
        hours_since_update = hours_since_update
        get_jira_issues.load_issues('updated >= -{}h'.format(hours_since_update))

        issue_key_results = jira_model.return_keys('{} hour'.format(hours_since_update))

        for i in issue_key_results:
            logger.info("Getting worklog for {}".format(i[0]))
            get_jira_worklog.load_worklog(i[0])

    else:
        logger.info("Too soon to check for updates")
else:
        get_jira_worklog.load_worklog(user_issue_key)
        logger.info("Getting user specified worklog for {}".format(user_issue_key))

logger.info("Process complete")
