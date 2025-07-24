"""
Different checker implementations for various platform types.
"""

import requests
import time
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json

class BaseChecker:
    """Base class for all checkers."""
    
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.session = requests.Session()
        # Set a user agent to avoid blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def check(self, platform_name, platform_config, username):
        """Check username availability on the platform."""
        raise NotImplementedError
    
    def _make_request(self, method, url, **kwargs):
        """Make HTTP request with error handling."""
        start_time = time.time()
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            response_time = round((time.time() - start_time) * 1000, 2)
            return response, response_time
        except requests.RequestException as e:
            response_time = round((time.time() - start_time) * 1000, 2)
            # Silently handle errors - don't raise in normal mode
            return None, response_time

class StandardChecker(BaseChecker):
    """Standard checker that uses HTTP status codes."""
    
    def check(self, platform_name, platform_config, username):
        url = platform_config['url_pattern'].format(username=username)
        method = platform_config.get('method', 'GET')
        
        try:
            result = self._make_request(method, url)
            if result is None:
                return {
                    'platform': platform_name,
                    'username': username,
                    'status': 'unknown',
                    'url': url,
                    'response_time': 0,
                    'category': platform_config.get('category', 'unknown')
                }
            
            response, response_time = result
            
            # Determine availability based on status code
            if response.status_code == 404:
                status = 'available'
            elif response.status_code == 200:
                status = 'taken'
            else:
                status = 'unknown'
            
            return {
                'platform': platform_name,
                'username': username,
                'status': status,
                'url': url,
                'status_code': response.status_code,
                'response_time': response_time,
                'category': platform_config.get('category', 'unknown')
            }
            
        except Exception as e:
            raise Exception(f"Standard check failed: {e}")

class ProfileChecker(BaseChecker):
    """Checker that analyzes page content to determine availability."""
    
    def check(self, platform_name, platform_config, username):
        url = platform_config['url_pattern'].format(username=username)
        method = platform_config.get('method', 'GET')
        
        try:
            response, response_time = self._make_request(method, url)
            
            # Check for specific indicators in the response
            content = response.text.lower()
            
            # Platform-specific content checks
            not_found_indicators = platform_config.get('not_found_indicators', [
                'user not found',
                'profile not found',
                'page not found',
                'does not exist',
                'user does not exist'
            ])
            
            found_indicators = platform_config.get('found_indicators', [
                'profile',
                'posts',
                'followers',
                'following'
            ])
            
            # Check for "not found" indicators
            for indicator in not_found_indicators:
                if indicator.lower() in content:
                    status = 'available'
                    break
            else:
                # Check for "found" indicators if no "not found" found
                if response.status_code == 200:
                    for indicator in found_indicators:
                        if indicator.lower() in content:
                            status = 'taken'
                            break
                    else:
                        status = 'unknown'
                else:
                    status = 'available' if response.status_code == 404 else 'unknown'
            
            return {
                'platform': platform_name,
                'username': username,
                'status': status,
                'url': url,
                'status_code': response.status_code,
                'response_time': response_time,
                'category': platform_config.get('category', 'unknown')
            }
            
        except Exception as e:
            raise Exception(f"Profile check failed: {e}")

class APIChecker(BaseChecker):
    """Checker for platforms that provide API endpoints."""
    
    def check(self, platform_name, platform_config, username):
        api_url = platform_config['api_url'].format(username=username)
        headers = platform_config.get('headers', {})
        
        try:
            response, response_time = self._make_request('GET', api_url, headers=headers)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    # Check if user exists in API response
                    exists_field = platform_config.get('exists_field', 'exists')
                    if exists_field in data:
                        status = 'taken' if data[exists_field] else 'available'
                    else:
                        status = 'taken'  # Assume taken if API returns data
                except json.JSONDecodeError:
                    status = 'unknown'
            elif response.status_code == 404:
                status = 'available'
            else:
                status = 'unknown'
            
            profile_url = platform_config['url_pattern'].format(username=username)
            
            return {
                'platform': platform_name,
                'username': username,
                'status': status,
                'url': profile_url,
                'api_url': api_url,
                'status_code': response.status_code,
                'response_time': response_time,
                'category': platform_config.get('category', 'unknown')
            }
            
        except Exception as e:
            raise Exception(f"API check failed: {e}")

class SocialMediaChecker(BaseChecker):
    """Specialized checker for social media platforms."""
    
    def check(self, platform_name, platform_config, username):
        url = platform_config['url_pattern'].format(username=username)
        
        try:
            response, response_time = self._make_request('GET', url)
            
            # Many social media platforms return 200 even for non-existent users
            # but include specific content or meta tags
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Check page title
                title = soup.find('title')
                if title:
                    title_text = title.get_text().lower()
                    if any(phrase in title_text for phrase in ['not found', 'doesn\'t exist', 'user not found']):
                        status = 'available'
                    else:
                        status = 'taken'
                else:
                    status = 'unknown'
                    
                # Additional checks for specific platforms
                platform_lower = platform_name.lower()
                if platform_lower == 'twitter' or platform_lower == 'x':
                    # Check for suspended account or not found
                    if 'account suspended' in response.text.lower():
                        status = 'taken'  # Suspended accounts are still taken
                elif platform_lower == 'instagram':
                    # Instagram specific checks
                    if 'sorry, this page isn\'t available' in response.text.lower():
                        status = 'available'
                elif platform_lower == 'tiktok':
                    # TikTok specific checks
                    if 'couldn\'t find this account' in response.text.lower():
                        status = 'available'
                        
            elif response.status_code == 404:
                status = 'available'
            else:
                status = 'unknown'
            
            return {
                'platform': platform_name,
                'username': username,
                'status': status,
                'url': url,
                'status_code': response.status_code,
                'response_time': response_time,
                'category': platform_config.get('category', 'unknown')
            }
            
        except Exception as e:
            raise Exception(f"Social media check failed: {e}")

class RedirectChecker(BaseChecker):
    """Checker that follows redirects to determine availability."""
    
    def check(self, platform_name, platform_config, username):
        url = platform_config['url_pattern'].format(username=username)
        
        try:
            response, response_time = self._make_request('GET', url, allow_redirects=True)
            
            # Check if we were redirected to a different URL
            if response.url != url:
                # If redirected to a generic page, username is likely available
                redirect_indicators = platform_config.get('redirect_indicators', [
                    '/signin',
                    '/login',
                    '/register',
                    '/404',
                    '/error'
                ])
                
                if any(indicator in response.url.lower() for indicator in redirect_indicators):
                    status = 'available'
                else:
                    status = 'taken'
            else:
                # No redirect, check status code
                if response.status_code == 200:
                    status = 'taken'
                elif response.status_code == 404:
                    status = 'available'
                else:
                    status = 'unknown'
            
            return {
                'platform': platform_name,
                'username': username,
                'status': status,
                'url': url,
                'final_url': response.url,
                'status_code': response.status_code,
                'response_time': response_time,
                'category': platform_config.get('category', 'unknown')
            }
            
        except Exception as e:
            raise Exception(f"Redirect check failed: {e}")
