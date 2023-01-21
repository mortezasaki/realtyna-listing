# realtyna task
Real state listing management

Realtyna task is a simple web application that allows you to manage real state listings.

Note: This application is not production ready, it is just a demo.
    Authentication/Authorization is not implemented, so anyone can access the application.

## Features
- Add, edit, delete listings
- Book a listing
- Report a listing reservations

## Installation
```bash
docker-compose up -d
```

## Usage
- Go to http://localhost:8000

## Run Samples
- First, install the Rest Client extension for VSCode
- Then, open the file `requests.http` in `samples` folder and run the requests
  
## Testing
```bash
manage.py test
```
