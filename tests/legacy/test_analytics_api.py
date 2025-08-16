#!/usr/bin/env python3
"""
Test de analytics API endpoints
"""

import requests
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def test_analytics_summary():
    """Test analytics summary endpoint"""
    try:
        response = requests.get("http://localhost:8002/api/analytics/summary")
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("success"):
            summary = data["data"]
            
            console.print(Panel.fit("📊 Analytics Summary", style="bold green"))
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Total Entries", str(summary.get("total_entries", 0)))
            table.add_row("Avg Emotion", f"{summary.get('avg_emotional_intensity', 0):.2f}")
            table.add_row("Avg Coherence", f"{summary.get('avg_awareness_coherence', 0):.2f}")
            
            # Entry types
            by_type = summary.get("entries_by_type", {})
            for entry_type, count in by_type.items():
                table.add_row(f"  {entry_type}", str(count))
            
            console.print(table)
            return True
        else:
            console.print(f"❌ API Error: {data}")
            return False
            
    except Exception as e:
        console.print(f"❌ Request failed: {e}")
        return False

def test_analytics_trends():
    """Test analytics trends endpoint"""
    try:
        response = requests.get("http://localhost:8002/api/analytics/trends")
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("success"):
            trends = data["data"]
            
            console.print(Panel.fit("📈 Analytics Trends", style="bold blue"))
            
            # Growth metrics
            growth_metrics = trends.get("growth_metrics", [])
            if growth_metrics:
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Metric", style="cyan")
                table.add_column("Trend", style="green")
                table.add_column("Significance", style="yellow")
                
                for metric in growth_metrics:
                    table.add_row(
                        metric.get("metric_name", ""),
                        metric.get("trend", ""),
                        f"{metric.get('significance', 0):.2f}"
                    )
                
                console.print(table)
            else:
                console.print("No growth metrics available")
            
            return True
        else:
            console.print(f"❌ API Error: {data}")
            return False
            
    except Exception as e:
        console.print(f"❌ Request failed: {e}")
        return False

def test_analytics_insights():
    """Test analytics insights endpoint"""
    try:
        response = requests.get("http://localhost:8002/api/analytics/insights")
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("success"):
            insights = data["data"]
            
            console.print(Panel.fit("💡 Analytics Insights", style="bold yellow"))
            
            # Summary
            summary = insights.get("summary", {})
            console.print(f"Total entries: {summary.get('total_entries', 0)}")
            
            # Clusters
            clusters = insights.get("clusters", [])
            if clusters:
                console.print(f"\n🎯 Found {len(clusters)} theme clusters")
                for i, cluster in enumerate(clusters[:3]):  # Show first 3
                    console.print(f"  Cluster {i+1}: {cluster.get('theme_name', 'Unknown')}")
            
            return True
        else:
            console.print(f"❌ API Error: {data}")
            return False
            
    except Exception as e:
        console.print(f"❌ Request failed: {e}")
        return False

def main():
    console.print("🚀 Testing Analytics API Endpoints")
    console.print("=" * 50)
    
    # Test all endpoints
    summary_ok = test_analytics_summary()
    console.print()
    
    trends_ok = test_analytics_trends()
    console.print()
    
    insights_ok = test_analytics_insights()
    console.print()
    
    # Results
    console.print("=" * 50)
    console.print("📊 TEST RESULTS:")
    console.print(f"   Summary: {'✅' if summary_ok else '❌'}")
    console.print(f"   Trends: {'✅' if trends_ok else '❌'}")
    console.print(f"   Insights: {'✅' if insights_ok else '❌'}")
    
    if summary_ok and trends_ok and insights_ok:
        console.print("\n🎉 All analytics endpoints working!")
    else:
        console.print("\n⚠️ Some endpoints have issues")

if __name__ == "__main__":
    main()
