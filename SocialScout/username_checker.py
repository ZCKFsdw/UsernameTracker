"""
Main username checker class that coordinates the checking process.
"""

import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from colorama import Fore, Style
import requests
from checkers import (
    StandardChecker, 
    ProfileChecker, 
    APIChecker, 
    SocialMediaChecker,
    RedirectChecker
)
from utils import setup_logging, RateLimiter

class UsernameChecker:
    def __init__(self, timeout=10, max_workers=50, delay=0.1, verbose=False, debug=False):
        self.timeout = timeout
        self.max_workers = max_workers
        self.delay = delay
        self.verbose = verbose
        self.debug = debug
        
        # Setup logging
        self.logger = setup_logging(debug)
        
        # Load platforms configuration
        self.platforms = self._load_platforms()
        
        # Initialize checkers
        self.checkers = {
            'standard': StandardChecker(timeout),
            'profile': ProfileChecker(timeout),
            'api': APIChecker(timeout),
            'social_media': SocialMediaChecker(timeout),
            'redirect': RedirectChecker(timeout)
        }
        
        # Rate limiter
        self.rate_limiter = RateLimiter(delay)
        
        # Progress tracking
        self.progress_lock = Lock()
        self.completed = 0
        self.total = 0
    
    def _load_platforms(self):
        """Load platform configurations from JSON file."""
        try:
            platforms_path = os.path.join(os.path.dirname(__file__), 'platforms.json')
            with open(platforms_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load platforms.json: {e}")
            raise
    
    def _filter_platforms(self, category=None, platforms=None):
        """Filter platforms based on category or specific platform names."""
        filtered = self.platforms.copy()
        
        if category:
            filtered = {k: v for k, v in filtered.items() 
                       if v.get('category', '').lower() == category.lower()}
        
        if platforms:
            platform_names = [p.lower() for p in platforms]
            filtered = {k: v for k, v in filtered.items() 
                       if k.lower() in platform_names}
        
        return filtered
    
    def _update_progress(self, platform_name, status):
        """Update progress counter and display."""
        with self.progress_lock:
            self.completed += 1
            if self.verbose and status != 'error':  # Don't show errors in verbose mode
                percentage = (self.completed / self.total) * 100
                if status == 'available':
                    status_color = Fore.GREEN
                    status_symbol = "✅"
                elif status == 'taken':
                    status_color = Fore.RED
                    status_symbol = "❌"
                else:
                    status_color = Fore.YELLOW
                    status_symbol = "❓"
                print(f"[{percentage:5.1f}%] {status_symbol} {platform_name}: {status_color}{Style.BRIGHT}{status.upper()}{Style.RESET_ALL}")
    
    def _check_single_platform(self, platform_name, platform_config, username):
        """Check username availability on a single platform."""
        try:
            # Rate limiting
            self.rate_limiter.wait()
            
            # Get appropriate checker
            checker_type = platform_config.get('checker_type', 'standard')
            checker = self.checkers.get(checker_type, self.checkers['standard'])
            
            # Perform the check
            result = checker.check(platform_name, platform_config, username)
            
            # Update progress
            self._update_progress(platform_name, result['status'])
            
            return result
            
        except Exception as e:
            if self.debug:
                self.logger.error(f"Error checking {platform_name}: {e}")
            error_result = {
                'platform': platform_name,
                'username': username,
                'status': 'error',
                'url': platform_config.get('url_pattern', '').format(username=username),
                'response_time': 0,
                'error': str(e),
                'category': platform_config.get('category', 'unknown')
            }
            self._update_progress(platform_name, 'error')
            return error_result
    
    def check_username(self, username, category=None, platforms=None):
        """
        Check username availability across filtered platforms.
        
        Args:
            username: Username to check
            category: Filter by platform category
            platforms: List of specific platforms to check
            
        Returns:
            List of result dictionaries
        """
        # Filter platforms
        platforms_to_check = self._filter_platforms(category, platforms)
        
        if not platforms_to_check:
            raise ValueError("No platforms found matching the specified criteria")
        
        self.total = len(platforms_to_check)
        self.completed = 0
        
        print(f"{Fore.CYAN}{Style.BRIGHT}🔍 Scanning {self.total} platforms...{Style.RESET_ALL}")
        if category:
            print(f"{Fore.MAGENTA}📂 Category filter: {Style.BRIGHT}{category}{Style.RESET_ALL}")
        if platforms:
            print(f"{Fore.MAGENTA}🎯 Platform filter: {Style.BRIGHT}{', '.join(platforms)}{Style.RESET_ALL}")
        print()
        
        results = []
        
        # Use ThreadPoolExecutor for concurrent checking
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_platform = {
                executor.submit(self._check_single_platform, name, config, username): name
                for name, config in platforms_to_check.items()
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_platform):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    platform_name = future_to_platform[future]
                    self.logger.error(f"Unexpected error for {platform_name}: {e}")
        
        # Sort results by platform name for consistent output
        results.sort(key=lambda x: x['platform'].lower())
        
        return results
    
    def get_categories(self):
        """Get list of available platform categories."""
        categories = set()
        for platform_config in self.platforms.values():
            category = platform_config.get('category', 'unknown')
            categories.add(category)
        return sorted(list(categories))
    
    def get_platform_names(self):
        """Get list of all platform names."""
        return sorted(list(self.platforms.keys()))
