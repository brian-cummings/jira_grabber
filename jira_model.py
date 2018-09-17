import psycopg2
import datetime
import configparser
import pytz
import logging

logger = logging.getLogger("jiraLogger")

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
        issue_key = (issue_key).upper()

        table = 'issue'
        db_conn = psycopg2.connect("host={} dbname={} user={} password={}".format(host, database, user, password))
        db_cursor = db_conn.cursor()
        insert_sql = """INSERT INTO Issue (Summary, IssueKey, IssueType, Status, ProjectKey, EpicLink, Resolution, 
                                Created, Updated, Resolved, SystemModified)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                ON CONFLICT (IssueKey) DO UPDATE SET
                                (Summary, IssueType, Status, ProjectKey, EpicLink, Resolution, 
                                Created, Updated, Resolved, SystemModified) =
                                (Excluded.Summary, Excluded.IssueType, Excluded.Status, Excluded.ProjectKey, 
                                Excluded.EpicLink, Excluded.Resolution, Excluded.Created, Excluded.Updated, 
                                Excluded.Resolved, Excluded.SystemModified);"""

        insert_data = (summary, issue_key, issue_type, status, project_key, epic_link, resolution, created, updated,
                       resolved, curr_datetime)
        db_cursor.execute(insert_sql, insert_data)
        db_conn.commit()
    except db_conn.Error:
        db_conn.rollback()
        logger.exception("Message")
    finally:
        db_conn.close()
    return


def insert_worklog(id, issue_key, comment, log_date, work_date, worker, seconds_worked):
    db_conn = psycopg2.connect("host={} dbname={} user={} password={}".format(host, database, user, password))
    db_cursor = db_conn.cursor()
    utc_datetime = pytz.utc.localize(datetime.datetime.utcnow())
    curr_datetime = utc_datetime.astimezone(pytz.timezone("America/New_York"))
    issue_key = (issue_key).upper()
    SQL = """INSERT INTO WORKLOG (Id, IssueKey, Comment, LogDate, WorkDate, Worker, SecondsWorked, 
        SystemModified) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (Id) DO UPDATE SET (IssueKey, Comment, LogDate, 
        WorkDate, Worker, SecondsWorked, SystemModified) = (Excluded.IssueKey, Excluded.Comment, 
        Excluded.LogDate, Excluded.WorkDate, Excluded.Worker, Excluded.SecondsWorked, Excluded.SystemModified);"""

    try:
        db_cursor.execute(SQL, (id, issue_key, comment, log_date, work_date, worker, seconds_worked, curr_datetime))
        db_conn.commit()

    except db_conn.Error:
        db_conn.rollback()
        logger.exception("Message")
    finally:
        db_conn.close()
    return


def return_keys(period):
    db_conn = psycopg2.connect("host={} dbname={} user={} password={}".format(host, database, user, password))
    db_cursor = db_conn.cursor()
    SQL = """SELECT IssueKey FROM ISSUE WHERE Updated >= now() - interval %s;"""
    try:
        db_cursor.execute(SQL, (period,))
        results = db_cursor.fetchall()
    except db_conn.Error:
        logger.exception("Message")
    finally:
        return results
        db_conn.close()


def return_last_update():
    db_conn = psycopg2.connect("host={} dbname={} user={} password={}".format(host, database, user, password))
    db_cursor = db_conn.cursor()
    SQL = """SELECT MAX(Updated) as max_updated FROM ISSUE;"""
    try:
        db_cursor.execute(SQL)

        for max_updated, in db_cursor:
            results = max_updated
        if results == None:
            results = 9999
    except db_conn.Error:
        logger.exception("Message")
    finally:
        return results
        db_conn.close()

def insert_user(id, display_name, email, active):
    db_conn = psycopg2.connect("host={} dbname={} user={} password={}".format(host, database, user, password))
    db_cursor = db_conn.cursor()
    utc_datetime = pytz.utc.localize(datetime.datetime.utcnow())
    curr_datetime = utc_datetime.astimezone(pytz.timezone("America/New_York"))
    id = id.lower()
    SQL = """INSERT INTO JIRAUSER (id, displayname, email, active, updated) VALUES (%s,%s,%s,%s,%s) 
        ON CONFLICT (id) DO UPDATE SET (id, displayname, email, active, updated) = (Excluded.id, Excluded.displayname, 
        Excluded.email, Excluded.active, Excluded.updated);"""
    try:
        db_cursor.execute(SQL, (id, display_name, email, active, curr_datetime))
        db_conn.commit()

    except db_conn.Error:
        db_conn.rollback()
        logger.exception("Message")
    finally:
        db_conn.close()
    return


def return_worklogs(worker,days):
    db_conn = psycopg2.connect("host={} dbname={} user={} password={}".format(host, database, user, password))
    db_cursor = db_conn.cursor()
    neg_days = int(days) * -1
    start_date = datetime.datetime.today() - datetime.timedelta(days=days)
    SQL = "SELECT workdate::date, round(sum(secondsworked)/3600,1) as hoursworked FROM \
        worklog WHERE worker = %s AND workdate between %s and now() \
        GROUP BY workdate::date;"
    try:
        db_cursor.execute(SQL, (worker, start_date))
        results = db_cursor.fetchall()

    except db_conn.Error:
        logger.exception("Message")
    finally:
        return results
        db_conn.close()
