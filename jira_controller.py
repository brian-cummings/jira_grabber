from jira import JIRA
import jira_model
import configparser

j_config = configparser.ConfigParser()
j_config.read('config.ini')
username = j_config['jira_config']['username']
secret_token = j_config['jira_config']['secret_token']
server = j_config['jira_config']['server']

jira = JIRA(server,
            basic_auth=(username, secret_token))
start_point = 0
stop_point = 99999
max_results = 100

while start_point < stop_point:

    # Search returns first 50 results, `maxResults` must be set to exceed this
    all_issues = jira.search_issues('project in (PP, ITAR, ITARC, ITACDC) and updated >= -1w', maxResults=max_results,
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

        # print('{} | {} | type: {} | {} | {} | {} | {} | {} | {}'.format(issue.fields.summary, issue.key,
        #                                                                issue.fields.issuetype,
        #                                                                issue.fields.status, issue.fields.project,
        #                                                                issue.fields.customfield_10118,
        #                                                                issue.fields.resolution,
        #                                                                issue.fields.created, issue.fields.updated,
        #                                                                issue.fields.resolutiondate))

        issue_load = jira_model.insert_issue(issue.fields.summary, issue.key, issue_type, status,
                                            issue.fields.project.name, issue.fields.customfield_10118, resolution,
                                            issue.fields.created, issue.fields.updated, issue.fields.resolutiondate)

    start_point += max_results
