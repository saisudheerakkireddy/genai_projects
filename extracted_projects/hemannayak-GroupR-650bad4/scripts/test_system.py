#!/usr/bin/env python3
"""
Quick system test to verify all components work
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def test_imports():
    """Test all imports work"""
    print("🧪 Testing imports...")
    try:
        from backend.models import DisasterEvent, DisasterType, Severity
        from backend.processing.extractor import DisasterInfoExtractor
        from backend.rag.vector_store import DisasterVectorStore
        from backend.rag.query_engine import DisasterQueryEngine
        from backend.agents.resource_matcher import ResourceMatcher
        from backend.utils.data_loader import load_disaster_tweets
        from backend.utils.geocoder import LocationGeocoder
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_data_loading():
    """Test data loading"""
    print("\n🧪 Testing data loading...")
    try:
        from backend.utils.data_loader import load_disaster_tweets
        tweets = load_disaster_tweets('data/raw/disaster_tweets.csv')
        print(f"✅ Loaded {len(tweets)} tweets")
        return len(tweets) > 0
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

def test_extractor():
    """Test information extraction"""
    print("\n🧪 Testing extractor...")
    try:
        from backend.processing.extractor import DisasterInfoExtractor
        extractor = DisasterInfoExtractor()
        result = extractor.extract("URGENT: Earthquake hit downtown, buildings collapsed!")
        print(f"✅ Extraction works: {result.disaster_type} - {result.severity}")
        return True
    except Exception as e:
        print(f"❌ Extractor failed: {e}")
        return False

def test_vector_store():
    """Test vector store"""
    print("\n🧪 Testing vector store...")
    try:
        from backend.rag.vector_store import DisasterVectorStore
        vs = DisasterVectorStore('data/chromadb')
        stats = vs.get_stats()
        print(f"✅ Vector store works: {stats.get('total_documents', 0)} documents")
        return True
    except Exception as e:
        print(f"❌ Vector store failed: {e}")
        return False

def test_query_engine():
    """Test query engine"""
    print("\n🧪 Testing query engine...")
    try:
        from backend.rag.vector_store import DisasterVectorStore
        from backend.rag.query_engine import DisasterQueryEngine
        import asyncio
        
        vs = DisasterVectorStore('data/chromadb')
        qe = DisasterQueryEngine(vs)
        
        async def run_query():
            result = await qe.query("earthquake")
            return result
        
        result = asyncio.run(run_query())
        print(f"✅ Query engine works: {len(result.sources)} sources")
        return True
    except Exception as e:
        print(f"❌ Query engine failed: {e}")
        return False

def test_resource_matcher():
    """Test resource matcher"""
    print("\n🧪 Testing resource matcher...")
    try:
        from backend.agents.resource_matcher import ResourceMatcher, MOCK_RESOURCES
        from backend.models import DisasterEvent, DisasterType, Severity
        from datetime import datetime
        
        matcher = ResourceMatcher()
        
        # Create test event
        event = DisasterEvent(
            id="test_1",
            text="Emergency",
            timestamp=datetime.now(),
            location="Mumbai",
            coordinates=(19.0760, 72.8777),
            disaster_type=DisasterType.EARTHQUAKE,
            severity=Severity.CRITICAL,
            confidence=0.9,
            source="test",
            needs=["rescue"],
            is_verified=False
        )
        
        matches = matcher.match_resources(event, k=3)
        print(f"✅ Resource matcher works: {len(matches)} matches found")
        return True
    except Exception as e:
        print(f"❌ Resource matcher failed: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 DisasterLens AI - System Test")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Data Loading", test_data_loading),
        ("Extractor", test_extractor),
        ("Vector Store", test_vector_store),
        ("Query Engine", test_query_engine),
        ("Resource Matcher", test_resource_matcher),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} crashed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 Test Results")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n🎯 Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to run.")
        print("\nNext steps:")
        print("1. Make sure .env has HF_TOKEN")
        print("2. Run: uvicorn backend.main:app --reload --port 8000")
        print("3. Run: streamlit run frontend/app.py")
    else:
        print("\n⚠️ Some tests failed. Check errors above.")
        print("\nCommon fixes:")
        print("- Run: python scripts/generate_sample_data.py")
        print("- Run: python scripts/initialize_system.py")
        print("- Check .env file exists")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
