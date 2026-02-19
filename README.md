# Smart Campus Navigation System

A complete university hackathon prototype for indoor/outdoor campus navigation. The system helps students find classrooms, labs, library, admin office, canteen, and hostels, while calculating the shortest path between buildings using the A* algorithm.

## Features

- Search campus buildings by name
- Shortest path navigation using NetworkX A*
- QR scan simulation to set current location
- Step-by-step route directions
- Admin APIs to add buildings and connect paths
- Preloaded sample campus data for demo use

## Tech Stack

- **Backend:** Python 3.11, Flask (REST API)
- **Database:** SQLite
- **Graph Navigation:** NetworkX with A* pathfinding
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Map:** Custom local campus image (`static/campus_map.png`)

## Project Structure

```text
hackathon-project/
│
├── backend/
│   ├── app.py
│   ├── routes.py
│   ├── models.py
│   ├── graph.py
│   ├── database.db
│   ├── seed_data.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│
├── static/
│   └── campus_map.png
│
├── requirements.txt
├── README.md
└── .env.example
```

## API Endpoints

- `GET /buildings`
- `GET /navigate?start=Library&end=Canteen`
- `POST /scan_qr`
- `POST /admin/add_building`
- `POST /admin/connect`

## How to Run

```bash
python -m venv venv
source venv/bin/activate
```

```powershell
venv\Scripts\activate
```

```bash
pip install -r requirements.txt
python backend/seed_data.py
python backend/app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## Sample Navigation Output

Example for `start=Library` and `end=Canteen`:

```text
You are at Library → Then go to Admin Office → Then go to Canteen (Destination reached)
Total distance: 27.0 units
```

## Offline Support

This project runs fully locally without internet access after dependencies are installed.
