# Ex1_YanivLavi

Ex1_YanivLavi is a demonstration of using FastAPI, Uvicorn, and Pydantic to build a web API.

## Requirements

To run this project, you will need the following software:

- Docker
- Python

## Libraries

This project uses the following libraries:

- FastAPI
- Uvicorn
- Pydantic

## How to use

1. Clone the repository:
```
git clone https://github.com/EASS-HIT-PART-A-2022-CLASS-II/Ex1_YanivLavi.git
```
2. Navigate to the project directory:
```
cd Ex1_YanivLavi
```
3. Build the Docker images:
```
docker build -t backend backend/
docker build -t frontend frontend/
```
4. Run the Docker containers:
```
sudo docker network create MusicApp
docker run -ti --name backend -p 8989:8080 --network MusicApp backend
docker run -ti --name frontend -p 80:80 --network MusicApp frontend 
```
5. Go to http://localhost/

## Additional Information

This project was created for the EASS-HIT-PART-A-2022-CLASS-II course.
