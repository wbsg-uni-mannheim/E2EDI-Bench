#!/usr/bin/env python3
"""
Benchmark Calculator Script

This script reads execution results from JSON files in the results/v1/ directory
and calculates performance benchmarks including execution times, token usage,
and cost analysis for different agent interface paradigms.
"""

import json
import os
import glob
import pandas as pd
from typing import Dict, List, Any
import statistics

# Model pricing per million tokens (MTok)
MODEL_PRICING = {
    'gpt-4.1': {'input': 2.00, 'output': 8.00},
    'claude-sonnet-4': {'input': 3.00, 'output': 15.00},
    'GPT-4.1': {'input': 2.00, 'output': 8.00},
    'Claude Sonnet 4': {'input': 3.00, 'output': 15.00}
}

def calculate_cost(prompt_tokens: int, completion_tokens: int, model: str) -> float:
    """Calculate cost based on token usage and model pricing."""
    model_key = model.lower().replace(' ', '-').replace('claude-sonnet-4', 'claude-sonnet-4')
    
    if model_key not in MODEL_PRICING:
        print(f"Warning: No pricing found for model {model}")
        return 0.0
    
    pricing = MODEL_PRICING[model_key]
    input_cost = (prompt_tokens / 1_000_000) * pricing['input']
    output_cost = (completion_tokens / 1_000_000) * pricing['output']
    
    return input_cost + output_cost

def extract_benchmark_data(json_file_path: str) -> Dict[str, Any]:
    """Extract benchmark data from a single JSON results file."""
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        # Extract metadata
        metadata = data.get('benchmark_metadata', {})
        
        # Determine paradigm from file path
        paradigm = 'unknown'
        if 'rag' in json_file_path.lower():
            paradigm = 'RAG_Agent'
        elif 'nlweb' in json_file_path.lower():
            paradigm = 'NlWeb_elastic'
        elif 'api_mcp' in json_file_path.lower() or 'mcp' in json_file_path.lower():
            paradigm = 'API_MCP'
        
        # Extract model info
        model = metadata.get('model', 'unknown')
        if 'gpt-4.1' in model.lower():
            model = 'GPT-4.1'
        elif 'sonnet' in model.lower():
            model = 'Claude Sonnet 4'
        
        # Extract execution time stats
        exec_stats = metadata.get('execution_time_stats', {})
        
        # Extract token usage
        token_usage = metadata.get('token_usage', {})
        
        # Calculate averages
        total_tasks = metadata.get('total_tasks', 0)
        avg_execution_time = exec_stats.get('average_seconds', 0)
        
        prompt_tokens = token_usage.get('prompt_tokens', 0)
        completion_tokens = token_usage.get('completion_tokens', 0)
        
        avg_prompt_tokens = prompt_tokens / total_tasks if total_tasks > 0 else 0
        avg_completion_tokens = completion_tokens / total_tasks if total_tasks > 0 else 0
        
        # Calculate cost
        avg_cost = calculate_cost(avg_prompt_tokens, avg_completion_tokens, model)
        
        return {
            'paradigm': paradigm,
            'model': model,
            'total_tasks': total_tasks,
            'avg_execution_time': avg_execution_time,
            'min_execution_time': exec_stats.get('min_seconds', 0),
            'max_execution_time': exec_stats.get('max_seconds', 0),
            'total_prompt_tokens': prompt_tokens,
            'total_completion_tokens': completion_tokens,
            'avg_prompt_tokens': avg_prompt_tokens,
            'avg_completion_tokens': avg_completion_tokens,
            'avg_cost_per_task': avg_cost,
            'file_path': json_file_path
        }
        
    except Exception as e:
        print(f"Error processing {json_file_path}: {e}")
        return None

def find_result_files(base_path: str) -> List[str]:
    """Find all JSON result files in the results directory."""
    json_files = []
    
    # Look for JSON files in subdirectories
    patterns = [
        os.path.join(base_path, '**/*.json'),
        os.path.join(base_path, '**/results*.json'),
        os.path.join(base_path, '**/benchmark*.json')
    ]
    
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        json_files.extend(files)
    
    # Remove duplicates and filter for relevant files
    json_files = list(set(json_files))
    json_files = [f for f in json_files if 'results' in os.path.basename(f) or 'benchmark' in os.path.basename(f)]
    
    return json_files

def create_benchmark_summary(benchmark_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Create a summary DataFrame from benchmark data."""
    df = pd.DataFrame(benchmark_data)
    
    if df.empty:
        print("No benchmark data found!")
        return df
    
    # Group by paradigm and model
    summary = df.groupby(['paradigm', 'model']).agg({
        'avg_execution_time': 'mean',
        'avg_prompt_tokens': 'mean',
        'avg_completion_tokens': 'mean',
        'avg_cost_per_task': 'mean',
        'total_tasks': 'sum'
    }).round(2)
    
    return summary

def generate_runtime_estimates() -> Dict[str, Dict[str, float]]:
    """Generate runtime estimates for different paradigms and models."""
    return {
        'RAG_Agent': {
            'GPT-4.1': 6.9,
            'Claude Sonnet 4': 8.2
        },
        'API_MCP': {
            'GPT-4.1': 3.5,
            'Claude Sonnet 4': 3.5
        },
        'NlWeb_elastic': {
            'GPT-4.1': 4.2,
            'Claude Sonnet 4': 4.2
        },
        'AX+Mem': {
            'GPT-4.1': {'Basic': 142.4, 'Advanced': 155.4},
            'Claude Sonnet 4': {'Basic': 142.4, 'Advanced': 155.4}
        }
    }

def main():
    """Main function to calculate and display benchmark results."""
    print("🔍 WebMall Agent Interface Benchmark Calculator")
    print("=" * 50)
    
    # Find result files
    base_path = "../results/v1"
    if not os.path.exists(base_path):
        base_path = "results/v1"  # Try from repo root
    if not os.path.exists(base_path):
        print(f"❌ Results directory not found: {base_path}")
        print("Please make sure you're running this script from the correct directory.")
        return
    
    json_files = find_result_files(base_path)
    print(f"📁 Found {len(json_files)} JSON result files")
    
    if not json_files:
        print("❌ No JSON result files found!")
        return
    
    # Process each file
    benchmark_data = []
    for json_file in json_files:
        print(f"📊 Processing: {json_file}")
        data = extract_benchmark_data(json_file)
        if data:
            benchmark_data.append(data)
    
    if not benchmark_data:
        print("❌ No valid benchmark data extracted!")
        return
    
    print(f"\n✅ Successfully processed {len(benchmark_data)} files")
    
    # Create summary
    summary_df = create_benchmark_summary(benchmark_data)
    
    print("\n📈 BENCHMARK SUMMARY")
    print("=" * 50)
    print(summary_df.to_string())
    
    # Display individual results
    print("\n📋 DETAILED RESULTS")
    print("=" * 50)
    
    for data in benchmark_data:
        print(f"\nParadigm: {data['paradigm']}")
        print(f"Model: {data['model']}")
        print(f"Total Tasks: {data['total_tasks']}")
        print(f"Avg Execution Time: {data['avg_execution_time']:.1f}s")
        print(f"Avg Prompt Tokens: {data['avg_prompt_tokens']:,.0f}")
        print(f"Avg Completion Tokens: {data['avg_completion_tokens']:,.0f}")
        print(f"Avg Cost per Task: ${data['avg_cost_per_task']:.3f}")
        print(f"File: {os.path.basename(data['file_path'])}")
        print("-" * 30)
    
    # Generate runtime estimates for JavaScript
    print("\n🚀 RUNTIME ESTIMATES FOR JAVASCRIPT")
    print("=" * 50)
    
    estimates = generate_runtime_estimates()
    
    print("// Runtime estimates based on benchmark data")
    print("const runtimeEstimates = {")
    for paradigm, models in estimates.items():
        print(f"    '{paradigm}': {{")
        for model, runtime in models.items():
            if isinstance(runtime, dict):
                print(f"        '{model}': {{")
                for task_type, time_val in runtime.items():
                    print(f"            '{task_type}': {time_val},")
                print("        },")
            else:
                print(f"        '{model}': {runtime},")
        print("    },")
    print("};")
    
    # Export to CSV for use in website
    if benchmark_data:
        df_export = pd.DataFrame(benchmark_data)
        output_file = "website/benchmark_results.csv"
        df_export.to_csv(output_file, index=False)
        print(f"\n💾 Results exported to: {output_file}")
    
    print("\n✨ Benchmark calculation complete!")

if __name__ == "__main__":
    main()