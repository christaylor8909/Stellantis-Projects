import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
from datetime import datetime
import re

class TrainingReportProcessor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("STELLANTIS Training Report Processor")
        self.root.geometry("900x700")
        
        # Configuration for easy pattern management
        self.config = {
            'level1_patterns': [
                # Core patterns
                r'LEVEL 1',
                r'INDUCTION LEVEL 1',
                r'BASIC LEVEL 1',
                r'FOUNDATION LEVEL 1',
                
                # X01 patterns (specific to your naming convention)
                r'X01EN',  # Specific pattern for Level 1 trainings
                r'X01[A-Z]{2}',  # Broader pattern for Level 1 (X01 + 2 letters)
                
                # Additional patterns found in data
                r'CET_LEVEL 1',
                r'CURRICULUM LEVEL 1',
                
                # Flexible patterns with wildcards
                r'INDUCTION.*LEVEL 1',  # INDUCTION anywhere before LEVEL 1
                r'LEVEL 1.*INDUCTION',  # LEVEL 1 before INDUCTION
                r'BASIC.*LEVEL 1',      # BASIC anywhere before LEVEL 1
                r'FOUNDATION.*LEVEL 1', # FOUNDATION anywhere before LEVEL 1
                
                # Future-proof patterns (can be easily extended)
                r'BEGINNER.*LEVEL 1',   # For potential future naming
                r'ENTRY.*LEVEL 1',      # For potential future naming
                r'STARTER.*LEVEL 1',    # For potential future naming
                r'FUNDAMENTAL.*LEVEL 1', # For potential future naming
                
                # Brand-specific patterns (can be extended for new brands)
                r'.*TRAINING PATH.*LEVEL 1',
                r'.*CURRICULUM.*LEVEL 1',
                r'.*PROGRAM.*LEVEL 1'
            ],
            'level2_patterns': [
                # Core patterns
                r'LEVEL 2',
                r'ADVANCED LEVEL 2',
                r'INTERMEDIATE LEVEL 2',
                
                # X02 patterns (specific to your naming convention)
                r'X02EN',  # Specific pattern for Level 2 trainings
                r'X02[A-Z]{2}',  # Broader pattern for Level 2 (X02 + 2 letters)
                
                # Future-proof patterns (can be easily extended)
                r'ADVANCED.*LEVEL 2',    # ADVANCED anywhere before LEVEL 2
                r'INTERMEDIATE.*LEVEL 2', # INTERMEDIATE anywhere before LEVEL 2
                r'PROFESSIONAL.*LEVEL 2', # For potential future naming
                r'EXPERT.*LEVEL 2',      # For potential future naming
                r'MASTER.*LEVEL 2',      # For potential future naming
                
                # Brand-specific patterns (can be extended for new brands)
                r'.*TRAINING PATH.*LEVEL 2',
                r'.*CURRICULUM.*LEVEL 2',
                r'.*PROGRAM.*LEVEL 2'
            ],
            'target_job_roles': [
                "SAL-2-New Vehicles Sales Advisor",
                "SAL-3-New Vehicles Sales Manager", 
                "SER-12-Technician",
                "SER-1-Aftersales Manager",
                "SER-2-Service Advisor"
            ]
        }
        
        # Define the 5 specific job roles we want to show
        self.target_job_roles = self.config['target_job_roles']
        
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.input_file_path = tk.StringVar()
        self.output_file_path = tk.StringVar()
        self.selected_job_roles = tk.StringVar(value="SAL-2-New Vehicles Sales Advisor")
        self.df_original = None
        self.df_processed = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title with STELLANTIS branding
        title_label = ttk.Label(main_frame, text="STELLANTIS Training Report Processor", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Subtitle explaining the focus
        subtitle_label = ttk.Label(main_frame, text="Focused on: SAL-2, SAL-3, SER-12, SER-1, SER-2 Job Roles", 
                                  font=('Arial', 10, 'italic'), foreground='#666666')
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Input file selection
        ttk.Label(main_frame, text="Input Excel File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_file_path, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_input_file).grid(row=2, column=2, padx=(5, 0), pady=5)
        
        # Output file selection
        ttk.Label(main_frame, text="Output Excel File:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_file_path, width=50).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output_file).grid(row=3, column=2, padx=(5, 0), pady=5)
        
        # Job Role Filter (now only shows the 5 specific roles)
        ttk.Label(main_frame, text="Job Role Filter:").grid(row=4, column=0, sticky=tk.W, pady=5)
        job_role_combo = ttk.Combobox(main_frame, textvariable=self.selected_job_roles, 
                                     values=self.target_job_roles,
                                     state="readonly", width=47)
        job_role_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        job_role_combo.set("SAL-2-New Vehicles Sales Advisor")
        
        # Process button
        process_btn = ttk.Button(main_frame, text="Generate Training Report", 
                                command=self.process_report, style='Accent.TButton')
        process_btn.grid(row=5, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Processing Results", padding="10")
        results_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)
        
        # Text widget for results
        self.results_text = tk.Text(results_frame, height=15, width=80, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to generate STELLANTIS training report (SAL-2, SAL-3, SER-12, SER-1, SER-2)")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure main frame row weights
        main_frame.rowconfigure(7, weight=1)
        
    def browse_input_file(self):
        filename = filedialog.askopenfilename(
            title="Select Input Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filename:
            self.input_file_path.set(filename)
            # Auto-generate output filename
            base_name = os.path.splitext(filename)[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"{base_name}_STELLANTIS_Report_{timestamp}.xlsx"
            self.output_file_path.set(output_name)
            
    def browse_output_file(self):
        filename = filedialog.asksaveasfilename(
            title="Save STELLANTIS Report As",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if filename:
            self.output_file_path.set(filename)
            
    def process_report(self):
        if not self.input_file_path.get():
            messagebox.showerror("Error", "Please select an input Excel file")
            return
            
        if not self.output_file_path.get():
            messagebox.showerror("Error", "Please select an output Excel file")
            return
            
        try:
            self.status_var.set("Processing...")
            self.progress.start()
            self.root.update()
            
            # Load the Excel file
            self.log_message("Loading Excel file...")
            self.df_original = pd.read_excel(self.input_file_path.get(), header=None)
            self.log_message(f"Loaded {len(self.df_original)} rows and {len(self.df_original.columns)} columns")
            
            # Remove first 8 rows and set proper headers
            self.log_message("Removing first 8 rows and setting headers...")
            df_clean = self.df_original.iloc[8:].reset_index(drop=True)
            df_clean.columns = df_clean.iloc[0]
            df_clean = df_clean.iloc[1:].reset_index(drop=True)
            
            self.log_message(f"After cleaning: {len(df_clean)} rows")
            
            # Filter to only show the 5 target job roles
            self.log_message("Filtering to target job roles (SAL-2, SAL-3, SER-12, SER-1, SER-2)...")
            df_clean = df_clean[df_clean['Position'].isin(self.target_job_roles)]
            self.log_message(f"After filtering to target job roles: {len(df_clean)} rows")
            
            # Show breakdown by job role
            for role in self.target_job_roles:
                role_count = len(df_clean[df_clean['Position'] == role])
                self.log_message(f"  {role}: {role_count} records")
            
            # Apply specific job role filter if selected
            if self.selected_job_roles.get() in self.target_job_roles:
                job_role = self.selected_job_roles.get()
                df_clean = df_clean[df_clean['Position'] == job_role]
                self.log_message(f"Filtered to {job_role}: {len(df_clean)} rows")
            
            # Identify Level 1 and Level 2 training titles
            level1_titles = self.identify_level1_trainings(df_clean)
            level2_titles = self.identify_level2_trainings(df_clean)
            
            self.log_message(f"Found {len(level1_titles)} Level 1 training titles")
            self.log_message(f"Found {len(level2_titles)} Level 2 training titles")
            
            # Calculate completion percentages per individual
            self.log_message("Calculating completion percentages...")
            completion_data = self.calculate_completion_percentages(df_clean, level1_titles, level2_titles)
            
            # Create summary report
            self.log_message("Creating STELLANTIS format report...")
            summary_df = self.create_stellantis_report(completion_data)
            
            # Save to Excel with multiple sheets
            self.log_message("Saving to Excel...")
            self.save_to_excel(summary_df, completion_data, level1_titles, level2_titles)
            
            self.progress.stop()
            self.status_var.set("STELLANTIS training report generated successfully!")
            messagebox.showinfo("Success", f"STELLANTIS training report generated successfully!\nOutput saved to: {self.output_file_path.get()}")
            
        except Exception as e:
            self.progress.stop()
            self.status_var.set("Error occurred during processing")
            self.log_message(f"ERROR: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def identify_level1_trainings(self, df):
        """Identify Level 1 training titles with flexible pattern matching"""
        level1_patterns = self.config['level1_patterns']
        
        level1_titles = set()
        for title in df['Training Title'].unique():
            title_str = str(title).upper()
            for pattern in level1_patterns:
                if re.search(pattern, title_str):
                    level1_titles.add(title)
                    break
                    
        return list(level1_titles)
        
    def identify_level2_trainings(self, df):
        """Identify Level 2 training titles with flexible pattern matching"""
        level2_patterns = self.config['level2_patterns']
        
        level2_titles = set()
        for title in df['Training Title'].unique():
            title_str = str(title).upper()
            for pattern in level2_patterns:
                if re.search(pattern, title_str):
                    level2_titles.add(title)
                    break
                    
        return list(level2_titles)
        
    def calculate_completion_percentages(self, df, level1_titles, level2_titles):
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
                'User Brand': self.extract_brand(user_df),
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
    
    def extract_brand(self, user_df):
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
        
    def create_stellantis_report(self, completion_data):
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
        
    def save_to_excel(self, summary_df, completion_data, level1_titles, level2_titles):
        """Save results to Excel with STELLANTIS format"""
        with pd.ExcelWriter(self.output_file_path.get(), engine='openpyxl') as writer:
            # Main STELLANTIS report sheet
            summary_df.to_excel(writer, sheet_name='STELLANTIS_Training_Report', index=False)
            
            # Detailed completion summary
            if completion_data:
                detailed_df = pd.DataFrame(completion_data)
                detailed_df = detailed_df.sort_values('Overall Completion %', ascending=False)
                detailed_df.to_excel(writer, sheet_name='Detailed_Completion_Summary', index=False)
            
            # Level 1 details sheet
            if self.df_original is not None:
                df_clean = self.df_original.iloc[8:].reset_index(drop=True)
                df_clean.columns = df_clean.iloc[0]
                df_clean = df_clean.iloc[1:].reset_index(drop=True)
                
                # Filter to only target job roles
                df_clean = df_clean[df_clean['Position'].isin(self.target_job_roles)]
                
                # Apply specific job role filter if selected
                if self.selected_job_roles.get() in self.target_job_roles:
                    job_role = self.selected_job_roles.get()
                    df_clean = df_clean[df_clean['Position'] == job_role]
                
                level1_df = df_clean[df_clean['Training Title'].isin(level1_titles)]
                if len(level1_df) > 0:
                    level1_df.to_excel(writer, sheet_name='Level_1_Training_Details', index=False)
                
                # Level 2 details sheet
                level2_df = df_clean[df_clean['Training Title'].isin(level2_titles)]
                if len(level2_df) > 0:
                    level2_df.to_excel(writer, sheet_name='Level_2_Training_Details', index=False)
                
                # All training details sheet
                df_clean.to_excel(writer, sheet_name='All_Training_Details', index=False)
            
            # Training titles reference sheet
            titles_df = pd.DataFrame({
                'Level 1 Training Titles': level1_titles,
                'Level 2 Training Titles': level2_titles + [''] * max(0, len(level1_titles) - len(level2_titles))
            })
            titles_df.to_excel(writer, sheet_name='Training_Titles_Reference', index=False)
            
        self.log_message(f"STELLANTIS Excel report saved with {len(summary_df)} individuals processed")
        
    def log_message(self, message):
        """Add message to results text widget"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.results_text.see(tk.END)
        self.root.update()

    def add_level1_pattern(self, new_pattern):
        """Add a new Level 1 pattern to the configuration"""
        if new_pattern not in self.config['level1_patterns']:
            self.config['level1_patterns'].append(new_pattern)
            self.log_message(f"Added new Level 1 pattern: {new_pattern}")
    
    def add_level2_pattern(self, new_pattern):
        """Add a new Level 2 pattern to the configuration"""
        if new_pattern not in self.config['level2_patterns']:
            self.config['level2_patterns'].append(new_pattern)
            self.log_message(f"Added new Level 2 pattern: {new_pattern}")
    
    def add_target_job_role(self, new_role):
        """Add a new target job role to the configuration"""
        if new_role not in self.config['target_job_roles']:
            self.config['target_job_roles'].append(new_role)
            self.target_job_roles = self.config['target_job_roles']
            self.log_message(f"Added new target job role: {new_role}")
    
    def get_current_patterns(self):
        """Get current patterns for review"""
        return {
            'level1_patterns': self.config['level1_patterns'],
            'level2_patterns': self.config['level2_patterns'],
            'target_job_roles': self.config['target_job_roles']
        }

def main():
    app = TrainingReportProcessor()
    app.root.mainloop()

if __name__ == "__main__":
    main()
