#!/usr/bin/env python3
"""
Security check script to detect exposed API keys and secrets
"""

import os
import re
import sys
from pathlib import Path

def check_for_exposed_secrets():
    """Check for exposed API keys and secrets in the codebase."""
    
    print("🔒 Security Check - Scanning for Exposed Secrets")
    print("=" * 60)
    
    # Patterns that indicate exposed secrets
    secret_patterns = [
        (r'AIza[0-9A-Za-z_-]{35}', 'Google API Key'),
        (r'sk-[a-zA-Z0-9]{48}', 'OpenAI API Key'),
        (r'GEMINI_API_KEY\s*=\s*["\']?AIza[^"\'\\s]+', 'Hardcoded Gemini API Key'),
        (r'api_key\s*=\s*["\']AIza[^"\'\\s]+', 'Hardcoded API Key'),
        (r'API_KEY\s*:\s*["\']?AIza[^"\'\\s]+', 'API Key in Config'),
        (r'Bearer\s+AIza[0-9A-Za-z_-]{35}', 'Bearer Token with API Key'),
    ]
    
    # Files to check
    files_to_check = []
    
    # Get all Python files
    for ext in ['*.py', '*.md', '*.txt', '*.yml', '*.yaml', '*.json', '*.toml']:
        files_to_check.extend(Path('.').rglob(ext))
    
    # Exclude certain directories and files
    exclude_patterns = [
        '.git', '__pycache__', '.venv', 'venv', 'env',
        'node_modules', '.streamlit', 'security_check.py'
    ]
    
    files_to_check = [
        f for f in files_to_check 
        if not any(exclude in str(f) for exclude in exclude_patterns)
    ]
    
    issues_found = []
    
    print(f"📁 Scanning {len(files_to_check)} files...")
    
    for file_path in files_to_check:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                for pattern, description in secret_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # Get line number
                        line_num = content[:match.start()].count('\n') + 1
                        
                        # Mask the secret for display
                        secret = match.group()
                        if len(secret) > 10:
                            masked_secret = secret[:6] + '*' * (len(secret) - 10) + secret[-4:]
                        else:
                            masked_secret = '*' * len(secret)
                        
                        issues_found.append({
                            'file': str(file_path),
                            'line': line_num,
                            'type': description,
                            'secret': masked_secret,
                            'full_secret': secret
                        })
                        
        except Exception as e:
            print(f"⚠️ Could not scan {file_path}: {e}")
    
    return issues_found

def check_gitignore():
    """Check if .gitignore properly excludes sensitive files."""
    
    print("\n🚫 Checking .gitignore Configuration...")
    print("-" * 40)
    
    gitignore_path = Path('.gitignore')
    
    if not gitignore_path.exists():
        print("❌ .gitignore file not found!")
        return False
    
    with open(gitignore_path, 'r') as f:
        gitignore_content = f.read()
    
    required_patterns = [
        '.env',
        '*.log',
        '__pycache__/',
        '.streamlit/secrets.toml'
    ]
    
    missing_patterns = []
    
    for pattern in required_patterns:
        if pattern not in gitignore_content:
            missing_patterns.append(pattern)
        else:
            print(f"✅ {pattern}")
    
    if missing_patterns:
        print(f"❌ Missing patterns: {missing_patterns}")
        return False
    
    print("✅ .gitignore properly configured")
    return True

def check_env_files():
    """Check environment file security."""
    
    print("\n🔑 Checking Environment Files...")
    print("-" * 40)
    
    env_files = ['.env', '.env.example', '.env.local', '.env.production']
    
    for env_file in env_files:
        if Path(env_file).exists():
            print(f"📄 Found: {env_file}")
            
            # Check if .env contains actual secrets
            if env_file == '.env':
                with open(env_file, 'r') as f:
                    content = f.read()
                    if 'AIza' in content and 'your_' not in content:
                        print(f"⚠️ {env_file} may contain real API keys!")
                    else:
                        print(f"✅ {env_file} appears safe (placeholders only)")
            else:
                print(f"✅ {env_file} (template file)")

def generate_security_report(issues):
    """Generate a security report."""
    
    print("\n" + "=" * 60)
    print("📊 SECURITY REPORT")
    print("=" * 60)
    
    if not issues:
        print("🎉 NO SECURITY ISSUES FOUND!")
        print("✅ Your codebase appears secure")
        return True
    
    print(f"🚨 FOUND {len(issues)} SECURITY ISSUES:")
    print()
    
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue['type']}")
        print(f"   📁 File: {issue['file']}")
        print(f"   📍 Line: {issue['line']}")
        print(f"   🔍 Content: {issue['secret']}")
        print()
    
    print("🔧 IMMEDIATE ACTIONS REQUIRED:")
    print("1. Revoke all exposed API keys immediately")
    print("2. Generate new API keys")
    print("3. Remove secrets from code")
    print("4. Use environment variables instead")
    print("5. Update .gitignore if needed")
    
    return False

def main():
    """Main security check function."""
    
    # Check for exposed secrets
    issues = check_for_exposed_secrets()
    
    # Check .gitignore
    gitignore_ok = check_gitignore()
    
    # Check environment files
    check_env_files()
    
    # Generate report
    secure = generate_security_report(issues)
    
    if secure and gitignore_ok:
        print("\n🛡️ SECURITY STATUS: SECURE")
        print("Your project follows security best practices!")
        return True
    else:
        print("\n⚠️ SECURITY STATUS: NEEDS ATTENTION")
        print("Please address the issues above before deploying!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)