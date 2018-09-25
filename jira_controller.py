import datetime
import pytz
import math
import get_jira_issues
import get_jira_users
import jira_model
import get_jira_worklog
import argparse
import logging
import send_email
from logging.handlers import TimedRotatingFileHandler

log_file = "../logs/jira.log"
logger = logging.getLogger("jiraLogger")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler(log_file, when="H", interval=1, backupCount=24)
logger.addHandler(handler)
handler.doRollover()

parser = argparse.ArgumentParser(__file__)
parser.add_argument('-t', dest='hours', help='Time in hours to retrieve', type=int)
parser.add_argument('-i', dest='issue_key', help='Jira issue key', type=str)
parser.add_argument('-s', dest='skip_update', help='Skip user update', action='store_true')
parser.add_argument('-e', dest='email_only', help='Send emails only', action='store_true')
args = parser.parse_args()
user_hours = args.hours
user_issue_key = args.issue_key
user_skip_update = args.skip_update
user_send_emails_only = args.email_only

utc_datetime = pytz.utc.localize(datetime.datetime.utcnow())
curr_datetime = utc_datetime.astimezone(pytz.timezone("America/New_York"))

if user_send_emails_only is not True:

    if user_hours is None:
        user_hours = -1
        logger.info("Retrieving most recent updates from db [{}]".format(curr_datetime))
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
                logger.info("Worklog for {} completed".format(i[0]))

        else:
            logger.info("Too soon to check for updates")
    else:
            logger.info("Getting user specified worklog for {}".format(user_issue_key))
            get_jira_worklog.load_worklog(user_issue_key)
            logger.info("User specified worklog for {} completed".format(user_issue_key))

if user_skip_update == False and user_issue_key is None:
    if user_send_emails_only == False:
        get_jira_users.load_users()
    subscribers = jira_model.return_subscribed_users()

    for jid, name, email, lastupdated in subscribers:
        dsu_int = 0
        if lastupdated is None:
            days_since_update = None
            dsu_int = -1
        else:
            days_since_update = (utc_datetime - lastupdated).days
        if dsu_int >= 7 or dsu_int == -1:
            send_email.send_recap_email(jid, name, email, days_since_update)

utc_finish_datetime = pytz.utc.localize(datetime.datetime.utcnow())
finish_datetime = utc_finish_datetime.astimezone(pytz.timezone("America/New_York"))
logger.info("Process complete [{}]".format(finish_datetime))
