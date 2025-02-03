# Restaurant recommendation API server
## Setup Instructions
### Prerequisites
- Docker
- Docker Compose:
- Python
### Step 1: clone the repository

### Step 2: create .env file
Create a .env file in your root directory with the following variables (add your password to PASSWORD):

NAME=restaurant_db
USER=postgres
PASSWORD= 
HOST=db
PORT=5432

### Step 3: add data
Add resteraunt.parquet, user.parquet, request.parquet to data folder

### Step 4: build and run
Run this command: docker-compose up --build

### Step 5: check api status
Check that the api status is running correctly at http://127.0.0.1:80/docs

### Step 6: test queries
Test that the API works at http://127.0.0.1:80/docs

### Step 7: performance testing
- run the to_json.py file in perf_test folder (converts request.parquet to json for k6)
- install k6
- navigate to perf_test folder and open in terminal
- run: k6 run load_test.js
