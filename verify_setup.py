"""
Setup Verification Script
Run this to check if all dependencies are installed correctly
"""
import sys

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 11:
        print("✅ Python version is compatible (3.11+)")
        return True
    else:
        print("❌ Python version too old. Need 3.11+")
        return False


def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        ("streamlit", "streamlit"),
        ("sqlalchemy", "sqlalchemy"),
        ("plotly", "plotly"),
        ("pandas", "pandas"),
        ("pydantic", "pydantic"),
        ("apscheduler", "apscheduler"),
        ("reportlab", "reportlab"),
        ("openpyxl", "openpyxl"),
        ("python-docx", "docx"),
        ("bcrypt", "bcrypt")
    ]
    
    print("\nChecking dependencies...")
    all_installed = True
    
    for display_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"❌ {display_name} - NOT INSTALLED")
            all_installed = False
    
    return all_installed


def check_database_access():
    """Check if database can be created"""
    print("\nChecking database access...")
    try:
        from database.database import init_database
        init_database()
        print("✅ Database initialization works")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False


def check_file_structure():
    """Check if all required files exist"""
    print("\nChecking file structure...")
    from pathlib import Path
    
    required_files = [
        "app.py",
        "requirements.txt",
        "database/models.py",
        "database/database.py",
        "database/seed.py",
        "engines/phase_engine.py",
        "engines/checklist_engine.py",
        "engines/revision_engine.py",
        "engines/analytics_engine.py",
        "pages/dashboard.py",
        "pages/checklist.py",
        "styles/main.css"
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    return all_exist


def main():
    print("=" * 60)
    print("Career Command Center - Setup Verification")
    print("=" * 60)
    
    results = []
    
    results.append(("Python Version", check_python_version()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("File Structure", check_file_structure()))
    results.append(("Database Access", check_database_access()))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check_name}: {status}")
    
    if all(result[1] for result in results):
        print("\n🎉 All checks passed! You're ready to run the app.")
        print("\nRun: streamlit run app.py")
    else:
        print("\n⚠️ Some checks failed. Please fix the issues above.")
        print("\nTo install dependencies: pip install -r requirements.txt")


if __name__ == "__main__":
    main()
