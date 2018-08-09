import psycopg2
import datetime
import configparser
import pytz

p_config = configparser.ConfigParser()
p_config.read('config.ini')
user = p_config['postgresql']['user']
host = p_config['postgresql']['host']
database = p_config['postgresql']['database']
password = p_config['postgresql']['password']

def insert_issue(summary, issue_key, issue_type, status, project_key, epic_link, resolution, created, updated,
                 resolved):
    try:
        utc_datetime = pytz.utc.localize(datetime.datetime.utcnow())
        curr_datetime = utc_datetime.astimezone(pytz.timezone("America/New_York"))

        table = 'issue'
        db_conn = psycopg2.connect("dbname={} user={} password={}".format(database, user, password))
        db_cursor = db_conn.cursor()
        insert_sql = """INSERT INTO Issue (Summary, IssueKey, IssueType, Status, ProjectKey, EpicLink, Resolution, 
                                Created, Updated, Resolved, SystemModified)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                ON CONFLICT (IssueKey) DO UPDATE SET
                                (Summary, IssueType, Status, ProjectKey, EpicLink, Resolution, 
                                Created, Updated, Resolved, SystemModified) =
                                (Excluded.Summary, Excluded.IssueType, Excluded.Status, Excluded.ProjectKey, Excluded.EpicLink, Excluded.Resolution, 
                                Excluded.Created, Excluded.Updated, Excluded.Resolved, Excluded.SystemModified);"""

        insert_data = (summary, issue_key, issue_type, status, project_key, epic_link, resolution, created, updated,
                       resolved, curr_datetime)
        print(insert_data)
        db_cursor.execute(insert_sql, insert_data)
        db_conn.commit()
    except db_conn.Error:
        db_conn.rollback()
    finally:

        db_conn.close()
    return


def insert_worklog(id, issue_key, comment, log_date, work_date, worker, seconds_worked):
    db_conn = psycopg2.connect("dbname={} user={} password={}".format(database, user, password))
    db_cursor = db_conn.cursor()
    utc_datetime = pytz.utc.localize(datetime.datetime.utcnow())
    curr_datetime = utc_datetime.astimezone(pytz.timezone("America/New_York"))

    try:
        db_cursor.execute("""INSERT INTO WORKLOG (Id, IssueKey, Comment, LogDate, WorkDate, Worker, SecondsWorked, 
        SystemModified) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (Id) DO UPDATE SET (IssueKey, Comment, LogDate, 
        WorkDate, Worker, SecondsWorked, SystemModified) = (Excluded.IssueKey, Excluded.Comment, 
        Excluded.LogDate, Excluded.WorkDate, Excluded.Worker, Excluded.SecondsWorked, Excluded.SystemModified);""",
                        (id, issue_key, comment, log_date, work_date, worker, seconds_worked, curr_datetime))
        db_conn.commit()

    except db_conn.Error:\
        db_conn.rollback()
     
    finally:
        db_conn.close()
    return


def return_keys(period):
    db_conn = psycopg2.connect("dbname={} user={} password={}".format(database, user, password))
    db_cursor = db_conn.cursor()
    try:
        db_cursor.execute("""SELECT IssueKey FROM ISSUE WHERE Updated >= now() - interval %s;""",
                          (period,))
        results = db_cursor.fetchall()
    except db_conn.Error:
        results = 'failure'
        raise

    finally:
        return results
        db_conn.close()
