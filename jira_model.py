import sqlite3
from datetime import datetime


def insert_issue(summary, issue_key, issue_type, status, project_key, epic_link, resolution, created, updated,
                 resolved):
    db_loc = 'jira.sqlite'
    db_conn = sqlite3.connect(db_loc)
    curr_datetime = datetime.now()

    try:
        db_conn.execute("""INSERT INTO ISSUE (Summary, IssueKey, IssueType, Status, ProjectKey, EpicLink, Resolution, Created, 
                            Updated, Resolved, SystemModified)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?);""",
                        (summary, issue_key, issue_type, status, project_key, epic_link,
                         resolution, created, updated, resolved, curr_datetime))
    except sqlite3.IntegrityError:
        db_conn.execute("""UPDATE ISSUE SET Summary = ?, IssueType = ?, Status = ?, ProjectKey = ?, EpicLink = ?, 
                        Resolution = ?, Created = ?, Updated = ?, Resolved = ?, SystemModified = ? WHERE IssueKey = ?;""",
                        (summary, issue_type, status, project_key, epic_link, resolution,
                         created, updated, resolved, curr_datetime, issue_key))

    db_conn.commit()
    db_conn.close()
    return
