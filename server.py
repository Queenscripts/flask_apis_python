from flask import Flask, render_template, request

from pprint import pformat
import os
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['TICKETMASTER_KEY']


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/afterparty')
def show_afterparty_form():
    """Show event search form"""

    return render_template('search-form.html')


@app.route('/afterparty/search')
def find_afterparties():
    """Search for afterparties on Eventbrite"""

    keyword = request.args.get('keyword', '')
    postalcode = request.args.get('zipcode', '')
    radius = request.args.get('radius', '')
    unit = request.args.get('unit', '')
    sort = request.args.get('sort', '')

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY}

    res= requests.get(url,params=payload)
    
    data = res.json()
    events = data['_embedded']['events']

    # for event in events:
    #     print(f"event: {event}")
    #     get_event_details(event)
    # get_event_details(events)

    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=events)
    


# ===========================================================================
# FURTHER STUDY
# ===========================================================================


@app.route('/event/<id>')
def get_event_details(id):
    """View the details of an event."""

    # TODO: Finish implementing this view function
    print('\n', 20*'*')
    print(id)

    print('\n', 20*'*')

    # name = id['name']
    return render_template('event-details.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
