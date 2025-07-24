# Username Availability Checker

## Overview

This is a comprehensive Python command-line application that checks username availability across 100+ websites and platforms. The system uses a modular checker architecture with different strategies for various platform types, concurrent execution for performance, and multiple output formats for flexibility.

## System Architecture

### Core Architecture Pattern
The application follows a **Strategy Pattern** with a **Factory Pattern** for checker instantiation. The main orchestrator (`UsernameChecker`) coordinates multiple specialized checker classes that handle different platform verification methods.

**Key Design Decisions:**
- **Modular Checker System**: Different checker classes handle various platform authentication and detection methods
- **Concurrent Execution**: ThreadPoolExecutor enables parallel checking across multiple platforms
- **Rate Limiting**: Built-in rate limiter prevents overwhelming target servers
- **Session Management**: Persistent HTTP sessions with proper user agent headers

### Technology Stack
- **Language**: Python 3.x
- **HTTP Client**: requests library with session management
- **Concurrency**: ThreadPoolExecutor from concurrent.futures
- **CLI Framework**: argparse for command-line interface
- **Output Formatting**: colorama for colored terminal output
- **Web Parsing**: BeautifulSoup4 for HTML parsing
- **Data Format**: JSON for platform configuration

## Key Components

### 1. Checker Classes (`checkers.py`)
**Purpose**: Implement different verification strategies for various platform types
- `BaseChecker`: Abstract base class with common HTTP functionality
- `StandardChecker`: Uses HTTP status codes for availability detection
- `ProfileChecker`: Analyzes profile page content
- `APIChecker`: Uses platform APIs when available
- `SocialMediaChecker`: Specialized for social media platforms
- `RedirectChecker`: Detects redirects to login/signup pages

### 2. Main Orchestrator (`username_checker.py`)
**Purpose**: Coordinates the entire checking process
- Loads platform configurations from JSON
- Manages concurrent execution across multiple platforms
- Implements rate limiting and progress tracking
- Handles result aggregation and error management

### 3. Output Handler (`output_handlers.py`)
**Purpose**: Manages result display and file output
- Supports multiple formats: text, CSV, JSON
- Provides colored terminal output
- Groups results by platform category
- Handles file saving with proper formatting

### 4. CLI Interface (`main.py`)
**Purpose**: Provides user-friendly command-line interface
- Comprehensive argument parsing
- Filtering options (category, platforms, availability status)
- Output format selection
- Performance tuning parameters

### 5. Platform Configuration (`platforms.json`)
**Purpose**: Centralized configuration for all supported platforms
- URL patterns with username placeholders
- Platform categorization (social_media, developer, professional, etc.)
- Checker type assignments
- Platform-specific detection indicators

### 6. Utilities (`utils.py`)
**Purpose**: Common functionality and helper classes
- Logging configuration
- Rate limiting implementation
- Username validation
- Threading utilities

## Data Flow

1. **Initialization**: Load platform configurations and initialize checker instances
2. **Input Processing**: Parse command-line arguments and validate username
3. **Platform Filtering**: Apply category and platform filters based on user preferences
4. **Concurrent Execution**: 
   - Submit checking tasks to ThreadPoolExecutor
   - Apply rate limiting before each request
   - Execute appropriate checker strategy for each platform
5. **Result Collection**: Aggregate results from all completed checks
6. **Output Processing**: Format and display results according to specified format

## External Dependencies

### Core Libraries
- `requests`: HTTP client for web requests
- `beautifulsoup4`: HTML parsing for content analysis
- `colorama`: Cross-platform colored terminal output
- `concurrent.futures`: Built-in Python concurrency

### Platform Dependencies
- Target platforms accessed via HTTP/HTTPS
- No API keys required (uses public endpoints)
- User-agent spoofing to avoid bot detection

## Deployment Strategy

### Local Execution
The application is designed as a standalone Python script that can be executed directly:
```bash
python main.py username123 --category social_media --output results.json
```

### Requirements
- Python 3.6+
- Internet connectivity for platform checking
- Optional: Virtual environment for dependency isolation

### Scalability Considerations
- Configurable concurrency limits (max_workers parameter)
- Rate limiting to respect platform server limits
- Timeout configuration for network requests
- Memory-efficient result processing

## Changelog
- July 01, 2025: Initial setup with 100 platforms
- July 01, 2025: Expanded to 191 platforms with diverse categories including dating, education, entertainment, fitness, food, transportation, and international platforms (Asian, European, Russian social media platforms)
- July 01, 2025: Enhanced visual output with professional ASCII logo, colorful formatting, emoji icons, improved error handling, and better progress indicators
- July 01, 2025: MAJOR ENHANCEMENT - Expanded to 240+ platforms with 50+ new popular websites including Netflix, Hulu, Disney+, Roblox, Minecraft, Fortnite, VALORANT, Uber, Lyft, DoorDash, Airbnb, Bumble, Tinder, Coursera, edX, Strava, Peloton, and many more. Added rainbow gradient logo, enhanced category colors, improved error suppression, and power-boosted performance
- July 01, 2025: ULTIMATE POWER-UP - Added ultra-enhanced rainbow gradient ASCII logo with vibrant multi-colors, advanced input validation with detailed error feedback, intelligent username suggestion system, fast-mode for speed optimization, smart filtering for reliable results, export-available feature for workflow automation, enhanced progress indicators with real-time status, and comprehensive error handling with graceful fallbacks. The tool now features 15+ advanced command-line options and supports intelligent pattern recognition for optimal username checking.

## User Preferences

Preferred communication style: Simple, everyday language.