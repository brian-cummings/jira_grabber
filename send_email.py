from sparkpost import SparkPost
import configparser
import jira_model
import argparse
import logging

logger = logging.getLogger("jiraLogger")

parser = argparse.ArgumentParser(__file__)
parser.add_argument('-u', dest='user', help='User id', type=str)
parser.add_argument('-n', dest='user_name', help='User name', type=str)
parser.add_argument('-e', dest='email', help='User email', type=str)
parser.add_argument('-d', dest='days', help='Days to query', type=int)
args = parser.parse_args()

sp_config = configparser.ConfigParser()
sp_config.read('config.ini')
sp_apikey = sp_config['sparkpost']['key']
sp = SparkPost(sp_apikey)

def send_weekly_email(user,username,email,days):

    table = ""
    results = jira_model.return_worklogs(user, days)
    email_body = '<p>Hello ' + username + ',</p>'
    result_count = sum(1 for i in results)
    if result_count > 1:
        for date, amount in results:
            amount_str = ('%f' % amount).rstrip('0').rstrip('.')
            final_string = '<tr><td align="center" valign="top">' + date.strftime("%B %d, %Y") \
                           + '</td><td align="center" valign="top">' + amount_str +'</td></tr>'
            table = table + final_string

        email_body = email_body \
            + '<p>Here are your results for the past ' + str(days) + ' days:</p>' \
            '<table border="1" cellpadding="0" cellspacing="0" width="50%" >' \
            '<tr> <th bgcolor="#D3D3D3">Date</th><th bgcolor="#D3D3D3">Hours</th>' \
            + table + '</table>'
    else:
        email_body = email_body + '<p>You have no worklogs for the past ' + str(days) + ' days.</p>'

    response = sp.transmissions.send(
        recipients=[
            {
                'address': {
                    'email': email,
                    'name': username
                }
            },
        ],
        html=email_body,
        from_email='Test User <test@sahmhill.com>',
        subject='Your ' + str(days) + ' day Jira Worklog',
        track_opens=True,
        track_clicks=True,
        reply_to='no-reply@sparkpostmail.com'
    )

if __name__ == "__main__":
    send_weekly_email(args.user, args.user_name, args.email, args.days)