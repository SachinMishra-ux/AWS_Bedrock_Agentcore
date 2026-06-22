---
name: PPT Design and Theme Formatting
description: Instructions and guidelines to design stunning PowerPoint slide layouts, choose color schemes, manage slide-by-slide structures, handle opening and closing slides, and apply slide backgrounds.
---

# PPT Design and Theme Formatting Skill

This skill contains the design system and guidelines for generating premium presentation slides. The AI agent must load and follow these guidelines when creating PowerPoint (.pptx) files.

---

## 1. Widescreen & Slide Dimensions
Always set the presentation size to 16:9 widescreen format:
* Slide Width: 13.333 inches (Inches(13.333))
* Slide Height: 7.5 inches (Inches(7.5))

---

## 2. Color Palette & Typography
* **Slide Background**: Deep Slate Black/Dark Blue (RGB: 11, 15, 25).
* **Card Container Background**: Lighter Slate Blue (RGB: 22, 30, 49).
* **Card Border Color**: Darker Slate Muted Border (RGB: 40, 55, 87).
* **Primary Text**: Off-White (RGB: 248, 250, 252) for readability.
* **Secondary Text**: Muted Blueish Gray (RGB: 148, 163, 184) for bullet lists.
* **Accent Cyan**: Neon Cyan (RGB: 0, 242, 254) for Section Labels and highlighted features.
* **Accent Purple**: Royal Violet/Purple (RGB: 138, 43, 226) for Title text or branding.
* **Accent Gold**: Bright Amber (RGB: 241, 196, 15) for Warning/Compliance blocks.
* **Fonts**: Default to `Arial` or `Helvetica` for clean, professional rendering across systems.

---

## 3. Slide Layout Formats

### Layout A: Title / Opening Slide
* **Visual Background**: Must use the predefined image `skills/ppt_design/resources/slide_background_theme.png` scaled to fit the entire slide.
* **Title Text**: Centered vertically, set to 36-40pt font, bold, Royal Purple.
* **Subtitle Text**: Centered, 18pt font, Muted Gray.
* **Meta-label**: Small uppercase Cyan text above the title (e.g., "SCHOOL OF CLOUD AI ARCHITECTURES").

### Layout B: Content Slide (Text & Visual Card)
* **Header**: Small Cyan section category text (10pt, bold) and a large White slide title (26pt, bold).
* **Left Column**: Text Box with up to 4 concise bullet points (13pt font, Muted Gray).
* **Right Column**: Rounded rectangle container (Card) acting as a "Key Insights" panel, containing a Royal Purple "Key Insight" title and brief analysis.

### Layout C: Content Slide (Text & Embedded Image)
* **Left Column**: Text Box with short bullet points.
* **Right Column**: Embedded image (e.g. `agentcore_architecture.png` representing the architecture diagram) positioned at `left=Inches(6.75), top=Inches(1.8), width=Inches(5.833), height=Inches(3.8)`.

### Layout D: Closing / Summary Slide
* **Visual Background**: Must use `skills/ppt_design/resources/slide_background_theme.png` scaled to fit the entire slide.
* **Left Column**: 3 short discussion questions/takeaways for the class.
* **Right Column**: Lighter Slate Blue Card container summarizing the lecture key concepts and displaying a centered "Ready for Labs" gradient badge.

---

## 4. Predefined Image Resources
* **Slide Background**: `skills/ppt_design/resources/slide_background_theme.png`
* **Architecture Diagram**: `agentcore_architecture.png` (available in the parent root folder if needed, e.g. `../agentcore_architecture.png`).
