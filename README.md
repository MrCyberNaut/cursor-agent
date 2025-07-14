# 🧾 AR Business Card - "The Sawant Drop"

An innovative WebAR business card experience that brings your printed business card to life with augmented reality. Simply point a phone camera at your business card to trigger an immersive 3D experience featuring a personal caricature, floating social icons, and an isometric room environment.

![AR Business Card Demo](https://img.shields.io/badge/WebAR-Experience-blue) ![A-Frame](https://img.shields.io/badge/A--Frame-1.4.0-orange) ![MindAR](https://img.shields.io/badge/MindAR-1.2.2-green)

## ✨ Features

- 🎯 **Image Tracking**: Uses your printed business card as an AR marker
- 👤 **3D Caricature**: Personal 3D avatar that links to your website
- 📱 **Social Icons**: Floating 3D social media icons (LinkedIn, GitHub, Twitter, Email)
- 🏠 **3D Environment**: Isometric room scene for visual appeal
- 📇 **Contact Export**: One-tap vCard download functionality
- 🌑 **Dark Mode**: Modern dark-themed UI and lighting
- ⚡ **Performance Adaptive**: Auto-optimizes for different device capabilities
- 📱 **Mobile-First**: Designed for smartphone WebAR experiences

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| WebAR Engine | [A-Frame](https://aframe.io/) + [MindAR](https://hiukim.github.io/mind-ar-js-doc/) |
| 3D Graphics | Three.js (via A-Frame) |
| Hosting | Vercel (with CDN optimization) |
| Assets | Optimized .glb models |
| Performance | Built-in FPS monitoring & adaptive rendering |

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone [your-repo-url]
cd ar-business-card-sawant-drop
```

### 2. Prepare Your Assets
1. **Business Card Marker**: 
   - Take a high-res photo of your business card
   - Generate marker at [MindAR Compiler](https://hiukim.github.io/mind-ar-js-doc/tools/compile)
   - Save as `assets/business-card-marker.mind`

2. **3D Caricature**:
   - Create using [Ready Player Me](https://readyplayer.me/) or Blender
   - Export as `assets/caricature.glb` (< 2MB, < 10k polygons)

3. **Isometric Room** (Optional):
   - Create in Blender or download from [Poly Pizza](https://poly.pizza/)
   - Export as `assets/isometric-room.glb` (< 3MB, < 15k polygons)

### 3. Configure Contact Info
Edit the contact information in `script.js`:
```javascript
this.contactInfo = {
    name: "Your Name",
    email: "your.email@example.com",
    phone: "+1234567890",
    website: "https://yourwebsite.com",
    linkedin: "https://linkedin.com/in/yourprofile",
    github: "https://github.com/yourusername",
    twitter: "https://twitter.com/yourusername"
};
```

### 4. Local Development
```bash
# Using Python (recommended)
npm run dev

# Using Node.js
npm run dev:node

# Open http://localhost:8000
```

### 5. Deploy to Vercel
```bash
npm install -g vercel
vercel login
vercel --prod
```

## 📁 Project Structure

```
ar-business-card/
├── index.html          # Main AR experience
├── styles.css          # Dark mode UI styling
├── script.js           # AR interactions & logic
├── assets/
│   ├── README.md       # Asset preparation guide
│   ├── business-card-marker.mind  # AR marker (you create)
│   ├── caricature.glb  # Your 3D avatar (you create)
│   └── isometric-room.glb         # 3D room (optional)
├── package.json        # Project metadata
├── vercel.json         # Deployment config
└── README.md          # This file
```

## 🎮 User Experience

### Desktop/Laptop
1. Open the URL in a WebXR-compatible browser
2. Allow camera permissions
3. Point camera at the printed business card
4. Watch AR content appear over the card
5. Click on elements to interact

### Mobile (Primary Experience)
1. Open URL in mobile browser (Chrome/Safari recommended)
2. Allow camera access
3. Point phone at business card
4. Tap floating icons to access social profiles
5. Tap "Add to Contacts" to download vCard

## 🔧 Customization

### Styling
- Edit `styles.css` for UI modifications
- Modify A-Frame components in `index.html` for 3D styling
- Adjust lighting and materials in the scene

### Functionality
- Update social links in `script.js`
- Modify animations in `index.html`
- Add new interactive elements

### Performance
- The system auto-detects device performance
- Optimizations include hiding 3D room on low-end devices
- FPS counter shows real-time performance

## 📱 Browser Compatibility

| Browser | Desktop | Mobile | WebXR Support |
|---------|---------|---------|---------------|
| Chrome | ✅ | ✅ | Full |
| Safari | ✅ | ✅ | Limited |
| Firefox | ✅ | ⚠️ | Partial |
| Edge | ✅ | ✅ | Full |

## 🎯 Performance Targets

| Metric | Target | Notes |
|--------|--------|--------|
| Load Time | < 3.5s | On 4G connection |
| Asset Size | < 5MB | Total assets |
| Frame Rate | 30+ FPS | On mid-range phones |
| Memory | < 100MB | Peak usage |

## 🐛 Troubleshooting

### Common Issues

**AR not working:**
- Ensure HTTPS connection (required for camera access)
- Check camera permissions
- Verify marker file exists at `assets/business-card-marker.mind`

**3D models not loading:**
- Check file paths in `index.html`
- Verify .glb files are properly optimized
- Monitor browser console for errors

**Performance issues:**
- The system will auto-optimize for your device
- Check FPS counter (top-right corner)
- Consider reducing 3D model complexity

### Debug Mode
Add `?debug=1` to URL for verbose console logging.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple devices
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🌟 Credits

- **A-Frame**: Web framework for building VR experiences
- **MindAR**: Computer vision for web-based AR
- **Three.js**: 3D graphics library
- **Vercel**: Deployment and hosting platform

---

**Made with ❤️ for memorable networking experiences**

> Transform your business card from paper to immersive 3D experience
