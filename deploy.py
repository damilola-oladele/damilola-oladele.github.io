#!/usr/bin/env python3
"""
Git Deployment Automation Script
Automates the workflow of pushing changes from main to production branch.

DESCRIPTION:
    This script automates the repetitive Git workflow for deploying changes from
    the 'main' development branch to the 'production' branch on GitHub. It provides
    an interactive command-line interface with clear status messages at every step.

PREREQUISITES:
    - Python 3.6 or higher
    - Git installed and configured
    - A Git repository with 'main' and 'production' branches
    - Remote repository configured as 'origin'

INSTALLATION:
    1. Save this script as 'deploy.py' in your repository root
    2. Make it executable (Unix/Linux/Mac):
       chmod +x deploy.py
    3. (Optional) Add to .gitignore if you don't want to track it

USAGE:
    Run the script from your repository root directory:
    
    python3 deploy.py
    
    Or if made executable:
    
    ./deploy.py

WORKFLOW:
    The script follows this automated workflow:
    
    1. BRANCH CHECK
       - Verifies you're on the 'main' branch
       - Offers to switch if you're on a different branch
       - Exits if switch fails or is declined
    
    2. STATUS CHECK
       - Checks for uncommitted changes
       - Exits if no changes are found
       - Displays current status if changes exist
    
    3. STAGING & COMMITTING (Two Options)
       
       Option A: Stage All at Once
       - Stages all changes with 'git add .'
       - Prompts for a single commit message
       - Commits all changes together
       - Proceeds directly to publishing
       
       Option B: Individual Staging
       - Interactive loop for staging specific files/patterns
       - Enter file paths like: src/file.js or patterns like: docs/*
       - Prompts for commit message for each staged group
       - Repeats until you're done staging
       - Asks if you want to publish now or later
    
    4. PUBLISHING FLOW
       - Switches to 'production' branch
       - Resets 'production' to match 'main' exactly
       - Pushes 'production' branch to remote
       - Pushes 'main' branch to remote
       - Switches back to 'main' branch
       - Displays deployment complete message

EXAMPLES:
    
    Example 1: Stage all changes at once
    $ python3 deploy.py
    Do you want to stage all changes at once? (yes/no): yes
    Enter commit message: Fix login bug and update docs
    
    Example 2: Stage files individually
    $ python3 deploy.py
    Do you want to stage all changes at once? (yes/no): no
    Enter file path(s) or pattern(s) to stage: src/auth.js
    Enter commit message for these files: Fix login bug
    Do you want to continue staging and committing more files? (yes/no): yes
    Enter file path(s) or pattern(s) to stage: docs/*
    Enter commit message for these files: Update documentation
    Do you want to continue staging and committing more files? (yes/no): no
    Do you wish to Publish Now? (yes/no): yes

INTERRUPTING THE SCRIPT:
    Press Ctrl+C at any time to safely exit the script.

ERROR HANDLING:
    The script provides clear error messages for common issues:
    - Not in a Git repository
    - Git commands fail
    - Invalid branch operations
    - Network issues during push
    
    All errors will stop the script with a descriptive message.

NOTES:
    - The script uses 'git reset --hard' on production, which is destructive
    - Always ensure your 'main' branch is in the desired state before publishing
    - The production branch will be force-synced to match main exactly
    - All staged changes must be committed before publishing

AUTHOR:
    Created for automating Git deployment workflows

VERSION:
    1.0.0
"""

import subprocess
import sys


def run_command(command, capture_output=True):
    """Execute a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=capture_output,
            text=True,
            check=False
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)


def get_current_branch():
    """Get the current Git branch name."""
    success, output, _ = run_command("git rev-parse --abbrev-ref HEAD")
    return output if success else None


def ask_yes_no(question):
    """Prompt user for yes/no answer."""
    while True:
        answer = input(f"{question} (yes/no): ").strip().lower()
        if answer in ['yes', 'y']:
            return True
        elif answer in ['no', 'n']:
            return False
        else:
            print("Please answer 'yes' or 'no'.")


def check_and_switch_branch():
    """Step 1: Verify current branch is main, or offer to switch."""
    print("\n=== Branch Check ===")
    current_branch = get_current_branch()
    
    if not current_branch:
        print("❌ ERROR: Could not determine current branch. Are you in a Git repository?")
        sys.exit(1)
    
    if current_branch == "main":
        print(f"✓ SUCCESS: You are on the 'main' branch.")
        return True
    
    print(f"⚠ WARNING: Current branch is '{current_branch}', but 'main' is required.")
    
    if ask_yes_no("Do you want to switch to 'main' now?"):
        success, _, error = run_command("git checkout main")
        if success:
            print("✓ SUCCESS: Switched to 'main' branch.")
            return True
        else:
            print(f"❌ ERROR: Failed to switch to 'main' branch. {error}")
            sys.exit(1)
    else:
        print("❌ STOPPED: User declined to switch to 'main' branch.")
        sys.exit(1)


def check_status():
    """Step 2: Check for uncommitted changes."""
    print("\n=== Status Check ===")
    success, output, _ = run_command("git status --porcelain")
    
    if not success:
        print("❌ ERROR: Failed to check Git status.")
        sys.exit(1)
    
    if not output:
        print("✓ No uncommitted changes found. Nothing to deploy.")
        sys.exit(0)
    
    print("✓ Uncommitted changes detected:")
    run_command("git status", capture_output=False)
    return True


def stage_all_and_commit():
    """Path A: Stage all changes and commit."""
    print("\n=== Staging All Changes ===")
    
    success, _, error = run_command("git add .")
    if success:
        print("✓ SUCCESS: All changes staged.")
    else:
        print(f"❌ ERROR: Failed to stage changes. {error}")
        sys.exit(1)
    
    commit_message = input("\nEnter commit message: ").strip()
    if not commit_message:
        print("❌ ERROR: Commit message cannot be empty.")
        sys.exit(1)
    
    success, _, error = run_command(f'git commit -m "{commit_message}"')
    if success:
        print("✓ SUCCESS: Changes committed.")
        return True
    else:
        print(f"❌ ERROR: Failed to commit changes. {error}")
        sys.exit(1)


def stage_individual_and_commit():
    """Path B: Interactive loop for staging and committing individual files."""
    print("\n=== Individual Staging Mode ===")
    
    while True:
        print("\n--- Current Status ---")
        run_command("git status", capture_output=False)
        
        files = input("\nEnter file path(s) or pattern(s) to stage (e.g., src/file.js, docs/*): ").strip()
        if not files:
            print("⚠ WARNING: No files specified.")
            continue
        
        success, _, error = run_command(f"git add {files}")
        if success:
            print(f"✓ SUCCESS: Staged '{files}'.")
        else:
            print(f"❌ ERROR: Failed to stage '{files}'. {error}")
            continue
        
        commit_message = input("Enter commit message for these files: ").strip()
        if not commit_message:
            print("❌ ERROR: Commit message cannot be empty.")
            continue
        
        success, _, error = run_command(f'git commit -m "{commit_message}"')
        if success:
            print("✓ SUCCESS: Changes committed.")
        else:
            print(f"❌ ERROR: Failed to commit changes. {error}")
        
        if not ask_yes_no("\nDo you want to continue staging and committing more files?"):
            break
    
    print("\n=== Staging Complete ===")
    if ask_yes_no("Do you wish to Publish Now?"):
        return True
    else:
        print("✓ Quit to publish later. Exiting.")
        sys.exit(0)


def publish_to_production():
    """Step 4: Publish changes to production branch."""
    print("\n=== Starting Deployment to Production ===")
    
    # Checkout production
    success, _, error = run_command("git checkout production")
    if success:
        print("✓ SUCCESS: Switched to 'production' branch.")
    else:
        print(f"❌ ERROR: Failed to switch to 'production' branch. {error}")
        sys.exit(1)
    
    # Reset production to match main
    success, _, error = run_command("git reset --hard main")
    if success:
        print("✓ SUCCESS: Synchronized 'production' with 'main'.")
    else:
        print(f"❌ ERROR: Failed to reset 'production' branch. {error}")
        sys.exit(1)
    
    # Push production
    success, _, error = run_command("git push origin production")
    if success:
        print("✓ SUCCESS: Pushed 'production' branch to remote.")
    else:
        print(f"❌ ERROR: Failed to push 'production' branch. {error}")
        sys.exit(1)
    
    # Push main
    success, _, error = run_command("git push origin main")
    if success:
        print("✓ SUCCESS: Pushed 'main' branch to remote.")
    else:
        print(f"❌ ERROR: Failed to push 'main' branch. {error}")
        sys.exit(1)
    
    # Return to main
    success, _, error = run_command("git checkout main")
    if success:
        print("✓ SUCCESS: Switched back to 'main' branch.")
    else:
        print(f"❌ ERROR: Failed to switch back to 'main' branch. {error}")
        sys.exit(1)
    
    print("\n🎉 DEPLOYMENT COMPLETE! 🎉")


def main():
    """Main workflow execution."""
    print("=" * 60)
    print("Git Deployment Automation Script")
    print("=" * 60)
    
    # Step 1: Branch check
    check_and_switch_branch()
    
    # Step 2: Status check
    check_status()
    
    # Step 3: Staging and committing
    if ask_yes_no("\nDo you want to stage all changes at once?"):
        stage_all_and_commit()
        publish_to_production()
    else:
        if stage_individual_and_commit():
            publish_to_production()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Script interrupted by user. Exiting.")
        sys.exit(1)