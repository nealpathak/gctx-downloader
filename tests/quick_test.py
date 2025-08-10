#!/usr/bin/env python3
"""
Quick automated test of court_scraper.py with case 25-CV-0880
"""

import sys
from pathlib import Path
# Add parent directory to path to import court_scraper
sys.path.insert(0, str(Path(__file__).parent.parent))
from court_scraper import GalvestonCourtScraper

def test_case_25_cv_0880():
    """Test the known working case 25-CV-0880"""
    print("Testing Galveston Court Scraper with case 25-CV-0880")
    print("=" * 60)
    
    case_number = "25-CV-0880"
    download_dir = Path("test_downloads") / case_number
    
    # Create scraper instance
    scraper = GalvestonCourtScraper(headless=True, verbose=True)
    
    try:
        print(f"Starting scrape for case: {case_number}")
        print("-" * 40)
        
        # Run complete scrape
        result = scraper.scrape_case(case_number, download_dir)
        
        print("\n" + "=" * 60)
        print("TEST RESULTS:")
        
        if result["success"]:
            print(f"✅ SUCCESS!")
            print(f"   Case: {result['case_number']}")
            print(f"   Documents found: {result['documents']}")
            print(f"   Documents downloaded: {result['downloaded']}")
            
            if download_dir.exists():
                files = list(download_dir.glob("*.pdf"))
                print(f"   Files in directory: {len(files)}")
                print(f"   Download directory: {download_dir}")
                
                # Show first few files
                if files:
                    print("\n   Sample files:")
                    for file in files[:3]:
                        size = file.stat().st_size
                        print(f"   - {file.name} ({size:,} bytes)")
                    
                    if len(files) > 3:
                        print(f"   ... and {len(files) - 3} more files")
                
                # Check for manifest
                manifest = download_dir / "MANIFEST.txt"
                if manifest.exists():
                    print(f"   ✅ Manifest created: {manifest}")
                else:
                    print(f"   ⚠️  No manifest found")
            
            return True
        else:
            print(f"❌ FAILED!")
            print(f"   Error: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ TEST EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_case_25_cv_0880()
    
    if success:
        print("\n🎉 Court scraper is working correctly!")
        print("Ready to use with: python court_scraper.py")
    else:
        print("\n💥 Court scraper test failed!")
        print("Check the error messages above")
    
    input("\nPress Enter to exit...")