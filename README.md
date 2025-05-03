webhook_service/
├── app/
│   ├── __init__.py
│   ├── api/                    # FastAPI Routers
│   │   ├── __init__.py
│   │   ├── subscriptions.py   # Subscription CRUD APIs
│   │   ├── ingest.py          # Webhook ingestion endpoint
│   │   └── status.py          # Status & analytics APIs
│   ├── core/                  # Core logic/helpers
│   │   ├── __init__.py
│   │   ├── config.py          # Environment variables/config
│   │   ├── security.py        # Signature validation (HMAC)
│   │   └── cache.py           # Redis caching helpers
│   ├── models/                
│   │   ├── __init__.py
│   │   ├── subscription.py    # Subscription model
│   │   ├── delivery_log.py    # Delivery log model
│   │   └── webhook.py         # Webhook payload model
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── subscription.py
│   │   ├── delivery_log.py
│   │   └── webhook.py
│   ├── database.py            # SQLAlchemy setup
│   ├── worker.py              # Celery worker entry point
│   └── background_tasks/
│       ├── __init__.py
│       └── delivery_worker.py # Async delivery & retry logic
├── ui/                        # Optional simple HTML UI
│   ├── index.html
│   └── style.css
├── tests/                     # Unit/Integration tests
│   ├── __init__.py
│   ├── test_subscriptions.py
│   └── test_ingest.py
├── logs/                      # Log storage (rotate/delete)
│   └── .gitkeep
├── README.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── create_structure.py        # CLI: Auto-generate folders/files



Alembic tracks changes in your models and creates scripts to apply them to the DB — this is more maintainable and production-ready than manually writing SQL.