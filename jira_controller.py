import datetime
import get_jira_issues
import jira_model
import get_jira_worklog

curr_date = datetime.datetime.date(datetime.datetime.now())
last_updated = datetime.datetime.date(jira_model.return_last_update())
days_since_update = (last_updated - curr_date).days

print(days_since_update)
if days_since_update > 0:
    get_issues_result: bool = get_jira_issues.load_issues('project in (PP, ITAR, ITARC, ITACDC, '
                                                          'ESITI, ITSV, SRT, SQL, EP) and updated >= -{}d'
                                                          .format(days_since_update))

    issue_key_results = jira_model.return_keys('{} day'.format(days_since_update))

    for i in issue_key_results:
        print(i[0])
        get_jira_worklog.load_worklog(i[0])

else:
    print('Too soon to tell')






