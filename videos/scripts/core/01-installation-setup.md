# Video Script: Installation and Setup

**Video #:** 01  
**Title:** Houdinis Framework - Installation and Setup Guide  
**Duration:** 10 minutes  
**Difficulty:** Beginner  
**Prerequisites:** Basic command line knowledge  
**Target Audience:** Security researchers, students, quantum computing enthusiasts

---

##  Learning Objectives

By the end of this video, viewers will be able to:
1.  Install Houdinis Framework on Linux, macOS, and Windows
2.  Configure Python virtual environment
3.  Install quantum computing dependencies (Qiskit, Cirq)
4.  Verify installation and run first test
5.  Understand directory structure and key files

---

##  Video Structure

### Timestamps (Chapter Markers)
```
00:00 - Introduction
01:30 - Prerequisites Check
03:00 - Installation on Linux
05:15 - Installation on macOS
06:30 - Installation on Windows
08:00 - Verification & First Test
09:30 - Next Steps & Conclusion
```

---

##  Full Script

### [00:00 - 01:30] Introduction

**[SCREEN: Houdinis logo animation, then fade to desktop]**

**NARRATION:**
"Welcome to the Houdinis Framework tutorial series! I'm [Your Name], and in this video, we'll install Houdinis, a comprehensive quantum cryptography testing platform.

Houdinis allows you to test quantum algorithms, evaluate cryptographic vulnerabilities, and run attacks like Shor's algorithm for RSA factorization and Grover's algorithm for symmetric key search.

Whether you're a security researcher, penetration tester, or just curious about quantum computing's impact on cryptography, this framework has you covered.

Before we dive in, let's check what you'll need."

**[VISUAL CUE: Show requirements on screen as bullets]**

---

### [01:30 - 03:00] Prerequisites Check

**[SCREEN: Terminal window, clean prompt]**

**NARRATION:**
"First, let's verify your system meets the requirements. You'll need:

- Python 3.11 or higher
- Git for cloning the repository
- At least 4GB of RAM
- 5GB of free disk space

Let's check your Python version."

**[TYPE COMMAND]**
```bash
python3 --version
```

**[SHOW OUTPUT]**
```
Python 3.11.5
```

**NARRATION:**
"Great! Python 3.11.5 is installed. If you see a version lower than 3.11, you'll need to upgrade first. I'll put links to Python installation guides in the description.

Now let's verify Git is installed."

**[TYPE COMMAND]**
```bash
git --version
```

**[SHOW OUTPUT]**
```
git version 2.39.2
```

**NARRATION:**
"Perfect! We have everything we need. Let's start the installation."

---

### [03:00 - 05:15] Installation on Linux

**[SCREEN: Terminal, showing Linux prompt]**

**NARRATION:**
"I'll demonstrate on Ubuntu Linux, but these steps work on most distributions. First, let's clone the repository."

**[TYPE COMMAND - SLOW, VISIBLE]**
```bash
git clone https://github.com/maurorisonho/Houdinis.git
```

**[SHOW OUTPUT: Cloning progress]**

**NARRATION:**
"This downloads the entire framework. It's about 50 megabytes, so it should only take a few seconds.

Now let's navigate into the directory."

**[TYPE COMMAND]**
```bash
cd Houdinis
ls -la
```

**[SHOW OUTPUT: Directory listing]**

**NARRATION:**
"Here's the project structure. You can see the main components:
- 'exploits' directory contains attack scripts
- 'quantum' has the quantum computing backend
- 'scanners' for network vulnerability scanning
- 'notebooks' with Jupyter tutorials

Next, let's create a Python virtual environment. This keeps Houdinis dependencies isolated from your system."

**[TYPE COMMAND]**
```bash
python3 -m venv venv
source venv/bin/activate
```

**[SHOW: Prompt changes with (venv) prefix]**

**NARRATION:**
"See the 'venv' prefix? That means we're in the virtual environment. Now let's install dependencies."

**[TYPE COMMAND]**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**[SHOW: Installation progress, speed up video 2x during this]**

**NARRATION (voiceover during sped-up footage):**
"This installs all the quantum computing libraries: Qiskit for IBM quantum computers, Cirq for Google's platform, PennyLane for quantum machine learning, plus cryptography libraries and network tools.

The installation takes about 5-10 minutes depending on your internet speed. I'm speeding this up to save time."

**[NORMAL SPEED when installation completes]**

**NARRATION:**
"Installation complete! Let's verify everything works."

---

### [05:15 - 06:30] Installation on macOS

**[SCREEN: macOS terminal]**

**NARRATION:**
"If you're on macOS, the process is almost identical. First, clone the repository."

**[TYPE COMMAND]**
```bash
git clone https://github.com/maurorisonho/Houdinis.git
cd Houdinis
```

**NARRATION:**
"Create the virtual environment. On macOS, you might need to use 'python3' explicitly."

**[TYPE COMMAND]**
```bash
python3 -m venv venv
source venv/bin/activate
```

**NARRATION:**
"And install dependencies, exactly the same way."

**[TYPE COMMAND]**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**NARRATION:**
"One macOS-specific note: if you see errors about Xcode command line tools, run this first:"

**[SHOW TEXT ON SCREEN]**
```bash
xcode-select --install
```

**NARRATION:**
"Then retry the pip install. Everything else is the same as Linux."

---

### [06:30 - 08:00] Installation on Windows

**[SCREEN: Windows PowerShell or Command Prompt]**

**NARRATION:**
"On Windows, I recommend using PowerShell or Windows Terminal. The steps are similar with small differences.

First, clone the repository."

**[TYPE COMMAND]**
```powershell
git clone https://github.com/maurorisonho/Houdinis.git
cd Houdinis
```

**NARRATION:**
"Create the virtual environment. On Windows, use 'python' instead of 'python3'."

**[TYPE COMMAND]**
```powershell
python -m venv venv
venv\Scripts\activate
```

**[SHOW: Prompt changes with (venv)]**

**NARRATION:**
"Notice the activation script is in 'Scripts', not 'bin'. Now install dependencies."

**[TYPE COMMAND]**
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

**NARRATION:**
"Windows users might see warnings about path length limits. If you do, enable long paths in Windows settings. There's a link in the description.

Also, some quantum libraries require Microsoft Visual C++ Build Tools. The installer will warn you if needed."

---

### [08:00 - 09:30] Verification & First Test

**[SCREEN: Terminal with Houdinis directory]**

**NARRATION:**
"Let's verify the installation works. Run the main script with the version flag."

**[TYPE COMMAND]**
```bash
python main.py --version
```

**[SHOW OUTPUT]**
```
Houdinis Framework v1.0.0
Quantum Cryptography Testing Platform
```

**NARRATION:**
"Excellent! Now let's run the built-in tests."

**[TYPE COMMAND]**
```bash
python tests/test_houdinis.py
```

**[SHOW OUTPUT: Tests running and passing]**
```
Testing Houdinis Framework...
 Quantum backend initialized
 RSA attack module loaded
 Grover's algorithm ready
 Network scanner operational

All tests passed! 
```

**NARRATION:**
"Perfect! All tests passed. Let's quickly explore the framework by running the interactive mode."

**[TYPE COMMAND]**
```bash
python main.py --interactive
```

**[SHOW: Interactive menu]**
```

   Houdinis Framework v1.0.0            
   Quantum Cryptography Testing         


Select an attack:
1) Shor's Algorithm (RSA Factorization)
2) Grover's Algorithm (Symmetric Key Search)
3) Quantum Network Scan
4) Post-Quantum Cryptography Assessment
5) Exit

Choice:
```

**NARRATION:**
"This is the interactive menu. You can select different quantum attacks to run. We'll explore these in detail in upcoming videos.

For now, press 5 to exit."

**[PRESS 5, return to prompt]**

---

### [09:30 - 10:00] Next Steps & Conclusion

**[SCREEN: Split screen - terminal on left, documentation website on right]**

**NARRATION:**
"Congratulations! You've successfully installed Houdinis Framework. You're now ready to run quantum cryptanalysis attacks.

In the next video, we'll run our first attack using Shor's algorithm to factor RSA keys. Make sure to subscribe so you don't miss it.

Here are some resources to explore:

- Try the interactive Binder environment - no installation needed, runs in your browser
- Check out the Jupyter notebooks in the 'notebooks' directory for comprehensive tutorials
- Read the documentation at maurorisonho.github.io/Houdinis
- Join our community on GitHub to ask questions and contribute

Thanks for watching, and I'll see you in the next video where we'll break some RSA encryption!"

**[SCREEN: End card with links]**
```
 Links:
 Documentation: maurorisonho.github.io/Houdinis
 Try in Browser: mybinder.org/v2/gh/maurorisonho/Houdinis/main
 GitHub: github.com/maurorisonho/Houdinis
 Next Video: Quick Start - First Attack

 Like |  Comment |  Subscribe
```

**[FADE OUT]**

---

##  Visual Elements

### B-Roll Footage Needed
- [ ] Python logo animation
- [ ] Quantum circuit visualizations
- [ ] Code editor closeups
- [ ] Terminal command typing (slow motion)
- [ ] Framework directory structure exploration

### Graphics to Create
- [ ] Intro animation (5 seconds) - Houdinis logo with glitch effect
- [ ] Outro animation (10 seconds) - Subscribe reminder + links
- [ ] Lower thirds (name, title)
- [ ] Requirement checklist graphic
- [ ] Platform comparison table (Linux/macOS/Windows)

### Screen Recordings
- [ ] Full installation on Linux (main footage)
- [ ] Quick macOS installation demo
- [ ] Quick Windows installation demo
- [ ] Test execution and output
- [ ] Interactive menu demo

---

##  Production Notes

### Recording Setup
- **Resolution:** 1920x1080 (1080p)
- **Frame Rate:** 30fps
- **Terminal:** Dark theme with high contrast
- **Font Size:** 16-18pt (readable on mobile)
- **Cursor:** Highlight cursor for visibility

### Audio
- **Pacing:** Moderate speed, clear pronunciation
- **Pauses:** Brief pauses after commands for viewer to process
- **Music:** Subtle background music (tech/ambient), -20dB

### Editing
- **Cuts:** Remove long pauses, installation waiting times
- **Speed:** 2x speed during long installations
- **Captions:** Add captions for all commands
- **Highlights:** Highlight important output lines

---

##  Pre-Recording Checklist

- [ ] Clean desktop (close unnecessary windows)
- [ ] Terminal configured with readable font
- [ ] Test all commands in fresh environment
- [ ] Prepare demo system (VM recommended)
- [ ] Review script timing
- [ ] Backup recording files
- [ ] Test microphone levels
- [ ] Close notification apps

---

##  Success Criteria

-  Video length: 10 minutes ±1 minute
-  All commands execute successfully
-  Clear audio throughout
-  Smooth transitions between sections
-  No awkward pauses or mistakes
-  Professional presentation
-  Engaging pacing

---

**Script Version:** 1.0  
**Last Updated:** December 15, 2025  
**Reviewed By:** [To be assigned]  
**Status:**  Ready for recording
