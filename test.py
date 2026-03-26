#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main.py - Fampiasana ny requests_html module
Maneho ny fomba fampiasana requests (sync) sy arequests (async)
"""

import asyncio
import time
from requests_html import (
    HTMLSession,      # Session sync
    AsyncHTMLSession, # Session async
    requests,         # Requests sync (toy ny tany am-boalohany)
    arequests,        # Requests async (vaovao)
    user_agent        # Maka user-agent
)


# ============================================
# 1. TEST SYNC REQUESTS (mahazatra)
# ============================================

def test_sync_requests():
    """Test ny requests mahazatra (synchronous)"""
    print("\n" + "="*50)
    print("1. TEST SYNC REQUESTS")
    print("="*50)
    
    # GET request
    print("\n📡 GET request:")
    resp = requests.get('https://httpbin.org/get')
    print(f"   Status: {resp.status_code}")
    print(f"   URL: {resp.url}")
    data = resp.json()
    print(f"   User-Agent: {data.get('headers', {}).get('User-Agent', 'N/A')[:50]}...")
    
    # POST request
    print("\n📝 POST request:")
    resp = requests.post(
        'https://httpbin.org/post',
        json={'name': 'Rakoto', 'age': 25}
    )
    print(f"   Status: {resp.status_code}")
    data = resp.json()
    print(f"   Data nampidirina: {data.get('json', {})}")
    
    # Headers
    print("\n📋 Manova headers:")
    custom_headers = {'X-Custom-Header': 'TestValue'}
    resp = requests.get('https://httpbin.org/headers', headers=custom_headers)
    data = resp.json()
    print(f"   Headers nandefasana: {data.get('headers', {}).get('X-Custom-Header', 'N/A')}")
    
    return "✅ Sync requests test passed!"


# ============================================
# 2. TEST HTML SESSION SYNC
# ============================================

def test_html_session():
    """Test ny HTMLSession (sync)"""
    print("\n" + "="*50)
    print("2. TEST HTML SESSION SYNC")
    print("="*50)
    
    session = HTMLSession()
    
    # Maka pejy iray
    print("\n🌐 Maka pejy https://example.com:")
    r = session.get('https://example.com')
    print(f"   Status: {r.status_code}")
    print(f"   Title: {r.html.find('title', first=True).text}")
    print(f"   Text vohiny: {r.html.text[:100]}...")
    
    # Mikaroka links
    print("\n🔗 Links hita:")
    links = list(r.html.links)[:5]
    for link in links:
        print(f"   - {link}")
    
    # Mampiasa find() sy xpath()
    print("\n🔍 Mikaroka element amin'ny CSS selector:")
    paragraphs = r.html.find('p')
    print(f"   Paragraphs hita: {len(paragraphs)}")
    for i, p in enumerate(paragraphs[:3]):
        print(f"   P{i+1}: {p.text[:60]}...")
    
    # XPath
    print("\n🎯 Mikaroka amin'ny XPath:")
    h1 = r.html.xpath('//h1', first=True)
    if h1:
        print(f"   H1: {h1.text}")
    
    session.close()
    return "✅ HTML Session test passed!"


# ============================================
# 3. TEST ASYNC REQUESTS (arequests)
# ============================================

async def test_async_requests():
    """Test ny arequests (asynchronous)"""
    print("\n" + "="*50)
    print("3. TEST ASYNC REQUESTS (arequests)")
    print("="*50)
    
    # GET request
    print("\n📡 GET request async:")
    async with arequests as req:
        resp = await req.get('https://httpbin.org/get')
        print(f"   Status: {resp.status_code}")
        data = await resp.json()
        print(f"   URL: {data.get('url', 'N/A')}")
        
        # POST request
        print("\n📝 POST request async:")
        post_resp = await req.post(
            'https://httpbin.org/post',
            json={'message': 'Hello from async!', 'language': 'Malagasy'}
        )
        post_data = await post_resp.json()
        print(f"   Status: {post_resp.status_code}")
        print(f"   Data nampidirina: {post_data.get('json', {})}")
        
        # TEXT response
        print("\n📄 Maka text:")
        text_resp = await req.get('https://example.com')
        text = await text_resp.text
        print(f"   Status: {text_resp.status_code}")
        print(f"   Text vohiny: {text[:100]}...")
    
    return "✅ Async requests test passed!"


# ============================================
# 4. TEST CONCURRENT ASYNC REQUESTS
# ============================================

async def fetch_multiple(urls):
    """Maka URL maro miaraka (concurrent)"""
    async with arequests as req:
        tasks = []
        for url in urls:
            tasks.append(req.get(url))
        
        # Mandeha miaraka ny requests rehetra
        responses = await asyncio.gather(*tasks)
        
        results = []
        for resp in responses:
            results.append({
                'url': str(resp.url),
                'status': resp.status_code,
                'size': len(await resp.text)
            })
        return results


async def test_concurrent_requests():
    """Test concurrent requests miaraka"""
    print("\n" + "="*50)
    print("4. TEST CONCURRENT ASYNC REQUESTS")
    print("="*50)
    
    urls = [
        'https://httpbin.org/get',
        'https://example.com',
        'https://httpbin.org/status/200',
        'https://httpbin.org/delay/1',  # 1 segondra delay
        'https://httpbin.org/headers',
    ]
    
    print(f"\n🚀 Maka URL {len(urls)} miaraka...")
    print(f"   URLs: {[u.split('/')[-1] for u in urls]}")
    
    start = time.time()
    results = await fetch_multiple(urls)
    elapsed = time.time() - start
    
    print(f"\n📊 Valiny:")
    for r in results:
        print(f"   {r['url']:<50} -> {r['status']} ({r['size']} bytes)")
    
    print(f"\n⏱️ Fotoana nandeha: {elapsed:.2f} segondra")
    print(f"   Raha nifandimby (sync): ~5 segondra mahery")
    
    return "✅ Concurrent requests test passed!"


# ============================================
# 5. TEST ASYNC HTML SESSION
# ============================================

async def test_async_html_session():
    """Test ny AsyncHTMLSession"""
    print("\n" + "="*50)
    print("5. TEST ASYNC HTML SESSION")
    print("="*50)
    
    session = AsyncHTMLSession()
    
    print("\n🌐 Maka pejy https://example.com (async):")
    r = await session.get('https://example.com')
    print(f"   Status: {r.status_code}")
    print(f"   Title: {r.html.find('title', first=True).text}")
    print(f"   Full text: {r.html.full_text[:100]}...")
    
    # Mikaroka links
    print("\n🔗 Absolute links:")
    abs_links = list(r.html.absolute_links)[:5]
    for link in abs_links:
        print(f"   - {link}")
    
    await session.close()
    return "✅ Async HTML Session test passed!"


# ============================================
# 6. TEST USER-AGENT
# ============================================

def test_user_agent():
    """Test user-agent generator"""
    print("\n" + "="*50)
    print("6. TEST USER-AGENT")
    print("="*50)
    
    # User-agent default
    ua_default = user_agent()
    print(f"\n🖥️ Default user-agent: {ua_default}")
    
    # User-agent chrome
    ua_chrome = user_agent('chrome')
    print(f"🖥️ Chrome user-agent: {ua_chrome}")
    
    # User-agent firefox
    ua_firefox = user_agent('firefox')
    print(f"🖥️ Firefox user-agent: {ua_firefox}")
    
    # User-agent safari
    ua_safari = user_agent('safari')
    print(f"🖥️ Safari user-agent: {ua_safari}")
    
    # User-agent random
    ua_random = user_agent('random')
    print(f"🖥️ Random user-agent: {ua_random}")
    
    return "✅ User-agent test passed!"


# ============================================
# 7. TEST ERROR HANDLING
# ============================================

async def test_error_handling():
    """Test fikarakarana erreur"""
    print("\n" + "="*50)
    print("7. TEST ERROR HANDLING")
    print("="*50)
    
    # URL tsy misy
    print("\n⚠️ URL tsy misy (404):")
    resp = requests.get('https://httpbin.org/status/404')
    print(f"   Status: {resp.status_code}")
    
    # URL tsy mety
    print("\n⚠️ URL tsy mety (invalid):")
    try:
        resp = requests.get('https://thisurldoesnotexist123456789.com')
    except Exception as e:
        print(f"   Error: {type(e).__name__}: {str(e)[:60]}...")
    
    # Timeout
    print("\n⏰ Timeout test:")
    try:
        resp = requests.get('https://httpbin.org/delay/3', timeout=1)
    except Exception as e:
        print(f"   Error: {type(e).__name__}: {str(e)}")
    
    return "✅ Error handling test passed!"


# ============================================
# 8. BENCHMARK: SYNC VS ASYNC
# ============================================

async def benchmark_sync_vs_async():
    """Fampitahana ny hafainganam-pandeha sync vs async"""
    print("\n" + "="*50)
    print("8. BENCHMARK: SYNC VS ASYNC")
    print("="*50)
    
    urls = [
        'https://httpbin.org/get',
        'https://httpbin.org/status/200',
        'https://httpbin.org/headers',
        'https://httpbin.org/user-agent',
    ]
    
    # TEST SYNC (mifandimby)
    print("\n🐢 SYNC (mifandimby):")
    start = time.time()
    for url in urls:
        resp = requests.get(url)
        print(f"   {url.split('/')[-1]}: {resp.status_code}")
    sync_time = time.time() - start
    print(f"   ⏱️ Fotoana: {sync_time:.2f} segondra")
    
    # TEST ASYNC (miaraka)
    print("\n🐇 ASYNC (miaraka):")
    start = time.time()
    async with arequests as req:
        tasks = [req.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        for resp in responses:
            print(f"   {str(resp.url).split('/')[-1]}: {resp.status_code}")
    async_time = time.time() - start
    print(f"   ⏱️ Fotoana: {async_time:.2f} segondra")
    
    print(f"\n📊 Fampitahana:")
    print(f"   Sync:  {sync_time:.2f}s")
    print(f"   Async: {async_time:.2f}s")
    print(f"   ✅ Async dia {sync_time/async_time:.1f}x haingana kokoa!")
    
    return "✅ Benchmark test passed!"


# ============================================
# 9. TEST MIXED: SYNC + ASYNC
# ============================================

async def test_mixed_sync_async():
    """Fampiasana sync sy async miaraka"""
    print("\n" + "="*50)
    print("9. TEST MIXED: SYNC + ASYNC")
    print("="*50)
    
    # Sync request aloha
    print("\n🔵 Sync request aloha:")
    sync_resp = requests.get('https://httpbin.org/get')
    print(f"   Sync status: {sync_resp.status_code}")
    
    # Async request aoriany
    print("\n🟢 Async request aoriany:")
    async with arequests as req:
        async_resp = await req.get('https://httpbin.org/get')
        print(f"   Async status: {async_resp.status_code}")
        data = await async_resp.json()
        print(f"   Async URL: {data.get('url')}")
    
    # Mampiasa HTMLSession sy arequests miaraka
    print("\n🟣 HTMLSession + arequests:")
    session = HTMLSession()
    r = session.get('https://example.com')
    print(f"   HTML title: {r.html.find('title', first=True).text}")
    
    async with arequests as req:
        aresp = await req.get('https://httpbin.org/get')
        print(f"   Async status: {aresp.status_code}")
    
    session.close()
    return "✅ Mixed sync/async test passed!"


# ============================================
# 10. TEST WEB SCRAPING SIMPLE
# ============================================

async def test_web_scraping():
    """Test web scraping minimal"""
    print("\n" + "="*50)
    print("10. TEST WEB SCRAPING")
    print("="*50)
    
    # Mampiasa HTMLSession
    print("\n🔍 Scraping https://example.com:")
    session = HTMLSession()
    r = session.get('https://example.com')
    
    # Maka ny lohateny
    title = r.html.find('title', first=True)
    print(f"   Title: {title.text if title else 'N/A'}")
    
    # Maka ny h1
    h1 = r.html.find('h1', first=True)
    print(f"   H1: {h1.text if h1 else 'N/A'}")
    
    # Maka ny paragraphs rehetra
    paragraphs = r.html.find('p')
    print(f"   Paragraphs: {len(paragraphs)}")
    for i, p in enumerate(paragraphs):
        print(f"   P{i+1}: {p.text[:80]}...")
    
    # Maka ny links
    links = r.html.absolute_links
    print(f"   Links: {len(links)}")
    for link in list(links)[:3]:
        print(f"     - {link}")
    
    session.close()
    return "✅ Web scraping test passed!"


# ============================================
# MAIN FUNCTION
# ============================================

async def run_all_tests():
    """Mampandeha ny tests rehetra"""
    print("\n" + "█"*50)
    print("🚀 REQUESTS-HTML TEST SUITE")
    print("█"*50)
    
    results = []
    
    # Sync tests
    try:
        results.append(test_sync_requests())
    except Exception as e:
        results.append(f"❌ Sync requests test failed: {e}")
    
    try:
        results.append(test_html_session())
    except Exception as e:
        results.append(f"❌ HTML Session test failed: {e}")
    
    try:
        results.append(test_user_agent())
    except Exception as e:
        results.append(f"❌ User-agent test failed: {e}")
    
    # Async tests
    try:
        results.append(await test_async_requests())
    except Exception as e:
        results.append(f"❌ Async requests test failed: {e}")
    
    try:
        results.append(await test_concurrent_requests())
    except Exception as e:
        results.append(f"❌ Concurrent requests test failed: {e}")
    
    try:
        results.append(await test_async_html_session())
    except Exception as e:
        results.append(f"❌ Async HTML Session test failed: {e}")
    
    try:
        results.append(await test_error_handling())
    except Exception as e:
        results.append(f"❌ Error handling test failed: {e}")
    
    try:
        results.append(await benchmark_sync_vs_async())
    except Exception as e:
        results.append(f"❌ Benchmark test failed: {e}")
    
    try:
        results.append(await test_mixed_sync_async())
    except Exception as e:
        results.append(f"❌ Mixed sync/async test failed: {e}")
    
    try:
        results.append(await test_web_scraping())
    except Exception as e:
        results.append(f"❌ Web scraping test failed: {e}")
    
    # Summary
    print("\n" + "="*50)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*50)
    
    passed = [r for r in results if r.startswith('✅')]
    failed = [r for r in results if r.startswith('❌')]
    
    for r in results:
        print(f"   {r}")
    
    print(f"\n✅ Passed: {len(passed)}/{len(results)}")
    if failed:
        print(f"❌ Failed: {len(failed)}")
    
    print("\n🎉 Fitsapana vita!")


# ============================================
# FANDEHANANA
# ============================================

if __name__ == "__main__":
    # Mampandeha ny tests rehetra
    asyncio.run(run_all_tests())
