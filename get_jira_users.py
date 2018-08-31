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
    load = 999
    max_results = 200

    try:
        while load >= max_results:
            users = jira.search_users(user='%',startAt=start_point,includeInactive=True,maxResults=max_results)
            load = sum(1 for e in users)
            logger.info("Fetching users {} - {}".format(start_point, start_point + load))

            for u in users:
                jira_model.insert_user(u.name, u.displayName, u.emailAddress, u.active)

            start_point = start_point + max_results
    except:
        logger.exception("Message")
    finally:
        jira.close()
        return

if __name__ == "__main__":
    load_users()