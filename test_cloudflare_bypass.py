#!/usr/bin/env python3
"""
Test script to verify Cloudflare bypass functionality.
Run this to ensure browser automation is working correctly.
"""

from casased import get_history, get_intraday, loadmany
import sys

def test_single_stock():
    """Test single stock historical data retrieval."""
    print("=" * 60)
    print("Test 1: Single Stock (BCP)")
    print("=" * 60)
    try:
        data = get_history('BCP', start='2024-06-01', end='2024-06-30')
        if not data.empty:
            print(f"✓ Success! Retrieved {len(data)} records")
            print(f"  Columns: {list(data.columns)}")
            print(f"  Date range: {data.index.min()} to {data.index.max()}")
            return True
        else:
            print("✗ Failed: Empty dataframe")
            return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def test_masi_index():
    """Test MASI index data retrieval."""
    print("\n" + "=" * 60)
    print("Test 2: MASI Index")
    print("=" * 60)
    try:
        masi = get_history('MASI')
        if not masi.empty:
            print(f"✓ Success! Retrieved {len(masi)} records")
            print(f"  Latest value: {masi.iloc[-1]['Value']:.2f}")
            print(f"  Latest date: {masi.index[-1]}")
            return True
        else:
            print("✗ Failed: Empty dataframe")
            return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def test_multiple_assets():
    """Test loading multiple assets."""
    print("\n" + "=" * 60)
    print("Test 3: Multiple Assets")
    print("=" * 60)
    try:
        data = loadmany(['BCP', 'Attijariwafa'], start='2024-06-01', end='2024-06-10')
        if not data.empty:
            print(f"✓ Success! Retrieved data for {data.shape[1]} assets")
            print(f"  Shape: {data.shape}")
            print(f"  Assets: {list(data.columns)}")
            return True
        else:
            print("✗ Failed: Empty dataframe")
            return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def main():
    """Run all tests."""
    print("\nCasased Cloudflare Bypass Test Suite")
    print("=" * 60)
    print("This will test if browser automation is working correctly.")
    print("Each test may take 10-30 seconds with browser automation.")
    print("=" * 60 + "\n")
    
    results = []
    results.append(("Single Stock", test_single_stock()))
    results.append(("MASI Index", test_masi_index()))
    results.append(("Multiple Assets", test_multiple_assets()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:.<40} {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print("=" * 60)
    print(f"Total: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed! Browser automation is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total_tests - total_passed} test(s) failed.")
        print("   Make sure you have installed: pip install nodriver seleniumbase")
        return 1

if __name__ == "__main__":
    sys.exit(main())
