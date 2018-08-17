import sqlite3
from datetime import datetime
# Use this module if running a sqlite database


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

    finally:
        db_conn.commit()
        db_conn.close()
    return


def insert_worklog(id, issue_key, comment, log_date, work_date, worker, seconds_worked):
    db_loc = 'jira.sqlite'
    db_conn = sqlite3.connect(db_loc)
    curr_datetime = datetime.now()

    try:
        db_conn.execute("""INSERT INTO WORKLOG (Id, IssueKey, Comment, LogDate, WorkDate, Worker, SecondsWorked, SystemModified)
                            VALUES (?,?,?,?,?,?,?,?);""",
                        (id, issue_key, comment, log_date, work_date, worker, seconds_worked, curr_datetime))
    except sqlite3.IntegrityError:
        db_conn.execute("""UPDATE WORKLOG SET Id = ?, IssueKey = ?, Comment = ?, LogDate = ?, WorkDate = ?, Worker = ?, 
                        SecondsWorked = ?, SystemModified = ? WHERE Id = ? AND IssueKey = ?;""",
                        (id, issue_key, comment, log_date, work_date, worker, seconds_worked, curr_datetime, id, issue_key))

    finally:
        db_conn.commit()
        db_conn.close()
    return


def return_keys():
    db_loc = 'jira.sqlite'
    db_conn = sqlite3.connect(db_loc)
    db_cur = db_conn.cursor()

    try:
        db_cur.execute("""SELECT IssueKey FROM ISSUE WHERE Updated >= date('now','-3 day');""")
        results = db_cur.fetchall()
    except:
        results = 'failure'
        raise

    finally:
        return results
        db_conn.close()
