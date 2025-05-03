import os

folders = [
    "app/api",
    "app/models",
    "app/schemas",
    "app/core",
    "app/background_tasks",
    "logs",
    "ui",
    "tests"
]

files = [
    "app/__init__.py",
    "app/api/__init__.py",
    "app/api/subscriptions.py",
    "app/api/ingest.py",
    "app/api/status.py",
    "app/models/__init__.py",
    "app/models/subscription.py",
    "app/models/delivery_log.py",
    "app/models/webhook.py",
    "app/schemas/__init__.py",
    "app/schemas/subscription.py",
    "app/schemas/delivery_log.py",
    "app/schemas/webhook.py",
    "app/core/__init__.py",
    "app/core/config.py",
    "app/core/security.py",
    "app/core/cache.py",
    "app/database.py",
    "app/worker.py",
    "app/background_tasks/__init__.py",
    "app/background_tasks/delivery_worker.py",
    "ui/index.html",
    "ui/style.css",
    "tests/__init__.py",
    "tests/test_subscriptions.py",
    "tests/test_ingest.py",
    "README.md",
    "requirements.txt",
    "Dockerfile",
    "docker-compose.yml"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            f.write("# Auto-generated\n")

print("✅ Project structure created.")

