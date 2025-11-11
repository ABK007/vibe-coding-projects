# Run Commands (Windows Command Prompt)

# Install dependencies

uv sync

# Run the application in development mode

uv run python main.py

# Run with uvicorn directly

uv run uvicorn main:app --reload

# Run on a specific port

uv run uvicorn main:app --reload --port 8080

# Run in production mode (no reload)

uv run uvicorn main:app --host 0.0.0.0 --port 8000

# Check installed packages

uv pip list

# Add a new package

uv add package-name

# Remove a package

uv remove package-name

# Update all packages

uv sync --upgrade
