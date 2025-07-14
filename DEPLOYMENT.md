# 🚀 Deployment & Testing Guide

This guide covers how to deploy your AR Business Card and test it across different platforms.

## 📋 Pre-Deployment Checklist

### 1. Assets Ready ✅
- [ ] `assets/business-card-marker.mind` - Generated from your business card image
- [ ] `assets/caricature.glb` - Your 3D avatar (< 2MB)
- [ ] `assets/isometric-room.glb` - 3D room scene (< 3MB, optional)

### 2. Contact Information ✅
- [ ] Updated contact info in `script.js`
- [ ] Verified all social media links work
- [ ] Tested vCard generation locally

### 3. Branding ✅
- [ ] Updated `package.json` with your details
- [ ] Modified README.md with your information
- [ ] Customized any visual elements

## 🌐 Deployment Options

### Option 1: Vercel (Recommended)
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy (from project root)
vercel --prod

# Your site will be available at: https://your-project.vercel.app
```

### Option 2: Netlify
1. Push code to GitHub
2. Connect repository to Netlify
3. Build settings: No build command needed (static site)
4. Publish directory: `/` (root)

### Option 3: GitHub Pages
```bash
# Enable GitHub Pages in repository settings
# Select source: Deploy from a branch
# Branch: main / (root)
# Your site: https://username.github.io/repository-name
```

### Option 4: Custom Server
```bash
# Any web server that serves static files
# Ensure HTTPS is enabled (required for camera access)
```

## 🧪 Testing Protocol

### 1. Local Testing
```bash
# Start local server
npm run dev

# Test on http://localhost:8000
# Note: Camera access requires HTTPS in production
```

### 2. HTTPS Testing
```bash
# Use ngrok for HTTPS testing locally
ngrok http 8000

# Test with the https:// URL provided by ngrok
```

### 3. Device Testing Matrix

| Device Type | Browser | Resolution | Notes |
|-------------|---------|------------|--------|
| iPhone 12+ | Safari | 1170x2532 | Primary target |
| Android Flagship | Chrome | 1080x2400 | Primary target |
| iPad | Safari | 1668x2388 | Secondary |
| Budget Android | Chrome | 720x1600 | Performance test |
| Desktop | Chrome | 1920x1080 | Development |

### 4. Performance Testing
- Monitor FPS counter (should stay above 20)
- Check loading times on 4G network
- Verify asset sizes meet targets
- Test on low-memory devices

## 🔍 Testing Checklist

### AR Functionality
- [ ] Camera permission requested
- [ ] Business card detection works
- [ ] 3D models load correctly
- [ ] Animations trigger on card detection
- [ ] Performance optimization activates on low-end devices

### Interactions
- [ ] Caricature click opens website
- [ ] Social icons link to correct profiles
- [ ] Email click opens mail app
- [ ] "Add to Contacts" downloads vCard
- [ ] All links open in new tabs (except email)

### Performance
- [ ] Initial load < 3.5 seconds on 4G
- [ ] FPS stays above 20 on target devices
- [ ] Total asset size < 5MB
- [ ] Graceful degradation on weak devices

### Cross-Browser
- [ ] Chrome (Desktop & Mobile)
- [ ] Safari (Desktop & Mobile)
- [ ] Firefox (Desktop)
- [ ] Edge (Desktop)

## 🐛 Common Issues & Solutions

### Issue: Camera access denied
**Solution**: Ensure site is served over HTTPS

### Issue: Business card not detected
**Solutions**:
- Check marker file exists and is correctly named
- Verify business card has sufficient contrast
- Test in good lighting conditions
- Re-generate marker with better source image

### Issue: 3D models not loading
**Solutions**:
- Check file paths in `index.html`
- Verify .glb files are optimized for web
- Check browser console for errors
- Test with simpler models first

### Issue: Poor performance
**Solutions**:
- Reduce polygon count in 3D models
- Enable texture compression
- Test automatic performance optimization
- Consider removing room model on mobile

## 📊 Analytics & Monitoring

### Performance Monitoring
```javascript
// Add to script.js for production monitoring
if (window.gtag) {
    gtag('event', 'ar_card_loaded', {
        device_type: navigator.userAgent,
        fps: this.performance.fps,
        load_time: performance.now()
    });
}
```

### Error Tracking
```javascript
// Add error reporting
window.addEventListener('error', (e) => {
    console.error('AR Business Card Error:', e);
    // Send to your preferred error tracking service
});
```

## 🚀 Going Live

### Final Steps
1. **Test extensively** on multiple devices
2. **Verify all links** point to correct destinations
3. **Check contact information** is accurate
4. **Test vCard download** on different devices
5. **Monitor performance** for first few users

### Share Your AR Business Card
- Print your business card with the marker design
- Include QR code linking to your AR experience
- Share the URL: `https://your-domain.com`
- Test with friends and colleagues

### Maintenance
- Monitor performance metrics
- Update contact information as needed
- Refresh 3D models periodically
- Keep dependencies updated

## 📈 Success Metrics

Track these metrics to measure success:
- Page loads and unique visitors
- AR experience activations
- vCard downloads
- Social link clicks
- Average session duration
- Device/browser distribution

---

**Ready to launch your AR business card? 🚀**

Remember: The goal is to create a memorable networking experience that stands out from traditional business cards!