# STELLANTIS Training Report Web Application - Deployment Guide

## 🌐 Self-Hosted Domain Deployment Options

### **Option 1: VPS/Cloud Server (Recommended)**

#### **Prerequisites:**
- Linux server (Ubuntu 20.04+ recommended)
- Domain name pointing to your server
- SSH access to server

#### **Step 1: Server Setup**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv nginx -y

# Install additional dependencies
sudo apt install build-essential python3-dev -y
```

#### **Step 2: Application Setup**
```bash
# Create application directory
sudo mkdir -p /var/www/stellantis-training
sudo chown $USER:$USER /var/www/stellantis-training
cd /var/www/stellantis-training

# Clone or upload your application files
# (Upload app.py, templates/, requirements_web.txt)

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements_web.txt
```

#### **Step 3: Gunicorn Setup**
```bash
# Install Gunicorn
pip install gunicorn

# Create Gunicorn service file
sudo nano /etc/systemd/system/stellantis-training.service
```

**Add this content to the service file:**
```ini
[Unit]
Description=STELLANTIS Training Report Web App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/stellantis-training
Environment="PATH=/var/www/stellantis-training/venv/bin"
ExecStart=/var/www/stellantis-training/venv/bin/gunicorn --workers 3 --bind unix:stellantis-training.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```

#### **Step 4: Nginx Configuration**
```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/stellantis-training
```

**Add this content:**
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/stellantis-training/stellantis-training.sock;
    }

    location /static {
        alias /var/www/stellantis-training/static;
    }

    # Increase upload size limit for Excel files
    client_max_body_size 50M;
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/stellantis-training /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Start the application
sudo systemctl start stellantis-training
sudo systemctl enable stellantis-training
```

#### **Step 5: SSL Certificate (Optional but Recommended)**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### **Option 2: Docker Deployment**

#### **Create Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements_web.txt .
RUN pip install -r requirements_web.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

#### **Create docker-compose.yml:**
```yaml
version: '3.8'
services:
  stellantis-training:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

#### **Deploy with Docker:**
```bash
docker-compose up -d
```

### **Option 3: Shared Hosting (cPanel)**

1. **Upload files** to your hosting directory
2. **Create Python app** in cPanel (if available)
3. **Set up virtual environment** and install requirements
4. **Configure .htaccess** for URL rewriting

### **Option 4: Heroku Deployment**

#### **Create Procfile:**
```
web: gunicorn app:app
```

#### **Deploy to Heroku:**
```bash
# Install Heroku CLI
# Create Heroku app
heroku create your-app-name

# Deploy
git add .
git commit -m "Initial deployment"
git push heroku main
```

## 🔧 Configuration

### **Environment Variables**
Create a `.env` file for production:
```env
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=52428800
```

### **Security Considerations**
1. **Change the secret key** in `app.py`
2. **Set up proper file permissions**
3. **Configure firewall rules**
4. **Enable HTTPS**
5. **Set up regular backups**

## 📊 Monitoring & Maintenance

### **Logs**
```bash
# View application logs
sudo journalctl -u stellantis-training

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### **Updates**
```bash
# Update application
cd /var/www/stellantis-training
git pull origin main
source venv/bin/activate
pip install -r requirements_web.txt
sudo systemctl restart stellantis-training
```

## 🚀 Performance Optimization

### **For High Traffic:**
1. **Add Redis** for session storage
2. **Use CDN** for static files
3. **Implement caching**
4. **Scale horizontally** with load balancer

### **Database Integration (Future Enhancement):**
```python
# Add to app.py for database storage
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/stellantis'
db = SQLAlchemy(app)
```

## 🔍 Troubleshooting

### **Common Issues:**
1. **Permission errors**: Check file ownership
2. **Port conflicts**: Ensure port 5000 is available
3. **Upload failures**: Check file size limits
4. **Memory issues**: Optimize worker processes

### **Health Check Endpoint:**
```python
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})
```

## 📈 Analytics & Monitoring

### **Add Google Analytics:**
```html
<!-- Add to templates/index.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### **Application Metrics:**
```python
# Add to app.py
from flask_prometheus_metrics import register_metrics

@app.route('/metrics')
def metrics():
    return generate_latest()
```

## 🎯 Domain Configuration

### **DNS Settings:**
- **A Record**: Point to your server IP
- **CNAME**: www → your-domain.com
- **MX Records**: For email (if needed)

### **SSL Certificate:**
- **Let's Encrypt**: Free SSL certificates
- **Commercial SSL**: For enterprise requirements

## 📞 Support

For deployment issues:
1. Check logs for error messages
2. Verify all dependencies are installed
3. Ensure proper file permissions
4. Test locally before deploying

---

**Your STELLANTIS Training Report Web Application is now ready for production deployment! 🚀**
