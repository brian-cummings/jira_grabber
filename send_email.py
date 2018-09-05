from sparkpost import SparkPost
import configparser

sp_config = configparser.ConfigParser()
sp_config.read('config.ini')
sp_apikey = sp_config['sparkpost']['key']

sp = SparkPost(sp_apikey)

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
    html='<p>Hello {{name}}</p>',
    text='Hello {{name}}',
    from_email='Test User <test@sparkpostbox.com>',
    subject='Example Script',
    description='contrived example',
    track_opens=True,
    track_clicks=True,
    campaign='sdk example',
    metadata={
        'key': 'value',
        'arbitrary': 'values'
    },
    substitution_data={
        'name': 'Example User'
    },
    reply_to='no-reply@sparkpostmail.com'
)