# Fuel Optimizer API

A Django REST Framework application that calculates the optimal fuel stops for a trip within the United States based on fuel prices and vehicle range constraints.

The API accepts a start and destination location, calculates the route, identifies cost-effective fuel stops along the route, and returns the estimated total fuel cost.

---

## Features

* Route calculation between two locations in the USA
* Geocoding using OpenStreetMap Nominatim
* Fuel stop optimization based on fuel prices
* Vehicle range constraint support (500 miles)
* Fuel cost estimation based on 10 MPG
* Response caching for improved performance
* RESTful API built with Django REST Framework

---

## Assumptions

* Vehicle fuel efficiency: **10 miles per gallon**
* Maximum vehicle range: **500 miles**
* Fuel prices are sourced from the provided dataset
* Start and destination locations must be within the United States

---

## Tech Stack

* Python 3.12+
* Django 5
* Django REST Framework
* SQLite (default)
* OpenStreetMap Nominatim (Geocoding)
* OpenRouteService (Routing)
* Django Cache Framework

---

## Project Structure

```text
fuel_optimizer/
│
├── fuel_optimizer/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── routes/
│   ├── views.py
│   ├── serializers.py
│   ├── services.py
│   ├── models.py
│   └── management/
│       └── commands/
│           └── import_fuel_prices.py
│
├── fuel-prices.csv
├── manage.py
└── requirements.txt
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd fuel_optimizer
```

### Create Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
ORS_API_KEY=your_openrouteservice_api_key
```

---

## Database Setup

Run migrations:

```bash
python manage.py migrate
```

Import fuel prices:

```bash
python manage.py import_fuel_prices fuel-prices.csv
```

---

## Running The Application

```bash
python manage.py runserver
```

Application will be available at:

```text
http://127.0.0.1:8000/
```

---

## API Endpoint

### Calculate Route

**POST**

```text
/api/route/
```

### Request

```json
{
    "start": "Dallas, TX",
    "finish": "Phoenix, AZ"
}
```

### Response

```json
{
    "distance_miles": 1064.54,
    "duration_hours": 15.83,
    "fuel_stops": [
        {
            "city": "Jarrell",
            "state": "TX",
            "price": 2.919,
            "gallons": 50,
            "cost": 145.95
        }
    ],
    "total_fuel_cost": 145.95
}
```

---

## Optimization Logic

The application calculates the route distance and identifies fuel stations located near the route.

Fuel stops are selected according to:

* Maximum driving range of 500 miles
* Fuel price competitiveness
* Route progression toward destination

The total fuel cost is computed using:

```text
Fuel Used = Distance / 10 MPG
```

and the selected fuel station prices.

---

## Caching

Responses are cached for 24 hours using Django's cache framework.

Benefits:

* Faster repeated requests
* Reduced routing API calls
* Improved overall performance

---

## Error Handling

The API returns appropriate error responses for:

* Invalid request payloads
* Missing locations
* Geocoding failures
* Routing API failures
* Internal processing errors

---

## Example cURL Request

```bash
curl -X POST http://127.0.0.1:8000/api/route/ \
-H "Content-Type: application/json" \
-d '{
  "start": "Dallas, TX",
  "finish": "Phoenix, AZ"
}'
```

---

## Future Improvements

* PostGIS spatial queries for route proximity searches
* Redis cache backend
* Swagger/OpenAPI documentation
* Docker support
* Route visualization using GeoJSON or encoded polylines
* More advanced fuel optimization strategies

---

## Author

Developed as part of a backend engineering assessment using Django REST Framework.
