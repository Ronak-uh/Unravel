#!/usr/bin/env python3
"""
Modular Automation Pipeline for Unravel

Orchestrates Research → Validation → Writing → Publishing agents
using Gemini 2.5 Flash model for enhanced content generation.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add the agents directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

from research_agent import ResearchAgent
from validation_agent import ValidationAgent
from writer_agent import WriterAgent
from publisher_agent import PublisherAgent

def load_environment():
    """Load and validate environment variables."""
    load_dotenv()
    
    required_vars = {
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'GHOST_URL': os.getenv('GHOST_URL'),
        'GHOST_ADMIN_API_KEY': os.getenv('GHOST_ADMIN_API_KEY')
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set them in your .env file")
        return None
    
    return required_vars

def run_full_pipeline():
    """Run the complete automation pipeline."""
    print("🚀 Starting Unravel Content Automation Pipeline")
    print("=" * 60)
    
    # Load environment variables
    env_vars = load_environment()
    if not env_vars:
        return False
    
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, 'data', 'sqlite.db')
    
    try:
        # Initialize agents
        print("🔧 Initializing agents...")
        research_agent = ResearchAgent(db_path)
        validation_agent = ValidationAgent(db_path, env_vars['GEMINI_API_KEY'])
        writer_agent = WriterAgent(db_path, env_vars['GEMINI_API_KEY'])
        publisher_agent = PublisherAgent(db_path, env_vars['GHOST_URL'], env_vars['GHOST_ADMIN_API_KEY'])
        
        print("✅ All agents initialized successfully")
        print()
        
        # Phase 1: Research
        print("📚 PHASE 1: RESEARCH")
        print("-" * 30)
        research_results = research_agent.research_and_add_candidates(limit=8)
        print(f"Research completed: {research_results} new candidates added")
        print()
        
        # Phase 2: Validation
        print("🔍 PHASE 2: VALIDATION")
        print("-" * 30)
        validation_results = validation_agent.validate_candidates(limit=8)
        print(f"Validation completed: {validation_results} candidates validated")
        print()
        
        # Phase 3: Content Generation
        print("✍️ PHASE 3: CONTENT GENERATION")
        print("-" * 30)
        writing_results = writer_agent.write_content(limit=4)
        print(f"Content generation completed: {writing_results} posts written")
        print()
        
        # Phase 4: Publishing
        print("📤 PHASE 4: PUBLISHING")
        print("-" * 30)
        publishing_results = publisher_agent.publish_content(limit=4)
        print(f"Publishing completed: {publishing_results} posts published")
        print()
        
        # Final statistics
        print("📊 FINAL STATISTICS")
        print("-" * 30)
        
        research_stats = research_agent.get_candidates_stats()
        validation_stats = validation_agent.get_validation_stats()
        writing_stats = writer_agent.get_writing_stats()
        publishing_stats = publisher_agent.get_publishing_stats()
        
        print(f"📊 Total candidates: {research_stats['total']}")
        print(f"📊 Validated: {validation_stats['total_validated']} (avg score: {validation_stats['average_score']})")
        print(f"📊 Content written: {writing_stats['total_written']} (with images: {writing_stats['with_images']})")
        print(f"📊 Published: {publishing_stats['total_published']}")
        print(f"📊 Ready to publish: {publishing_stats['ready_to_publish']}")
        print()
        
        # Success summary
        total_processed = research_results + validation_results + writing_results + publishing_results
        if total_processed > 0:
            print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
            print(f"✅ Research: {research_results} candidates")
            print(f"✅ Validation: {validation_results} candidates")
            print(f"✅ Writing: {writing_results} posts")
            print(f"✅ Publishing: {publishing_results} posts")
        else:
            print("ℹ️ Pipeline completed - no new content to process")
        
        return True
        
    except Exception as e:
        print(f"❌ Pipeline error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_single_phase(phase):
    """Run a single phase of the pipeline."""
    env_vars = load_environment()
    if not env_vars:
        return False
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, 'data', 'sqlite.db')
    
    try:
        if phase == 'research':
            agent = ResearchAgent(db_path)
            result = agent.research_and_add_candidates(limit=8)
            print(f"Research completed: {result} new candidates added")
            
        elif phase == 'validation':
            agent = ValidationAgent(db_path, env_vars['GEMINI_API_KEY'])
            result = agent.validate_candidates(limit=8)
            print(f"Validation completed: {result} candidates validated")
            
        elif phase == 'writing':
            agent = WriterAgent(db_path, env_vars['GEMINI_API_KEY'])
            result = agent.write_content(limit=4)
            print(f"Content generation completed: {result} posts written")
            
        elif phase == 'publishing':
            agent = PublisherAgent(db_path, env_vars['GHOST_URL'], env_vars['GHOST_ADMIN_API_KEY'])
            result = agent.publish_content(limit=4)
            print(f"Publishing completed: {result} posts published")
            
        else:
            print(f"❌ Unknown phase: {phase}")
            print("Available phases: research, validation, writing, publishing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error in {phase} phase: {str(e)}")
        return False

def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        phase = sys.argv[1].lower()
        print(f"🚀 Running {phase.title()} Phase Only")
        print("=" * 40)
        success = run_single_phase(phase)
    else:
        success = run_full_pipeline()
    
    if success:
        print(f"\n🎉 Automation completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        sys.exit(0)
    else:
        print(f"\n❌ Automation failed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        sys.exit(1)

if __name__ == "__main__":
    main()