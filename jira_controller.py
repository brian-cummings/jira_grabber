import get_jira_issues
import jira_model
import get_jira_worklog

get_issues_result: bool = get_jira_issues.load_issues()

print(get_issues_result)

issue_key_results = jira_model.return_keys('5 day')

for i in issue_key_results:
    print(i[0])
    get_jira_worklog.load_worklog(i[0])








