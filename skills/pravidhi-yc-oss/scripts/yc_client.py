#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import argparse
import sys
import re
from datetime import datetime

# Configuration
BASE_URL = "https://yc-oss.github.io/api"
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; YC-Agent/2.1; +https://agentskills.io)'}
TIMEOUT_SECONDS = 15

# Hardcoded taxonomy for fallback/info mode to avoid extra file I/O
TAXONOMY = {
    "batches": ["w24", "s23", "w23", "s22", "w22", "s21", "w21", "s20", "w20"],
    "industries": ["b2b", "consumer", "education", "fintech", "healthcare", "industrials", "real-estate", "government"],
    "tags": ["artificial-intelligence", "generative-ai", "developer-tools", "saas", "marketplace", "biotech", "crypto", "open-source", "climate"]
}

def fetch_json(endpoint):
    """Robust JSON fetcher with error handling and timeouts."""
    url = f"{BASE_URL}/{endpoint}"
    if not url.endswith('.json'):
        url += '.json'
        
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error: HTTP {e.code} fetching {url}. The resource might not exist.", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Network issue ({str(e.reason)}). Check internet connection.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unexpected failure ({str(e)}).", file=sys.stderr)
        sys.exit(1)

def safe_get(d, key, default=None):
    """Safely get value from dictionary even if d is None."""
    if not isinstance(d, dict):
        return default
    return d.get(key, default)

def format_company(company):
    """Format a single company record for LLM consumption with schema safety."""
    try:
        name = safe_get(company, 'name', 'Unknown')
        batch = safe_get(company, 'batch', 'N/A')
        
        # Safe string handling for descriptions
        one_liner = safe_get(company, 'one_liner')
        long_desc = safe_get(company, 'long_description')
        
        desc_text = one_liner if one_liner else (long_desc if long_desc else '')
        desc = str(desc_text)[:100] + "..." if len(str(desc_text)) > 100 else str(desc_text)
        
        website = safe_get(company, 'website', 'N/A')
        team = safe_get(company, 'team_size', 0)
        
        return f"- **{name}** ({batch}) | Team: {team} | {website}\n  {desc}"
    except Exception as e:
        return f"- [Error formatting record: {str(e)}]"

def filter_data(data, keyword=None, min_team=0, year=None):
    """Apply filters to the dataset with regex matching."""
    results = []
    
    # Pre-compile regex if keyword exists
    keyword_regex = None
    if keyword:
        try:
            # escapes special regex characters in keyword, adds word boundaries
            pattern = r'(?i)\b' + re.escape(keyword) + r'\b'
            keyword_regex = re.compile(pattern)
        except re.error:
            # Fallback to simple substring if regex fails (rare)
            keyword_regex = None

    for c in data:
        if not isinstance(c, dict):
            continue

        # Keyword filter (Name, Tags, Description)
        if keyword:
            tags = safe_get(c, 'tags', [])
            tag_str = " ".join(tags) if isinstance(tags, list) else str(tags)
            
            blob = (
                f"{safe_get(c, 'name', '')} "
                f"{safe_get(c, 'one_liner', '')} "
                f"{tag_str} "
                f"{safe_get(c, 'industry', '')}"
            )
            
            if keyword_regex:
                if not keyword_regex.search(blob):
                    continue
            else:
                if keyword.lower() not in blob.lower():
                    continue
                
        # Team size filter
        if min_team > 0:
            team_size = safe_get(c, 'team_size', 0)
            if not isinstance(team_size, (int, float)) or team_size < min_team:
                continue
                
        # Year filter (Launch year)
        if year:
            launched = safe_get(c, 'launched_at')
            if not launched:
                continue
            try:
                # Handle both timestamp integers and ISO strings if schema changes
                if isinstance(launched, (int, float)):
                    if datetime.fromtimestamp(launched).year != year:
                        continue
                else:
                    continue 
            except:
                continue
                
        results.append(c)
    return results

def print_info():
    """Display valid taxonomy info."""
    print("# Valid YC Data Identifiers")
    print("\n## Batches (Partial)")
    print(", ".join(TAXONOMY['batches']))
    print("\n## Industries")
    print(", ".join(TAXONOMY['industries']))
    print("\n## Common Tags")
    print(", ".join(TAXONOMY['tags']))

def main():
    parser = argparse.ArgumentParser(description="YC Company Intelligence Tool")
    parser.add_argument('--mode', choices=['all', 'top', 'hiring', 'batch', 'industry', 'tag', 'search'], help="Data source mode")
    parser.add_argument('--target', help="Specific batch/industry/tag slug (e.g., 'w24', 'fintech')")
    parser.add_argument('--keyword', help="Filter results by keyword (regex-supported)")
    parser.add_argument('--limit', type=int, default=10, help="Max results to display")
    parser.add_argument('--sort-by', choices=['team_size', 'launched_at'], help="Sort criteria")
    parser.add_argument('--info', action='store_true', help="List valid batches, industries, and tags")
    
    args = parser.parse_args()

    if args.info:
        print_info()
        sys.exit(0)

    if not args.mode:
        parser.print_help()
        sys.exit(1)

    # Determine Endpoint
    if args.mode == 'search':
        endpoint = "companies/all"
    elif args.mode in ['top', 'hiring']:
        endpoint = f"companies/{args.mode}"
    elif args.mode == 'batch':
        if not args.target:
            print("Error: --target required for batch mode (e.g., --target w24)", file=sys.stderr)
            sys.exit(1)
        endpoint = f"batches/{args.target.lower()}"
    elif args.mode == 'industry':
        if not args.target:
            print("Error: --target required for industry mode (e.g., --target b2b)", file=sys.stderr)
            sys.exit(1)
        endpoint = f"industries/{args.target.lower()}"
    elif args.mode == 'tag':
        if not args.target:
            print("Error: --target required for tag mode (e.g., --target ai)", file=sys.stderr)
            sys.exit(1)
        endpoint = f"tags/{args.target.lower()}"
    else:
        endpoint = "companies/all"

    # Fetch
    data = fetch_json(endpoint)
    
    # Process
    results = filter_data(data, keyword=args.keyword, limit=args.limit) # Passing limit isn't strictly necessary here as it's sliced later, but kept for clarity if logic expands
    
    # Sort
    if args.sort_by == 'team_size':
        results.sort(key=lambda x: safe_get(x, 'team_size', 0), reverse=True)
    elif args.sort_by == 'launched_at':
        results.sort(key=lambda x: safe_get(x, 'launched_at', 0), reverse=True)

    # Output
    print(f"Found {len(results)} companies. Showing top {args.limit}:")
    print("---")
    for company in results[:args.limit]:
        print(format_company(company))

if __name__ == "__main__":
    main()

