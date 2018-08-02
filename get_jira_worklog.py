from jira import JIRA
import jira_model
import configparser


def load_worklog(issue_key):
    success: bool = None
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

        issue = jira.issue(issue_key).fields.worklog.worklogs

        for w in issue:

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
            jira_model.insert_worklog(id,issue_key,comment,created,started,author,time_spent)

        success = True
        return time_spent

    except:
        success = False
        raise

    finally:
        return success