# 🆓 Free Deployment Guide - STELLANTIS Training Report

## 🚀 Railway Deployment (Recommended - 5 minutes)

### Step 1: Prepare Your Files
Your files are already ready! You have:
- ✅ `app.py` - Main Flask application
- ✅ `templates/index.html` - Web interface
- ✅ `requirements_web.txt` - Dependencies
- ✅ `Procfile` - Production server
- ✅ `railway.json` - Railway configuration

### Step 2: Upload to GitHub
1. **Create a GitHub account** at [github.com](https://github.com)
2. **Create a new repository** called `stellantis-training-report`
3. **Upload all your files** to the repository
4. **Make sure these files are included:**
   ```
   ├── app.py
   ├── templates/
   │   └── index.html
   ├── requirements_web.txt
   ├── Procfile
   ├── railway.json
   └── runtime.txt
   ```

### Step 3: Deploy to Railway
1. **Go to [railway.app](https://railway.app)**
2. **Sign up with your GitHub account**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your `stellantis-training-report` repository**
6. **Railway will automatically detect it's a Python app**
7. **Click "Deploy"**

### Step 4: Get Your URL
- **Railway will give you a URL** like: `https://stellantis-training-report-production-xxxx.up.railway.app`
- **Share this URL** with your team!
- **Your app is now live** and accessible worldwide

## 🌐 Alternative Free Options

### Option A: Render (Also Free)
1. **Go to [render.com](https://render.com)**
2. **Sign up with GitHub**
3. **Create new Web Service**
4. **Connect your GitHub repo**
5. **Deploy** - Get URL like: `https://stellantis-training.onrender.com`

### Option B: Heroku (Free Tier)
1. **Go to [heroku.com](https://heroku.com)**
2. **Sign up and install Heroku CLI**
3. **Run these commands:**
   ```bash
   heroku create stellantis-training-app
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```
4. **Get URL**: `https://stellantis-training-app.herokuapp.com`

### Option C: PythonAnywhere (Python-Specific)
1. **Go to [pythonanywhere.com](https://pythonanywhere.com)**
2. **Sign up for free account**
3. **Upload your files via web interface**
4. **Configure WSGI file**
5. **Deploy** - Get URL: `https://yourusername.pythonanywhere.com`

## 📱 Custom Domain (Optional - Costs ~$10/year)

If you want a custom domain like `training.stellantis.com`:

1. **Buy a domain** from Namecheap/GoDaddy (~$10/year)
2. **Add custom domain** in Railway/Render settings
3. **Update DNS records** to point to your app
4. **Your app will be available at your custom domain**

## 🔧 Troubleshooting

### Common Issues:
1. **Build fails**: Check `requirements_web.txt` has all dependencies
2. **App won't start**: Check `Procfile` is correct
3. **Upload errors**: Check file size limits (usually 50MB)

### Free Tier Limitations:
- **Railway**: 500 hours/month free
- **Render**: 750 hours/month free
- **Heroku**: 550 hours/month free
- **PythonAnywhere**: Always free for basic usage

## 🎯 Success Checklist

- ✅ App deploys successfully
- ✅ Can upload Excel files
- ✅ Can download reports
- ✅ Works on mobile devices
- ✅ Team can access via URL

## 📞 Support

If you get stuck:
1. **Check the deployment logs** in Railway/Render
2. **Verify all files are uploaded** to GitHub
3. **Test locally first** with `python app.py`
4. **Check the free tier limits** haven't been exceeded

---

**Your STELLANTIS Training Report will be live and free! 🎉**
