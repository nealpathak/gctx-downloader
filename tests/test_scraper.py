#!/usr/bin/env python3
"""
Test script for Galveston County Court Document Scraper
Quick testing with known working case numbers
"""

import sys
from pathlib import Path
# Add parent directory to path to import court_scraper
sys.path.insert(0, str(Path(__file__).parent.parent))
from court_scraper import GalvestonCourtScraper

def test_navigation_only(case_number: str):
    """Test just the navigation part without downloading"""
    print(f"Testing navigation for case: {case_number}")
    print("=" * 50)
    
    scraper = GalvestonCourtScraper(headless=False, verbose=True)
    
    try:
        # Test navigation
        html_source = scraper.navigate_to_case(case_number)
        
        if html_source:
            print("\n✓ Navigation successful!")
            
            # Parse documents
            documents = scraper.parse_documents(html_source)
            
            if documents:
                print(f"\n✓ Found {len(documents)} documents:")
                print("-" * 40)
                for i, doc in enumerate(documents[:5], 1):  # Show first 5
                    print(f"{i}. {doc.filename}")
                    print(f"   Date: {doc.date} | Type: {doc.doc_type}")
                
                if len(documents) > 5:
                    print(f"   ... and {len(documents) - 5} more documents")
                
                return True
            else:
                print("✓ Navigation successful but no documents found")
                return True
        else:
            print("✗ Navigation failed")
            return False
    
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False
    
    finally:
        scraper.close_driver()

def test_full_scrape(case_number: str):
    """Test complete scrape process including downloads"""
    print(f"Testing full scrape for case: {case_number}")
    print("=" * 50)
    
    download_dir = Path("test_downloads") / case_number.replace('/', '_').replace('\\', '_')
    
    scraper = GalvestonCourtScraper(headless=True, verbose=True)  # Headless for faster testing
    result = scraper.scrape_case(case_number, download_dir)
    
    if result["success"]:
        print(f"\n✓ Full scrape successful!")
        print(f"  Documents found: {result['documents']}")
        print(f"  Documents downloaded: {result['downloaded']}")
        print(f"  Files saved to: {download_dir.absolute()}")
        return True
    else:
        print(f"\n✗ Full scrape failed: {result['error']}")
        return False

def test_multiple_cases():
    """Test multiple case numbers to verify robustness"""
    test_cases = [
        "25-CV-0880",  # Known working case
        "24-CV-1234",  # Test case (may not exist)
        "23-CV-5678"   # Test case (may not exist)
    ]
    
    print("Testing multiple case numbers...")
    print("=" * 60)
    
    results = {}
    
    for case_number in test_cases:
        print(f"\nTesting case: {case_number}")
        print("-" * 30)
        
        scraper = GalvestonCourtScraper(headless=True, verbose=False)  # Quiet mode
        result = scraper.scrape_case(case_number)
        results[case_number] = result
        
        if result["success"]:
            if result["documents"] > 0:
                print(f"✓ {case_number}: {result['documents']} documents found")
            else:
                print(f"✓ {case_number}: No documents (case may be empty)")
        else:
            print(f"✗ {case_number}: {result['error']}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    successful = sum(1 for r in results.values() if r["success"])
    total_docs = sum(r.get("documents", 0) for r in results.values() if r["success"])
    
    print(f"Cases tested: {len(test_cases)}")
    print(f"Successful: {successful}")
    print(f"Total documents found: {total_docs}")
    
    return results

def main():
    """Main test function"""
    print("Galveston County Court Document Scraper - Test Suite")
    print("=" * 60)
    
    while True:
        print("\nTest Options:")
        print("1. Test navigation only (with visible browser)")
        print("2. Test full scrape (navigation + download)")
        print("3. Test multiple cases (robustness test)")
        print("4. Exit")
        
        choice = input("\nSelect test (1-4): ").strip()
        
        if choice == "1":
            case_number = input("Enter case number (or press Enter for 25-CV-0880): ").strip()
            if not case_number:
                case_number = "25-CV-0880"
            test_navigation_only(case_number)
            
        elif choice == "2":
            case_number = input("Enter case number (or press Enter for 25-CV-0880): ").strip()
            if not case_number:
                case_number = "25-CV-0880"
            test_full_scrape(case_number)
            
        elif choice == "3":
            test_multiple_cases()
            
        elif choice == "4":
            break
            
        else:
            print("Invalid choice. Please enter 1-4.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()