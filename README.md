<div align="center">
  <h2 align="center">Requestly Account Creator</h2>
  <p align="center">
    An automated tool for creating Requestly accounts to get a free 1m premium plan with email verification support, proxy handling, and multi-threading capabilities.
    <br />
    <br />
    <a href="https://discord.cyberious.xyz">💬 Discord</a>
    ·
    <a href="#-changelog">📜 ChangeLog</a>
    ·
    <a href="https://github.com/sexfrance/Requestly-Account-Creator/issues">⚠️ Report Bug</a>
    ·
    <a href="https://github.com/sexfrance/Requestly-Account-Creator/issues">💡 Request Feature</a>
  </p>
</div>

---

### ⚙️ Installation

- Requires: `Python 3.7+`
- Make a python virtual environment: `python3 -m venv venv`
- Source the environment: `venv\Scripts\Activate` (Windows) / `source venv/bin/activate` (macOS, Linux)
- Install the requirements: `pip install -r requirements.txt`

---

### 🔥 Features

- Email verification support using cybertemp.xyz email service
- Proxy support for avoiding rate limits
- Multi-threaded account generation
- Real-time creation tracking with console title updates
- Configurable thread count
- Debug mode for troubleshooting
- Proxy/Proxyless mode support
- Random user agent generation
- Detailed logging system
- Account data saving (email:uid format)
- Custom API key support for email service

---

### 📝 Usage

1. **Configuration**:
   Edit `input/config.toml`:

   ```toml
   [dev]
   Debug = false
   Proxyless = false
   Threads = 1

   [data]
   Cybertemp_Api_Key = "your_api_key_here" # Optional
   ```

2. **Proxy Setup** (Optional):

   - Add proxies to `input/proxies.txt` (one per line)
   - Format: `ip:port` or `user:pass@ip:port`

3. **Running the script**:

   ```bash
   python main.py
   ```

4. **Output**:
   - Created accounts are saved to `output/accounts.txt` (email:uid format)

---

### 📹 Preview

![Preview](https://i.imgur.com/VwiZ0QR.gif)

---

### ❗ Disclaimers

- This project is for educational purposes only
- The author is not responsible for any misuse of this tool
- Use responsibly and in accordance with Requestly's terms of service

---

### 📜 ChangeLog

```diff
v0.0.1 ⋮ 12/26/2024
! Initial release with email verification and proxy support
```

<p align="center">
  <img src="https://img.shields.io/github/license/sexfrance/Requestly-Account-Creator.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/stars/sexfrance/Requestly-Account-Creator.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/languages/top/sexfrance/Requestly-Account-Creator.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=python"/>
</p>
