#!/usr/bin/env python3

import sqlite3
import os
import json
from datetime import datetime, timedelta
import glob

def get_database_stats():
    """Get current database statistics"""
    db_path = os.path.join(os.path.dirname(__file__), "data", "sqlite.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    stats = {}
    
    # Total candidates
    c.execute("SELECT COUNT(*) FROM candidates")
    stats['total_candidates'] = c.fetchone()[0]
    
    # Validated candidates
    c.execute("SELECT COUNT(*) FROM candidates WHERE validated=1")
    stats['validated'] = c.fetchone()[0]
    
    # Published posts
    c.execute("SELECT COUNT(*) FROM candidates WHERE published=1")
    stats['published'] = c.fetchone()[0]
    
    # Ready to publish
    c.execute("SELECT COUNT(*) FROM candidates WHERE validated=1 AND published=0")
    stats['ready_to_publish'] = c.fetchone()[0]
    
    # Posts by category
    c.execute("SELECT category, COUNT(*) FROM candidates WHERE published=1 GROUP BY category")
    stats['categories'] = dict(c.fetchall())
    
    # Recent activity - get last 10 candidates as proxy
    c.execute("SELECT COUNT(*) FROM candidates ORDER BY id DESC LIMIT 10")
    stats['recent_candidates'] = c.fetchone()[0]
    
    conn.close()
    return stats

def get_log_summary():
    """Get summary from recent log files"""
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    if not os.path.exists(log_dir):
        return {"message": "No logs directory found"}
    
    log_files = glob.glob(os.path.join(log_dir, "auto-pipeline-*.log"))
    if not log_files:
        return {"message": "No log files found"}
    
    # Get most recent log file
    latest_log = max(log_files, key=os.path.getctime)
    
    with open(latest_log, 'r') as f:
        content = f.read()
    
    # Extract key information
    summary = {
        "latest_run": os.path.basename(latest_log),
        "file_size": f"{os.path.getsize(latest_log)} bytes",
        "completed": "completed successfully" in content.lower(),
        "errors": content.lower().count("error"),
        "warnings": content.lower().count("warning")
    }
    
    return summary

def display_dashboard():
    """Display automation monitoring dashboard"""
    print("🤖 AUTOMATED CONTENT GENERATION DASHBOARD")
    print("=" * 50)
    print(f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Database Statistics
    stats = get_database_stats()
    print("📊 DATABASE STATISTICS")
    print(f"   Total Candidates: {stats['total_candidates']}")
    print(f"   Validated: {stats['validated']}")
    print(f"   Published: {stats['published']}")
    print(f"   Ready to Publish: {stats['ready_to_publish']}")
    print(f"   New (24h): {stats['recent_candidates']}")
    print()
    
    # Category Breakdown
    print("📂 PUBLISHED POSTS BY CATEGORY")
    for category, count in sorted(stats['categories'].items()):
        print(f"   {category}: {count} posts")
    print()
    
    # Log Summary
    log_summary = get_log_summary()
    print("📝 AUTOMATION STATUS")
    if "message" in log_summary:
        print(f"   {log_summary['message']}")
    else:
        status = "✅ SUCCESS" if log_summary['completed'] else "❌ ISSUES"
        print(f"   Latest Run: {status}")
        print(f"   Log File: {log_summary['latest_run']}")
        print(f"   Errors: {log_summary['errors']}")
        print(f"   Warnings: {log_summary['warnings']}")
    print()
    
    # Next Run Time (cron schedule: every 5 hours)
    now = datetime.now()
    next_hours = [h for h in [0, 5, 10, 15, 20] if h > now.hour]
    if next_hours:
        next_run = now.replace(hour=next_hours[0], minute=0, second=0, microsecond=0)
    else:
        next_run = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    
    print("⏰ SCHEDULE")
    print(f"   Next Run: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Time Until: {next_run - now}")
    print()
    
    print("🔍 MONITORING COMMANDS")
    print("   View live logs: tail -f logs/auto-pipeline-*.log")
    print("   Manual run: ./auto-pipeline.sh")
    print("   View this dashboard: python monitor.py")

if __name__ == "__main__":
    display_dashboard()