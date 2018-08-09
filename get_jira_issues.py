from jira import JIRA
import jira_model
import configparser


def load_issues(jql):
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
        start_point = 0
        stop_point = 99999
        max_results = 100
        while start_point < stop_point:

            # Get issues with JQL
            all_issues = jira.search_issues(jql_str=jql,
                                            maxResults=max_results,
                                            startAt=start_point,
                                            fields='key,summary,issuetype,status,project,customfield_10118,'
                                                   'resolution,created,updated,resolutiondate')
            stop_point = all_issues.total

            for issue in all_issues:
                if hasattr(issue.fields.issuetype, "name"):
                    issue_type = issue.fields.issuetype.name
                else:
                    issue_type = None

                if hasattr(issue.fields.status, "name"):
                    status = issue.fields.status.name
                else:
                    status = None

                if hasattr(issue.fields.resolution, "name"):
                    resolution = issue.fields.resolution.name
                else:
                    resolution = None

                issue_load = jira_model.insert_issue(issue.fields.summary, issue.key, issue_type, status,
                                                     issue.fields.project.key, issue.fields.customfield_10118,
                                                     resolution,
                                                     issue.fields.created, issue.fields.updated,
                                                     issue.fields.resolutiondate)

            start_point += max_results
        success = True
    except:
        success = False
        raise
    finally:
        return success
