#!/usr/bin/env python3
"""
Test script specifically for case 20-fd-1967 with enhanced secured file handling
"""

from pathlib import Path
from court_scraper import GalvestonCourtScraper

def test_case_20fd1967():
    """Test case 20-fd-1967 with visible browser first, then headless"""
    case_number = "20-FD-1967"
    download_dir = Path("test_downloads") / case_number.replace('/', '_').replace('\\', '_')
    
    print(f"Testing case: {case_number}")
    print("=" * 60)
    
    # Try with headless browser for speed
    print("Processing case with enhanced secured file handling...")
    scraper = GalvestonCourtScraper(headless=True, verbose=True)
    
    try:
        result = scraper.scrape_case(case_number, download_dir)
        
        print("\nRESULTS:")
        print("=" * 40)
        
        if result["success"]:
            print(f"SUCCESS! Case processed successfully")
            print(f"   Case: {result['case_number']}")
            print(f"   Documents found: {result['documents']}")
            print(f"   Documents downloaded: {result.get('downloaded', 0)}")
            print(f"   Secured documents: {result.get('secured', 0)}")
            print(f"   Failed downloads: {result.get('failed', 0)}")
            print(f"   Skipped (existing): {result.get('skipped', 0)}")
            
            if download_dir.exists():
                files = list(download_dir.glob("*.pdf"))
                print(f"   Total files in directory: {len(files)}")
                
                if files:
                    print(f"\nFile details:")
                    regular_files = []
                    placeholder_files = []
                    
                    for file in sorted(files):
                        size = file.stat().st_size
                        if size < 5000:  # Likely placeholder
                            placeholder_files.append((file.name, size))
                        else:  # Likely regular document
                            regular_files.append((file.name, size))
                    
                    if regular_files:
                        print(f"   Regular documents ({len(regular_files)}):")
                        for name, size in regular_files[:5]:  # Show first 5
                            print(f"     - {name} ({size:,} bytes)")
                        if len(regular_files) > 5:
                            print(f"     ... and {len(regular_files) - 5} more regular files")
                    
                    if placeholder_files:
                        print(f"   Secured/Protected documents ({len(placeholder_files)}):")
                        for name, size in placeholder_files[:5]:  # Show first 5
                            print(f"     - {name} ({size:,} bytes) [PLACEHOLDER]")
                        if len(placeholder_files) > 5:
                            print(f"     ... and {len(placeholder_files) - 5} more placeholders")
                
                # Check manifest
                manifest = download_dir / "MANIFEST.txt"
                if manifest.exists():
                    print(f"\n   Manifest created: {manifest}")
                
            return True
        else:
            print(f"FAILED: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_case_20fd1967()
    
    if success:
        print(f"\n🎉 Case 20-fd-1967 processed successfully!")
        print("Enhanced scraper handled secured files properly.")
    else:
        print(f"\n💥 Case 20-fd-1967 test failed.")
        print("This might indicate navigation issues or the case doesn't exist.")
    
    input("\nPress Enter to exit...")