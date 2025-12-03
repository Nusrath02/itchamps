"""
Test script for GitHub API integration
Run this to verify GitHub API is working correctly
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from itchamps.api.github_helper import GitHubHelper

    print("=" * 60)
    print("GitHub API Integration Test")
    print("=" * 60)

    github = GitHubHelper(owner="Nusrath02", repo="itchamps")

    # Test 1: Repository Info
    print("\n1. Testing Repository Information...")
    info = github.get_repository_info()
    if info:
        print(f"✅ Repository: {info['name']}")
        print(f"   Description: {info['description'] or 'No description'}")
        print(f"   Stars: {info['stars']}, Forks: {info['forks']}")
        print(f"   Language: {info['language']}")
    else:
        print("❌ Failed to fetch repository info")

    # Test 2: Recent Commits
    print("\n2. Testing Recent Commits...")
    commits = github.get_commits(limit=3)
    if commits:
        print(f"✅ Found {len(commits)} commits")
        for commit in commits:
            print(f"   - {commit['sha']}: {commit['message'][:50]}...")
    else:
        print("❌ Failed to fetch commits")

    # Test 3: Issues
    print("\n3. Testing Issues...")
    issues = github.get_issues(limit=3)
    if issues is not None:
        print(f"✅ Found {len(issues)} open issues")
        for issue in issues:
            print(f"   - #{issue['number']}: {issue['title']}")
    else:
        print("❌ Failed to fetch issues")

    # Test 4: Branches
    print("\n4. Testing Branches...")
    branches = github.get_branches(limit=5)
    if branches:
        print(f"✅ Found {len(branches)} branches")
        for branch in branches:
            protected = "🔒" if branch['protected'] else ""
            print(f"   - {branch['name']} {protected}")
    else:
        print("❌ Failed to fetch branches")

    # Test 5: Contributors
    print("\n5. Testing Contributors...")
    contributors = github.get_contributors(limit=3)
    if contributors:
        print(f"✅ Found {len(contributors)} contributors")
        for contributor in contributors:
            print(f"   - {contributor['login']}: {contributor['contributions']} contributions")
    else:
        print("❌ Failed to fetch contributors")

    print("\n" + "=" * 60)
    print("✅ GitHub API integration test completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check if you need a GitHub token for higher rate limits")
    print("2. Add token to site_config.json if needed")
    print("3. Restart your Frappe server: bench restart")
    print("4. Test the chatbot by asking: 'Show repo info'")

except ImportError as e:
    print("❌ Import Error:", str(e))
    print("\nMake sure you're running this from the correct directory")
    print("Or the itchamps app is properly installed in Frappe")

except Exception as e:
    print("❌ Error:", str(e))
    print("\nPossible causes:")
    print("- No internet connection")
    print("- GitHub API rate limit exceeded")
    print("- Repository doesn't exist or is private")
    print("\nCheck GitHub API status: https://www.githubstatus.com/")
