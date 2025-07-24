"""
Output handlers for different formats (text, CSV, JSON).
"""

import json
import csv
import os
from datetime import datetime
from colorama import Fore, Style

class OutputHandler:
    """Handles different output formats for results."""
    
    def display_results(self, results, format_type='text'):
        """Display results in the specified format."""
        if format_type == 'text':
            self._display_text(results)
        elif format_type == 'csv':
            self._display_csv(results)
        elif format_type == 'json':
            self._display_json(results)
    
    def save_to_file(self, results, filepath, format_type='text'):
        """Save results to a file in the specified format."""
        if format_type == 'text':
            self._save_text(results, filepath)
        elif format_type == 'csv':
            self._save_csv(results, filepath)
        elif format_type == 'json':
            self._save_json(results, filepath)
    
    def _display_text(self, results):
        """Display results in enhanced formatted text."""
        if not results:
            print(f"{Fore.YELLOW}{Style.BRIGHT}📭 No results found.{Style.RESET_ALL}")
            return
        
        # Filter out errors for clean display
        clean_results = [r for r in results if r['status'] != 'error']
        
        # Group by category
        categories = {}
        for result in clean_results:
            category = result.get('category', 'unknown')
            if category not in categories:
                categories[category] = []
            categories[category].append(result)
        
        # Enhanced category icons and colors mapping
        category_icons = {
            'social_media': ('📱', Fore.BLUE + Style.BRIGHT),
            'developer': ('💻', Fore.GREEN + Style.BRIGHT),
            'gaming': ('🎮', Fore.MAGENTA + Style.BRIGHT),
            'creative': ('🎨', Fore.CYAN + Style.BRIGHT),
            'professional': ('💼', Fore.YELLOW + Style.BRIGHT),
            'forums': ('💬', Fore.WHITE + Style.BRIGHT),
            'dating': ('💕', Fore.MAGENTA + Style.BRIGHT),
            'education': ('🎓', Fore.BLUE + Style.BRIGHT),
            'entertainment': ('🎬', Fore.RED + Style.BRIGHT),
            'fitness': ('🏋️', Fore.GREEN + Style.BRIGHT),
            'food': ('🍕', Fore.YELLOW + Style.BRIGHT),
            'financial': ('💰', Fore.GREEN + Style.BRIGHT),
            'marketplace': ('🛒', Fore.YELLOW + Style.BRIGHT),
            'reviews': ('⭐', Fore.YELLOW + Style.BRIGHT),
            'transportation': ('🚗', Fore.CYAN + Style.BRIGHT),
            'travel': ('✈️', Fore.BLUE + Style.BRIGHT),
            'adult': ('🔞', Fore.RED + Style.BRIGHT),
            'unknown': ('❓', Fore.WHITE + Style.BRIGHT)
        }
        
        # Display by category with enhanced colors
        for category, category_results in sorted(categories.items()):
            icon_data = category_icons.get(category, ('📂', Fore.WHITE))
            icon, color = icon_data
            print(f"\n{color}{icon} {category.upper().replace('_', ' ')}{Style.RESET_ALL}")
            print(f"{color}{'─' * (len(category) + 15)}{Style.RESET_ALL}")
            
            for result in sorted(category_results, key=lambda x: x['platform']):
                status = result['status']
                platform = result['platform']
                url = result['url']
                response_time = result.get('response_time', 0)
                
                # Enhanced color coding and symbols with better visual appeal
                if status == 'available':
                    status_color = Fore.GREEN + Style.BRIGHT
                    status_symbol = "✅"
                    status_text = f"{Fore.GREEN + Style.BRIGHT}AVAILABLE{Style.RESET_ALL}"
                elif status == 'taken':
                    status_color = Fore.RED + Style.BRIGHT
                    status_symbol = "❌"
                    status_text = f"{Fore.RED + Style.BRIGHT}TAKEN{Style.RESET_ALL}"
                else:
                    status_color = Fore.YELLOW + Style.BRIGHT
                    status_symbol = "❓"
                    status_text = f"{Fore.YELLOW + Style.BRIGHT}UNKNOWN{Style.RESET_ALL}"
                
                # Format response time with color
                if response_time < 200:
                    time_color = Fore.GREEN
                elif response_time < 1000:
                    time_color = Fore.YELLOW
                else:
                    time_color = Fore.RED
                
                # Enhanced display with more vibrant colors and better formatting
                print(f"  {status_symbol} {Fore.WHITE}{Style.BRIGHT}{platform:<22}{Style.RESET_ALL} "
                      f"{status_text} "
                      f"{Fore.CYAN}{Style.DIM}{url:<45}{Style.RESET_ALL} "
                      f"{time_color}{Style.BRIGHT}({response_time:.0f}ms){Style.RESET_ALL}")
    
    def _display_csv(self, results):
        """Display results in CSV format."""
        if not results:
            print("No results found.")
            return
        
        # Print CSV header
        print("Platform,Username,Status,URL,Category,Response Time (ms),Status Code,Error")
        
        # Print CSV rows
        for result in results:
            print(f"{result['platform']},{result['username']},{result['status']},{result['url']},"
                  f"{result.get('category', '')},"
                  f"{result.get('response_time', 0)},{result.get('status_code', '')},"
                  f"\"{result.get('error', '')}\"")
    
    def _display_json(self, results):
        """Display results in JSON format."""
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_platforms': len(results),
            'summary': self._get_summary(results),
            'results': results
        }
        print(json.dumps(output, indent=2))
    
    def _save_text(self, results, filepath):
        """Save results to text file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Username Availability Check Results\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total platforms checked: {len(results)}\n\n")
            
            # Group by category
            categories = {}
            for result in results:
                category = result.get('category', 'unknown')
                if category not in categories:
                    categories[category] = []
                categories[category].append(result)
            
            # Write by category
            for category, category_results in sorted(categories.items()):
                f.write(f"=== {category.upper()} ===\n")
                
                for result in sorted(category_results, key=lambda x: x['platform']):
                    status_symbol = "✓" if result['status'] == 'available' else "✗" if result['status'] == 'taken' else "?"
                    f.write(f"  {status_symbol} {result['platform']:<20} {result['status']:<10} {result['url']} ({result.get('response_time', 0)}ms)\n")
                    
                    if 'error' in result:
                        f.write(f"    Error: {result['error']}\n")
                
                f.write("\n")
            
            # Summary
            summary = self._get_summary(results)
            f.write("SUMMARY:\n")
            for key, value in summary.items():
                f.write(f"{key.replace('_', ' ').title()}: {value}\n")
    
    def _save_csv(self, results, filepath):
        """Save results to CSV file."""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['platform', 'username', 'status', 'url', 'category', 
                         'response_time', 'status_code', 'error']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in results:
                row = {
                    'platform': result['platform'],
                    'username': result['username'],
                    'status': result['status'],
                    'url': result['url'],
                    'category': result.get('category', ''),
                    'response_time': result.get('response_time', 0),
                    'status_code': result.get('status_code', ''),
                    'error': result.get('error', '')
                }
                writer.writerow(row)
    
    def _save_json(self, results, filepath):
        """Save results to JSON file."""
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_platforms': len(results),
            'summary': self._get_summary(results),
            'results': results
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
    
    def _get_summary(self, results):
        """Generate summary statistics."""
        total = len(results)
        available = len([r for r in results if r['status'] == 'available'])
        taken = len([r for r in results if r['status'] == 'taken'])
        errors = len([r for r in results if r['status'] == 'error'])
        unknown = len([r for r in results if r['status'] == 'unknown'])
        
        # Category breakdown
        categories = {}
        for result in results:
            category = result.get('category', 'unknown')
            if category not in categories:
                categories[category] = {'available': 0, 'taken': 0, 'error': 0, 'unknown': 0}
            categories[category][result['status']] += 1
        
        return {
            'total_platforms': total,
            'available': available,
            'taken': taken,
            'errors': errors,
            'unknown': unknown,
            'categories': categories
        }
