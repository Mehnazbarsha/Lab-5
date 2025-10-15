# Flask Publish-Subscribe HTTP Server

A simple HTTP server implementing a publish-subscribe pattern using Python Flask.

## Overview

This project implements a basic pub-sub system where:
- Subscribers can be added/deleted
- Each subscriber has a name and URL
- When the subject is updated, all subscribers are notified
- All operations are performed via HTTP endpoints

## Prerequisites

- Python 3.7 or higher
- Flask library

## Installation

1. Clone the repository or open in GitHub Codespaces

2. Install dependencies:
```bash
pip install flask
```

## Running the Server

Start the Flask server:
```bash
python flaskHttpServer.py
```

The server will run on `http://localhost:5000` (or `http://0.0.0.0:5000` in Codespaces)

## Running Tests

In a separate terminal, run the unit tests:
```bash
python test_flaskHttpServer.py
```

Or with verbose output:
```bash
python -m unittest test_flaskHttpServer.py -v
```

## API Endpoints

### 1. Root Endpoint
```bash
curl http://localhost:5000/
```
Returns a simple acknowledgment.

### 2. List Subscribers
```bash
curl http://localhost:5000/list-subscribers
```
Returns JSON object of all subscribers and their URLs.

### 3. Add Subscriber
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","URI":"http://alice.example.com"}' \
  http://localhost:5000/add-subscriber
```

### 4. Delete Subscriber
```bash
curl -X DELETE \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice"}' \
  http://localhost:5000/delete-subscriber
```

### 5. Update Subject and Notify All Subscribers
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"subject-update":"New topic: Flask pub-sub"}' \
  http://localhost:5000/update-and-notify
```

## Testing Workflow

1. **Start the server** in one terminal:
   ```bash
   python flaskHttpServer.py
   ```

2. **In another terminal**, test the endpoints:

   ```bash
   # Add some subscribers
   curl -X POST -H "Content-Type: application/json" \
     -d '{"name":"Bob","URI":"http://bob.com"}' \
     http://localhost:5000/add-subscriber
   
   curl -X POST -H "Content-Type: application/json" \
     -d '{"name":"Charlie","URI":"http://charlie.com"}' \
     http://localhost:5000/add-subscriber
   
   # List all subscribers
   curl http://localhost:5000/list-subscribers
   
   # Update and notify
   curl -X POST -H "Content-Type: application/json" \
     -d '{"subject-update":"Important update!"}' \
     http://localhost:5000/update-and-notify
   
   # Delete a subscriber
   curl -X DELETE -H "Content-Type: application/json" \
     -d '{"name":"Bob"}' \
     http://localhost:5000/delete-subscriber
   
   # List subscribers again
   curl http://localhost:5000/list-subscribers
   ```

3. **Watch the server terminal** for notification print statements

## Project Structure

```
.
├── flaskHttpServer.py       # Main Flask application
├── test_flaskHttpServer.py  # Unit tests
└── README.md                # This file
```

## Implementation Notes

- Subscribers are stored in an in-memory dictionary
- Notifications are printed to the console (backend terminal)
- The server runs in debug mode for development
- All endpoints return JSON responses
