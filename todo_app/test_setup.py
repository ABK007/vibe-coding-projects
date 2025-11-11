"""
Quick test script to verify the setup
Run this to check if all imports work correctly
"""

import sys


def test_imports():
    """Test if all required packages can be imported"""
    try:
        print("Testing imports...")

        print("✓ Testing FastAPI...", end=" ")
        import fastapi

        print(f"OK (v{fastapi.__version__})")

        print("✓ Testing SQLAlchemy...", end=" ")
        import sqlalchemy

        print(f"OK (v{sqlalchemy.__version__})")

        print("✓ Testing Pydantic...", end=" ")
        import pydantic

        print(f"OK (v{pydantic.__version__})")

        print("✓ Testing psycopg2...", end=" ")
        import psycopg2

        print("OK")

        print("✓ Testing uvicorn...", end=" ")
        import uvicorn

        print(f"OK (v{uvicorn.__version__})")

        print("✓ Testing python-dotenv...", end=" ")
        import dotenv

        print("OK")

        print("\n✅ All imports successful!")
        print("\nNext steps:")
        print("1. Update the DATABASE_URL in .env file")
        print("2. Run: uv run python main.py")
        print("3. Open: http://localhost:8000/docs")

        return True

    except ImportError as e:
        print(f"\n❌ Import failed: {e}")
        print("\nRun: uv sync")
        return False


def test_env_file():
    """Check if .env file exists and has required variables"""
    import os
    from dotenv import load_dotenv

    print("\n\nTesting environment configuration...")

    if not os.path.exists(".env"):
        print("⚠️  .env file not found!")
        print("   Copy .env.example to .env and update the DATABASE_URL")
        return False

    load_dotenv()

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("⚠️  DATABASE_URL not set in .env file")
        return False

    if "username:password" in database_url:
        print("⚠️  DATABASE_URL contains placeholder values")
        print("   Please update with your actual PostgreSQL credentials")
        return False

    print("✓ .env file configured")
    print(f"✓ DATABASE_URL: {database_url[:30]}...")

    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Todo App - Setup Verification")
    print("=" * 60)

    imports_ok = test_imports()
    env_ok = test_env_file()

    print("\n" + "=" * 60)
    if imports_ok and env_ok:
        print("✅ Setup complete! Ready to run the application.")
    else:
        print("⚠️  Please fix the issues above before running the app.")
    print("=" * 60)
