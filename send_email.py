from sparkpost import SparkPost
import configparser
import jira_model
import argparse
import logging
import json

logger = logging.getLogger("jiraLogger")

#parser = argparse.ArgumentParser(__file__)
#parser.add_argument('-u', dest='user', help='User id', type=str)
#parser.add_argument('-n', dest='user_name', help='User name', type=str)
#parser.add_argument('-e', dest='email', help='User email', type=str)
#parser.add_argument('-d', dest='days', help='Days to query', type=int)
#args = parser.parse_args()

sp_config = configparser.ConfigParser()
sp_config.read('config.ini')
sp_apikey = sp_config['sparkpost']['key']
sp_email = sp_config['sparkpost']['email']
sp_noreply = sp_config['sparkpost']['noreply']
sp_base_uri = sp_config['sparkpost']['base_uri']
sp = SparkPost(sp_apikey, base_uri=sp_base_uri)


def send_recap_email(user,username,email,days):

    table = ""
    results = jira_model.return_worklogs(user, days)
    email_body = '<p>Hello ' + username + ',</p>'
    if days == -1:
        results_intro_text = '<p>This is your first email! Here are your results since you started tracking:</p>'
    else:
        results_intro_text = '<p>Here are your results for the past ' + str(days) + ' days:</p>'
    result_count = sum(1 for i in results)
    if result_count > 1:
        for date, amount in results:
            amount_str = ('%f' % amount).rstrip('0').rstrip('.')
            final_string = '<tr><td align="center" valign="top">' + date.strftime("%B %d, %Y") \
                           + '</td><td align="center" valign="top">' + amount_str +'</td></tr>'
            table = table + final_string

        email_body = email_body + results_intro_text \
            + '<table border="1" cellpadding="0" cellspacing="0" width="50%" >' \
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
                },
                "metadata" : {
                    "binding" : "dedicated1"
                  }
            },
        ],
        html=email_body,
        from_email=sp_email,
        subject='Your ' + str(days) + ' day Jira Worklog',
        track_opens=True,
        track_clicks=True,
        reply_to=sp_noreply
    )
    accepted_recipients = response['total_accepted_recipients']
    if accepted_recipients >= 1:
        jira_model.update_user_emailedate(user)

#if __name__ == "__main__":
#    send_recap_email(args.user, args.user_name, args.email, args.days)