from jira import JIRA
import jira_model
import configparser
import logging

logger = logging.getLogger("jiraLogger")

def load_worklog(issue_key):
    success = None
    try:
        # Assign Jira configuration
        j_config = configparser.ConfigParser()
        j_config.read('config.ini')
        username = j_config['jira_config']['username']
        secret_token = j_config['jira_config']['secret_token']
        server = j_config['jira_config']['server']

        # Instantiate Jira connection
        jira = JIRA(server,
                    basic_auth=(username, secret_token))

        worklogs = jira.worklogs(issue_key)

        for w in worklogs:

            time_spent = w.timeSpentSeconds
            author = w.author.name
            created = w.created
            started = w.started
            if hasattr(w, "comment"):
                comment = w.comment
            else:
                comment = None
            updated = w.updated
            id = w.id
            logger.info("{}: {} seconds tracked".format(issue_key,time_spent))
            jira_model.insert_worklog(id,issue_key,comment,created,started,author,time_spent)

        success = True
        return time_spent

    except:
        success = False
        logger.exception("Message")

    finally:
        return success