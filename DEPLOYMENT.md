# Deployment Guide - Streamlit Cloud

## Quick Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- This repository pushed to GitHub

### Deployment Steps

1. **Push your code to GitHub**
   ```bash
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Sign in with your GitHub account

3. **Deploy the App**
   - Click "New app" button
   - **Repository**: Select this repository
   - **Branch**: `main`
   - **Main file path**: `code/app.py`
   - Click "Deploy"

4. **Wait for Deployment**
   - Streamlit Cloud will:
     - Install dependencies from `code/requirements.txt`
     - Apply settings from `code/.streamlit/config.toml`
     - Create `code/data/` directory automatically
     - Generate initial `users.csv` on first run

5. **Access Your App**
   - You'll get a URL like: `https://[your-app-name].streamlit.app`
   - Share this URL with your class/professor

## Default Login Credentials

**Username**: `admin`
**Password**: `admin123`

**Important**: Change these credentials immediately after first login via the user management page.

## Configuration Files

### `.streamlit/config.toml`
Located at `code/.streamlit/config.toml`, this file configures:
- Theme colors and fonts
- Server settings for deployment
- Security settings (CORS, XSRF protection)

### `requirements.txt`
Located at `code/requirements.txt`, contains all Python dependencies:
- streamlit>=1.51.0
- pandas>=2.3.3
- numpy>=2.3.4
- plotly>=6.3.1
- PyJWT>=2.8.0
- python-dotenv>=1.0.0
- streamlit-calendar>=0.7.0

## Data Persistence

- User data is stored in `code/data/users.csv`
- On Streamlit Cloud, this file persists between restarts
- **Note**: Streamlit Cloud Community tier may reset data on redeployment
- For production, migrate to a proper database (PostgreSQL, MongoDB, etc.)

## Monorepo Structure

This deployment preserves your monorepo structure:
```
root/
├── presentation/        # Presentation files (not deployed)
├── paper/              # Research papers (not deployed)
├── data/               # OULAD dataset (not deployed)
└── code/               # Application (deployed)
    ├── .streamlit/
    ├── app.py          # Entry point
    ├── modules/
    ├── pages/
    ├── data/           # User data (auto-created)
    └── requirements.txt
```

Only the `code/` directory is relevant for deployment.

## Troubleshooting

### Issue: "Module not found" errors
**Solution**: Ensure all dependencies are in `code/requirements.txt`

### Issue: "File not found: data/users.csv"
**Solution**: The app creates this automatically on first run. If issues persist, check that `code/data/` directory exists.

### Issue: App won't start
**Solution**: Check Streamlit Cloud logs (available in deployment dashboard)

### Issue: Path errors
**Solution**: All paths are now dynamically resolved relative to the app location

## Local Testing Before Deployment

Test locally to ensure everything works:

```bash
cd code
source .venv/bin/activate  # or .venv/Scripts/activate on Windows
streamlit run app.py
```

Visit: http://localhost:8501

## Post-Deployment Checklist

- [ ] App loads without errors
- [ ] Can log in with admin credentials
- [ ] Create a test user (student/teacher role)
- [ ] Verify all pages load correctly
- [ ] Change admin password
- [ ] Share deployment URL with instructor

## Support

- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-community-cloud
- Streamlit Forum: https://discuss.streamlit.io
