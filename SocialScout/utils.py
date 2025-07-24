"""
Utility functions and classes.
"""

import logging
import time
import threading

def setup_logging(debug=False):
    """Setup logging configuration."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

class RateLimiter:
    """Simple rate limiter to prevent overwhelming servers."""
    
    def __init__(self, delay=0.1):
        self.delay = delay
        self.last_request = 0
        self.lock = threading.Lock()
    
    def wait(self):
        """Wait if necessary to maintain rate limit."""
        with self.lock:
            current_time = time.time()
            time_since_last = current_time - self.last_request
            
            if time_since_last < self.delay:
                sleep_time = self.delay - time_since_last
                time.sleep(sleep_time)
            
            self.last_request = time.time()

def validate_username(username):
    """Enhanced username validation with detailed feedback."""
    from colorama import Fore, Style
    
    if not username:
        raise ValueError(f"{Fore.RED}{Style.BRIGHT}❌ Username cannot be empty{Style.RESET_ALL}")
    
    if len(username) < 2:
        raise ValueError(f"{Fore.RED}{Style.BRIGHT}❌ Username must be at least 2 characters long{Style.RESET_ALL}")
    
    if len(username) > 30:
        raise ValueError(f"{Fore.RED}{Style.BRIGHT}❌ Username must be 30 characters or less{Style.RESET_ALL}")
    
    # Check for valid characters (alphanumeric, underscore, hyphen, period)
    import re
    if not re.match(r'^[a-zA-Z0-9._-]+$', username):
        raise ValueError(f"{Fore.RED}{Style.BRIGHT}❌ Username can only contain letters, numbers, underscore, hyphen, and period{Style.RESET_ALL}")
    
    # Additional checks for better usernames
    if username.startswith('.') or username.endswith('.'):
        print(f"{Fore.YELLOW}{Style.BRIGHT}⚠️  Warning: Username should not start or end with a period{Style.RESET_ALL}")
    
    if username.startswith('-') or username.endswith('-'):
        print(f"{Fore.YELLOW}{Style.BRIGHT}⚠️  Warning: Username should not start or end with a hyphen{Style.RESET_ALL}")
    
    # Check for consecutive special characters
    if re.search(r'[._-]{2,}', username):
        print(f"{Fore.YELLOW}{Style.BRIGHT}⚠️  Warning: Username contains consecutive special characters{Style.RESET_ALL}")
    
    return True

def suggest_username_variations(username):
    """Suggest username variations if original might be taken."""
    variations = []
    
    # Remove consecutive special chars
    import re
    clean_username = re.sub(r'[._-]+', '_', username)
    if clean_username != username:
        variations.append(clean_username)
    
    # Add numbers and suffixes
    variations.extend([
        f"{username}123",
        f"{username}2024",
        f"{username}_official",
        f"real_{username}",
        f"{username}_pro",
        f"{username}99",
        f"the_{username}",
        f"{username}_",
        f"_{username}"
    ])
    
    # Capitalize variations
    variations.extend([
        username.capitalize(),
        username.upper(),
        username.lower()
    ])
    
    return list(set(variations))[:8]  # Return top 8 unique suggestions

def format_response_time(ms):
    """Format response time for display."""
    if ms < 1000:
        return f"{ms:.0f}ms"
    else:
        return f"{ms/1000:.1f}s"

def get_platform_by_url(url, platforms):
    """Try to identify platform from URL."""
    url_lower = url.lower()
    
    for platform_name, config in platforms.items():
        platform_domains = config.get('domains', [])
        for domain in platform_domains:
            if domain.lower() in url_lower:
                return platform_name
    
    return None
