import os
import http.server
import socketserver
import json
import tempfile
import base64
from datetime import datetime
import io

# Import heavy dependencies only when needed
def get_pandas():
    import pandas as pd
    return pd

def get_re():
    import re
    return re

# Configuration for easy pattern management
CONFIG = {
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

def identify_level1_trainings(df):
    """Identify Level 1 training titles with flexible pattern matching"""
    re = get_re()
    level1_patterns = CONFIG['level1_patterns']
    
    level1_titles = set()
    for title in df['Training Title'].unique():
        title_str = str(title).upper()
        for pattern in level1_patterns:
            if re.search(pattern, title_str):
                level1_titles.add(title)
                break
                
    return list(level1_titles)

def identify_level2_trainings(df):
    """Identify Level 2 training titles with flexible pattern matching"""
    re = get_re()
    level2_patterns = CONFIG['level2_patterns']
    
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
        return get_pandas().DataFrame()
        
    df = get_pandas().DataFrame(completion_data)
    
    # Reorder columns to match STELLANTIS format with assigned counts
    column_order = [
        'User ID', 'First Name', 'Last Name', 'Job Role', 'Dealer Name', 
        'User Brand', 'Total Level 1 Trainings', 'Completed Level 1 Trainings', 'Level 1 Completion %',
        'Total Level 2 Trainings', 'Completed Level 2 Trainings', 'Level 2 Completion %'
    ]
    
    # Filter to only include columns that exist
    existing_columns = [col for col in column_order if col in df.columns]
    df = df[existing_columns]
    
    return df

# HTML template for the main page
MAIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stellantis Training Report Processor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: #1a1a2e;
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .header h1 {
            margin: 0;
            font-size: 2.8em;
            font-weight: 700;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }
        .upload-section {
            background: white;
            border-radius: 15px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 60px 40px;
            text-align: center;
            transition: all 0.3s ease;
            background: #f8f9ff;
        }
        .upload-area:hover {
            border-color: #764ba2;
            background: #f0f2ff;
        }
        .upload-area.dragover {
            border-color: #28a745;
            background: #f0fff4;
        }
        .file-icon {
            font-size: 4em;
            color: #667eea;
            margin-bottom: 20px;
        }
        .file-input {
            display: none;
        }
        .btn-primary {
            background: #667eea;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-weight: 600;
        }
        .btn-primary:hover {
            background: #764ba2;
        }
        .btn-success {
            background: #28a745;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-weight: 600;
        }
        .btn-success:hover {
            background: #218838;
        }
        .file-info {
            margin-top: 20px;
            padding: 20px;
            background: #e8f4fd;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            display: none;
        }
        .controls-section {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .form-select {
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 12px;
            font-size: 16px;
        }
        .form-select:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        }
        .results-section {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            display: none;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .stat-card i {
            font-size: 2em;
            margin-bottom: 10px;
        }
        .stat-number {
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        .training-titles {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .training-titles h5 {
            color: #667eea;
            margin-bottom: 15px;
        }
        .training-list {
            max-height: 200px;
            overflow-y: auto;
            background: white;
            border-radius: 8px;
            padding: 15px;
        }
        .training-item {
            padding: 8px 0;
            border-bottom: 1px solid #eee;
            font-size: 0.9em;
        }
        .training-item:last-child {
            border-bottom: none;
        }
        .job-breakdown {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
        }
        .job-breakdown h5 {
            color: #667eea;
            margin-bottom: 15px;
        }
        .job-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        .job-item:last-child {
            border-bottom: none;
        }
        .loading {
            text-align: center;
            padding: 40px;
            display: none;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .download-section {
            text-align: center;
            margin-top: 30px;
        }
        .btn-download {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: 600;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
        }
        .btn-download:hover {
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(40, 167, 69, 0.3);
        }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="header">
            <h1>Stellantis Training Report Processor</h1>
            <p>Focused on: SAL-2, SAL-3, SER-12, SER-1, SER-2 Job Roles</p>
        </div>
        
        <div class="upload-section">
            <div class="upload-area" id="uploadArea">
                <div class="file-icon">
                    <i class="fas fa-file-excel"></i>
                </div>
                <h3>Upload Training Report Excel File</h3>
                <p class="text-muted">Select your Enterprise Training Report Excel file to process</p>
                <input type="file" id="fileInput" class="file-input" accept=".xlsx,.xls">
                <button class="btn btn-primary" onclick="document.getElementById('fileInput').click()">
                    <i class="fas fa-upload"></i> Choose File
                </button>
                <div class="file-info" id="fileInfo"></div>
            </div>
        </div>
        
        <div class="controls-section">
            <div class="row align-items-center">
                <div class="col-md-6">
                    <label for="jobRole" class="form-label fw-bold">Job Role Filter:</label>
                    <select id="jobRole" class="form-select">
                        <option value="All">All Target Job Roles</option>
                        <option value="SAL-2-New Vehicles Sales Advisor">SAL-2-New Vehicles Sales Advisor</option>
                        <option value="SAL-3-New Vehicles Sales Manager">SAL-3-New Vehicles Sales Manager</option>
                        <option value="SER-12-Technician">SER-12-Technician</option>
                        <option value="SER-1-Aftersales Manager">SER-1-Aftersales Manager</option>
                        <option value="SER-2-Service Advisor">SER-2-Service Advisor</option>
                    </select>
                </div>
                <div class="col-md-6 text-end">
                    <button class="btn btn-success" id="processBtn" onclick="processFile()" disabled>
                        <i class="fas fa-cogs"></i> Generate Training Report
                    </button>
                </div>
            </div>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <h4>Processing your training report...</h4>
            <p class="text-muted">This may take a few moments</p>
        </div>
        
        <div class="results-section" id="results"></div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let selectedFile = null;
        
        // Drag and drop functionality
        const uploadArea = document.getElementById('uploadArea');
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFileSelect(files[0]);
            }
        });
        
        document.getElementById('fileInput').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                handleFileSelect(file);
            }
        });
        
        function handleFileSelect(file) {
            selectedFile = file;
            document.getElementById('fileInfo').innerHTML = `
                <div class="d-flex align-items-center">
                    <i class="fas fa-file-excel text-success me-3" style="font-size: 2em;"></i>
                    <div>
                        <strong>File Selected:</strong> ${file.name}<br>
                        <strong>Size:</strong> ${(file.size / (1024 * 1024)).toFixed(2)} MB
                    </div>
                </div>
            `;
            document.getElementById('fileInfo').style.display = 'block';
            document.getElementById('processBtn').disabled = false;
        }
        
        function processFile() {
            if (!selectedFile) return;
            
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('job_role', document.getElementById('jobRole').value);
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('loading').style.display = 'none';
                if (data.success) {
                    showResults(data);
                } else {
                    alert('Error: ' + (data.error || 'Unknown error occurred'));
                }
            })
            .catch(error => {
                document.getElementById('loading').style.display = 'none';
                alert('Error: ' + error.message);
            });
        }
        
        function showResults(data) {
            const resultsDiv = document.getElementById('results');
            
            // Create stats grid
            const statsHTML = `
                <div class="stats-grid">
                    <div class="stat-card">
                        <i class="fas fa-users"></i>
                        <div class="stat-number">${data.total_individuals}</div>
                        <div class="stat-label">Total Individuals</div>
                    </div>
                    <div class="stat-card">
                        <i class="fas fa-graduation-cap"></i>
                        <div class="stat-number">${data.level1_titles_count}</div>
                        <div class="stat-label">Level 1 Available</div>
                    </div>
                    <div class="stat-card">
                        <i class="fas fa-star"></i>
                        <div class="stat-number">${data.level2_titles_count}</div>
                        <div class="stat-label">Level 2 Available</div>
                    </div>
                    <div class="stat-card">
                        <i class="fas fa-chart-pie"></i>
                        <div class="stat-number">${data.avg_level1_completion}%</div>
                        <div class="stat-label">Avg Level 1 Completion</div>
                    </div>
                    <div class="stat-card">
                        <i class="fas fa-chart-line"></i>
                        <div class="stat-number">${data.avg_level2_completion}%</div>
                        <div class="stat-label">Avg Level 2 Completion</div>
                    </div>
                    <div class="stat-card">
                        <i class="fas fa-tasks"></i>
                        <div class="stat-number">${data.avg_assigned_level1}/${data.avg_assigned_level2}</div>
                        <div class="stat-label">Avg Assigned L1/L2</div>
                    </div>
                </div>
            `;
            
            // Create training titles section
            const trainingTitlesHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <div class="training-titles">
                            <h5><i class="fas fa-graduation-cap"></i> Level 1 Training Titles</h5>
                            <div class="training-list">
                                ${data.level1_titles.map(title => `<div class="training-item"><i class="fas fa-check text-success me-2"></i>${title}</div>`).join('')}
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="training-titles">
                            <h5><i class="fas fa-star"></i> Level 2 Training Titles</h5>
                            <div class="training-list">
                                ${data.level2_titles.map(title => `<div class="training-item"><i class="fas fa-check text-success me-2"></i>${title}</div>`).join('')}
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Create job breakdown section
            const jobBreakdownHTML = `
                <div class="job-breakdown">
                    <h5><i class="fas fa-users"></i> Job Role Breakdown</h5>
                    ${Object.entries(data.job_role_breakdown).map(([role, count]) => 
                        `<div class="job-item">
                            <span>${role}</span>
                            <span class="badge bg-primary">${count}</span>
                        </div>`
                    ).join('')}
                </div>
            `;
            
            // Create download section
            const downloadHTML = `
                <div class="download-section">
                                         <a href="/download/${data.filename}" class="btn-download">
                         <i class="fas fa-download"></i> Download Stellantis Report
                     </a>
                </div>
            `;
            
            resultsDiv.innerHTML = statsHTML + trainingTitlesHTML + jobBreakdownHTML + downloadHTML;
            resultsDiv.style.display = 'block';
        }
    </script>
</body>
</html>
"""

# Simple HTTP server for Railway with training report functionality
class TrainingReportHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(MAIN_HTML.encode('utf-8'))
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                                 'message': 'Stellantis Training Report Processor is running',
                'timestamp': datetime.now().isoformat(),
                'port': os.environ.get('PORT', '5000')
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/test':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Stellantis Training Report Processor is working! 🚀".encode('utf-8'))
        elif self.path.startswith('/download/'):
            filename = self.path.split('/download/')[1]
            filepath = os.path.join('uploads', filename)
            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header('Content-type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
    
    def do_POST(self):
        if self.path == '/upload':
            self.handle_upload()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
    
    def handle_upload(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse multipart form data
            boundary = self.headers['Content-Type'].split('boundary=')[1]
            parts = post_data.split(b'--' + boundary.encode())
            
            file_data = None
            job_role = 'All'
            
            for part in parts:
                if b'Content-Disposition: form-data' in part:
                    if b'name="file"' in part:
                        # Extract file data
                        file_start = part.find(b'\r\n\r\n') + 4
                        file_end = part.rfind(b'\r\n')
                        file_data = part[file_start:file_end]
                    elif b'name="job_role"' in part:
                        # Extract job role
                        value_start = part.find(b'\r\n\r\n') + 4
                        value_end = part.rfind(b'\r\n')
                        job_role = part[value_start:value_end].decode('utf-8')
            
            if file_data:
                # Save file temporarily
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"temp_upload_{timestamp}.xlsx"
                filepath = os.path.join('uploads', filename)
                
                os.makedirs('uploads', exist_ok=True)
                with open(filepath, 'wb') as f:
                    f.write(file_data)
                
                # Process the file
                result = process_training_report(filepath, job_role)
                
                # Clean up
                os.remove(filepath)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'No file provided'}).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

def process_training_report(filepath, selected_job_role):
    """Process the training report and return results"""
    pd = get_pandas()
    
    # Load the Excel file
    df_original = pd.read_excel(filepath, header=None)
    
    # Remove first 8 rows and set proper headers
    df_clean = df_original.iloc[8:].reset_index(drop=True)
    df_clean.columns = df_clean.iloc[0]
    df_clean = df_clean.iloc[1:].reset_index(drop=True)
    
    # Filter to only show the 5 target job roles
    df_clean = df_clean[df_clean['Position'].isin(CONFIG['target_job_roles'])]
    
    # Apply specific job role filter if selected
    if selected_job_role != 'All' and selected_job_role in CONFIG['target_job_roles']:
        df_clean = df_clean[df_clean['Position'] == selected_job_role]
    
    # Identify Level 1 and Level 2 training titles
    level1_titles = identify_level1_trainings(df_clean)
    level2_titles = identify_level2_trainings(df_clean)
    
    # Calculate completion percentages
    completion_data = calculate_completion_percentages(df_clean, level1_titles, level2_titles)
    
    # Create summary report
    summary_df = create_stellantis_report(completion_data)
    
    # Generate output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"Stellantis_Report_{timestamp}.xlsx"
    output_path = os.path.join('uploads', output_filename)
    
    os.makedirs('uploads', exist_ok=True)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        summary_df.to_excel(writer, sheet_name='Stellantis_Training_Report', index=False)
        
        # Detailed completion summary
        if completion_data:
            detailed_df = pd.DataFrame(completion_data)
            detailed_df = detailed_df.sort_values('Overall Completion %', ascending=False)
            detailed_df.to_excel(writer, sheet_name='Detailed_Completion_Summary', index=False)
        
        # Training titles reference
        titles_df = pd.DataFrame({
            'Level 1 Training Titles': level1_titles,
            'Level 2 Training Titles': level2_titles + [''] * max(0, len(level1_titles) - len(level2_titles))
        })
        titles_df.to_excel(writer, sheet_name='Training_Titles_Reference', index=False)
    
    # Calculate summary statistics
    if len(summary_df) > 0:
        avg_level1 = summary_df['Level 1 Completion %'].mean()
        avg_level2 = summary_df['Level 2 Completion %'].mean()
        
        # Calculate average assigned trainings
        avg_assigned_level1 = summary_df['Total Level 1 Trainings'].mean()
        avg_assigned_level2 = summary_df['Total Level 2 Trainings'].mean()
    else:
        avg_level1 = avg_level2 = avg_assigned_level1 = avg_assigned_level2 = 0
    
    return {
        'success': True,
        'filename': output_filename,
        'total_individuals': len(summary_df),
        'level1_titles_count': len(level1_titles),
        'level2_titles_count': len(level2_titles),
        'avg_level1_completion': round(avg_level1, 2),
        'avg_level2_completion': round(avg_level2, 2),
        'avg_assigned_level1': round(avg_assigned_level1, 1),
        'avg_assigned_level2': round(avg_assigned_level2, 1),
        'level1_titles': level1_titles[:10],  # First 10 for display
        'level2_titles': level2_titles[:10],  # First 10 for display
        'job_role_breakdown': df_clean['Position'].value_counts().to_dict()
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚀 Starting Stellantis Training Report Processor...")
    print(f"📡 Port: {port}")
    print(f"🌐 Host: 0.0.0.0")
    print(f"🔗 Health check at: /health")
    print(f"📊 Full training report functionality ready!")
    
    with socketserver.TCPServer(("0.0.0.0", port), TrainingReportHandler) as httpd:
        print(f"✅ Server started on port {port}")
        httpd.serve_forever()
