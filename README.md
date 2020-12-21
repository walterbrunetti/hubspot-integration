# hubspot-integration

### Local setup:

* python3 -m venv hubspot-integration-env
* cd hubspot-integration-env
* source bin/activate
* git clone git@github.com:walterbrunetti/hubspot-integration.git
* cd hubspot-integration
* pip install -r requirements.txt
* cd hubspot_integration_app
* python manage.py test


### Running App locally
* Make sure you have these ENV variables setup:
  - export MONGO_HOST=<YOUR_MONGO_CONNECTION>
  - export HUBSPOT_CLIENT_ID=<HUBSPOT_CLIENT_ID>  # will be provided separately
  - export HUBSPOT_CLIENT_SECRET=<HUBSPOT_CLIENT_SECRET>  # will be provided separately
* python manage.py runserver
* Open http://localhost:8000/deals/home in your browser and follow instructions there


### Running Dockerized version
* Make sure you have these ENV variables setup:
  - export MONGO_USER=<USERNAME>
  - export MONGO_PASSWORD=<PASSWORD>
  - export HUBSPOT_CLIENT_ID=<HUBSPOT_CLIENT_ID>  # will be provided separately
  - export HUBSPOT_CLIENT_SECRET=<HUBSPOT_CLIENT_SECRET>  # will be provided separately
* cd into project directory (/hubspot-integration-env/hubspot-integration)
* docker-compose build
* docker-compose up
* Open http://localhost:8000/deals/home in your browser and follow instructions there

Note: Hubspot credentials will be provided in an email.
