# 🔑 Google AI Studio API Key Setup (Paid Version)

## 📋 Step-by-Step Setup for Paid Account

### Step 1: Access Google AI Studio
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Make sure you're on the **paid plan**

### Step 2: Get API Key
1. Click on **"Get API key"** in the top right
2. Select **"Create API key"**
3. Choose your project or create a new one
4. Copy the generated API key

### Step 3: Enable Billing
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Go to **"Billing"** in the left menu
4. **Enable billing** for your project
5. Add a payment method

### Step 4: Enable Gemini API
1. In Google Cloud Console, go to **"APIs & Services"**
2. Click **"Enable APIs and Services"**
3. Search for **"Generative Language API"**
4. Click **"Enable"**

### Step 5: Update Your App
1. Replace the API key in `.streamlit/secrets.toml`:
```toml
GOOGLE_API_KEY = "YOUR_NEW_PAID_API_KEY"
```

### Step 6: Deploy
1. Commit and push the changes
2. Streamlit Cloud will auto-update

## 🔍 Troubleshooting

### If Still Getting Quota Errors:
1. **Check API key source**: Make sure it's from paid account
2. **Verify billing**: Ensure billing is enabled
3. **Check quotas**: Go to Google Cloud Console → APIs & Services → Quotas
4. **Wait**: Sometimes takes a few minutes for billing to activate

### Alternative Models to Try:
If `gemini-1.5-pro` still has issues, try:
- `gemini-1.0-pro`
- `gemini-pro`
- `gemini-pro-vision`

## 📞 Support
- **Google AI Studio Help**: [support.google.com](https://support.google.com)
- **Google Cloud Support**: [cloud.google.com/support](https://cloud.google.com/support) 