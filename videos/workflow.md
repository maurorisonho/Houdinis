# Video Production Workflow

Complete guide from script to published video.

---

## Phase 1: Pre-Production (1-2 days)

### 1.1 Script Preparation
- [ ] Read script 3+ times aloud
- [ ] Time yourself reading (should match target duration ±20%)
- [ ] Mark difficult pronunciations or technical terms
- [ ] Prepare all code samples in advance
- [ ] Test every command in clean environment
- [ ] Create backup VM snapshot

### 1.2 Environment Setup
- [ ] Clean desktop (minimal icons, clean wallpaper)
- [ ] Configure terminal (font size 16-18pt, high contrast theme)
- [ ] Setup code editor (Zen mode, large fonts)
- [ ] Close notification apps (Slack, email, etc.)
- [ ] Enable Do Not Disturb mode
- [ ] Prepare demo files and test data

### 1.3 Equipment Check
- [ ] Test microphone (audio levels peak at -12dB)
- [ ] Verify lighting (no harsh shadows on face)
- [ ] Check webcam focus and framing (if using)
- [ ] Ensure stable internet (if screen recording cloud services)
- [ ] Have water nearby
- [ ] Charge laptop / plug in power

### 1.4 OBS Studio Setup
- [ ] Launch OBS and load scene collection
- [ ] Test screen capture (verify correct monitor)
- [ ] Check audio levels (microphone + desktop audio)
- [ ] Verify recording path has space (20GB+ free)
- [ ] Do 30-second test recording and playback
- [ ] Set up hotkeys (F9 start, F10 stop)

**Time investment:** 2-3 hours

---

## Phase 2: Recording (2-4 hours)

### 2.1 Initial Take
1. Start OBS recording (F9)
2. Count down: "3, 2, 1, recording..."
3. Pause 3 seconds
4. Begin intro (as scripted)
5. **Record straight through without stopping**
6. If you make a mistake:
   - Pause 3 seconds
   - Resume from last good sentence
   - DON'T stop recording
7. Complete outro
8. Pause 3 seconds
9. Stop recording (F10)

**Duration:** 1-1.5x target length (15 min video = 15-22 min recording)

### 2.2 Review Take 1
- [ ] Watch entire recording
- [ ] Note timestamps of major issues
- [ ] Check audio quality throughout
- [ ] Verify all visuals are clear
- [ ] Decide: Good enough or need Take 2?

**Criteria for Take 2:**
- Audio issues (background noise, mic pops)
- Major mistakes or confusing explanations
- Technical failures (code didn't work)
- Energy/enthusiasm too low

**If minor issues only:** Continue to editing, fix in post

### 2.3 Take 2 (if needed)
- Address specific issues from Take 1
- No need to re-record perfect sections
- Can record segments and splice later
- Rest 15 minutes between takes

### 2.4 B-Roll & Additional Footage
- [ ] Record close-ups of code snippets
- [ ] Capture additional terminal commands
- [ ] Screen record any visualizations
- [ ] Film any physical demonstrations
- [ ] Record voice-over for time-lapse sections

**Time investment:** 2-4 hours (including breaks)

---

## Phase 3: Post-Production (4-8 hours)

### 3.1 Import & Organization (30 min)
1. Create project folder structure:
   ```
   VideoXX_Title/
    RAW/           # Original recordings
    Project/       # DaVinci Resolve project
    Assets/        # Graphics, music, B-roll
    Export/        # Final rendered video
    Subtitles/     # SRT files
   ```
2. Copy recordings to RAW/ folder
3. **Backup immediately to external drive**
4. Launch DaVinci Resolve
5. Create new project: "VideoXX_Title"
6. Import all media to Media Pool

### 3.2 Rough Cut (2-3 hours)
1. **Add to timeline:** Drag main recording to Video 1 track
2. **Scrub through** and mark:
   - Intro start (⌘I to mark in)
   - Outro end (⌘O to mark out)
   - Sections to cut (long pauses, mistakes)
3. **Cut out dead air:**
   - Blade tool (B key) to split
   - Delete gaps over 3 seconds
   - Ripple delete to close gaps
4. **Speed up installations:**
   - Select long install segments
   - Change speed to 200% (2x)
   - Add "Speeding up installation..." text overlay
5. **Add chapter markers:**
   - Place playhead at chapter start
   - Press M to add marker
   - Name marker with chapter title

**Result:** Rough timeline, all unnecessary parts removed

### 3.3 Fine Cut (1-2 hours)
1. **Audio cleanup:**
   - Go to Fairlight page
   - Select audio track
   - Add: Dynamics → Compressor (ratio 4:1, threshold -20dB)
   - Add: Noise Reduction → -20dB
   - Add: EQ → Boost 100Hz, reduce 8kHz
   - Normalize loudness to -16 LUFS
2. **Visual polish:**
   - Go to Color page
   - Apply basic color correction (if needed)
   - Slightly increase contrast and saturation
   - Ensure consistent look throughout
3. **Smooth transitions:**
   - Replace jump cuts with smooth transitions (1-2 frames)
   - Add dissolve between major sections (20-30 frames)

### 3.4 Graphics & Overlay (2-3 hours)
1. **Intro sequence (5 seconds):**
   - Houdinis logo animation
   - Text: "Video #XX: [Title]"
   - Background music fade in
2. **Lower thirds:**
   - Add name/title at 0:10
   - Duration: 5 seconds
3. **Text overlays for commands:**
   - Highlight important commands
   - Use monospace font (Fira Code)
   - Background: semi-transparent black
4. **Chapter title cards:**
   - Brief 2-second card between major sections
   - Format: "Part 2: Installation on macOS"
5. **Captions/subtitles:**
   - Auto-transcribe in DaVinci Resolve (or YouTube)
   - Review and correct technical terms
   - Export as SRT file
6. **Outro sequence (10 seconds):**
   - Subscribe animation
   - Links overlay:
     - Next video
     - GitHub repository
     - Documentation
   - Background music fade out

### 3.5 Audio Mix (30 min)
1. **Balance levels:**
   - Voice: Peak at -6dB
   - Music: -20dB (background, not distracting)
   - Sound effects: -12dB
2. **Ducking:**
   - Automatically lower music when speaking
   - Fairlight → Dynamics → Compressor (sidechain to voice)
3. **Final listen:**
   - Watch full video at playback speed
   - Ensure audio is clear and balanced throughout

**Time investment:** 4-8 hours

---

## Phase 4: Export & Publish (1-2 hours)

### 4.1 Render Video (30-60 min)
1. Go to Deliver page
2. **Settings:**
   - Format: MP4
   - Codec: H.264
   - Resolution: 1920x1080
   - Frame rate: 30fps
   - Quality: YouTube preset (or custom 6000 Kbps)
   - Audio: AAC, 192 Kbps, 48kHz
3. **Export location:** `Export/VideoXX_Title_FINAL.mp4`
4. Click "Add to Render Queue"
5. Click "Start Render"
6. **Wait:** 10-30 minutes depending on length and computer speed

### 4.2 Create Thumbnail (20 min)
1. Open Canva or Photoshop
2. Use template: `templates/thumbnail-template.psd`
3. **Elements:**
   - Video number: Large, top-left
   - Title: Bold, center, readable at small size
   - Screenshot: Relevant visual from video
   - Houdinis logo: Bottom-right corner
   - Colors: Brand colors (#2E86AB blue, #F18F01 orange)
4. Export: 1280x720px, JPEG, high quality
5. Save as: `VideoXX_Thumbnail.jpg`

### 4.3 Write Description (15 min)
Use template: `templates/youtube-description-template.md`

```markdown
 Learn how to [video objective] using Houdinis Framework!

⏱ Timestamps:
00:00 - Introduction
02:00 - [Section 1]
05:00 - [Section 2]
...

 Links:
 Documentation: https://maurorisonho.github.io/Houdinis/
 Try in Browser: https://mybinder.org/v2/gh/maurorisonho/Houdinis/main
 GitHub: https://github.com/maurorisonho/Houdinis
 Code Samples: [GitHub Gist link]

 Prerequisites:
- [List prerequisites]

 What you'll learn:
- [Learning objective 1]
- [Learning objective 2]
- [Learning objective 3]

 Related Videos:
- Previous: [Link to video #XX-1]
- Next: [Link to video #XX+1]

#QuantumComputing #Cryptography #Houdinis #Cybersecurity #Python

---

 Subscribe for more quantum computing tutorials!
 Star the project on GitHub: https://github.com/maurorisonho/Houdinis
 Questions? Ask in the comments!
```

### 4.4 Upload to YouTube (20 min)
1. Go to YouTube Studio
2. Click "CREATE" → "Upload videos"
3. **Select file:** `VideoXX_Title_FINAL.mp4`
4. **Details:**
   - Title: "Houdinis Framework #XX: [Title]"
   - Description: Paste from template
   - Thumbnail: Upload custom thumbnail
5. **Visibility:** Set to "Unlisted" initially for review
6. **Playlist:** Add to "Houdinis Tutorials"
7. **Tags:** quantum computing, cryptography, houdinis, cybersecurity, python, qiskit, shor's algorithm, etc.
8. **End screen:** Add subscribe button + next video
9. **Cards:** Add 2-3 cards linking to related videos
10. Click "Save"

### 4.5 Add Subtitles (30 min per language)
1. YouTube auto-generates English subtitles
2. Click "Subtitles" tab
3. **Review and edit English:**
   - Fix technical terms (Qiskit, qubit, superposition, etc.)
   - Correct command spellings
   - Add punctuation for better readability
4. **Download English SRT:**
   - Save to `Subtitles/VideoXX_EN.srt`
5. **Translate to other languages:**
   - Upload to translation service (e.g., Rev.com, $1.50/min)
   - Or use Google Translate + manual review
   - Generate: PT-BR, ES, ZH subtitle files
6. **Upload translated subtitles:**
   - YouTube Studio → Subtitles → Add language
   - Upload SRT files for each language

### 4.6 Publish (5 min)
1. Review video one final time on YouTube
2. Check:
   - [ ] Thumbnail looks good
   - [ ] Description has all links
   - [ ] Timestamps work correctly
   - [ ] End screen and cards active
   - [ ] English subtitles accurate
3. Change visibility to "Public"
4. Set premiere time (optional) or publish immediately
5. **Share immediately:**
   - Copy video link
   - Post to social media
   - Add to documentation

**Time investment:** 1-2 hours

---

## Phase 5: Promotion (Ongoing)

### 5.1 Initial Announcement (Day 1)
- [ ] Twitter: Thread with key highlights + video link
- [ ] LinkedIn: Professional post with context
- [ ] Reddit: Post to r/QuantumComputing, r/crypto, r/netsec
- [ ] Dev.to: Article with embedded video
- [ ] GitHub: Update README with new video
- [ ] Documentation: Add video embed to relevant page
- [ ] Email list: Announcement to subscribers (if any)

### 5.2 Engagement (Week 1-2)
- [ ] Respond to all comments within 24 hours
- [ ] Pin best comment
- [ ] Heart helpful comments
- [ ] Create discussion questions in comments
- [ ] Share user feedback on social media

### 5.3 Analysis (Week 2)
- [ ] Review YouTube Analytics:
  - Views, watch time, audience retention
  - Traffic sources (where viewers came from)
  - Demographics (age, location, gender)
  - Average view duration
- [ ] Identify drop-off points in retention graph
- [ ] Note feedback for next video improvements

---

## Checklist Templates

### Pre-Recording Checklist
```
 Script reviewed and practiced
 Demo environment prepared and tested
 All commands verified working
 Desktop cleaned and organized
 Notifications disabled (Do Not Disturb)
 Microphone tested (levels at -12dB)
 OBS scenes configured
 Test recording completed
 Water nearby
 Comfortable and ready to record
```

### Post-Recording Checklist
```
 Recording saved successfully
 Backup created immediately
 Full recording reviewed
 Timestamps noted for editing
 B-roll footage captured (if needed)
 Audio quality acceptable throughout
 All visuals clear and readable
 Ready to proceed to editing
```

### Pre-Publish Checklist
```
 Video rendered successfully
 Thumbnail created (1280x720)
 Description written with timestamps
 All links tested and working
 Subtitles reviewed (at minimum English)
 End screen configured
 Cards added (2-3 relevant)
 Playlist assignment
 Tags added (10-15)
 Preview watch-through complete
 Social media posts drafted
 Documentation updates prepared
 Ready to publish!
```

---

## Time Budget Summary

| Phase | Time | Can Parallelize? |
|-------|------|------------------|
| Pre-Production | 2-3 hours | No |
| Recording | 2-4 hours | No |
| Post-Production | 4-8 hours | Partially |
| Export & Publish | 1-2 hours | Yes (during render) |
| Promotion | 1-2 hours | Yes (ongoing) |
| **Total per video** | **10-19 hours** | - |

**For 18 videos:** 180-342 hours = 4.5-8.5 weeks full-time

**Realistic timeline (part-time):** 2-3 videos/week = 6-9 weeks

---

## Tips for Efficiency

1. **Batch similar tasks:**
   - Record multiple videos in one day
   - Edit multiple videos in sequence
   - Create all thumbnails at once

2. **Use templates:**
   - Intro/outro animations (render once, reuse)
   - Lower third graphics
   - YouTube description format
   - Thumbnail design

3. **Automate where possible:**
   - Auto-transcription for subtitles
   - Batch export settings
   - Scheduled publishing

4. **Delegate if budget allows:**
   - Hire editor for post-production ($500-1000/video)
   - Professional subtitle translation ($50-60/video)
   - Thumbnail designer ($20-50/thumbnail)

5. **Learn keyboard shortcuts:**
   - DaVinci Resolve shortcuts save hours
   - OBS hotkeys speed up recording
   - YouTube Studio shortcuts for publishing

---

## Quality Standards

### Audio
-  Clear voice, no background noise
-  Consistent volume throughout
-  Peak levels at -6dB to -3dB
-  Music doesn't overpower voice
-  No pops, clicks, or distortion

### Video
-  1080p minimum resolution
-  Smooth 30fps throughout
-  Text readable on mobile devices
-  High contrast for code/terminal
-  No shaky camera (if using webcam)

### Content
-  Accurate information, no errors
-  Clear explanations, good pacing
-  All code examples work as shown
-  Good balance of theory and practice
-  Engaging delivery, enthusiasm

### Accessibility
-  Subtitles in English (minimum)
-  Clear enunciation
-  Visual indicators for important points
-  Not relying solely on color to convey information

---

**Last Updated:** December 15, 2025  
**Version:** 1.0  
**Maintainer:** Content Team
