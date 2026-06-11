#!/usr/bin/env python3
"""
CSV Category Name Updater

This script updates the category names in CSV files based on the rename.csv mapping.
"""

import csv
import os
from typing import Dict

def load_rename_mapping(rename_file: str) -> Dict[str, str]:
    """Load the category name mapping from rename.csv"""
    mapping = {}
    try:
        with open(rename_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                old_name = row['old_name'].strip()
                new_name = row['new_name'].strip()
                mapping[old_name] = new_name
        print(f"✅ Loaded {len(mapping)} category mappings from {rename_file}")
        return mapping
    except FileNotFoundError:
        print(f"❌ Rename file not found: {rename_file}")
        return {}
    except Exception as e:
        print(f"❌ Error loading rename file: {e}")
        return {}

def clean_category_name(category_name: str) -> str:
    """Clean category name by removing prefixes and formatting"""
    if not category_name:
        return category_name
    
    # Remove 'Webmall_' prefix
    cleaned = category_name.replace('Webmall_', '')
    
    # Replace underscores with spaces
    cleaned = cleaned.replace('_', ' ')
    
    # Fix multiple spaces
    import re
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned

def update_csv_file(csv_file: str, rename_mapping: Dict[str, str], backup: bool = True):
    """Update category names in a CSV file"""
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return False
    
    # Create backup if requested
    if backup:
        backup_file = csv_file + '.backup'
        import shutil
        shutil.copy2(csv_file, backup_file)
        print(f"📁 Created backup: {backup_file}")
    
    try:
        # Read the CSV file
        rows = []
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            
            # Find category column (case insensitive)
            category_col = None
            for field in fieldnames:
                if field.lower() == 'category':
                    category_col = field
                    break
            
            if not category_col:
                print(f"⚠️  No 'category' column found in {csv_file}")
                return False
            
            updated_count = 0
            for row in reader:
                original_category = row[category_col]
                if original_category:
                    # Clean the category name first
                    cleaned_category = clean_category_name(original_category)
                    
                    # Apply rename mapping if exists
                    if cleaned_category in rename_mapping:
                        row[category_col] = rename_mapping[cleaned_category]
                        updated_count += 1
                        print(f"  📝 Updated: '{original_category}' → '{row[category_col]}'")
                    else:
                        # Even if no mapping, use the cleaned version
                        if cleaned_category != original_category:
                            row[category_col] = cleaned_category
                            updated_count += 1
                            print(f"  🧹 Cleaned: '{original_category}' → '{cleaned_category}'")
                
                rows.append(row)
        
        # Write back to CSV file
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"✅ Updated {updated_count} category names in {csv_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {csv_file}: {e}")
        return False

def main():
    """Main function to update CSV files"""
    print("🔄 CSV Category Name Updater")
    print("=" * 50)
    
    # Load rename mapping
    rename_file = "../rename.csv"
    if not os.path.exists(rename_file):
        rename_file = "rename.csv"  # Try current directory
    
    rename_mapping = load_rename_mapping(rename_file)
    if not rename_mapping:
        print("❌ No rename mapping loaded. Exiting.")
        return
    
    # Print mapping for verification
    print("\n📋 Category Rename Mapping:")
    for old_name, new_name in rename_mapping.items():
        print(f"  '{old_name}' → '{new_name}'")
    
    # Find CSV files to update
    csv_files = [
        "results/WebMall 1.0 Results - By_Type_view.csv",
        "results/WebMall 1.0 Results - By_category_view.csv"
    ]
    
    # Check if files exist in current directory or parent
    existing_files = []
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            existing_files.append(csv_file)
        elif os.path.exists("../" + csv_file):
            existing_files.append("../" + csv_file)
        elif os.path.exists(os.path.basename(csv_file)):
            existing_files.append(os.path.basename(csv_file))
    
    if not existing_files:
        print("❌ No CSV files found to update!")
        print("Expected files:")
        for f in csv_files:
            print(f"  - {f}")
        return
    
    print(f"\n🎯 Found {len(existing_files)} CSV files to update:")
    for f in existing_files:
        print(f"  - {f}")
    
    # Auto-proceed with updates (backup files will be created automatically)
    print(f"\n⚠️  Updating category names in CSV files...")
    print("Backup files will be created automatically.")
    
    # Update each file
    print(f"\n🚀 Updating CSV files...")
    success_count = 0
    
    for csv_file in existing_files:
        print(f"\n📄 Processing {csv_file}:")
        if update_csv_file(csv_file, rename_mapping):
            success_count += 1
    
    print(f"\n✨ Update complete!")
    print(f"Successfully updated {success_count}/{len(existing_files)} files")
    
    if success_count > 0:
        print("\n💡 Remember to refresh your browser to see the updated category names!")

if __name__ == "__main__":
    main()