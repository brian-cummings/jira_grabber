import datetime
import get_jira_issues
import jira_model
import get_jira_worklog
import argparse
import logging
from logging.handlers import TimedRotatingFileHandler

log_file = "../logs/jira.log"
logger = logging.getLogger("jiraLogger")
logger.setLevel(logging.INFO)
parser = argparse.ArgumentParser(__file__)
parser.add_argument('-d',metavar='days', dest='days', help='Days to retrieve', type=int)
parser.add_argument('-i',metavar='issue key', dest='issue_key', help='Jira issue key', type=str)
args = parser.parse_args()
user_days = args.days
user_issue_key = args.issue_key

handler = TimedRotatingFileHandler(log_file, when="D", interval=1, backupCount=7)
logger.addHandler(handler)
curr_date = datetime.datetime.date(datetime.datetime.now())
if user_days is None:
    user_days = -1
    logger.info("Retrieving most recent updates from db")
    last_updated = datetime.datetime.date(jira_model.return_last_update())
    days_since_update = (curr_date - last_updated).days
else:
    logger.info("Received user input of {} days".format(user_days))
    days_since_update = user_days


logger.info("Looking for updates in the past {} days".format(days_since_update))

if user_issue_key is None:
    if days_since_update > 0:
        get_jira_issues.load_issues('project in (PP, ITAR, ITARC, ITACDC, '
                                    'ESITI, ITSV, SRT, SQL, EP) and updated >= -{}d'
                                    .format(days_since_update))

        issue_key_results = jira_model.return_keys('{} day'.format(days_since_update))

        for i in issue_key_results:
            logger.info("Getting worklog for {}".format(i[0]))
            get_jira_worklog.load_worklog(i[0])

    else:
        logger.info("Too soon to check for updates")
else:
        get_jira_worklog.load_worklog(user_issue_key)
        logger.info("Getting user specified worklog for {}".format(user_issue_key))

logger.info("Process complete")
