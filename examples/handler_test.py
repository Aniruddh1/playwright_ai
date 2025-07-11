"""Test the implemented handlers with real functionality."""

import asyncio
import sys
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent))

from playwright_ai import PlaywrightAI


class WebsiteInfo(BaseModel):
    """Model for extracting website information."""
    title: str
    main_heading: Optional[str] = None
    description: Optional[str] = None
    links_count: int = 0
    has_form: bool = False


async def main():
    """Test handler functionality."""
    print("Testing PlaywrightAI handlers...")
    
    try:
        # Create PlaywrightAI instance
        async with PlaywrightAI(
            headless=False,
            verbose=2,
            enable_caching=True,
        ) as browser:
            print(f"\n[OK] PlaywrightAI initialized")
            
            # Create a page
            page = await browser.page()
            print(f"[OK] Page created")
            
            # Navigate to a test website
            await page.goto("https://example.com")
            print(f"[OK] Navigated to: {page.url}")
            
            # Test 1: Observe elements on the page
            print("\n--- Testing Observe Handler ---")
            elements = await page.observe()
            print(f"[OK] Found {len(elements)} elements")
            for i, elem in enumerate(elements[:3]):
                print(f"  {i+1}. {elem.description} [{elem.selector}]")
            
            # Test 2: Extract structured data
            print("\n--- Testing Extract Handler ---")
            website_info = await page.extract(
                WebsiteInfo,
                instruction="Extract information about this website"
            )
            print(f"[OK] Extracted data:")
            print(f"  Title: {website_info.data.title}")
            print(f"  Main heading: {website_info.data.main_heading}")
            print(f"  Description: {website_info.data.description}")
            print(f"  Links count: {website_info.data.links_count}")
            print(f"  Has form: {website_info.data.has_form}")
            
            # Test 3: Act on an element
            print("\n--- Testing Act Handler ---")
            # Try to click on "More information" link
            act_result = await page.act("Click on the More information link")
            print(f"[OK] Action result: {act_result.success}")
            if act_result.success:
                print(f"  Action: {act_result.action}")
                print(f"  Description: {act_result.description}")
                
                # Wait for navigation
                await asyncio.sleep(2)
                print(f"  New URL: {page.url}")
            
            # Test 4: Observe with specific instruction
            print("\n--- Testing Observe with instruction ---")
            links = await page.observe("Find all links on the page")
            print(f"[OK] Found {len(links)} links")
            for i, link in enumerate(links[:3]):
                print(f"  {i+1}. {link.description} [{link.selector}]")
            
            # Wait before closing
            await asyncio.sleep(3)
            
        print("\n[OK] All handler tests completed!")
        
    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())