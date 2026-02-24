"""
Safely executes a DuckDuckGo search.
Uses sys.executable for environment consistency and implements soft failures (JSON errors) 
instead of crashing, ensuring agents can read the error cause.
"""
import sys
import json
import time
import random
import argparse

def soft_fail(code, message, details=None):
    """
    Prints a JSON error payload and exits with success (0) so the agent 
    can read the output instead of seeing a generic shell crash.
    """
    payload = {
        "status": "error",
        "code": code,
        "message": message
    }
    if details:
        payload["details"] = details
    
    print(json.dumps(payload, indent=2))
    sys.exit(0)

# --- Dependency Import with Soft Failure ---
try:
    from duckduckgo_search import DDGS
except ImportError:
    soft_fail(
        code="MISSING_DEPENDENCY",
        message="The 'duckduckgo-search' library is not installed.",
        details={
            "python_executable": sys.executable,
            "fix": f"{sys.executable} -m pip install duckduckgo-search"
        }
    )

def truncate_results(results, char_limit=250):
    """Truncates the body of search results to save context window space."""
    clean_results = []
    for r in results:
        body = r.get('body', '')
        if len(body) > char_limit:
            body = body[:char_limit] + "..."
        
        clean_results.append({
            "title": r.get('title', 'No Title'),
            "href": r.get('href', ''),
            "body": body
        })
    return clean_results

def run_search(query, max_results=5, safe_mode=False):
    max_results = min(int(max_results), 10) 
    
    # Jitter logic
    delay = random.uniform(1.0, 2.0)
    if safe_mode:
        delay = random.uniform(3.0, 5.0)
    
    time.sleep(delay)

    try:
        results = []
        with DDGS() as ddgs:
            raw_results = ddgs.text(keywords=query, max_results=max_results)
            if raw_results:
                results = list(raw_results)
        
        final_output = {
            "status": "success",
            "results": truncate_results(results)
        }
        print(json.dumps(final_output, indent=2))

    except Exception as e:
        error_msg = str(e).lower()
        
        if "ratelimit" in error_msg or "429" in error_msg:
            soft_fail("RATE_LIMIT", "Too many requests. IP likely blocked by DDG.")
        elif "timeout" in error_msg:
             soft_fail("TIMEOUT", "Connection timed out.")
        else:
            soft_fail("SCRAPER_ERROR", f"Library exception: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DuckDuckGo Search Wrapper")
    parser.add_argument("-q", "--query", required=True, help="Search query")
    parser.add_argument("-m", "--max-results", type=int, default=5, help="Max results (1-10)")
    parser.add_argument("--safe", action="store_true", help="Increase delay to avoid blocking")
    
    args = parser.parse_args()
    
    run_search(args.query, args.max_results, args.safe)