# MusicApp

MusicApp is a platform designed to manage and organize a music collection. You can save information about audio tracks and create playlists. This is achieved through an API interface built using FastAPI, Uvicorn and Pydantic, which communicates with a database.
The platform is divided into three components, each running in its own Docker container: database, frontend and backend. Each component runs in isolation. The database stores all the information, the frontend provides a user interface using streamlit library. The backend acts as a bridge, handling the communication between the two.

Check out the project on this video:
https://youtu.be/7iZ8YZN-_U4


## Requirements

To run this project, you will need the following software:
- Docker compose (https://docs.docker.com/compose/install/)


## Libraries

This project uses 3 microservices on separate containers:

Backend is built using a python image and using the following libraries:
- FastAPI
- Uvicorn
- Pydantic
- mysql-connector-python
- pytest

Frontend is built using a python image and using the following libraries:
- Stearmlit
- requests

Database is built using a mysql image and build the db from a predefined sql file:
- db.sql


## How to Use MusicApp
Follow these steps to get MusicApp up and running on your local machine:

1. Clone the repository:
```
git clone https://github.com/EASS-HIT-PART-A-2022-CLASS-II/MusicApp.git
```
2. Change into the project directory:
```
cd MusicApp
```
3. Use the following command to run MusicApp using Docker Compose:
```
docker-compose up --build
```
4. Once the services are up and running, access MusicApp in your web browser:
```
http://localhost/
```
5. Docs is also available on the endpoint server:
```
http://localhost:8080/docs
```
6. To stop the services, run the following command:
```
docker-compose down
```


## Additional Information

This project was created for the EASS-HIT-PART-A-2022-CLASS-II course.
