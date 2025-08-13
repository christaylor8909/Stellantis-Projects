import pandas as pd
import re
from datetime import datetime

def test_processing():
    """Test the STELLANTIS training report processing functionality"""
    print("Testing STELLANTIS Training Report Processor...")
    print("Focused on: SAL-2, SAL-3, SER-12, SER-1, SER-2 Job Roles")
    
    try:
        # Load the Excel file
        print("Loading Excel file...")
        df_original = pd.read_excel('Enterprise_Training_Report_20250730_02_56_56_PM.xlsx', header=None)
        print(f"Loaded {len(df_original)} rows and {len(df_original.columns)} columns")
        
        # Remove first 8 rows and set proper headers
        print("Removing first 8 rows and setting headers...")
        df_clean = df_original.iloc[8:].reset_index(drop=True)
        df_clean.columns = df_clean.iloc[0]
        df_clean = df_clean.iloc[1:].reset_index(drop=True)
        
        print(f"After cleaning: {len(df_clean)} rows")
        print(f"Columns: {list(df_clean.columns)}")
        
        # Define the 5 target job roles
        target_job_roles = [
            "SAL-2-New Vehicles Sales Advisor",
            "SAL-3-New Vehicles Sales Manager", 
            "SER-12-Technician",
            "SER-1-Aftersales Manager",
            "SER-2-Service Advisor"
        ]
        
        # Filter to only show the 5 target job roles
        print(f"\nFiltering to target job roles (SAL-2, SAL-3, SER-12, SER-1, SER-2)...")
        df_clean = df_clean[df_clean['Position'].isin(target_job_roles)]
        print(f"After filtering to target job roles: {len(df_clean)} rows")
        
        # Show breakdown by job role
        print(f"\nBreakdown by target job role:")
        for role in target_job_roles:
            role_count = len(df_clean[df_clean['Position'] == role])
            print(f"  {role}: {role_count} records")
        
        # Identify Level 1 and Level 2 training titles
        level1_titles = identify_level1_trainings(df_clean)
        level2_titles = identify_level2_trainings(df_clean)
        
        print(f"\nFound {len(level1_titles)} Level 1 training titles:")
        for title in level1_titles[:5]:  # Show first 5
            print(f"  - {title}")
        if len(level1_titles) > 5:
            print(f"  ... and {len(level1_titles) - 5} more")
            
        print(f"\nFound {len(level2_titles)} Level 2 training titles:")
        for title in level2_titles[:5]:  # Show first 5
            print(f"  - {title}")
        if len(level2_titles) > 5:
            print(f"  ... and {len(level2_titles) - 5} more")
        
        # Calculate completion percentages
        print("\nCalculating completion percentages...")
        completion_data = calculate_completion_percentages(df_clean, level1_titles, level2_titles)
        
        print(f"Processed {len(completion_data)} individuals")
        
        # Show sample results
        if completion_data:
            print("\nSample results (first 5 individuals):")
            for i, data in enumerate(completion_data[:5]):
                print(f"\n{i+1}. {data['First Name']} {data['Last Name']} ({data['User ID']})")
                print(f"   Job Role: {data['Job Role']}")
                print(f"   Brand: {data['User Brand']}")
                print(f"   Level 1: {data['Completed Level 1 Trainings']}/{data['Total Level 1 Trainings']} ({data['Level 1 Completion %']}%)")
                print(f"   Level 2: {data['Completed Level 2 Trainings']}/{data['Total Level 2 Trainings']} ({data['Level 2 Completion %']}%)")
                print(f"   Overall: {data['Overall Completion %']}%")
        
        # Create STELLANTIS format report
        summary_df = create_stellantis_report(completion_data)
        if len(summary_df) > 0:
            print(f"\nSTELLANTIS Report Summary:")
            print(f"Columns: {list(summary_df.columns)}")
            print(f"Total individuals: {len(summary_df)}")
            
            print(f"\nSummary Statistics:")
            if 'Level 1 Completion %' in summary_df.columns:
                print(f"Average Level 1 Completion: {summary_df['Level 1 Completion %'].mean():.2f}%")
            if 'Level 2 Completion %' in summary_df.columns:
                print(f"Average Level 2 Completion: {summary_df['Level 2 Completion %'].mean():.2f}%")
            if 'Overall Completion %' in summary_df.columns:
                print(f"Average Overall Completion: {summary_df['Overall Completion %'].mean():.2f}%")
            
            # Save test output
            output_file = f"STELLANTIS_Focused_test_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                summary_df.to_excel(writer, sheet_name='STELLANTIS_Training_Report', index=False)
                
                # Detailed completion summary
                detailed_df = pd.DataFrame(completion_data)
                detailed_df = detailed_df.sort_values('Overall Completion %', ascending=False)
                detailed_df.to_excel(writer, sheet_name='Detailed_Completion_Summary', index=False)
                
                level1_df = df_clean[df_clean['Training Title'].isin(level1_titles)]
                if len(level1_df) > 0:
                    level1_df.to_excel(writer, sheet_name='Level_1_Training_Details', index=False)
                
                level2_df = df_clean[df_clean['Training Title'].isin(level2_titles)]
                if len(level2_df) > 0:
                    level2_df.to_excel(writer, sheet_name='Level_2_Training_Details', index=False)
                
                titles_df = pd.DataFrame({
                    'Level 1 Training Titles': level1_titles,
                    'Level 2 Training Titles': level2_titles + [''] * max(0, len(level1_titles) - len(level2_titles))
                })
                titles_df.to_excel(writer, sheet_name='Training_Titles_Reference', index=False)
            
            print(f"\nSTELLANTIS focused test output saved to: {output_file}")
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

def identify_level1_trainings(df):
    """Identify Level 1 training titles"""
    level1_patterns = [
        r'LEVEL 1',
        r'INDUCTION LEVEL 1',
        r'BASIC LEVEL 1',
        r'FOUNDATION LEVEL 1',
        r'X01EN',  # Specific pattern for Level 1 trainings
        r'X01[A-Z]{2}',  # Broader pattern for Level 1 (X01 + 2 letters)
        r'CET_LEVEL 1',  # Additional pattern found in data
        r'CURRICULUM LEVEL 1',  # Additional pattern
        r'INDUCTION.*LEVEL 1',  # Broader induction pattern
        r'LEVEL 1.*INDUCTION',  # Alternative induction pattern
        r'BASIC.*LEVEL 1',  # Broader basic pattern
        r'FOUNDATION.*LEVEL 1'  # Broader foundation pattern
    ]
    
    level1_titles = set()
    for title in df['Training Title'].unique():
        title_str = str(title).upper()
        for pattern in level1_patterns:
            if re.search(pattern, title_str):
                level1_titles.add(title)
                break
                
    return list(level1_titles)

def identify_level2_trainings(df):
    """Identify Level 2 training titles"""
    level2_patterns = [
        r'LEVEL 2',
        r'ADVANCED LEVEL 2',
        r'INTERMEDIATE LEVEL 2',
        r'X02EN',  # Specific pattern for Level 2 trainings
        r'X02[A-Z]{2}'  # Broader pattern for Level 2 (X02 + 2 letters)
    ]
    
    level2_titles = set()
    for title in df['Training Title'].unique():
        title_str = str(title).upper()
        for pattern in level2_patterns:
            if re.search(pattern, title_str):
                level2_titles.add(title)
                break
                
    return list(level2_titles)

def extract_brand(user_df):
    """Extract brand information from training data"""
    # Look for brand information in training titles or other fields
    training_titles = user_df['Training Title'].astype(str).str.upper()
    
    if any('FIAT' in title for title in training_titles):
        return 'Fiat Professional'
    elif any('JEEP' in title for title in training_titles):
        return 'Jeep'
    elif any('PEUGEOT' in title for title in training_titles):
        return 'Peugeot'
    elif any('CITROEN' in title for title in training_titles):
        return 'Citroen'
    elif any('ALFA ROMEO' in title for title in training_titles):
        return 'Alfa Romeo'
    else:
        return 'Other'

def calculate_completion_percentages(df, level1_titles, level2_titles):
    """Calculate completion percentages for each individual"""
    completion_data = []
    
    # Group by User ID and User Full Name
    user_groups = df.groupby(['User ID', 'User Full Name'])
    
    for (user_id, user_name), user_df in user_groups:
        # Split full name into first and last name
        name_parts = str(user_name).split(', ')
        if len(name_parts) >= 2:
            last_name = name_parts[0]
            first_name = name_parts[1] if len(name_parts) > 1 else ""
        else:
            last_name = str(user_name)
            first_name = ""
        
        user_data = {
            'User ID': user_id,
            'First Name': first_name,
            'Last Name': last_name,
            'Job Role': user_df['Position'].iloc[0] if len(user_df) > 0 else '',
            'Dealer Name': user_df['Division'].iloc[0] if len(user_df) > 0 else '',
            'User Brand': extract_brand(user_df),
            'Total Level 1 Trainings': 0,
            'Completed Level 1 Trainings': 0,
            'Level 1 Completion %': 0.0,
            'Total Level 2 Trainings': 0,
            'Completed Level 2 Trainings': 0,
            'Level 2 Completion %': 0.0,
            'Overall Completion %': 0.0
        }
        
        # Level 1 calculations
        level1_df = user_df[user_df['Training Title'].isin(level1_titles)]
        user_data['Total Level 1 Trainings'] = len(level1_df)
        user_data['Completed Level 1 Trainings'] = len(level1_df[level1_df['Transcript Status'].isin(['Completed', 'Approved'])])
        
        if user_data['Total Level 1 Trainings'] > 0:
            user_data['Level 1 Completion %'] = round(
                (user_data['Completed Level 1 Trainings'] / user_data['Total Level 1 Trainings']) * 100, 2
            )
        
        # Level 2 calculations
        level2_df = user_df[user_df['Training Title'].isin(level2_titles)]
        user_data['Total Level 2 Trainings'] = len(level2_df)
        user_data['Completed Level 2 Trainings'] = len(level2_df[level2_df['Transcript Status'].isin(['Completed', 'Approved'])])
        
        if user_data['Total Level 2 Trainings'] > 0:
            user_data['Level 2 Completion %'] = round(
                (user_data['Completed Level 2 Trainings'] / user_data['Total Level 2 Trainings']) * 100, 2
            )
        
        # Overall completion percentage
        total_trainings = user_data['Total Level 1 Trainings'] + user_data['Total Level 2 Trainings']
        total_completed = user_data['Completed Level 1 Trainings'] + user_data['Completed Level 2 Trainings']
        
        if total_trainings > 0:
            user_data['Overall Completion %'] = round((total_completed / total_trainings) * 100, 2)
        
        completion_data.append(user_data)
        
    return completion_data

def create_stellantis_report(completion_data):
    """Create a STELLANTIS format report DataFrame"""
    if not completion_data:
        return pd.DataFrame()
        
    df = pd.DataFrame(completion_data)
    
    # Reorder columns to match STELLANTIS format
    column_order = [
        'User ID', 'First Name', 'Last Name', 'Job Role', 'Dealer Name', 
        'User Brand', 'Level 1 Completion %', 'Level 2 Completion %'
    ]
    
    # Filter to only include columns that exist
    existing_columns = [col for col in column_order if col in df.columns]
    df = df[existing_columns]
    
    # Sort by overall completion percentage (descending)
    if 'Overall Completion %' in df.columns:
        df = df.sort_values('Overall Completion %', ascending=False)
    
    return df

if __name__ == "__main__":
    test_processing()
