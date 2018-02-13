from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
from flask import render_template

import pprint
import os

# This code originally from https://github.com/lepture/flask-oauthlib/blob/master/example/github.py
# Edited by P. Conrad for SPIS 2016 to add getting Client Id and Secret from
# environment variables, so that this will work on Heroku.
# Edited by S. Adams for Designing Software for the Web to add comments and remove flash messaging

app = Flask(__name__)

app.debug = False #Change this to False for production

app.secret_key = os.environ['SECRET_KEY'] #use SECRET_KEY to sign session cookies
oauth = OAuth(app)

# Set up GitHub as OAuth provider
github = oauth.remote_app(
    'github',
    consumer_key=os.environ['GITHUB_CLIENT_ID'], #your web apps "username" for OAuth
    consumer_secret=os.environ['GITHUB_CLIENT_SECRET'], # web apps "password" for OAUTh
    request_token_params={'scope': 'user:email'}, #request read-only access to the user's email.  For a list of possible scopes, see developer.github.com/apps/building-oauth-apps/scopes-for-oauth-apps
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',  
    authorize_url='https://github.com/login/oauth/authorize' #URL for github's OAuth login
)

#context  processors run before templates are rendered and add variables to the template context
#context processors must return a dictionary
#this context processor adds the variable logged_in to the context for all temlates
@app.context_processor
def inject_logged_in():
    return {"logged_in":('github_token' in session)}

@app.route('/')
def home():
    return render_template('home.html')
#redirect to GITHUB's OAUTH page and confirm the callback URL
@app.route('/login')
def login():   
    return github.authorize(callback=url_for('authorized', _external=True, _scheme='https'))                                                                                                                    '''{'avatar_url': 'https://avatars3.githubusercontent.com/u/31492762?v=4',
 'bio': 'Aspiring full stack developer',
 'blog': '',
 'company': None,
 'created_at': '2017-08-30T23:12:58Z',
 'email': None,
 'events_url': 'https://api.github.com/users/lukeborders/events{/privacy}',
 'followers': 0,
 'followers_url': 'https://api.github.com/users/lukeborders/followers',
 'following': 0,
 'following_url': 'https://api.github.com/users/lukeborders/following{/other_user}',
 'gists_url': 'https://api.github.com/users/lukeborders/gists{/gist_id}',
 'gravatar_id': '',
 'hireable': None,
 'html_url': 'https://github.com/lukeborders',
 'id': 31492762,
 'location': None,
 'login': 'lukeborders',
 'name': 'Luke Borders',
 'organizations_url': 'https://api.github.com/users/lukeborders/orgs',
 'public_gists': 0,
 'public_repos': 18,
 'received_events_url': 'https://api.github.com/users/lukeborders/received_events',
 'repos_url': 'https://api.github.com/users/lukeborders/repos',
 'site_admin': False,
 'starred_url': 'https://api.github.com/users/lukeborders/starred{/owner}{/repo}',
 'subscriptions_url': 'https://api.github.com/users/lukeborders/subscriptions',
 'type': 'User',
 'updated_at': '2018-02-09T17:04:37Z',
 'url': 'https://api.github.com/users/lukeborders'}'''

@app.route('/logout')
def logout():
    session.clear()
    return render_template('message.html', message='You were logged out')

@app.route('/login/authorized')#the route should match the callback URL registered with the OAuth provider
def authorized():
    resp = github.authorized_response()
    if resp is None:
        session.clear()
        message = 'Access denied: reason=' + request.args['error'] + ' error=' + request.args['error_description'] + ' full=' + pprint.pformat(request.args)      
    else:
        try:
            #save user data and set log in message
            session['github_token']=(resp['access_token'],'')
            session['user_data']=github.get('user').data
            message = 'You were successfully logged in as ' + session['user_data']['login']
        except:
            #clear the session and give error message
            session.clear()
            message='Unable to login. Please try again.'
    return render_template('message.html', message=message)


@app.route('/page1')
def renderPage1():
    if 'user_data' in session:
        user_data_pprint = pprint.pformat(session['user_data'])#format the user data nicely
    else:
        user_data_pprint = '';
    return render_template('page1.html',dump_user_data=user_data_pprint)

@app.route('/page2')
def renderPage2():
    return render_template('page2.html')

# the tokengetter is automaticallly called to check who is logged in
@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')


if __name__ == '__main__':
    app.run()
    
    #A
    #G
    #L
    #E
    #T
    #AGLET
    #DONT FORGET IT
