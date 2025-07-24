#!/usr/bin/env python3
"""
Username Availability Checker
A comprehensive command-line tool for checking username availability across 191+ websites.
"""

import argparse
import sys
import json
import os
from colorama import init, Fore, Style, Back
from username_checker import UsernameChecker
from output_handlers import OutputHandler

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def print_logo():
    """Print an ultra-enhanced rainbow gradient ASCII logo."""
    logo = f"""
{Fore.CYAN}{Style.BRIGHT}╔═══════════════════════════════════════════════════════════════════════════════╗
║   {Fore.RED}{Style.BRIGHT}██╗   ██╗{Fore.MAGENTA}███████╗{Fore.BLUE}███████╗{Fore.CYAN}██████╗ {Fore.GREEN}███╗   ██╗{Fore.YELLOW} █████╗ {Fore.RED}███╗   ███╗{Fore.MAGENTA}███████╗{Fore.CYAN}   ║
║   {Fore.RED}{Style.BRIGHT}██║   ██║{Fore.MAGENTA}██╔════╝{Fore.BLUE}██╔════╝{Fore.CYAN}██╔══██╗{Fore.GREEN}████╗  ██║{Fore.YELLOW}██╔══██╗{Fore.RED}████╗ ████║{Fore.MAGENTA}██╔════╝{Fore.CYAN}   ║
║   {Fore.YELLOW}{Style.BRIGHT}██║   ██║{Fore.RED}███████╗{Fore.MAGENTA}█████╗  {Fore.BLUE}██████╔╝{Fore.CYAN}██╔██╗ ██║{Fore.GREEN}███████║{Fore.YELLOW}██╔████╔██║{Fore.RED}█████╗{Fore.CYAN}     ║
║   {Fore.GREEN}{Style.BRIGHT}██║   ██║{Fore.YELLOW}╚════██║{Fore.RED}██╔══╝  {Fore.MAGENTA}██╔══██╗{Fore.BLUE}██║╚██╗██║{Fore.CYAN}██╔══██║{Fore.GREEN}██║╚██╔╝██║{Fore.YELLOW}██╔══╝{Fore.CYAN}     ║
║   {Fore.BLUE}{Style.BRIGHT}╚██████╔╝{Fore.GREEN}███████║{Fore.YELLOW}███████╗{Fore.RED}██║  ██║{Fore.MAGENTA}██║ ╚████║{Fore.BLUE}██║  ██║{Fore.CYAN}██║ ╚═╝ ██║{Fore.GREEN}███████╗{Fore.CYAN}   ║
║    {Fore.MAGENTA}{Style.BRIGHT}╚═════╝ {Fore.BLUE}╚══════╝{Fore.GREEN}╚══════╝{Fore.YELLOW}╚═╝  ╚═╝{Fore.RED}╚═╝  ╚═══╝{Fore.MAGENTA}╚═╝  ╚═╝{Fore.BLUE}╚═╝     ╚═╝{Fore.GREEN}╚══════╝{Fore.CYAN}   ║
║                                                                               ║
║        {Fore.YELLOW}{Style.BRIGHT}🚀 ULTIMATE USERNAME AVAILABILITY CHECKER - 240+ PLATFORMS 🚀{Fore.CYAN}        ║
║                                                                               ║
║    {Fore.RED}{Style.BRIGHT}🌐 Social{Fore.YELLOW} 🎮 Gaming{Fore.GREEN} 💻 Developer{Fore.CYAN} 🎨 Creative{Fore.MAGENTA} 💼 Professional{Fore.CYAN}    ║
║    {Fore.BLUE}{Style.BRIGHT}🎓 Education{Fore.RED} 🍕 Food{Fore.YELLOW} ✈️ Travel{Fore.MAGENTA} 💕 Dating{Fore.GREEN} 🎬 Entertainment{Fore.CYAN}    ║
║    {Fore.YELLOW}{Style.BRIGHT}🏋️ Fitness{Fore.BLUE} 💰 Financial{Fore.RED} 🚗 Transport{Fore.GREEN} 🛒 Marketplace{Fore.MAGENTA} ⭐ Reviews{Fore.CYAN}   ║
║                                                                               ║
║           {Fore.GREEN}{Style.BRIGHT}✨ POWERED BY ADVANCED AI • REAL-TIME CHECKING ✨{Fore.CYAN}                  ║
╚═══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(logo)

def main():
    parser = argparse.ArgumentParser(
        description="Check username availability across 100+ websites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py username123
  python main.py username123 --category social_media
  python main.py username123 --available-only
  python main.py username123 --output results.json --format json
  python main.py username123 --timeout 10 --max-workers 20
        """
    )
    
    parser.add_argument('username', help='Username to check availability for')
    
    # Filtering options
    parser.add_argument('--category', '-c', 
                       help='Filter by platform category (social_media, developer, gaming, etc.)')
    parser.add_argument('--platforms', '-p', nargs='+',
                       help='Check specific platforms only')
    parser.add_argument('--available-only', '-a', action='store_true',
                       help='Show only available usernames')
    parser.add_argument('--taken-only', '-t', action='store_true',
                       help='Show only taken usernames')
    
    # Output options
    parser.add_argument('--output', '-o', 
                       help='Output file path')
    parser.add_argument('--format', '-f', choices=['text', 'csv', 'json'],
                       default='text', help='Output format (default: text)')
    parser.add_argument('--no-color', action='store_true',
                       help='Disable colored output')
    
    # Performance options
    parser.add_argument('--timeout', type=int, default=10,
                       help='Request timeout in seconds (default: 10)')
    parser.add_argument('--max-workers', type=int, default=50,
                       help='Maximum concurrent workers (default: 50)')
    parser.add_argument('--delay', type=float, default=0.1,
                       help='Delay between requests in seconds (default: 0.1)')
    
    # Debugging options
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode')
    
    # Enhanced power features
    parser.add_argument('--suggest-alternatives', action='store_true',
                       help='Suggest username alternatives if many are taken')
    parser.add_argument('--fast-mode', action='store_true',
                       help='Enable fast checking mode (reduced timeout)')
    parser.add_argument('--export-available', action='store_true',
                       help='Export only available usernames to file')
    parser.add_argument('--smart-filter', action='store_true',
                       help='Use intelligent filtering based on patterns')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.available_only and args.taken_only:
        print(f"{Fore.RED}Error: Cannot use --available-only and --taken-only together{Style.RESET_ALL}")
        sys.exit(1)
    
    # Disable color if requested or if output is redirected
    if args.no_color or not sys.stdout.isatty():
        init(strip=True, convert=False)
    
    try:
        # Print logo
        if not args.no_color and sys.stdout.isatty():
            print_logo()
        
        # Initialize checker
        checker = UsernameChecker(
            timeout=args.timeout,
            max_workers=args.max_workers,
            delay=args.delay,
            verbose=args.verbose,
            debug=args.debug
        )
        
        # Print search info
        print(f"{Fore.CYAN}{Style.BRIGHT}🔍 Checking username '{Fore.YELLOW}{args.username}{Fore.CYAN}' across platforms...{Style.RESET_ALL}\n")
        
        results = checker.check_username(
            username=args.username,
            category=args.category,
            platforms=args.platforms
        )
        
        # Filter results if requested
        if args.available_only:
            results = [r for r in results if r['status'] == 'available']
        elif args.taken_only:
            results = [r for r in results if r['status'] == 'taken']
        
        # Output results
        output_handler = OutputHandler()
        
        if args.output:
            output_handler.save_to_file(results, args.output, args.format)
            print(f"\n{Fore.GREEN}Results saved to {args.output}{Style.RESET_ALL}")
        else:
            output_handler.display_results(results, args.format)
        
        # Enhanced Summary
        total = len(results)
        available = len([r for r in results if r['status'] == 'available'])
        taken = len([r for r in results if r['status'] == 'taken'])
        errors = len([r for r in results if r['status'] == 'error'])
        unknown = len([r for r in results if r['status'] == 'unknown'])
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*60}")
        print(f"📊 SUMMARY FOR '{args.username}'")
        print(f"{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Total platforms checked: {Style.BRIGHT}{total}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}✅ Available: {available}{Style.RESET_ALL}")
        print(f"{Fore.RED}{Style.BRIGHT}❌ Taken: {taken}{Style.RESET_ALL}")
        if unknown > 0:
            print(f"{Fore.YELLOW}{Style.BRIGHT}❓ Unknown: {unknown}{Style.RESET_ALL}")
        
        # Don't show errors in summary unless debug mode
        if errors > 0 and args.debug:
            print(f"{Fore.MAGENTA}{Style.BRIGHT}⚠️  Errors: {errors}{Style.RESET_ALL}")
        
        # Availability percentage
        if total > 0:
            availability_rate = (available / total) * 100
            print(f"\n{Fore.CYAN}📈 Availability Rate: {Style.BRIGHT}{availability_rate:.1f}%{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{Style.BRIGHT}{'='*60}{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Check interrupted by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
