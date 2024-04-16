# resy-hacking

Bot to get reservations from resy

## Getting Started

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Starting Up

```
celery -A main beat --loglevel=info
celery -A tasks worker --loglevel=info --concurrency=1 -Q l
```
