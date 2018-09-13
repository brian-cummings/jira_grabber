from sparkpost import SparkPost
import configparser
import jira_model

sp_config = configparser.ConfigParser()
sp_config.read('config.ini')
sp_apikey = sp_config['sparkpost']['key']
table = ""
sp = SparkPost(sp_apikey)

results = jira_model.return_worklogs('bcummings', '21 days')

for date, amount in results:
    final_string = '<tr><td align="center" valign="top">' + date.strftime("%B %d, %Y") \
                   + '</td><td align="center" valign="top">' + '{0:.1g}'.format(amount) +'</td></tr>'
    table = table + final_string

response = sp.transmissions.send(
    recipients=[
        {
            'address': {
                'email': 'brian.m.cummings@gmail.com',
                'name': 'BC G'
            }
        },
        {
            'address': {
                'email': 'brian.cummings@careerbuilder.com',
                'name': 'BC C'
            }
        }
    ],
    html='<p>Hello {{name}}</p>'
    '<p>Here are your results for the past week:</p>'
    '<table border="1" cellpadding="0" cellspacing="0" width="100%" >'
    '<tr> <th bgcolor="#D3D3D3">Date</th><th bgcolor="#D3D3D3">Hours</th>' +
    table + '</table>',
    from_email='Test User <test@sahmhill.com>',
    subject='Your Weekly Jira Worklog',
    track_opens=True,
    track_clicks=True,
    substitution_data={
        'name': 'Example User'
    },
    reply_to='no-reply@sparkpostmail.com'
)