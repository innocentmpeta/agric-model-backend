import sys
print(f"Python version: {sys.version}")

try:
    import fastapi
    print(f"✓ FastAPI: {fastapi.__version__}")
except ImportError:
    print("✗ FastAPI not installed")

try:
    import uvicorn
    print(f"✓ Uvicorn installed")
except ImportError:
    print("✗ Uvicorn not installed")

try:
    import numpy
    print(f"✓ NumPy: {numpy.__version__}")
except ImportError:
    print("✗ NumPy not installed")

try:
    import pandas
    print(f"✓ Pandas: {pandas.__version__}")
except ImportError:
    print("✗ Pandas not installed")