"""
Test script to verify the RAG service installation
تحقق من أن التثبيت تم بنجاح
"""

def test_imports():
    """Test that all main imports work correctly"""
    print("Testing imports...")
    
    try:
        from src.config import get_settings
        print("✓ src.config imported successfully")
        
        from src.db.factory import make_database
        print("✓ src.db.factory imported successfully")
        
        from src.routes import ask, ping, papers
        print("✓ src.routes imported successfully")
        
        from src.models.paper import Paper
        print("✓ src.models.paper imported successfully")
        
        from src.repositories.paper import PaperRepository
        print("✓ src.repositories.paper imported successfully")
        
        from src.schemas.paper import PaperResponse
        print("✓ src.schemas.paper imported successfully")
        
        print("\n✅ All imports working correctly!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("\nPlease run: pip install -e .")
        return False

def test_settings():
    """Test that settings can be loaded"""
    print("\nTesting settings...")
    
    try:
        from src.config import get_settings
        settings = get_settings()
        print(f"✓ Settings loaded successfully")
        print(f"  - App Version: {settings.app_version}")
        print(f"  - Environment: {settings.environment}")
        print(f"  - Service Name: {settings.service_name}")
        print(f"  - Database URL: {settings.postgres_database_url}")
        return True
        
    except Exception as e:
        print(f"❌ Settings error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("RAG Service Installation Test")
    print("اختبار تثبيت خدمة RAG")
    print("=" * 60)
    print()
    
    imports_ok = test_imports()
    settings_ok = test_settings()
    
    print("\n" + "=" * 60)
    if imports_ok and settings_ok:
        print("🎉 Installation is working correctly!")
        print("🎉 التثبيت يعمل بشكل صحيح!")
        print("\nYou can now run the API with:")
        print("  uvicorn src.main:app --reload")
        print("  or")
        print("  make run-local")
    else:
        print("⚠️  There are some issues. Please run:")
        print("  pip install -e .")
    print("=" * 60)
