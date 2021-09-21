# Mark CSS classes as content.
This project is a simple server application used to store annotations in a database.
The implementation utilizes Flask and Flask-SQLAlchemy and provides an API for fetching
and creating domain specific annotations.

## Running the application
If you wish to run the application, I recommend utilizing Docker-Compose and the provided compose files. With Docker-Compose (and Docker) installed, simply run `docker-compose up --build`. Tests can be run with `docker-compose -f docker-compose.test.yml up`. The project also includes a compose file for creating migrations by running `docker-compose -f docker-compose.yml -f docker-compose.migrate.yml`.

If you whish to run the application without containers, you'll need to have Python installed. Dependencies are listed in the requirements.txt file. Easiest way to install them is with pip by running `pip install -r requirements.txt`. You'll also need to setup some environment variables which can be found in the compose files and a database to connec to.