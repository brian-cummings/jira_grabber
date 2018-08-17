import datetime
import get_jira_issues
import jira_model
import get_jira_worklog
import sys
import logging
from logging.handlers import TimedRotatingFileHandler

log_file = "../logs/jira.log"
logger = logging.getLogger("jiraLogger")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(log_file, when="D", interval=1, backupCount=7)
logger.addHandler(handler)
curr_date = datetime.datetime.date(datetime.datetime.now())
try:
    user_days = int(sys.argv[1])
    logger.info("Received user input of {} days".format(user_days))
    days_since_update = user_days
except:
    user_days = -1
    logger.info("Retrieving most recent updates from db")
    last_updated = datetime.datetime.date(jira_model.return_last_update())
    days_since_update = (curr_date - last_updated).days
    pass

logger.info("Looking for updates in the past {} days".format(days_since_update))

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

logger.info("Process complete")
