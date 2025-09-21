# STELLANTIS Training Report Processor

A GUI application for processing enterprise training reports and generating STELLANTIS format reports with completion percentages for Level 1 and Level 2 trainings per individual.

**Focused on: SAL-2, SAL-3, SER-12, SER-1, SER-2 Job Roles**

## Features

- **Excel File Upload**: Upload training report Excel files
- **Automatic Header Removal**: Removes the first 8 rows of header information
- **Focused Job Role Processing**: Automatically filters to show only the 5 target job roles
- **Job Role Filtering**: Choose specific job roles from the focused list
- **Training Level Detection**: Automatically identifies Level 1 and Level 2 training titles
- **Completion Percentage Calculation**: Calculates completion percentages for each individual
- **STELLANTIS Format Output**: Generates reports matching the STELLANTIS training report format
- **Multi-Sheet Output**: Generates comprehensive Excel reports with multiple sheets
- **User-Friendly GUI**: Simple and intuitive interface with STELLANTIS branding

## Target Job Roles

The application is specifically designed for and automatically filters to these 5 job roles:
- **SAL-2-New Vehicles Sales Advisor**
- **SAL-3-New Vehicles Sales Manager**
- **SER-12-Technician**
- **SER-1-Aftersales Manager**
- **SER-2-Service Advisor**

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python training_report_processor.py
   ```

## How to Use

1. **Launch the Application**: Run the Python script to open the GUI
2. **Select Input File**: Click "Browse" to select your training report Excel file
3. **Set Output File**: The output filename will be auto-generated with STELLANTIS branding
4. **Choose Job Role Filter** (Optional): Select specific job roles from the focused list
5. **Generate Report**: Click "Generate Training Report" to start the analysis
6. **View Results**: The processing results will be displayed in the text area
7. **Access Output**: The processed Excel file will be saved with STELLANTIS format

## Output Excel Structure

The processed Excel file contains the following sheets:

### 1. STELLANTIS_Training_Report
Main STELLANTIS format report with completion percentages for each individual:
- User ID
- First Name
- Last Name
- Job Role
- Dealer Name
- User Brand
- Level 1 Completion %
- Level 2 Completion %

### 2. Detailed_Completion_Summary
Detailed summary with all completion metrics:
- User ID, First Name, Last Name
- Job Role, Dealer Name, User Brand
- Total Level 1/2 Trainings
- Completed Level 1/2 Trainings
- Level 1/2 Completion %
- Overall Completion %

### 3. Level_1_Training_Details
Detailed view of all Level 1 training records (filtered to target job roles)

### 4. Level_2_Training_Details
Detailed view of all Level 2 training records (filtered to target job roles)

### 5. All_Training_Details
Complete training data after header removal (filtered to target job roles)

### 6. Training_Titles_Reference
Reference list of identified Level 1 and Level 2 training titles

## Training Level Detection

The application automatically identifies training levels using pattern matching:

### Level 1 Training Patterns:
- "LEVEL 1"
- "INDUCTION LEVEL 1"
- "BASIC LEVEL 1"
- "FOUNDATION LEVEL 1"

### Level 2 Training Patterns:
- "LEVEL 2"
- "ADVANCED LEVEL 2"
- "INTERMEDIATE LEVEL 2"

## Brand Detection

The application automatically detects and assigns brands based on training content:
- **Fiat Professional**
- **Jeep**
- **Peugeot**
- **Citroen**
- **Alfa Romeo**
- **Other**

## Requirements

- Python 3.7 or higher
- pandas >= 2.0.0
- openpyxl >= 3.1.0
- tkinter (built into Python)

## Input File Format

The application expects Excel files with the following structure:
- First 8 rows contain header information (will be removed)
- Row 9 contains column headers
- Data starts from row 10
- Required columns: User ID, User Full Name, Training Title, Transcript Status, Division, Position

## Example Usage

```python
# The application will automatically:
# 1. Load your Excel file
# 2. Remove the first 8 rows
# 3. Filter to target job roles (SAL-2, SAL-3, SER-12, SER-1, SER-2)
# 4. Apply specific job role filtering (if selected)
# 5. Identify Level 1 and Level 2 trainings
# 6. Calculate completion percentages per individual
# 7. Generate a STELLANTIS format Excel report
```

## Test Results

The application has been tested with real STELLANTIS training data:
- **75,887 training records** filtered to target job roles
- **761 individuals** processed from target job roles
- **25 Level 1 training titles** identified
- **5 Level 2 training titles** identified
- **Average Level 1 completion:** 41.69%
- **Average Level 2 completion:** 0.00%

### Job Role Breakdown:
- **SAL-2-New Vehicles Sales Advisor**: 10,357 records
- **SAL-3-New Vehicles Sales Manager**: 0 records (not found in current data)
- **SER-12-Technician**: 48,141 records
- **SER-1-Aftersales Manager**: 8,910 records
- **SER-2-Service Advisor**: 8,479 records

## Troubleshooting

- **File Not Found**: Ensure the input Excel file exists and is accessible
- **Permission Error**: Make sure you have write permissions for the output directory
- **Memory Error**: For very large files, consider processing in smaller batches
- **No Training Data Found**: Check that your Excel file contains the expected column structure
- **Job Role Not Found**: The application automatically filters to target job roles, so this should not occur

## Support

For issues or questions, please check the processing log in the application's text area for detailed error messages.

## Files Included

- `training_report_processor.py` - Main STELLANTIS GUI application (focused on target job roles)
- `test_processor.py` - Test script for verification
- `requirements.txt` - Python dependencies
- `README.md` - This documentation
- `run_processor.bat` - Windows batch file for easy execution
