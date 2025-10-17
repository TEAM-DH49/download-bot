#!/bin/bash
# Auto-refresh Instagram cookies from browser

cd ~/premium_downloader_bot

# Extract from Chrome (if logged in)
python3 << PYTHON
import browser_cookie3
import os

try:
    cj = browser_cookie3.chrome(domain_name='instagram.com')
    
    with open('instagram_cookies.txt', 'w') as f:
        f.write('# Netscape HTTP Cookie File\n')
        for cookie in cj:
            f.write(f'{cookie.domain}\tTRUE\t{cookie.path}\t'
                    f'{"TRUE" if cookie.secure else "FALSE"}\t'
                    f'{cookie.expires if cookie.expires else 0}\t'
                    f'{cookie.name}\t{cookie.value}\n')
    
    print("✅ Cookies refreshed!")
except:
    print("⚠️ Keep using existing cookies")
PYTHON
