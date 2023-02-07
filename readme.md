# MusicApp

MusicApp is a platform designed to manage and organize a music collection. You can save information about audio tracks and create playlists. This is achieved through an API interface built using FastAPI, Uvicorn and Pydantic, which communicates with a database.
The platform is divided into three components, each running in its own Docker container: database, frontend and backend. Each component runs in isolation. The database stores all the information, the frontend provides a user interface using streamlit library. The backend acts as a bridge, handling the communication between the two.

## Requirements

To run this project, you will need the following software:
- Docker
- Python
- Docker compose

## Libraries

This project uses 3 microservices on separate containers with the following libraries:

Backend:
- FastAPI
- Uvicorn
- Pydantic

Database:
- Mysql 

Frontend:
- Stearmlit


## How to use

1. Clone the repository:
```
git clone https://github.com/EASS-HIT-PART-A-2022-CLASS-II/MusicApp.git
```
2. Navigate to the project directory:
```
cd MusicApp
```
3. Run the docker compose command below:
```
docker-compose up --build
```
4. Go to http://localhost/

## Additional Information

This project was created for the EASS-HIT-PART-A-2022-CLASS-II course.
