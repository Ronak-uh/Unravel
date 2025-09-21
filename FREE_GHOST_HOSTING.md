# 🚂 Complete Railway Ghost Deployment Walkthrough

## � Prerequisites
- GitHub account
- Email address
- 5-10 minutes of time

## 🚀 Step-by-Step Railway Deployment

### Step 1: Access Railway
1. **Open your browser** and go to: https://railway.app
2. **Click "Login"** in the top right corner
3. **Select "Login with GitHub"**
4. **Authorize Railway** to access your GitHub account
5. You'll be redirected to the Railway dashboard

### Step 2: Create New Project
1. **Click "New Project"** button (big purple button)
2. **Select "Deploy from GitHub repo"** 
3. **OR click "Browse Templates"** (easier option)

### Step 3A: Using Template (Recommended)
1. **Click "Browse Templates"**
2. **Search for "ghost"** in the search bar
3. **Look for "Ghost CMS"** template
4. **Click "Deploy"** on the Ghost template
5. **Give your project a name** (e.g., "my-ghost-blog")
6. **Click "Deploy"** button

### Step 3B: Manual Setup (Alternative)
If template doesn't work:
1. **Click "Empty Project"**
2. **Click "Add Service"**
3. **Select "Docker Image"**
4. **Enter image name**: `ghost:5-alpine`
5. **Click "Add"**

### Step 4: Configure Environment Variables
1. **Click on your Ghost service** in the dashboard
2. **Go to "Variables" tab**
3. **Add these variables** by clicking "New Variable":

   | Variable Name | Value |
   |---------------|--------|
   | `NODE_ENV` | `production` |
   | `database__client` | `sqlite3` |
   | `database__connection__filename` | `/var/lib/ghost/content/data/ghost.db` |
   | `mail__transport` | `Direct` |

4. **Don't add URL yet** - we'll get it after deployment

### Step 5: Wait for Deployment
1. **Watch the "Deployments" tab** for progress
2. **Wait for green checkmark** (usually 2-5 minutes)
3. **Look for "Success" status**

### Step 6: Get Your Public URL
1. **Go to "Settings" tab** of your service
2. **Click "Generate Domain"** button
3. **Copy the generated URL** (looks like: `https://my-ghost-blog-production-xxxx.up.railway.app`)
4. **Test the URL** in your browser - you should see Ghost setup page

### Step 7: Add URL to Environment
1. **Go back to "Variables" tab**
2. **Add new variable**:
   - **Name**: `url`
   - **Value**: Your Railway URL (the one you just copied)
3. **Click "Add"**
4. **Service will redeploy automatically**

### Step 8: Setup Ghost Admin Account
1. **Visit your Railway URL** in browser
2. **You'll see Ghost welcome screen**
3. **Click "Create your account"**
4. **Fill in the form**:
   - **Site title**: Your blog name (e.g., "My Awesome Blog")
   - **Full name**: Your name
   - **Email**: Your email address
   - **Password**: Strong password (save this!)
5. **Click "Create account & start publishing"**

### Step 9: Get Admin API Key
1. **You're now in Ghost admin dashboard**
2. **Click the gear icon** (⚙️) in bottom left for Settings
3. **Click "Integrations"** in the left sidebar
4. **Scroll down to "Custom integrations"**
5. **Click "Add custom integration"**
6. **Name it**: "Unravel Automation"
7. **Click "Create"**
8. **Copy the "Admin API Key"** - this is what you need!
9. **Copy the "API URL"** as well (should match your Railway URL)

### Step 10: Test Your Ghost Blog
1. **Visit your Railway URL** (your public blog)
2. **Visit `your-url/ghost`** (admin area)
3. **Try creating a test post**:
   - Click "New post"
   - Add title and content
   - Click "Publish" → "Publish right now"
4. **Check if post appears** on your public blog

## ✅ Success! You Now Have:
- **✅ Free Ghost blog** at your Railway URL
- **✅ Admin access** at `your-url/ghost`
- **✅ Admin API key** for automation
- **✅ 500 hours/month** free hosting

## 📝 What You'll Use for Vercel:

Copy these values for your Vercel environment variables:

```
GHOST_URL=https://your-actual-railway-url.up.railway.app
GHOST_ADMIN_API_KEY=your_copied_admin_api_key_from_step_9
```

## 🔧 Troubleshooting

### If deployment fails:
1. **Check the "Deployments" tab** for error logs
2. **Try redeploying** by clicking "Redeploy"
3. **Check environment variables** are correct

### If Ghost won't load:
1. **Wait 2-3 minutes** after deployment
2. **Check the URL** includes `https://`
3. **Try hard refresh** (Ctrl+F5 or Cmd+Shift+R)

### If admin setup fails:
1. **Clear browser cache**
2. **Try incognito/private mode**
3. **Check Railway logs** in deployments tab

## 💰 Railway Free Tier Details

**What you get for FREE:**
- **500 execution hours/month** (enough for a blog)
- **1GB storage** (plenty for blog posts)
- **Custom domain support** (can add your own domain later)
- **Automatic HTTPS** (secure by default)
- **No credit card required** for basic usage

**Limits:**
- Service sleeps after 30 minutes of inactivity
- Wakes up automatically when accessed (3-5 second delay)

Your Ghost blog is now ready for production! 🎉