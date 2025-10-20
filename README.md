<div align="center">

# 🌟 Hikari Image Compressor

### Modern Image Compression Tool with Clean & Intuitive Interface

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/Gary19gts/hikari-image-compressor)
[![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red.svg)](https://github.com/Gary19gts)

<img src="https://via.placeholder.com/800x450/007AFF/FFFFFF?text=Hikari+Image+Compressor+Screenshot" alt="Hikari Image Compressor Screenshot" width="800"/>

**Compress images effortlessly with a beautiful, intuitive interface designed for simplicity and power.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Contributing](#-contributing) • [Support](#-support)

</div>

---

## 📖 About

**Hikari Image Compressor** (光 - meaning "light" in Japanese) is a free, open-source desktop application that makes image compression simple and elegant. Whether you're optimizing photos for the web, reducing file sizes for storage, or preparing images for social media, Hikari provides powerful compression tools wrapped in a clean, modern interface.

### Why Hikari?

- 🎨 **Beautiful UI** - Clean, modern design that's both elegant and functional
- ⚡ **Fast & Efficient** - Batch process multiple images with real-time previews
- 🔧 **Flexible Options** - Multiple quality presets, formats, and resize capabilities
- 📊 **Smart Estimates** - See compression results before processing
- 🆓 **100% Free** - Open source and always will be
- 🌍 **Cross-Platform** - Works on Windows, macOS, and Linux

---

## ✨ Features

### Core Functionality

- **📁 Batch Processing** - Compress multiple images at once
- **🖼️ Multiple Formats** - Support for JPEG, PNG, WebP, BMP, and TIFF
- **🎚️ Quality Presets** - Choose from Low (30%), Medium (60%), High (80%), or Maximum (95%)
- **📐 Smart Resizing** - Scale images by percentage while maintaining aspect ratio
- **👁️ Live Preview** - See thumbnails and estimated compression before processing
- **💾 Flexible Output** - Save to custom folder or same location as source

### Advanced Features

- **🔄 Format Conversion** - Convert between image formats during compression
- **📊 Compression Estimates** - Real-time calculation of expected file sizes
- **🎯 Transparency Handling** - Automatic RGBA to RGB conversion for JPEG
- **⚙️ Multiple Engines** - Choose between Pillow and Imageio compression engines
- **🗂️ Smart Naming** - Output files include quality and scale suffixes
- **🚀 Non-Blocking UI** - Background processing keeps the interface responsive

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Quick Install

1. **Clone the repository**
   ```bash
   git clone https://github.com/Gary19gts/hikari-image-compressor.git
   cd hikari-image-compressor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python hikari_image_compressor.py
   ```

### Dependencies

```
customtkinter>=5.2.0
Pillow>=10.0.0
imageio>=2.31.0
```

---

## 💻 Usage

### Basic Workflow

1. **Load Images** - Click "Select Images" to choose files to compress
2. **Configure Settings** - Adjust quality, format, and resize options
3. **Preview** - Review thumbnails and estimated compression ratios
4. **Select Output** - Choose where to save compressed images
5. **Compress** - Click "Start Compression" and watch the magic happen!

### Quality Guide

| Quality Level | Use Case | Compression | Quality |
|--------------|----------|-------------|---------|
| **Low (30%)** | Thumbnails, previews | Maximum | Noticeable loss |
| **Medium (60%)** | Web images, social media | High | Good balance |
| **High (80%)** | General use, archiving | Moderate | Excellent ⭐ |
| **Maximum (95%)** | Professional work | Minimal | Near-lossless |

### Format Recommendations

- **JPEG** - Best for photographs, no transparency support
- **WebP** - Modern format, excellent compression, supports transparency
- **PNG** - Lossless compression, transparency support, larger files

### Resize Options

Scale images by percentage to reduce dimensions:
- **50%** - Perfect for web optimization
- **25%** - Ideal for thumbnails
- **75%** - Moderate size reduction

---

## 📸 Screenshots

<div align="center">

### Main Interface
<img src="https://via.placeholder.com/700x400/F8F9FA/1D1D1F?text=Main+Interface" alt="Main Interface" width="700"/>

### Batch Processing
<img src="https://via.placeholder.com/700x400/F8F9FA/1D1D1F?text=Batch+Processing" alt="Batch Processing" width="700"/>

### Settings Panel
<img src="https://via.placeholder.com/700x400/F8F9FA/1D1D1F?text=Settings+Panel" alt="Settings Panel" width="700"/>

</div>

---

## 🛠️ Technical Details

### Built With

- **[Python](https://www.python.org/)** - Core programming language
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - Modern UI framework
- **[Pillow](https://pillow.readthedocs.io/)** - Image processing library
- **[Imageio](https://imageio.readthedocs.io/)** - Advanced image I/O

### Architecture

- **Single-class design** for simplicity
- **Threading** for non-blocking compression
- **Event-driven UI** with real-time updates
- **Cross-platform compatibility** with OS-specific optimizations

---

## 🤝 Contributing

Contributions are welcome! Whether it's bug reports, feature requests, or code contributions, your help makes Hikari better.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/hikari-image-compressor.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python hikari_image_compressor.py
```

---

## 📝 License

This project is licensed under the **GNU Affero General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

### What this means:

- ✅ Free to use, modify, and distribute
- ✅ Open source forever
- ✅ Commercial use allowed
- ⚠️ Must disclose source code
- ⚠️ Must use same license for derivatives
- ⚠️ Network use requires source disclosure

---

## 🌟 Support

Thank you for using **Hikari Image Compressor**! Made with ❤️ by [Gary19gts](https://github.com/Gary19gts)

If Hikari has been helpful to you, please consider supporting its development:

<div align="center">

### ☕ Buy me a coffee on Ko-fi

[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20Development-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/gary19gts)

**✨ Even the smallest donation can bring a big light during these tough times.**

**Even $1 can help more than you think 😀🙏**

**Thank you so much for standing with me! ✨**

</div>

### Other Ways to Support

- ⭐ **Star this repository** - It helps others discover Hikari
- 🐛 **Report bugs** - Help improve the software
- 💡 **Suggest features** - Share your ideas
- 📢 **Spread the word** - Tell others about Hikari
- 🤝 **Contribute code** - Join the development

---

## 📞 Contact & Links

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-Gary19gts-181717?style=for-the-badge&logo=github)](https://github.com/Gary19gts)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-gary19gts-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/gary19gts)

**Project Link:** [https://github.com/Gary19gts/hikari-image-compressor](https://github.com/Gary19gts/hikari-image-compressor)

</div>

---

## 🙏 Acknowledgments

Special thanks to:

- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** by Tom Schimansky - For the beautiful UI framework
- **[Pillow](https://pillow.readthedocs.io/)** team - For powerful image processing
- **Python Software Foundation** - For the amazing Python language
- **Open Source Community** - For inspiration and support
- **All contributors and users** - For making this project possible

---

<div align="center">

### 🌟 If you find Hikari useful, please give it a star! 🌟

**Made with ❤️ and ☕ by Gary19gts**

*Bringing light to image compression, one pixel at a time.*

</div>
