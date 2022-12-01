# Meeting booking calendar

Core code of Meeting booking calendar based on FastAPI, Quasar project

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

If you haven't **docker** in machine, please install it before go on.

### 1. Setup project on local machine.

#### 1.1 Create and add env variable to project

Create **.env** file at the root folder of the project.

Define all variable from .env.example.
#### 1.2 Run project
Run **docker** containers:

For Linux/Mac OS: 
```bash
make start
```
For Windows:
```powerahell
docker-compose up
```
After conteiners has been built open web app console and run next commands:
```powerahell
cd src
yarn quasar dev
```
### 2. Project usage.
After running the project, open http://127.0.0.1/docs and use Swagger UI to work with API.

To get access to Quasar: http://127.0.0.1:8080
### 3. Some useful commands

#### 3.1 Docker
**Build app container via docker-compose:**

For Linux/Mac OS: 
```bash
make build
```
For Windows:
```powerahell
docker-compose build
```

**Build container without cache:**

For Linux/Mac OS: 
```bash
make build-nc
```
For Windows:
```powerahell
docker-compose build --no-cache
```

**Get access to app conrainer:**

For Linux/Mac OS: 
```bash
make exec-app
```
For Windows:
```powerahell
docker exec -ti teklabs_test_task_app_1 sh
```

**Get access to db conrainer**

For Linux/Mac OS: 
```bash
make exec-db
```
For Windows:
```powerahell
docker exec -ti teklabs_test_db_app_1 sh
```