from jira import JIRA
import jira_model
import configparser
import logging

logger = logging.getLogger("jiraLogger")

def load_users():
    j_config = configparser.ConfigParser()
    j_config.read('config.ini')
    username = j_config['jira_config']['username']
    secret_token = j_config['jira_config']['secret_token']
    server = j_config['jira_config']['server']

    # Instantiate Jira connection
    jira = JIRA(server,
                basic_auth=(username, secret_token))
    start_point = 0
    stop_point = 99999
    max_results = 200

    try:
        while start_point < stop_point:
            users = jira.search_users(user='%',startAt=start_point,includeInactive=True,maxResults=max_results)
            stop_point = users.total
            logger.info("Fetching {} - {} of {} users".format(start_point, min(start_point + max_results, stop_point),
                                                              stop_point))

            for u in users:
                print(u.name, u.displayName, u.emailAddress, u.active)
                jira_model.insert_user(u.name, u.displayName, u.emailAddress, u.active)

            start_point = start_point + max_results
    except:
        logger.exception("Message")
    finally:
        jira.close()
        return