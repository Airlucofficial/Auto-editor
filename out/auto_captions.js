// AutoEditor Auto-Captions & CapCut Styles Client Controller (64 Presets & 8 Categories)
(function() {
  const API_BASE = "http://localhost:4001";

  // Embedded comprehensive library of 64 curated styles across 8 categories
  const EMBEDDED_STYLES = [
  {
    "id": "bouncy_shorts",
    "name": "Bouncy Social",
    "category": "viral_shorts",
    "category_label": "Viral Shorts",
    "description": "High engagement TikTok/Shorts style with active word scale pop and vibrant lime green highlight.",
    "font": "Arial Black",
    "fallback_font": "Arial",
    "fontsize": 48,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0000FF00",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.0,
    "shadow": 2.0,
    "alignment": 2,
    "margin_v": 80,
    "uppercase": true,
    "animation_type": "bounce_pop",
    "preview_class": "preview-bouncy",
    "preview_html": "BOUNCY <span class=\"act\">SCALE</span> POP",
    "css": {
      "fontFamily": "Arial Black, sans-serif",
      "color": "#ffffff",
      "activeColor": "#22c55e",
      "textTransform": "uppercase",
      "textShadow": "-2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000"
    }
  },
  {
    "id": "tiktok_pop",
    "name": "TikTok Speed Pop",
    "category": "viral_shorts",
    "category_label": "Viral Shorts",
    "description": "Electric yellow scale pop with dark stroke for fast-paced viral videos.",
    "font": "Arial Black",
    "fallback_font": "Impact",
    "fontsize": 50,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0000FFFF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.5,
    "shadow": 2.0,
    "alignment": 2,
    "margin_v": 78,
    "uppercase": true,
    "animation_type": "bounce_pop",
    "preview_class": "preview-tiktok-pop",
    "preview_html": "VIRAL <span class=\"act\">SPEED</span> HOOK",
    "css": {
      "fontFamily": "Arial Black, sans-serif",
      "color": "#ffffff",
      "activeColor": "#facc15",
      "textTransform": "uppercase",
      "textShadow": "2px 2px 0 #000, -2px -2px 0 #000"
    }
  },
  {
    "id": "viral_green_hook",
    "name": "Viral Green Hook",
    "category": "viral_shorts",
    "category_label": "Viral Shorts",
    "description": "High-contrast neon emerald highlight designed for maximum retention on first 3 seconds.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 52,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0014FF39",
    "outline_color": "&H00000000",
    "back_color": "&H80000000",
    "bold": 1,
    "outline": 4.5,
    "shadow": 2.5,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "karaoke_highlight",
    "preview_class": "preview-viral-green",
    "preview_html": "STOP <span class=\"act\">SCROLLING</span> NOW",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#ffffff",
      "activeColor": "#10b981",
      "textTransform": "uppercase",
      "textShadow": "2px 2px 0 #000, -2px -2px 0 #000"
    }
  },
  {
    "id": "snap_yellow",
    "name": "Snap Yellow Pulse",
    "category": "viral_shorts",
    "category_label": "Viral Shorts",
    "description": "Bright sunshine yellow with snap pulse animation for punchy storytelling.",
    "font": "Trebuchet MS",
    "fallback_font": "Arial Black",
    "fontsize": 48,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0000E1FF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.0,
    "shadow": 2.0,
    "alignment": 2,
    "margin_v": 76,
    "uppercase": true,
    "animation_type": "scale_pulse",
    "preview_class": "preview-snap-yellow",
    "preview_html": "SNAP <span class=\"act\">PULSE</span> ACTION",
    "css": {
      "fontFamily": "Trebuchet MS, sans-serif",
      "fontWeight": "bold",
      "color": "#ffffff",
      "activeColor": "#f59e0b",
      "textTransform": "uppercase",
      "textShadow": "2px 2px 0 #000"
    }
  },
  {
    "id": "speed_demon",
    "name": "Speed Demon Coral",
    "category": "viral_shorts",
    "category_label": "Viral Shorts",
    "description": "Fiery coral orange pop for high-velocity talking head reels.",
    "font": "Arial Black",
    "fallback_font": "Impact",
    "fontsize": 50,
    "primary_color": "&H00F0F0F0",
    "active_color": "&H003366FF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.0,
    "shadow": 2.0,
    "alignment": 2,
    "margin_v": 80,
    "uppercase": true,
    "animation_type": "bounce_pop",
    "preview_class": "preview-speed-demon",
    "preview_html": "ULTRA <span class=\"act\">FAST</span> PACED",
    "css": {
      "fontFamily": "Arial Black, sans-serif",
      "color": "#f8fafc",
      "activeColor": "#ff6b4a",
      "textTransform": "uppercase",
      "textShadow": "2px 2px 0 #000"
    }
  },
  {
    "id": "reel_zoomer",
    "name": "Reel Zoomer Cyan",
    "category": "viral_shorts",
    "category_label": "Viral Shorts",
    "description": "Dynamic cyan active pop with subtle scale zoom for Reels and TikTok.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 50,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H00FFFF00",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.0,
    "shadow": 2.0,
    "alignment": 2,
    "margin_v": 78,
    "uppercase": true,
    "animation_type": "bounce_pop",
    "preview_class": "preview-reel-zoomer",
    "preview_html": "SMASH <span class=\"act\">THAT</span> FOLLOW",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#ffffff",
      "activeColor": "#06b6d4",
      "textTransform": "uppercase",
      "textShadow": "2px 2px 0 #000"
    }
  },
  {
    "id": "trendsetter_red",
    "name": "Trendsetter Crimson",
    "category": "viral_shorts",
    "category_label": "Viral Shorts",
    "description": "Deep crimson pop highlight that commands immediate viewer focus.",
    "font": "Arial Black",
    "fallback_font": "Arial",
    "fontsize": 48,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H002A2AFF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.2,
    "shadow": 2.2,
    "alignment": 2,
    "margin_v": 80,
    "uppercase": true,
    "animation_type": "karaoke_highlight",
    "preview_class": "preview-trend-red",
    "preview_html": "SECRET <span class=\"act\">HACK</span> REVEALED",
    "css": {
      "fontFamily": "Arial Black, sans-serif",
      "color": "#ffffff",
      "activeColor": "#ef4444",
      "textTransform": "uppercase",
      "textShadow": "2px 2px 0 #000"
    }
  },
  {
    "id": "karaoke_gold",
    "name": "Karaoke Golden Fill",
    "category": "viral_shorts",
    "category_label": "Viral Shorts",
    "description": "Dim text fills with brilliant gold word-by-word as spoken.",
    "font": "Arial Black",
    "fallback_font": "Arial",
    "fontsize": 46,
    "primary_color": "&H88CCCCCC",
    "active_color": "&H0000C8FF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 3.5,
    "shadow": 2.0,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": false,
    "animation_type": "karaoke_highlight",
    "preview_class": "preview-gold",
    "preview_html": "Vibrant <span class=\"act\">golden</span> speech",
    "css": {
      "fontFamily": "Arial Black, sans-serif",
      "color": "#94a3b8",
      "activeColor": "#f59e0b",
      "textShadow": "2px 2px 0 #000"
    }
  },
  {
    "id": "hormozi_bold",
    "name": "Hormozi Kinetic",
    "category": "hormozi",
    "category_label": "Hormozi",
    "description": "Bold all-caps with bright yellow active-word highlight and heavy black stroke. Viral shorts/reels style.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 52,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0000FFFF",
    "outline_color": "&H00000000",
    "back_color": "&H80000000",
    "bold": 1,
    "outline": 4.5,
    "shadow": 2.5,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "karaoke_highlight",
    "preview_class": "preview-hormozi",
    "preview_html": "READY TO <span class=\"act\">DOMINATE</span> SOCIAL",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#ffffff",
      "activeColor": "#ffe600",
      "textTransform": "uppercase",
      "textShadow": "-2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000"
    }
  },
  {
    "id": "hormozi_lime",
    "name": "Hormozi Lime Retention",
    "category": "hormozi",
    "category_label": "Hormozi",
    "description": "Signature Hormozi heavy typography with electric lime active highlight.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 52,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0000FF00",
    "outline_color": "&H00000000",
    "back_color": "&H80000000",
    "bold": 1,
    "outline": 4.5,
    "shadow": 2.5,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "karaoke_highlight",
    "preview_class": "preview-hormozi-lime",
    "preview_html": "SCALE TO <span class=\"act\">ONE MILLION</span> FAST",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#ffffff",
      "activeColor": "#22c55e",
      "textTransform": "uppercase",
      "textShadow": "-2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000"
    }
  },
  {
    "id": "hormozi_gold",
    "name": "Gold Beast Retention",
    "category": "hormozi",
    "category_label": "Hormozi",
    "description": "Massive Impact letters with luxury gold highlight for business & wealth content.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 52,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0000D7FF",
    "outline_color": "&H00000000",
    "back_color": "&H80000000",
    "bold": 1,
    "outline": 4.8,
    "shadow": 2.8,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "karaoke_highlight",
    "preview_class": "preview-hormozi-gold",
    "preview_html": "THE 100M <span class=\"act\">OFFER</span> PLAYBOOK",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#ffffff",
      "activeColor": "#f59e0b",
      "textTransform": "uppercase",
      "textShadow": "-2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000"
    }
  },
  {
    "id": "hormozi_cyan",
    "name": "Cyan Striker Retention",
    "category": "hormozi",
    "category_label": "Hormozi",
    "description": "Vivid cyan active word on dark background with heavy black outline.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 52,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H00FFFF00",
    "outline_color": "&H00000000",
    "back_color": "&H80000000",
    "bold": 1,
    "outline": 4.5,
    "shadow": 2.5,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "karaoke_highlight",
    "preview_class": "preview-hormozi-cyan",
    "preview_html": "NEVER <span class=\"act\">GIVE UP</span> ON IT",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#ffffff",
      "activeColor": "#06b6d4",
      "textTransform": "uppercase",
      "textShadow": "-2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000"
    }
  },
  {
    "id": "hormozi_red",
    "name": "Millionaire Crimson",
    "category": "hormozi",
    "category_label": "Hormozi",
    "description": "Aggressive red active word pop for hard-hitting business statements.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 52,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H000000FF",
    "outline_color": "&H00000000",
    "back_color": "&H80000000",
    "bold": 1,
    "outline": 4.5,
    "shadow": 2.5,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "karaoke_highlight",
    "preview_class": "preview-hormozi-red",
    "preview_html": "THIS IS <span class=\"act\">THE BIGGEST</span> MISTAKE",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#ffffff",
      "activeColor": "#ef4444",
      "textTransform": "uppercase",
      "textShadow": "-2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000"
    }
  },
  {
    "id": "hormozi_white_black",
    "name": "Monochrome Heavy Punch",
    "category": "hormozi",
    "category_label": "Hormozi",
    "description": "Pure high-contrast black and white typography with extreme outline weight.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 54,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H00FFFFFF",
    "outline_color": "&H00000000",
    "back_color": "&H80000000",
    "bold": 1,
    "outline": 5.0,
    "shadow": 3.0,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "bounce_pop",
    "preview_class": "preview-monochrome-punch",
    "preview_html": "TOTAL <span class=\"act\">CLARITY</span> WINS",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#ffffff",
      "activeColor": "#ffffff",
      "textTransform": "uppercase",
      "textShadow": "-3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000, 3px 3px 0 #000"
    }
  },
  {
    "id": "hormozi_orange",
    "name": "Hyper Growth Orange",
    "category": "hormozi",
    "category_label": "Hormozi",
    "description": "Warm flame orange highlight for energy and high conversion.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 52,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0000A5FF",
    "outline_color": "&H00000000",
    "back_color": "&H80000000",
    "bold": 1,
    "outline": 4.5,
    "shadow": 2.5,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "karaoke_highlight",
    "preview_class": "preview-hormozi-orange",
    "preview_html": "MAKE YOUR <span class=\"act\">BUSINESS</span> SCALE",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#ffffff",
      "activeColor": "#f97316",
      "textTransform": "uppercase",
      "textShadow": "-2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000"
    }
  },
  {
    "id": "hormozi_electric",
    "name": "Electric Titan Blue",
    "category": "hormozi",
    "category_label": "Hormozi",
    "description": "Bold sapphire blue active highlight with maximum presence.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 52,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H00FF9600",
    "outline_color": "&H00000000",
    "back_color": "&H80000000",
    "bold": 1,
    "outline": 4.5,
    "shadow": 2.5,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "bounce_pop",
    "preview_class": "preview-hormozi-electric",
    "preview_html": "BUILD AN <span class=\"act\">EMPIRE</span> TODAY",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#ffffff",
      "activeColor": "#3b82f6",
      "textTransform": "uppercase",
      "textShadow": "-2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000"
    }
  },
  {
    "id": "neon_glow",
    "name": "Neon Cyber Glow",
    "category": "neon_glow",
    "category_label": "Neon Cyber",
    "description": "Futuristic cyan & magenta glowing caption text. Ideal for tech, dark backgrounds, and gaming.",
    "font": "Trebuchet MS",
    "fallback_font": "Arial",
    "fontsize": 46,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H00FFFF00",
    "outline_color": "&H00FF00FF",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 3.0,
    "shadow": 4.0,
    "alignment": 2,
    "margin_v": 70,
    "uppercase": false,
    "animation_type": "glow_highlight",
    "preview_class": "preview-neon",
    "preview_html": "FUTURE <span class=\"act\">CYBER</span> GLOW",
    "css": {
      "fontFamily": "Trebuchet MS, sans-serif",
      "fontWeight": "bold",
      "color": "#ffffff",
      "activeColor": "#22d3ee",
      "textShadow": "0 0 8px #06b6d4, 0 0 14px #a855f7"
    }
  },
  {
    "id": "neon_purple",
    "name": "Electric Purple Glow",
    "category": "neon_glow",
    "category_label": "Neon Cyber",
    "description": "Deep electric violet glow for gaming, music, and nocturnal aesthetics.",
    "font": "Arial Black",
    "fallback_font": "Arial",
    "fontsize": 46,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H00FF32B4",
    "outline_color": "&H00330033",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 3.2,
    "shadow": 4.5,
    "alignment": 2,
    "margin_v": 72,
    "uppercase": true,
    "animation_type": "glow_highlight",
    "preview_class": "preview-neon-purple",
    "preview_html": "DEEP <span class=\"act\">VIOLET</span> PULSE",
    "css": {
      "fontFamily": "Arial Black, sans-serif",
      "color": "#ffffff",
      "activeColor": "#c084fc",
      "textTransform": "uppercase",
      "textShadow": "0 0 10px #a855f7, 0 0 20px #7e22ce"
    }
  },
  {
    "id": "neon_pink",
    "name": "Hot Magenta Neon",
    "category": "neon_glow",
    "category_label": "Neon Cyber",
    "description": "High-intensity hot pink neon with soft magenta radiance.",
    "font": "Trebuchet MS",
    "fallback_font": "Arial",
    "fontsize": 46,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H00CC00FF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 3.0,
    "shadow": 4.0,
    "alignment": 2,
    "margin_v": 70,
    "uppercase": true,
    "animation_type": "glow_highlight",
    "preview_class": "preview-neon-pink",
    "preview_html": "HOT <span class=\"act\">MAGENTA</span> NIGHTS",
    "css": {
      "fontFamily": "Trebuchet MS, sans-serif",
      "fontWeight": "bold",
      "color": "#ffffff",
      "activeColor": "#f43f5e",
      "textTransform": "uppercase",
      "textShadow": "0 0 10px #f43f5e, 0 0 20px #e11d48"
    }
  },
  {
    "id": "neon_acid",
    "name": "Acid Matrix Green",
    "category": "neon_glow",
    "category_label": "Neon Cyber",
    "description": "Terminal matrix phosphor green glow for tech and coding tutorials.",
    "font": "Courier New",
    "fallback_font": "Arial",
    "fontsize": 44,
    "primary_color": "&H0000FF00",
    "active_color": "&H00FFFFFF",
    "outline_color": "&H00003300",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 2.5,
    "shadow": 4.0,
    "alignment": 2,
    "margin_v": 70,
    "uppercase": false,
    "animation_type": "glow_highlight",
    "preview_class": "preview-neon-acid",
    "preview_html": "$ <span class=\"act\">ACCESS</span>_GRANTED",
    "css": {
      "fontFamily": "Courier New, monospace",
      "fontWeight": "bold",
      "color": "#22c55e",
      "activeColor": "#ffffff",
      "textShadow": "0 0 8px #22c55e, 0 0 16px #15803d"
    }
  },
  {
    "id": "neon_ice_blue",
    "name": "Ice Laser Blue",
    "category": "neon_glow",
    "category_label": "Neon Cyber",
    "description": "Crisp arctic ice laser glow for high-tech and sleek video aesthetics.",
    "font": "Segoe UI",
    "fallback_font": "Arial",
    "fontsize": 45,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H00FFFF00",
    "outline_color": "&H00663300",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 2.8,
    "shadow": 4.0,
    "alignment": 2,
    "margin_v": 72,
    "uppercase": false,
    "animation_type": "glow_highlight",
    "preview_class": "preview-ice-blue",
    "preview_html": "Glacial <span class=\"act\">ice laser</span> precision",
    "css": {
      "fontFamily": "Segoe UI, sans-serif",
      "fontWeight": "bold",
      "color": "#ffffff",
      "activeColor": "#38bdf8",
      "textShadow": "0 0 10px #38bdf8, 0 0 20px #0284c7"
    }
  },
  {
    "id": "neon_tokyo",
    "name": "Tokyo Sunset Violet",
    "category": "neon_glow",
    "category_label": "Neon Cyber",
    "description": "Shinjuku neon nightlife aesthetic with dual violet and warm amber glow.",
    "font": "Trebuchet MS",
    "fallback_font": "Arial",
    "fontsize": 46,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0000D7FF",
    "outline_color": "&H00800080",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 3.2,
    "shadow": 4.0,
    "alignment": 2,
    "margin_v": 70,
    "uppercase": true,
    "animation_type": "glow_highlight",
    "preview_class": "preview-neon-tokyo",
    "preview_html": "TOKYO <span class=\"act\">MIDNIGHT</span> RUN",
    "css": {
      "fontFamily": "Trebuchet MS, sans-serif",
      "fontWeight": "bold",
      "color": "#ffffff",
      "activeColor": "#fbbf24",
      "textTransform": "uppercase",
      "textShadow": "0 0 10px #c084fc, 0 0 20px #d946ef"
    }
  },
  {
    "id": "neon_toxic",
    "name": "Toxic Amber Glow",
    "category": "neon_glow",
    "category_label": "Neon Cyber",
    "description": "Radioactive neon yellow-amber glow for high-adrenaline clips.",
    "font": "Arial Black",
    "fallback_font": "Impact",
    "fontsize": 48,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0000E6FF",
    "outline_color": "&H00002233",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 3.5,
    "shadow": 4.2,
    "alignment": 2,
    "margin_v": 74,
    "uppercase": true,
    "animation_type": "glow_highlight",
    "preview_class": "preview-toxic-amber",
    "preview_html": "DANGER <span class=\"act\">TOXIC</span> ZONE",
    "css": {
      "fontFamily": "Arial Black, sans-serif",
      "color": "#ffffff",
      "activeColor": "#facc15",
      "textTransform": "uppercase",
      "textShadow": "0 0 10px #eab308, 0 0 22px #ca8a04"
    }
  },
  {
    "id": "neon_synthwave",
    "name": "Synthwave Horizon",
    "category": "neon_glow",
    "category_label": "Neon Cyber",
    "description": "80s retro outrun synthwave style with neon cyan and pink highlights.",
    "font": "Trebuchet MS",
    "fallback_font": "Arial",
    "fontsize": 46,
    "primary_color": "&H00FFFF00",
    "active_color": "&H00FF00FF",
    "outline_color": "&H00330033",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 3.0,
    "shadow": 4.0,
    "alignment": 2,
    "margin_v": 72,
    "uppercase": true,
    "animation_type": "glow_highlight",
    "preview_class": "preview-synthwave",
    "preview_html": "OUTRUN <span class=\"act\">THE SUN</span> 1984",
    "css": {
      "fontFamily": "Trebuchet MS, sans-serif",
      "fontWeight": "bold",
      "color": "#22d3ee",
      "activeColor": "#f43f5e",
      "textTransform": "uppercase",
      "textShadow": "0 0 10px #f43f5e, 0 0 20px #06b6d4"
    }
  },
  {
    "id": "minimalist_modern",
    "name": "Minimalist Documentary",
    "category": "cinematic",
    "category_label": "Cinematic",
    "description": "Clean, elegant lower-third subtitle bar with soft translucent backing. YouTube essays and interviews.",
    "font": "Arial",
    "fallback_font": "Helvetica",
    "fontsize": 38,
    "primary_color": "&H00F1F5F9",
    "active_color": "&H0038BDF8",
    "outline_color": "&H000F172A",
    "back_color": "&H88000000",
    "bold": 0,
    "outline": 1.5,
    "shadow": 1.0,
    "alignment": 2,
    "margin_v": 60,
    "uppercase": false,
    "animation_type": "clean_karaoke",
    "preview_class": "preview-minimal",
    "preview_html": "Clean <span class=\"act\">documentary</span> essay",
    "css": {
      "fontFamily": "Arial, sans-serif",
      "color": "#cbd5e1",
      "activeColor": "#38bdf8",
      "background": "rgba(0, 0, 0, 0.7)",
      "padding": "4px 10px",
      "borderRadius": "4px"
    }
  },
  {
    "id": "film_slate",
    "name": "35mm Film Slate",
    "category": "cinematic",
    "category_label": "Cinematic",
    "description": "Crisp white cinema lettering with subtle letter-spacing for feature films and trailers.",
    "font": "Arial",
    "fallback_font": "Helvetica",
    "fontsize": 36,
    "primary_color": "&H00F8FAFC",
    "active_color": "&H00FFFFFF",
    "outline_color": "&H00000000",
    "back_color": "&H40000000",
    "bold": 1,
    "outline": 2.0,
    "shadow": 1.5,
    "alignment": 2,
    "margin_v": 58,
    "uppercase": false,
    "animation_type": "standard_phrase",
    "preview_class": "preview-film-slate",
    "preview_html": "The truth behind <span class=\"act\">the story</span> unfolds",
    "css": {
      "fontFamily": "Arial, sans-serif",
      "fontWeight": "bold",
      "color": "#f8fafc",
      "activeColor": "#ffffff",
      "letterSpacing": "1px",
      "textShadow": "1px 1px 2px #000"
    }
  },
  {
    "id": "noir_editorial",
    "name": "Film Noir Monochrome",
    "category": "cinematic",
    "category_label": "Cinematic",
    "description": "High contrast black-and-white elegance for dramatic narratives and deep commentary.",
    "font": "Georgia",
    "fallback_font": "Times New Roman",
    "fontsize": 38,
    "primary_color": "&H00E2E8F0",
    "active_color": "&H00FFFFFF",
    "outline_color": "&H00000000",
    "back_color": "&H90000000",
    "bold": 0,
    "outline": 1.8,
    "shadow": 2.0,
    "alignment": 2,
    "margin_v": 62,
    "uppercase": false,
    "animation_type": "clean_karaoke",
    "preview_class": "preview-noir",
    "preview_html": "Shadows in the <span class=\"act\">dark alleyway</span>",
    "css": {
      "fontFamily": "Georgia, serif",
      "fontStyle": "italic",
      "color": "#e2e8f0",
      "activeColor": "#ffffff",
      "textShadow": "2px 2px 3px #000"
    }
  },
  {
    "id": "editorial_serif",
    "name": "Editorial Serif Elegance",
    "category": "cinematic",
    "category_label": "Cinematic",
    "description": "Refined classic serif typography for video essays and historical deep dives.",
    "font": "Georgia",
    "fallback_font": "Times New Roman",
    "fontsize": 40,
    "primary_color": "&H00F1F5F9",
    "active_color": "&H0060A5FA",
    "outline_color": "&H000F172A",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 2.2,
    "shadow": 1.8,
    "alignment": 2,
    "margin_v": 64,
    "uppercase": false,
    "animation_type": "clean_karaoke",
    "preview_class": "preview-editorial-serif",
    "preview_html": "A timeless <span class=\"act\">editorial</span> perspective",
    "css": {
      "fontFamily": "Georgia, serif",
      "fontWeight": "bold",
      "color": "#f1f5f9",
      "activeColor": "#60a5fa",
      "textShadow": "1px 1px 2px #0f172a"
    }
  },
  {
    "id": "masterclass_sub",
    "name": "Masterclass Studio White",
    "category": "cinematic",
    "category_label": "Cinematic",
    "description": "Sleek, high-production corporate studio subtitles inspired by MasterClass videos.",
    "font": "Segoe UI",
    "fallback_font": "Arial",
    "fontsize": 38,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H00F8FAFC",
    "outline_color": "&H001E293B",
    "back_color": "&H70000000",
    "bold": 1,
    "outline": 2.0,
    "shadow": 1.2,
    "alignment": 2,
    "margin_v": 60,
    "uppercase": false,
    "animation_type": "clean_karaoke",
    "preview_class": "preview-masterclass",
    "preview_html": "Mastering the craft of <span class=\"act\">filmmaking</span>",
    "css": {
      "fontFamily": "Segoe UI, sans-serif",
      "fontWeight": "600",
      "color": "#ffffff",
      "activeColor": "#ffffff",
      "background": "rgba(15, 23, 42, 0.75)",
      "padding": "4px 12px",
      "borderRadius": "4px"
    }
  },
  {
    "id": "cinematic_gold",
    "name": "A24 Warm Amber",
    "category": "cinematic",
    "category_label": "Cinematic",
    "description": "Warm muted amber tone for indie films, atmospheric cinema, and moody vlogs.",
    "font": "Arial",
    "fallback_font": "Helvetica",
    "fontsize": 38,
    "primary_color": "&H00D0E0E8",
    "active_color": "&H0020C0FF",
    "outline_color": "&H00000000",
    "back_color": "&H60000000",
    "bold": 1,
    "outline": 2.2,
    "shadow": 1.5,
    "alignment": 2,
    "margin_v": 60,
    "uppercase": false,
    "animation_type": "clean_karaoke",
    "preview_class": "preview-cinematic-gold",
    "preview_html": "A poetic vision of <span class=\"act\">golden light</span>",
    "css": {
      "fontFamily": "Arial, sans-serif",
      "fontWeight": "600",
      "color": "#e2e8f0",
      "activeColor": "#fbbf24",
      "textShadow": "1px 1px 3px #000"
    }
  },
  {
    "id": "horizon_bar",
    "name": "Horizon Translucent Plate",
    "category": "cinematic",
    "category_label": "Cinematic",
    "description": "Full-width soft frosted bottom banner for flawless reading over busy camera pans.",
    "font": "Arial",
    "fallback_font": "Helvetica",
    "fontsize": 36,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0038BDF8",
    "outline_color": "&H00000000",
    "back_color": "&HAA101010",
    "bold": 0,
    "border_style": 3,
    "outline": 2.0,
    "shadow": 0.0,
    "alignment": 2,
    "margin_v": 55,
    "uppercase": false,
    "animation_type": "clean_karaoke",
    "preview_class": "preview-horizon-bar",
    "preview_html": "Across the vast <span class=\"act\">ocean horizon</span>",
    "css": {
      "fontFamily": "Arial, sans-serif",
      "color": "#ffffff",
      "activeColor": "#38bdf8",
      "background": "rgba(16, 16, 16, 0.8)",
      "padding": "5px 14px",
      "borderRadius": "2px"
    }
  },
  {
    "id": "nordic_frost",
    "name": "Nordic Frosted Minimal",
    "category": "cinematic",
    "category_label": "Cinematic",
    "description": "Cool slate grey inactive text with pure crisp white active reveal.",
    "font": "Segoe UI",
    "fallback_font": "Arial",
    "fontsize": 38,
    "primary_color": "&H0094A3B8",
    "active_color": "&H00FFFFFF",
    "outline_color": "&H000F172A",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 2.0,
    "shadow": 1.5,
    "alignment": 2,
    "margin_v": 62,
    "uppercase": false,
    "animation_type": "clean_karaoke",
    "preview_class": "preview-nordic",
    "preview_html": "Quiet reflections in the <span class=\"act\">winter stillness</span>",
    "css": {
      "fontFamily": "Segoe UI, sans-serif",
      "fontWeight": "bold",
      "color": "#94a3b8",
      "activeColor": "#ffffff",
      "textShadow": "1px 1px 2px #0f172a"
    }
  },
  {
    "id": "boxed_pill",
    "name": "Boxed Pill Tag",
    "category": "boxed_pill",
    "category_label": "Boxed & Pill",
    "description": "Clean rounded orange/dark badge behind active text. High contrast readability on any video background.",
    "font": "Segoe UI",
    "fallback_font": "Arial",
    "fontsize": 42,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0000D7FF",
    "outline_color": "&H00000000",
    "back_color": "&HCC1E1E1E",
    "bold": 1,
    "border_style": 3,
    "outline": 3.0,
    "shadow": 0.0,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": false,
    "animation_type": "box_pill",
    "preview_class": "preview-boxed",
    "preview_html": "HIGH <span class=\"act\">CONTRAST</span> READ",
    "css": {
      "fontFamily": "Segoe UI, sans-serif",
      "fontWeight": "bold",
      "color": "#ffffff",
      "activeColor": "#ffffff",
      "activeBg": "#ea580c"
    }
  },
  {
    "id": "dark_slate_pill",
    "name": "Dark Slate Rounded Pill",
    "category": "boxed_pill",
    "category_label": "Boxed & Pill",
    "description": "Modern rounded dark slate pill backing for clean UI aesthetics.",
    "font": "Arial",
    "fallback_font": "Segoe UI",
    "fontsize": 40,
    "primary_color": "&H00E2E8F0",
    "active_color": "&H0038BDF8",
    "outline_color": "&H00000000",
    "back_color": "&HE01E293B",
    "bold": 1,
    "border_style": 3,
    "outline": 3.0,
    "shadow": 0.0,
    "alignment": 2,
    "margin_v": 72,
    "uppercase": false,
    "animation_type": "box_pill",
    "preview_class": "preview-slate-pill",
    "preview_html": "MODERN <span class=\"act\">SLATE</span> BADGE",
    "css": {
      "fontFamily": "Arial, sans-serif",
      "fontWeight": "bold",
      "color": "#e2e8f0",
      "activeColor": "#ffffff",
      "activeBg": "#0284c7"
    }
  },
  {
    "id": "red_alert_box",
    "name": "Red Alert Tag Pill",
    "category": "boxed_pill",
    "category_label": "Boxed & Pill",
    "description": "High-urgency red badge behind active words, perfect for shocking hooks and facts.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 46,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H000000FF",
    "outline_color": "&H00000000",
    "back_color": "&HCC111827",
    "bold": 1,
    "border_style": 3,
    "outline": 3.2,
    "shadow": 0.0,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "box_pill",
    "preview_class": "preview-red-alert",
    "preview_html": "CRITICAL <span class=\"act\">WARNING</span> NOW",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#ffffff",
      "activeColor": "#ffffff",
      "activeBg": "#dc2626",
      "textTransform": "uppercase"
    }
  },
  {
    "id": "emerald_pill",
    "name": "Emerald Pill Badge",
    "category": "boxed_pill",
    "category_label": "Boxed & Pill",
    "description": "Vibrant emerald green active word badge for finance, eco, and success topics.",
    "font": "Segoe UI",
    "fallback_font": "Arial",
    "fontsize": 42,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0014FF39",
    "outline_color": "&H00000000",
    "back_color": "&HCC0F172A",
    "bold": 1,
    "border_style": 3,
    "outline": 3.0,
    "shadow": 0.0,
    "alignment": 2,
    "margin_v": 74,
    "uppercase": false,
    "animation_type": "box_pill",
    "preview_class": "preview-emerald-pill",
    "preview_html": "PROVEN <span class=\"act\">GROWTH</span> FORMULA",
    "css": {
      "fontFamily": "Segoe UI, sans-serif",
      "fontWeight": "bold",
      "color": "#ffffff",
      "activeColor": "#ffffff",
      "activeBg": "#059669"
    }
  },
  {
    "id": "purple_glow_box",
    "name": "Electric Violet Box",
    "category": "boxed_pill",
    "category_label": "Boxed & Pill",
    "description": "Violet pill badge with bright white active lettering for lifestyle and AI creators.",
    "font": "Trebuchet MS",
    "fallback_font": "Arial",
    "fontsize": 44,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H00FF32B4",
    "outline_color": "&H00000000",
    "back_color": "&HCC1E1B4B",
    "bold": 1,
    "border_style": 3,
    "outline": 3.0,
    "shadow": 0.0,
    "alignment": 2,
    "margin_v": 74,
    "uppercase": true,
    "animation_type": "box_pill",
    "preview_class": "preview-violet-box",
    "preview_html": "NEXT GEN <span class=\"act\">CREATIVE</span> AI",
    "css": {
      "fontFamily": "Trebuchet MS, sans-serif",
      "fontWeight": "bold",
      "color": "#ffffff",
      "activeColor": "#ffffff",
      "activeBg": "#7c3aed",
      "textTransform": "uppercase"
    }
  },
  {
    "id": "sunset_pill",
    "name": "Sunset Gradient Pill",
    "category": "boxed_pill",
    "category_label": "Boxed & Pill",
    "description": "Warm coral-sunset boxed tag that pops softly on both bright and dark frames.",
    "font": "Arial",
    "fallback_font": "Segoe UI",
    "fontsize": 42,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H002080FF",
    "outline_color": "&H00000000",
    "back_color": "&HCC18181B",
    "bold": 1,
    "border_style": 3,
    "outline": 3.0,
    "shadow": 0.0,
    "alignment": 2,
    "margin_v": 72,
    "uppercase": false,
    "animation_type": "box_pill",
    "preview_class": "preview-sunset-pill",
    "preview_html": "Golden hour <span class=\"act\">sunset</span> vibes",
    "css": {
      "fontFamily": "Arial, sans-serif",
      "fontWeight": "bold",
      "color": "#ffffff",
      "activeColor": "#ffffff",
      "activeBg": "#f97316"
    }
  },
  {
    "id": "royal_blue_badge",
    "name": "Royal Blue Clean Badge",
    "category": "boxed_pill",
    "category_label": "Boxed & Pill",
    "description": "Deep corporate royal blue pill badge with white typography.",
    "font": "Segoe UI",
    "fallback_font": "Arial",
    "fontsize": 40,
    "primary_color": "&H00F8FAFC",
    "active_color": "&H00FF8000",
    "outline_color": "&H00000000",
    "back_color": "&HCC0F172A",
    "bold": 1,
    "border_style": 3,
    "outline": 2.8,
    "shadow": 0.0,
    "alignment": 2,
    "margin_v": 70,
    "uppercase": false,
    "animation_type": "box_pill",
    "preview_class": "preview-royal-blue",
    "preview_html": "Trusted by <span class=\"act\">industry leaders</span>",
    "css": {
      "fontFamily": "Segoe UI, sans-serif",
      "fontWeight": "bold",
      "color": "#ffffff",
      "activeColor": "#ffffff",
      "activeBg": "#1d4ed8"
    }
  },
  {
    "id": "high_vis_amber",
    "name": "High-Vis Amber Pill",
    "category": "boxed_pill",
    "category_label": "Boxed & Pill",
    "description": "High-visibility industrial black pill with pure vibrant amber active text.",
    "font": "Arial Black",
    "fallback_font": "Impact",
    "fontsize": 44,
    "primary_color": "&H00E2E8F0",
    "active_color": "&H0000D7FF",
    "outline_color": "&H00000000",
    "back_color": "&HEE000000",
    "bold": 1,
    "border_style": 3,
    "outline": 3.2,
    "shadow": 0.0,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "box_pill",
    "preview_class": "preview-vis-amber",
    "preview_html": "ATTENTION <span class=\"act\">HIGH VALUE</span> STEP",
    "css": {
      "fontFamily": "Arial Black, sans-serif",
      "color": "#ffffff",
      "activeColor": "#000000",
      "activeBg": "#fbbf24",
      "textTransform": "uppercase"
    }
  },
  {
    "id": "headline_3d_punch",
    "name": "3D Punch Out Headline",
    "category": "headline",
    "category_label": "Headline",
    "description": "Heavy 3D extruded drop shadow giving physical weight to every word.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 54,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0000E6FF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.5,
    "shadow": 4.5,
    "alignment": 2,
    "margin_v": 76,
    "uppercase": true,
    "animation_type": "bounce_pop",
    "preview_class": "preview-3d-punch",
    "preview_html": "MASSIVE <span class=\"act\">3D PUNCH</span> IMPACT",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#ffffff",
      "activeColor": "#facc15",
      "textTransform": "uppercase",
      "textShadow": "3px 3px 0 #000, 6px 6px 0 rgba(0,0,0,0.6)"
    }
  },
  {
    "id": "headline_angled",
    "name": "Angled Action Banner",
    "category": "headline",
    "category_label": "Headline",
    "description": "Slightly skewed high-velocity sports and action headline typography.",
    "font": "Arial Black",
    "fallback_font": "Impact",
    "fontsize": 50,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0000FF00",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.0,
    "shadow": 3.0,
    "alignment": 2,
    "margin_v": 78,
    "uppercase": true,
    "animation_type": "bounce_pop",
    "preview_class": "preview-angled",
    "preview_html": "EXPLOSIVE <span class=\"act\">ACTION</span> SPEED",
    "css": {
      "fontFamily": "Arial Black, sans-serif",
      "fontStyle": "italic",
      "color": "#ffffff",
      "activeColor": "#22c55e",
      "textTransform": "uppercase",
      "textShadow": "3px 3px 0 #000"
    }
  },
  {
    "id": "headline_big_impact",
    "name": "Big Impact Heavyweight",
    "category": "headline",
    "category_label": "Headline",
    "description": "Ultra-thick, condensed heavyweight letters for dramatic YouTube titles.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 56,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0000FFFF",
    "outline_color": "&H00000000",
    "back_color": "&H90000000",
    "bold": 1,
    "outline": 5.0,
    "shadow": 3.0,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "scale_pulse",
    "preview_class": "preview-big-impact",
    "preview_html": "THE BIGGEST <span class=\"act\">SECRET</span> EVER",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#ffffff",
      "activeColor": "#facc15",
      "textTransform": "uppercase",
      "textShadow": "-3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000, 3px 3px 0 #000"
    }
  },
  {
    "id": "headline_blackout",
    "name": "Blackout Inverted Punch",
    "category": "headline",
    "category_label": "Headline",
    "description": "Inverted black typography with heavy yellow and white strokes.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 52,
    "primary_color": "&H00000000",
    "active_color": "&H0000FFFF",
    "outline_color": "&H00FFFFFF",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.5,
    "shadow": 3.0,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "bounce_pop",
    "preview_class": "preview-blackout",
    "preview_html": "INVERTED <span class=\"act\">BLACKOUT</span> PUNCH",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#000000",
      "activeColor": "#ffe600",
      "textTransform": "uppercase",
      "textShadow": "-2px -2px 0 #fff, 2px -2px 0 #fff, -2px 2px 0 #fff, 2px 2px 0 #fff"
    }
  },
  {
    "id": "headline_thunder",
    "name": "Thunder Yellow Stroke",
    "category": "headline",
    "category_label": "Headline",
    "description": "High-voltage lightning yellow stroke with dark midnight blue body.",
    "font": "Arial Black",
    "fallback_font": "Impact",
    "fontsize": 50,
    "primary_color": "&H00201005",
    "active_color": "&H0000E6FF",
    "outline_color": "&H0000D7FF",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.0,
    "shadow": 3.0,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "scale_pulse",
    "preview_class": "preview-thunder",
    "preview_html": "THUNDER <span class=\"act\">STRIKE</span> POWER",
    "css": {
      "fontFamily": "Arial Black, sans-serif",
      "color": "#0f172a",
      "activeColor": "#fbbf24",
      "textTransform": "uppercase",
      "textShadow": "-2px -2px 0 #facc15, 2px -2px 0 #facc15"
    }
  },
  {
    "id": "headline_heavy_metal",
    "name": "Heavy Metal Chrome",
    "category": "headline",
    "category_label": "Headline",
    "description": "Chiseled metallic chrome with sharp black bevel shadow.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 52,
    "primary_color": "&H00E2E8F0",
    "active_color": "&H00FFFFFF",
    "outline_color": "&H00000000",
    "back_color": "&H80000000",
    "bold": 1,
    "outline": 4.5,
    "shadow": 3.5,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "bounce_pop",
    "preview_class": "preview-heavy-metal",
    "preview_html": "RAW <span class=\"act\">UNSTOPPABLE</span> FORCE",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#e2e8f0",
      "activeColor": "#ffffff",
      "textTransform": "uppercase",
      "textShadow": "3px 3px 0 #000, 5px 5px 0 #475569"
    }
  },
  {
    "id": "headline_stencil",
    "name": "Military Bold Stencil",
    "category": "headline",
    "category_label": "Headline",
    "description": "Tactical military-grade stencil aesthetic for survival and outdoor content.",
    "font": "Arial Black",
    "fallback_font": "Trebuchet MS",
    "fontsize": 48,
    "primary_color": "&H00D9E2EC",
    "active_color": "&H0010E030",
    "outline_color": "&H000F1710",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 3.8,
    "shadow": 2.5,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "karaoke_highlight",
    "preview_class": "preview-stencil",
    "preview_html": "TACTICAL <span class=\"act\">SURVIVAL</span> GEAR",
    "css": {
      "fontFamily": "Arial Black, sans-serif",
      "letterSpacing": "2px",
      "color": "#cbd5e1",
      "activeColor": "#4ade80",
      "textTransform": "uppercase",
      "textShadow": "2px 2px 0 #0f172a"
    }
  },
  {
    "id": "headline_iron",
    "name": "Iron Titan Display",
    "category": "headline",
    "category_label": "Headline",
    "description": "Solid, grounded heavy headline typography for motivational edits.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 54,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0000A5FF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.5,
    "shadow": 2.8,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "scale_pulse",
    "preview_class": "preview-iron-titan",
    "preview_html": "FORGED IN <span class=\"act\">IRON</span> DISCIPLINE",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#ffffff",
      "activeColor": "#f97316",
      "textTransform": "uppercase",
      "textShadow": "-2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000"
    }
  },
  {
    "id": "comic_pop",
    "name": "Comic Pop Playful",
    "category": "comic_pop",
    "category_label": "Comic Pop",
    "description": "Playful, bold, high-contrast comic aesthetic with 3D shadow depth. Great for storytelling & kids content.",
    "font": "Trebuchet MS",
    "fallback_font": "Arial Black",
    "fontsize": 48,
    "primary_color": "&H0000FFFF",
    "active_color": "&H00FF33FF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 5.0,
    "shadow": 4.0,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "bounce_pop",
    "preview_class": "preview-comic",
    "preview_html": "PLAYFUL <span class=\"act\">COMIC</span> FUN",
    "css": {
      "fontFamily": "Trebuchet MS, cursive",
      "fontWeight": "bold",
      "color": "#facc15",
      "activeColor": "#ec4899",
      "textTransform": "uppercase",
      "textShadow": "2px 2px 0 #ec4899, 4px 4px 0 #000"
    }
  },
  {
    "id": "bubble_pink",
    "name": "Bubblegum Pink Pop",
    "category": "comic_pop",
    "category_label": "Comic Pop",
    "description": "Sweet bubblegum pink with cyan drop shadow for fun vlog edits.",
    "font": "Arial Black",
    "fallback_font": "Trebuchet MS",
    "fontsize": 46,
    "primary_color": "&H00FF80DF",
    "active_color": "&H00FFFFFF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.0,
    "shadow": 3.5,
    "alignment": 2,
    "margin_v": 74,
    "uppercase": true,
    "animation_type": "bounce_pop",
    "preview_class": "preview-bubble-pink",
    "preview_html": "SWEET <span class=\"act\">BUBBLEGUM</span> POP",
    "css": {
      "fontFamily": "Arial Black, sans-serif",
      "color": "#f472b6",
      "activeColor": "#ffffff",
      "textTransform": "uppercase",
      "textShadow": "2px 2px 0 #06b6d4, 4px 4px 0 #000"
    }
  },
  {
    "id": "arcade_8bit",
    "name": "Arcade Retro 8-Bit",
    "category": "comic_pop",
    "category_label": "Comic Pop",
    "description": "Pixel arcade gaming aesthetic with neon yellow and hot magenta colors.",
    "font": "Trebuchet MS",
    "fallback_font": "Courier New",
    "fontsize": 44,
    "primary_color": "&H0000FF00",
    "active_color": "&H0000FFFF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.0,
    "shadow": 3.0,
    "alignment": 2,
    "margin_v": 70,
    "uppercase": true,
    "animation_type": "bounce_pop",
    "preview_class": "preview-arcade-8bit",
    "preview_html": "PRESS <span class=\"act\">START</span> TO PLAY",
    "css": {
      "fontFamily": "Trebuchet MS, monospace",
      "fontWeight": "bold",
      "color": "#4ade80",
      "activeColor": "#facc15",
      "textTransform": "uppercase",
      "textShadow": "3px 3px 0 #000"
    }
  },
  {
    "id": "cartoon_blast",
    "name": "Cartoon Dynamic Blast",
    "category": "comic_pop",
    "category_label": "Comic Pop",
    "description": "High-bounce comic lettering with energetic color pops.",
    "font": "Impact",
    "fallback_font": "Trebuchet MS",
    "fontsize": 50,
    "primary_color": "&H0000E6FF",
    "active_color": "&H000000FF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.8,
    "shadow": 3.5,
    "alignment": 2,
    "margin_v": 76,
    "uppercase": true,
    "animation_type": "bounce_pop",
    "preview_class": "preview-cartoon-blast",
    "preview_html": "KA-BOOM <span class=\"act\">EXPLOSION</span> NOW",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#facc15",
      "activeColor": "#ef4444",
      "textTransform": "uppercase",
      "textShadow": "2px 2px 0 #ef4444, 4px 4px 0 #000"
    }
  },
  {
    "id": "pop_art_yellow",
    "name": "Pop Art Halftone Yellow",
    "category": "comic_pop",
    "category_label": "Comic Pop",
    "description": "Lichtenstein-inspired vintage pop art yellow with bold black outlines.",
    "font": "Arial Black",
    "fallback_font": "Trebuchet MS",
    "fontsize": 48,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0000E1FF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.5,
    "shadow": 3.2,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "karaoke_highlight",
    "preview_class": "preview-pop-art",
    "preview_html": "VINTAGE <span class=\"act\">POP ART</span> LOOK",
    "css": {
      "fontFamily": "Arial Black, sans-serif",
      "color": "#ffffff",
      "activeColor": "#fbbf24",
      "textTransform": "uppercase",
      "textShadow": "3px 3px 0 #000"
    }
  },
  {
    "id": "comic_kapow",
    "name": "Kapow Action Comic",
    "category": "comic_pop",
    "category_label": "Comic Pop",
    "description": "Superhero action scene font with bright cyan and fiery orange highlights.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 52,
    "primary_color": "&H00FFFF00",
    "active_color": "&H000066FF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.8,
    "shadow": 3.8,
    "alignment": 2,
    "margin_v": 76,
    "uppercase": true,
    "animation_type": "bounce_pop",
    "preview_class": "preview-comic-kapow",
    "preview_html": "KAPOW <span class=\"act\">SUPER</span> PUNCH",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#06b6d4",
      "activeColor": "#f97316",
      "textTransform": "uppercase",
      "textShadow": "2px 2px 0 #000, 4px 4px 0 #f97316"
    }
  },
  {
    "id": "kawaii_lilac",
    "name": "Kawaii Pastel Lilac",
    "category": "comic_pop",
    "category_label": "Comic Pop",
    "description": "Gentle pastel lilac and mint tones for cozy, cute, and aesthetic vlogs.",
    "font": "Trebuchet MS",
    "fallback_font": "Arial",
    "fontsize": 44,
    "primary_color": "&H00F0D0FF",
    "active_color": "&H00C0FFB0",
    "outline_color": "&H00331033",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 3.0,
    "shadow": 2.0,
    "alignment": 2,
    "margin_v": 72,
    "uppercase": false,
    "animation_type": "bounce_pop",
    "preview_class": "preview-kawaii",
    "preview_html": "Super cute <span class=\"act\">cozy vlog</span> vibes",
    "css": {
      "fontFamily": "Trebuchet MS, sans-serif",
      "fontWeight": "bold",
      "color": "#e9d5ff",
      "activeColor": "#86efac",
      "textShadow": "2px 2px 0 #581c87"
    }
  },
  {
    "id": "superhero_red",
    "name": "Superhero Comic Punch",
    "category": "comic_pop",
    "category_label": "Comic Pop",
    "description": "Iconic comic book red letters with golden yellow active glow.",
    "font": "Impact",
    "fallback_font": "Arial Black",
    "fontsize": 52,
    "primary_color": "&H002020FF",
    "active_color": "&H0000FFFF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 4.5,
    "shadow": 3.5,
    "alignment": 2,
    "margin_v": 75,
    "uppercase": true,
    "animation_type": "bounce_pop",
    "preview_class": "preview-superhero-red",
    "preview_html": "MIGHTY <span class=\"act\">HERO</span> RISES",
    "css": {
      "fontFamily": "Impact, sans-serif",
      "color": "#ef4444",
      "activeColor": "#facc15",
      "textTransform": "uppercase",
      "textShadow": "2px 2px 0 #000, 4px 4px 0 #facc15"
    }
  },
  {
    "id": "classic_broadcast",
    "name": "Classic Broadcast",
    "category": "broadcast",
    "category_label": "Broadcast",
    "description": "Standard Netflix / TV crisp white typography with deep black shadow outline. 100% timeless.",
    "font": "Arial",
    "fallback_font": "Helvetica",
    "fontsize": 40,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H00FFFFFF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 3.0,
    "shadow": 2.0,
    "alignment": 2,
    "margin_v": 65,
    "uppercase": false,
    "animation_type": "standard_phrase",
    "preview_class": "preview-broadcast",
    "preview_html": "Standard broadcast clarity",
    "css": {
      "fontFamily": "Arial, sans-serif",
      "fontWeight": "bold",
      "color": "#ffffff",
      "activeColor": "#ffffff",
      "textShadow": "2px 2px 3px #000"
    }
  },
  {
    "id": "netflix_clean",
    "name": "Netflix Standard Subtitle",
    "category": "broadcast",
    "category_label": "Broadcast",
    "description": "Calibrated to Netflix technical subtitle delivery specs for international streaming.",
    "font": "Arial",
    "fallback_font": "Helvetica",
    "fontsize": 38,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H00F1F5F9",
    "outline_color": "&H00000000",
    "back_color": "&H80000000",
    "bold": 0,
    "outline": 2.0,
    "shadow": 1.5,
    "alignment": 2,
    "margin_v": 60,
    "uppercase": false,
    "animation_type": "standard_phrase",
    "preview_class": "preview-netflix",
    "preview_html": "Streaming clarity for all viewers worldwide.",
    "css": {
      "fontFamily": "Arial, sans-serif",
      "color": "#ffffff",
      "activeColor": "#f8fafc",
      "textShadow": "1.5px 1.5px 2px #000"
    }
  },
  {
    "id": "youtube_standard",
    "name": "YouTube CC Crisp",
    "category": "broadcast",
    "category_label": "Broadcast",
    "description": "Standard YouTube closed-captioning typography with black backing strip.",
    "font": "Roboto",
    "fallback_font": "Arial",
    "fontsize": 36,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H00FFFFFF",
    "outline_color": "&H00000000",
    "back_color": "&HE0080808",
    "bold": 0,
    "border_style": 3,
    "outline": 2.0,
    "shadow": 0.0,
    "alignment": 2,
    "margin_v": 60,
    "uppercase": false,
    "animation_type": "standard_phrase",
    "preview_class": "preview-youtube-cc",
    "preview_html": "Official YouTube closed caption format",
    "css": {
      "fontFamily": "Arial, sans-serif",
      "color": "#ffffff",
      "activeColor": "#ffffff",
      "background": "rgba(8, 8, 8, 0.85)",
      "padding": "4px 8px"
    }
  },
  {
    "id": "bbc_crisp",
    "name": "BBC Editorial Subtitle",
    "category": "broadcast",
    "category_label": "Broadcast",
    "description": "High-legibility typography matching BBC news broadcast standard.",
    "font": "Arial",
    "fallback_font": "Helvetica",
    "fontsize": 38,
    "primary_color": "&H0000FFFF",
    "active_color": "&H0000FFFF",
    "outline_color": "&H00000000",
    "back_color": "&H80000000",
    "bold": 1,
    "outline": 2.5,
    "shadow": 1.5,
    "alignment": 2,
    "margin_v": 62,
    "uppercase": false,
    "animation_type": "standard_phrase",
    "preview_class": "preview-bbc",
    "preview_html": "BBC News international broadcast format",
    "css": {
      "fontFamily": "Arial, sans-serif",
      "fontWeight": "bold",
      "color": "#facc15",
      "activeColor": "#facc15",
      "textShadow": "2px 2px 2px #000"
    }
  },
  {
    "id": "corporate_navy",
    "name": "Corporate Clean Navy",
    "category": "broadcast",
    "category_label": "Broadcast",
    "description": "Subtle deep navy and crisp white for enterprise and B2B SaaS presentations.",
    "font": "Segoe UI",
    "fallback_font": "Arial",
    "fontsize": 38,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H0060A5FA",
    "outline_color": "&H000F172A",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 2.2,
    "shadow": 1.5,
    "alignment": 2,
    "margin_v": 65,
    "uppercase": false,
    "animation_type": "clean_karaoke",
    "preview_class": "preview-corp-navy",
    "preview_html": "Enterprise <span class=\"act\">quarterly review</span> metrics",
    "css": {
      "fontFamily": "Segoe UI, sans-serif",
      "fontWeight": "600",
      "color": "#ffffff",
      "activeColor": "#60a5fa",
      "textShadow": "1px 1px 3px #0f172a"
    }
  },
  {
    "id": "ted_speaker",
    "name": "TED Stage Keynote",
    "category": "broadcast",
    "category_label": "Broadcast",
    "description": "Refined sans-serif subtitle for keynote speeches and TED-style ideas.",
    "font": "Helvetica",
    "fallback_font": "Arial",
    "fontsize": 38,
    "primary_color": "&H00F8FAFC",
    "active_color": "&H000000FF",
    "outline_color": "&H00000000",
    "back_color": "&H00000000",
    "bold": 1,
    "outline": 2.2,
    "shadow": 1.5,
    "alignment": 2,
    "margin_v": 62,
    "uppercase": false,
    "animation_type": "clean_karaoke",
    "preview_class": "preview-ted",
    "preview_html": "Ideas worth <span class=\"act\">spreading</span> worldwide",
    "css": {
      "fontFamily": "Arial, sans-serif",
      "fontWeight": "bold",
      "color": "#f8fafc",
      "activeColor": "#ef4444",
      "textShadow": "1px 1px 2px #000"
    }
  },
  {
    "id": "swiss_neutral",
    "name": "Swiss Neutral Typography",
    "category": "broadcast",
    "category_label": "Broadcast",
    "description": "Understated Helvetica Swiss grid typography for architectural and design content.",
    "font": "Arial",
    "fallback_font": "Helvetica",
    "fontsize": 36,
    "primary_color": "&H00E2E8F0",
    "active_color": "&H00FFFFFF",
    "outline_color": "&H0018181B",
    "back_color": "&H00000000",
    "bold": 0,
    "outline": 1.8,
    "shadow": 1.0,
    "alignment": 2,
    "margin_v": 58,
    "uppercase": false,
    "animation_type": "standard_phrase",
    "preview_class": "preview-swiss",
    "preview_html": "Functional and objective typographic form",
    "css": {
      "fontFamily": "Arial, sans-serif",
      "color": "#e2e8f0",
      "activeColor": "#ffffff",
      "letterSpacing": "0.5px",
      "textShadow": "1px 1px 1px #18181b"
    }
  },
  {
    "id": "subtitle_pro",
    "name": "Universal Subtitle Pro",
    "category": "broadcast",
    "category_label": "Broadcast",
    "description": "High-contrast accessibility-compliant subtitle for universal legibility.",
    "font": "Verdana",
    "fallback_font": "Arial",
    "fontsize": 36,
    "primary_color": "&H00FFFFFF",
    "active_color": "&H00FFFFFF",
    "outline_color": "&H00000000",
    "back_color": "&HCC000000",
    "bold": 1,
    "outline": 3.0,
    "shadow": 1.5,
    "alignment": 2,
    "margin_v": 62,
    "uppercase": false,
    "animation_type": "standard_phrase",
    "preview_class": "preview-sub-pro",
    "preview_html": "Universal legibility across all displays",
    "css": {
      "fontFamily": "Verdana, sans-serif",
      "fontWeight": "bold",
      "color": "#ffffff",
      "activeColor": "#ffffff",
      "textShadow": "2px 2px 2px #000"
    }
  }
];

  let allStyles = EMBEDDED_STYLES;
  let currentTranscript = null;
  let currentFileId = null;
  let currentStyle = "hormozi_bold";
  let currentCategory = "all";
  let searchQuery = "";
  let audioElement = null;
  let animFrame = null;
  let isServerOnline = false;

  const CATEGORY_TABS = [
    { id: "all", name: "All (64)" },
    { id: "viral_shorts", name: "Viral Shorts" },
    { id: "hormozi", name: "Hormozi" },
    { id: "neon_glow", name: "Neon Cyber" },
    { id: "cinematic", name: "Cinematic" },
    { id: "boxed_pill", name: "Boxed & Pill" },
    { id: "headline", name: "Headline" },
    { id: "comic_pop", name: "Comic Pop" },
    { id: "broadcast", name: "Broadcast" }
  ];

  const FEATURED_EDITOR_PRESETS = [
    { id: "bouncy_shorts", label: "⚡ Viral Shorts", nativeMatch: "classic" },
    { id: "hormozi_bold", label: "🔥 Hormozi Bold", nativeMatch: "yellow" },
    { id: "neon_glow", label: "💎 Neon Cyber", nativeMatch: "classic" },
    { id: "boxed_pill", label: "📦 Boxed Pill", nativeMatch: "boxed" },
    { id: "headline_3d_punch", label: "💥 3D Punch", nativeMatch: "boxed" },
    { id: "comic_pop", label: "🎨 Comic Pop", nativeMatch: "yellow" },
    { id: "classic_broadcast", label: "🎬 Classic Crisp", nativeMatch: "classic" },
    { id: "snap_yellow", label: "🟡 Snap Yellow", nativeMatch: "yellow" }
  ];

  // Intercept URL.createObjectURL to reliably capture any voiceover audio file
  try {
    const _origCreateObjectURL = URL.createObjectURL;
    URL.createObjectURL = function(obj) {
      try {
        if (obj && (obj instanceof Blob || obj instanceof File)) {
          const isAudio = (obj.type && obj.type.startsWith("audio/")) ||
                          (obj.name && obj.name.match(/\.(mp3|wav|m4a|aac|ogg|flac)$/i));
          if (isAudio) {
            window._autoEditorVoiceover = obj;
            console.log("AutoEditor Captions: Cached voiceover audio file:", obj.name || "audio blob");
          }
        }
      } catch (e) {}
      return _origCreateObjectURL.apply(this, arguments);
    };
  } catch (e) {}

  let isUpdatingUI = false;
  let mutationDebounceTimer = null;

  function init() {
    console.log("Initializing AutoEditor Auto-Captions & Transcribe Extension (64 Presets + In-Editor Sync)...");
    
    // Track voiceover audio files globally
    trackVoiceoverAudio();

    // Ensure modal container is created safely
    ensureModal();
    checkServerHealth();
    fetchRemoteStyles();
    
    // Wait for initial React hydration before injecting into header actions
    setTimeout(() => {
      removeUnwantedLinks();
      injectHeaderButton();
      injectAutoSpeedBadge();
    }, 300);

    // Heartbeat for server & UI watcher
    setInterval(checkServerHealth, 4000);
    setInterval(() => {
      if (!isUpdatingUI) watchEditorUI();
    }, 600);

    // Watch for DOM changes with debounce & re-entrancy guard
    const observer = new MutationObserver((mutations) => {
      if (isUpdatingUI) return;

      // Filter out mutations on extension's own elements
      const isInternal = mutations.every(m => {
        const target = m.target;
        return target && (
          (target.id && (target.id === "cap-modal-root" || target.id === "btn-auto-captions" || target.id === "cap-auto-speed-pill")) ||
          (target.closest && (target.closest("#cap-modal-root") || target.closest("#btn-auto-captions") || target.closest("#cap-auto-speed-pill") || target.closest(".clip__speed"))) ||
          (target.classList && target.classList.contains("clip__speed"))
        );
      });
      if (isInternal) return;

      if (mutationDebounceTimer) clearTimeout(mutationDebounceTimer);
      mutationDebounceTimer = setTimeout(() => {
        mutationDebounceTimer = null;
        if (isUpdatingUI) return;
        isUpdatingUI = true;
        try {
          removeUnwantedLinks();
          injectHeaderButton();
          ensureModal();
          watchEditorUI();
        } finally {
          isUpdatingUI = false;
        }
      }, 100);
    });
    if (document.body) {
      observer.observe(document.body, { childList: true, subtree: true });
    }
  }

  // Remove Discord and Extension links
  function removeUnwantedLinks() {
    try {
      const links = document.querySelectorAll(".dc-link, .ext-link");
      links.forEach(el => el.remove());
    } catch (e) {}
  }

  // Track voiceover audio file whenever uploaded or dropped
  function trackVoiceoverAudio() {
    document.addEventListener("change", (e) => {
      const target = e.target;
      if (target && target.tagName === "INPUT" && target.type === "file") {
        if (target.accept && target.accept.includes("audio")) {
          if (target.files && target.files[0]) {
            window._autoEditorVoiceover = target.files[0];
            console.log("Captured voiceover file:", target.files[0].name);
          }
        }
      }
    }, true);

    document.addEventListener("drop", (e) => {
      if (e.dataTransfer && e.dataTransfer.files) {
        for (let f of e.dataTransfer.files) {
          if (f.type.startsWith("audio/") || f.name.match(/\.(mp3|wav|m4a|aac|ogg|flac)$/i)) {
            window._autoEditorVoiceover = f;
            console.log("Captured dropped voiceover:", f.name);
            break;
          }
        }
      }
    }, true);
  }

  // Retrieve current voiceover audio (from memory or active audio element)
  async function getVoiceoverAudio() {
    if (window._autoEditorVoiceover) {
      return window._autoEditorVoiceover;
    }
    const audioEl = document.querySelector('audio[src^="blob:"]') || document.querySelector('audio[src]') || document.querySelector('audio');
    if (audioEl && audioEl.src) {
      try {
        const res = await fetch(audioEl.src);
        const blob = await res.blob();
        const ext = blob.type.includes("wav") ? "wav" : "mp3";
        const file = new File([blob], `voiceover.${ext}`, { type: blob.type || "audio/wav" });
        window._autoEditorVoiceover = file;
        return file;
      } catch (err) {
        console.warn("Could not fetch blob audio:", err);
      }
    }
    return null;
  }

  // Format seconds to SRT time format: 00:00:03,400
  function formatSRTTime(sec) {
    const s = Math.max(0, Number(sec) || 0);
    const hrs = Math.floor(s / 3600);
    const mins = Math.floor((s % 3600) / 60);
    const secs = Math.floor(s % 60);
    const millis = Math.floor((s % 1) * 1000);
    return `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')},${String(millis).padStart(3, '0')}`;
  }

  // Convert segments to valid SRT string
  function segmentsToSRT(segments) {
    if (!segments || !segments.length) return "";
    return segments.map((seg, idx) => {
      const start = formatSRTTime(seg.start);
      const end = formatSRTTime(seg.end);
      const text = (seg.text || "").trim();
      return `${idx + 1}\n${start} --> ${end}\n${text}\n`;
    }).join("\n");
  }

  // Inject SRT file directly into AutoEditor's caption input
  function injectCaptionsIntoEditor(srtText) {
    const captionInput = document.querySelector('input[accept*=".srt"], input[accept*=".vtt"], input[accept*="text/plain"]');
    if (!captionInput) {
      console.warn("AutoEditor caption input element not found.");
      return false;
    }
    try {
      const blob = new Blob([srtText], { type: "text/plain" });
      const file = new File([blob], "auto_captions.srt", { type: "text/plain" });
      const dt = new DataTransfer();
      dt.items.add(file);
      captionInput.files = dt.files;
      captionInput.dispatchEvent(new Event("change", { bubbles: true }));
      console.log("Successfully dispatched auto_captions.srt into AutoEditor!");
      return true;
    } catch (err) {
      console.error("Failed to inject captions into AutoEditor:", err);
      return false;
    }
  }

  // Watch for In-Editor Captions panel elements
  function watchEditorUI() {
    removeUnwantedLinks();
    ensureModal();
    injectHeaderButton();
    injectAutoSpeedBadge();
    updateTimelineSpeedBadges();

    // 1. Check for empty captions state in editor sidebar
    const capEmpty = document.querySelector(".panel.captions .cap-empty");
    if (capEmpty && !document.getElementById("btn-editor-auto-captions")) {
      const card = document.createElement("div");
      card.className = "cap-ai-generate-card";
      card.id = "cap-ai-generate-card-wrapper";
      card.innerHTML = `
        <button type="button" class="cap-ai-generate-btn" id="btn-editor-auto-captions">
          <span class="cap-ai-btn-icon">✨</span>
          <span class="cap-ai-btn-text">Create Automatic Captions</span>
        </button>
        <div class="cap-ai-subtitle">Auto-transcribes voiceover with Whisper AI into synced timeline captions</div>
      `;
      card.querySelector("#btn-editor-auto-captions").onclick = () => handleInEditorGenerateCaptions(card.querySelector("#btn-editor-auto-captions"));
      capEmpty.insertBefore(card, capEmpty.firstChild);
    }

    // 2. Check for active captions body in editor sidebar to inject preset styles
    const capBody = document.querySelector(".panel.captions .cap-body");
    if (capBody && !document.getElementById("cap-editor-presets-container")) {
      const presetsSection = document.createElement("div");
      presetsSection.className = "cap-editor-presets-section";
      presetsSection.id = "cap-editor-presets-container";

      let chipsHtml = "";
      FEATURED_EDITOR_PRESETS.forEach(p => {
        const isAct = p.id === currentStyle;
        chipsHtml += `<button type="button" class="cap-preset-chip ${isAct ? 'is-active' : ''}" data-style="${p.id}" data-native="${p.nativeMatch}">${p.label}</button>`;
      });

      presetsSection.innerHTML = `
        <div class="cap-editor-presets-head">
          <span class="cap-editor-presets-title">✨ Caption Presets</span>
          <button type="button" class="cap-editor-studio-link" id="btn-open-full-presets-studio">Browse All (64)...</button>
        </div>
        <div class="cap-editor-chips">
          ${chipsHtml}
        </div>
      `;

      // Preset click handlers
      presetsSection.querySelectorAll(".cap-preset-chip").forEach(chip => {
        chip.onclick = () => {
          presetsSection.querySelectorAll(".cap-preset-chip").forEach(c => c.classList.remove("is-active"));
          chip.classList.add("is-active");
          const styleId = chip.getAttribute("data-style");
          const nativeMatch = chip.getAttribute("data-native");
          currentStyle = styleId;

          // Sync with native AutoEditor chips if applicable
          if (nativeMatch) {
            const nativeChips = document.querySelectorAll(".panel.captions .trchip");
            nativeChips.forEach(nc => {
              const text = nc.innerText.toLowerCase();
              if (text.includes(nativeMatch)) {
                nc.click();
              }
            });
          }
        };
      });

      const studioLink = presetsSection.querySelector("#btn-open-full-presets-studio");
      if (studioLink) {
        studioLink.onclick = () => {
          openModal();
          switchTab(2);
        };
      }

      capBody.appendChild(presetsSection);
    }
  }

  // Handle "Create Automatic Captions" directly from in-editor panel
  async function handleInEditorGenerateCaptions(btn) {
    if (!btn) return;

    // Check if voiceover audio is available
    let audioFile = await getVoiceoverAudio();
    if (!audioFile) {
      // If voiceover is not yet captured, open the studio modal to Tab 1 so user can immediately import/drop it!
      openModal();
      switchTab(1);
      return;
    }

    btn.disabled = true;
    btn.innerHTML = `<span class="cap-ai-spin">⏳</span> <span>Generating captions with Whisper AI...</span>`;

    try {

      const formData = new FormData();
      formData.append("audio", audioFile);

      const res = await fetch(`${API_BASE}/api/transcribe`, {
        method: "POST",
        body: formData
      });

      if (!res.ok) throw new Error(`Transcription server returned HTTP ${res.status}`);
      const data = await res.json();

      currentTranscript = data.transcript;
      currentFileId = data.id;

      // Convert to SRT and inject into AutoEditor
      const srtText = segmentsToSRT(data.transcript.segments);
      const injected = injectCaptionsIntoEditor(srtText);

      btn.innerHTML = `<span>✓</span> <span>Captions Created (${data.transcript.segments.length} lines)!</span>`;
      btn.style.background = "linear-gradient(135deg, #10b981 0%, #059669 100%)";

      // Also set up audio player in modal
      if (!audioElement) {
        audioElement = new Audio(URL.createObjectURL(audioFile));
      }
      renderTranscript(data);

      setTimeout(() => {
        btn.disabled = false;
        btn.innerHTML = `<span class="cap-ai-btn-icon">✨</span> <span class="cap-ai-btn-text">Re-create Automatic Captions</span>`;
        btn.style.background = "";
      }, 3500);

    } catch (err) {
      console.error("In-editor caption generation failed:", err);
      alert(`Could not generate automatic captions: ${err.message}\n\nEnsure the AI Engine is running.`);
      btn.disabled = false;
      btn.innerHTML = `<span class="cap-ai-btn-icon">✨</span> <span class="cap-ai-btn-text">Create Automatic Captions</span>`;
    }
  }

  async function checkServerHealth() {
    const statusBadge = document.getElementById("cap-server-status-badge");
    try {
      const res = await fetch(`${API_BASE}/api/health`, { method: "GET" });
      if (res.ok) {
        isServerOnline = true;
        if (statusBadge) {
          statusBadge.innerHTML = "🟢 AI Engine Ready";
          statusBadge.style.color = "#4ade80";
          statusBadge.style.background = "rgba(34, 197, 94, 0.15)";
          statusBadge.style.borderColor = "rgba(34, 197, 94, 0.3)";
        }
      } else {
        throw new Error("Bad response");
      }
    } catch {
      isServerOnline = false;
      if (statusBadge) {
        statusBadge.innerHTML = "🔴 AI Engine Offline";
        statusBadge.style.color = "#f87171";
        statusBadge.style.background = "rgba(239, 68, 68, 0.15)";
        statusBadge.style.borderColor = "rgba(239, 68, 68, 0.3)";
      }
    }
  }

  async function fetchRemoteStyles() {
    try {
      const res = await fetch(`${API_BASE}/api/styles`, { method: "GET" });
      if (res.ok) {
        const remoteData = await res.json();
        const stylesList = Object.values(remoteData);
        if (stylesList.length >= 60) {
          allStyles = stylesList;
          renderCategoryPills();
          renderStyleCards();
        }
      }
    } catch (e) {
      console.log("Using embedded 64 presets library (offline mode ready).");
    }
  }

  function injectHeaderButton() {
    const existing = document.getElementById("btn-auto-captions");
    const actionsBar = document.querySelector(".bar__actions") || document.querySelector(".bar");
    if (!actionsBar) return;

    if (existing) {
      if (actionsBar.contains(existing)) {
        return;
      }
      existing.remove();
    }

    const btn = document.createElement("button");
    btn.id = "btn-auto-captions";
    btn.type = "button";
    btn.className = "cap-magic-btn";
    btn.innerHTML = "<span>✨</span><span>Auto Captions & Transcribe</span>";
    btn.onclick = openModal;

    if (actionsBar.firstChild) {
      actionsBar.insertBefore(btn, actionsBar.firstChild);
    } else {
      actionsBar.appendChild(btn);
    }
  }

  // Global Video Duration Cache
  window._videoDurationCache = window._videoDurationCache || {};

  function injectAutoSpeedBadge() {
    const actionsBar = document.querySelector(".bar__actions") || document.querySelector(".bar");
    if (!actionsBar) return;
    if (document.getElementById("cap-auto-speed-pill")) return;

    const pill = document.createElement("div");
    pill.id = "cap-auto-speed-pill";
    pill.className = "cap-auto-speed-pill";
    pill.title = "Intelligent Video Speed: Active. Videos longer than their timestamp slots are automatically accelerated to fit seamlessly.";
    pill.innerHTML = '<span class="pill-dot"></span><span>⚡ Auto-Speed: Active</span>';

    const captionsBtn = document.getElementById("btn-auto-captions");
    if (captionsBtn && captionsBtn.nextSibling) {
      actionsBar.insertBefore(pill, captionsBtn.nextSibling);
    } else {
      actionsBar.appendChild(pill);
    }
  }

  function updateTimelineSpeedBadges() {
    const clips = document.querySelectorAll(".clip");
    if (!clips || !clips.length) return;

    clips.forEach(clip => {
      const isVideo = clip.querySelector(".clip__video");
      if (!isVideo) return;

      const meta = clip.querySelector(".clip__meta");
      if (!meta) return;

      const title = clip.getAttribute("title") || "";
      const slotDur = parseFloat(meta.innerText) || 0;

      // Extract filename from title (e.g. "my_video.mp4 · 0:05.5 · 4.5s")
      const fnMatch = title.match(/^([^·\n]+)\s*·/);
      const filename = fnMatch ? fnMatch[1].trim() : "";
      if (!filename || filename.length === 0) return;

      let srcDur = 0;
      if (window._videoDurationCache && window._videoDurationCache[filename]) {
        srcDur = window._videoDurationCache[filename];
      } else if (window._videoDurationCache) {
        for (const k in window._videoDurationCache) {
          if (k && (filename.includes(k) || k.includes(filename))) {
            srcDur = window._videoDurationCache[k];
            break;
          }
        }
      }

      let badge = clip.querySelector(".clip__speed");
      if (srcDur > 0 && slotDur > 0 && srcDur > slotDur + 0.05) {
        const speed = (srcDur / slotDur).toFixed(1);
        const speedHtml = `⚡ ${speed}&times;`;
        const speedTitle = `Auto-fit: ${srcDur.toFixed(1)}s video accelerated at ${speed}× to fit slot`;
        if (!badge) {
          badge = document.createElement("span");
          badge.className = "clip__speed";
          badge.title = speedTitle;
          badge.innerHTML = speedHtml;
          isVideo.parentNode.insertBefore(badge, isVideo.nextSibling);
        } else {
          if (badge.innerHTML !== speedHtml) badge.innerHTML = speedHtml;
          if (badge.title !== speedTitle) badge.title = speedTitle;
        }
      } else if (badge) {
        badge.remove();
      }
    });
  }

  // Pre-cache video durations on file selection or drag-and-drop
  try {
    document.addEventListener("change", function(e) {
      const input = e.target;
      if (input && input.type === "file" && input.files) {
        Array.from(input.files).forEach(f => {
          if (f.type && f.type.startsWith("video/")) {
            const v = document.createElement("video");
            v.preload = "metadata";
            v.src = URL.createObjectURL(f);
            v.onloadedmetadata = () => {
              if (isFinite(v.duration) && v.duration > 0) {
                window._videoDurationCache[f.name] = v.duration;
                updateTimelineSpeedBadges();
              }
            };
          }
        });
      }
    }, true);

    document.addEventListener("drop", function(e) {
      if (e.dataTransfer && e.dataTransfer.files) {
        Array.from(e.dataTransfer.files).forEach(f => {
          if (f.type && f.type.startsWith("video/")) {
            const v = document.createElement("video");
            v.preload = "metadata";
            v.src = URL.createObjectURL(f);
            v.onloadedmetadata = () => {
              if (isFinite(v.duration) && v.duration > 0) {
                window._videoDurationCache[f.name] = v.duration;
                updateTimelineSpeedBadges();
              }
            };
          }
        });
      }
    }, true);
  } catch (e) {}

  function createModal() {
    let root = document.getElementById("cap-modal-root");
    let overlay = document.getElementById("cap-modal-overlay");
    const inBody = !!(document.body && root && (typeof document.body.contains === "function" ? document.body.contains(root) : true));
    if (root && overlay && inBody) {
      return;
    }
    if (root) {
      try {
        if (typeof root.remove === "function") {
          root.remove();
        } else if (root.parentNode && typeof root.parentNode.removeChild === "function") {
          root.parentNode.removeChild(root);
        }
      } catch (e) {}
    }
    if (!document.body) return;

    root = document.createElement("div");
    root.id = "cap-modal-root";
    root.innerHTML = `
      <div id="cap-modal-overlay" class="cap-modal-overlay" style="display: none;">
        <div class="cap-modal">
          <!-- Header -->
          <div class="cap-modal-header">
            <div class="cap-modal-title">
              <span>✨</span>
              <span>Auto Captions & Audio Transcription Studio</span>
              <span id="cap-server-status-badge" class="cap-badge">Checking AI Engine...</span>
            </div>
            <button id="cap-btn-close" class="cap-close-btn">&times;</button>
          </div>

          <!-- Tabs -->
          <div class="cap-tabs">
            <button id="cap-tab-1-btn" class="cap-tab-btn active">
              <span>🎙️</span> Audio to Transcript & Export
            </button>
            <button id="cap-tab-2-btn" class="cap-tab-btn">
              <span>🎨</span> CapCut Caption Styles (64 Presets)
            </button>
          </div>

          <!-- Body -->
          <div class="cap-modal-body">
            <!-- TAB 1: TRANSCRIPTION & EXPORT -->
            <div id="cap-tab-1" class="cap-tab-pane active">
              <div class="cap-dropzone" id="cap-dropzone">
                <div class="cap-drop-icon">🎙️</div>
                <div class="cap-drop-title">Import Audio File (MP3, WAV, M4A)</div>
                <div class="cap-drop-subtitle">High-accuracy local Whisper speech-to-text with exact word timestamps</div>
                <input type="file" id="cap-audio-input" accept="audio/*" style="display: none;">
                <button type="button" class="cap-magic-btn" style="margin-top: 14px;" id="cap-btn-choose-file">
                  <span>📁</span><span>Choose Audio File</span>
                </button>
              </div>

              <!-- Loading State -->
              <div id="cap-loading-state" class="cap-loading-state" style="display: none;">
                <div class="cap-spinner"></div>
                <div class="cap-loading-title">Generating High-Accuracy Transcript...</div>
                <div class="cap-loading-sub">Running local Whisper model with Voice Activity Detection & beam search</div>
              </div>

              <!-- Error State -->
              <div id="cap-error-banner" class="cap-error-banner" style="display: none;">
                <span id="cap-error-msg">Failed to connect to AI server.</span>
              </div>

              <!-- Results Section -->
              <div id="cap-results-section" style="display: none;">
                <!-- Action Bar with strict R3 seconds badges & download buttons -->
                <div class="cap-transcript-actions">
                  <div class="cap-meta-group">
                    <span id="cap-meta-dur" class="cap-meta-badge">⏱️ 0.0s</span>
                    <span id="cap-meta-words" class="cap-meta-badge">📝 0 words</span>
                    <span id="cap-meta-lang" class="cap-meta-badge">🌐 EN</span>
                  </div>
                  <div class="cap-export-group">
                    <button type="button" class="cap-action-btn cap-btn-apply-editor" id="cap-btn-apply-transcript-editor">
                      <span>✨</span><span>Apply to Video Editor</span>
                    </button>
                    <a id="cap-btn-download-txt" href="#" target="_blank" class="cap-action-btn cap-btn-txt">
                      <span>📄</span><span>Download TXT (0.0s – 3.4s)</span>
                    </a>
                    <a id="cap-btn-download-pdf" href="#" target="_blank" class="cap-action-btn cap-btn-pdf">
                      <span>📑</span><span>Download PDF</span>
                    </a>
                  </div>
                </div>

                <!-- Segments Container -->
                <div class="cap-segments-container" id="cap-segments-container">
                  <!-- Segments populated dynamically -->
                </div>
              </div>
            </div>

            <!-- TAB 2: CAPCUT STYLES LIBRARY (64 Presets) -->
            <div id="cap-tab-2" class="cap-tab-pane">
              <!-- Live Visual Stage Player -->
              <div class="cap-stage-wrapper">
                <div class="cap-stage-box" id="cap-stage-screen">
                  <div class="cap-preview-caption" id="cap-preview-text">
                    SAMPLE <span class="act">CAPCUT STYLE</span> PREVIEW
                  </div>
                </div>
                <!-- Playback controls -->
                <div class="cap-player-bar">
                  <button id="cap-preview-play-btn" class="cap-play-btn" title="Toggle preview playback">&#9658;</button>
                  <div class="cap-progress-track" id="cap-progress-track">
                    <div class="cap-progress-fill" id="cap-progress-fill"></div>
                  </div>
                  <div class="cap-time-text" id="cap-time-text">0.0s / 0.0s</div>
                </div>
              </div>

              <!-- Search and Filter Pills -->
              <div class="cap-filter-section">
                <div class="cap-search-wrap">
                  <input type="text" id="cap-style-search" class="cap-search-input" placeholder="🔍 Search 64 styles (e.g. Hormozi, Neon, TikTok, Bouncy, Glow, Minimal)...">
                </div>
                <div class="cap-category-pills" id="cap-category-pills">
                  <!-- Category pills injected dynamically -->
                </div>
              </div>

              <!-- Styles Grid -->
              <div class="cap-styles-header">
                <div class="cap-styles-title">
                  <span>Available Styles</span>
                  <span class="cap-count-badge" id="cap-styles-count">64 Presets</span>
                </div>
                <div class="cap-styles-actions">
                  <button type="button" class="cap-magic-btn" id="cap-btn-apply-captions">
                    <span>✨</span><span>Sync & Apply to Editor</span>
                  </button>
                </div>
              </div>

              <div class="cap-styles-grid" id="cap-styles-grid">
                <!-- 64 Style cards injected dynamically -->
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(root);

    // Event listeners
    const closeBtn = root.querySelector("#cap-btn-close");
    if (closeBtn) closeBtn.onclick = closeModal;

    const modalOverlay = root.querySelector("#cap-modal-overlay");
    if (modalOverlay) {
      modalOverlay.onclick = (e) => {
        if (e.target.id === "cap-modal-overlay") closeModal();
      };
    }

    const tab1Btn = root.querySelector("#cap-tab-1-btn");
    if (tab1Btn) tab1Btn.onclick = () => switchTab(1);

    const tab2Btn = root.querySelector("#cap-tab-2-btn");
    if (tab2Btn) tab2Btn.onclick = () => switchTab(2);

    const chooseBtn = root.querySelector("#cap-btn-choose-file");
    const audioInput = root.querySelector("#cap-audio-input");
    if (chooseBtn && audioInput) {
      chooseBtn.onclick = () => audioInput.click();
      audioInput.onchange = (e) => {
        if (e.target.files && e.target.files[0]) {
          window._autoEditorVoiceover = e.target.files[0];
          handleAudioUpload(e.target.files[0]);
        }
      };
    }

    const dz = root.querySelector("#cap-dropzone");
    if (dz) {
      dz.ondragover = (e) => { e.preventDefault(); dz.style.borderColor = "#a855f7"; };
      dz.ondragleave = () => { dz.style.borderColor = "#232936"; };
      dz.ondrop = (e) => {
        e.preventDefault();
        dz.style.borderColor = "#232936";
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
          window._autoEditorVoiceover = e.dataTransfer.files[0];
          handleAudioUpload(e.dataTransfer.files[0]);
        }
      };
    }

    // Apply to Video Editor button in Tab 1
    const applyFromTab1Btn = root.querySelector("#cap-btn-apply-transcript-editor");
    if (applyFromTab1Btn) {
      applyFromTab1Btn.onclick = () => {
        if (!currentTranscript || !currentTranscript.segments) {
          alert("Please transcribe an audio file first.");
          return;
        }
        const srtText = segmentsToSRT(currentTranscript.segments);
        const ok = injectCaptionsIntoEditor(srtText);
        if (ok) {
          alert("✨ Captions successfully synced with your video editor timeline!");
          closeModal();
        } else {
          alert("Could not automatically locate editor timeline. Build the timeline first, then apply.");
        }
      };
    }

    const playBtn = root.querySelector("#cap-preview-play-btn");
    if (playBtn) playBtn.onclick = togglePlayback;

    const applyCaptionsBtn = root.querySelector("#cap-btn-apply-captions");
    if (applyCaptionsBtn) applyCaptionsBtn.onclick = applyCaptionsToVideo;

    // Search input handler
    const searchInput = root.querySelector("#cap-style-search");
    if (searchInput) {
      searchInput.oninput = (e) => {
        searchQuery = e.target.value.toLowerCase().trim();
        renderStyleCards();
      };
    }

    renderCategoryPills();
    renderStyleCards();
  }

  function ensureModal() {
    createModal();
    return document.getElementById("cap-modal-overlay");
  }

  function openModal() {
    const overlay = ensureModal();
    if (overlay) {
      overlay.style.display = "flex";
      overlay.style.setProperty("display", "flex", "important");
      overlay.style.setProperty("visibility", "visible", "important");
      overlay.style.setProperty("opacity", "1", "important");
      overlay.style.setProperty("z-index", "999999", "important");
      overlay.classList.add("is-open");
      checkServerHealth();
      if (!currentTranscript) {
        getVoiceoverAudio().then(f => {
          if (f && !audioElement) {
            audioElement = new Audio(URL.createObjectURL(f));
          }
        });
      }
    } else {
      console.error("AutoEditor Captions: Could not open modal overlay.");
    }
  }

  function closeModal() {
    const overlay = document.getElementById("cap-modal-overlay");
    if (overlay) {
      overlay.style.display = "none";
      overlay.style.setProperty("display", "none", "important");
      overlay.classList.remove("is-open");
    }
    if (audioElement && !audioElement.paused) {
      audioElement.pause();
      cancelAnimationFrame(animFrame);
      const playBtn = document.getElementById("cap-preview-play-btn");
      if (playBtn) playBtn.innerHTML = "&#9658;";
    }
  }

  function switchTab(num) {
    document.getElementById("cap-tab-1-btn").classList.toggle("active", num === 1);
    document.getElementById("cap-tab-2-btn").classList.toggle("active", num === 2);
    document.getElementById("cap-tab-1").classList.toggle("active", num === 1);
    document.getElementById("cap-tab-2").classList.toggle("active", num === 2);

    if (num === 2) {
      updatePreviewDisplayStatic();
    }
  }

  function renderCategoryPills() {
    const container = document.getElementById("cap-category-pills");
    if (!container) return;
    container.innerHTML = "";

    CATEGORY_TABS.forEach(cat => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = `cap-cat-pill ${cat.id === currentCategory ? "active" : ""}`;
      btn.innerText = cat.name;
      btn.onclick = () => {
        currentCategory = cat.id;
        document.querySelectorAll(".cap-cat-pill").forEach(p => p.classList.remove("active"));
        btn.classList.add("active");
        renderStyleCards();
      };
      container.appendChild(btn);
    });
  }

  function getFilteredStyles() {
    return allStyles.filter(s => {
      const matchCat = currentCategory === "all" || s.category === currentCategory;
      const matchSearch = !searchQuery || 
        s.name.toLowerCase().includes(searchQuery) ||
        (s.description || "").toLowerCase().includes(searchQuery) ||
        (s.category_label || "").toLowerCase().includes(searchQuery);
      return matchCat && matchSearch;
    });
  }

  function renderStyleCards() {
    const grid = document.getElementById("cap-styles-grid");
    const countBadge = document.getElementById("cap-styles-count");
    if (!grid) return;
    grid.innerHTML = "";

    const filtered = getFilteredStyles();
    if (countBadge) {
      countBadge.innerText = `${filtered.length} of ${allStyles.length} Presets`;
    }

    if (filtered.length === 0) {
      grid.innerHTML = `<div class="cap-style-empty-state">No caption presets match "${searchQuery}". Try another keyword or category.</div>`;
      return;
    }

    const trendingIds = ["hormozi_bold", "bouncy_shorts", "neon_glow", "boxed_pill", "headline_3d_punch", "comic_pop", "classic_broadcast", "viral_green_hook"];

    filtered.forEach(s => {
      const isSelected = s.id === currentStyle;
      const isTrending = trendingIds.includes(s.id);
      const card = document.createElement("div");
      card.className = `cap-style-card ${isSelected ? "selected" : ""}`;
      card.id = `style-card-${s.id}`;

      const previewHtml = s.preview_html || `${s.name} <span class="act">ACTIVE</span>`;
      const catLabel = s.category_label || (s.category || '').toUpperCase();

      card.innerHTML = `
        <div class="cap-card-category-tag">${catLabel}</div>
        <div class="cap-card-badge">
          <span>${s.name}</span>
          ${isTrending ? '<span style="color:#f59e0b">★ POPULAR</span>' : ''}
        </div>
        <div class="cap-card-preview-box">
          <div class="cap-item-preview ${s.preview_class || ''}" id="card-preview-${s.id}">
            ${previewHtml}
          </div>
        </div>
        <div class="cap-card-desc">${s.description || ''}</div>
      `;

      const previewEl = card.querySelector(`#card-preview-${s.id}`);
      if (previewEl && s.css) {
        applyStyleObject(previewEl, s.css);
      }

      card.onclick = () => {
        document.querySelectorAll(".cap-style-card").forEach(c => c.classList.remove("selected"));
        card.classList.add("selected");
        currentStyle = s.id;
        if (!audioElement || audioElement.paused) {
          updatePreviewDisplayStatic();
        } else {
          updatePreviewFrame();
        }
      };

      grid.appendChild(card);
    });
  }

  function applyStyleObject(el, css) {
    if (!el || !css) return;
    if (css.fontFamily) el.style.fontFamily = css.fontFamily;
    if (css.color) el.style.color = css.color;
    if (css.fontWeight) el.style.fontWeight = css.fontWeight;
    if (css.textTransform) el.style.textTransform = css.textTransform;
    if (css.textShadow) el.style.textShadow = css.textShadow;
    if (css.letterSpacing) el.style.letterSpacing = css.letterSpacing;
    if (css.background) el.style.background = css.background;
    if (css.padding) el.style.padding = css.padding;
    if (css.borderRadius) el.style.borderRadius = css.borderRadius;
    
    const actSpan = el.querySelector(".act");
    if (actSpan) {
      if (css.activeColor) actSpan.style.color = css.activeColor;
      if (css.activeBg) {
        actSpan.style.background = css.activeBg;
        actSpan.style.padding = "2px 6px";
        actSpan.style.borderRadius = "4px";
      }
    }
  }

  function updatePreviewDisplayStatic() {
    const previewBox = document.getElementById("cap-preview-text");
    if (!previewBox) return;
    const s = allStyles.find(item => item.id === currentStyle) || allStyles[0];
    if (!s) return;

    previewBox.className = `cap-preview-caption ${s.preview_class || ''}`;
    previewBox.removeAttribute("style");
    previewBox.innerHTML = s.preview_html || `PREVIEW <span class="act">${s.name.toUpperCase()}</span> STYLE`;
    applyStyleObject(previewBox, s.css);
  }

  async function handleAudioUpload(file) {
    const dz = document.getElementById("cap-dropzone");
    const loading = document.getElementById("cap-loading-state");
    const results = document.getElementById("cap-results-section");
    const errBanner = document.getElementById("cap-error-banner");

    errBanner.style.display = "none";
    dz.style.display = "none";
    loading.style.display = "block";
    results.style.display = "none";

    if (audioElement) {
      audioElement.pause();
    }
    audioElement = new Audio(URL.createObjectURL(file));
    audioElement.onended = () => {
      document.getElementById("cap-preview-play-btn").innerHTML = "&#9658;";
    };

    try {
      const formData = new FormData();
      formData.append("audio", file);

      const res = await fetch(`${API_BASE}/api/transcribe`, {
        method: "POST",
        body: formData
      });

      if (!res.ok) throw new Error(`Server returned HTTP ${res.status}`);
      const data = await res.json();

      currentTranscript = data.transcript;
      currentFileId = data.id;

      renderTranscript(data);
      dz.style.display = "block";
      loading.style.display = "none";
      results.style.display = "block";

    } catch (err) {
      console.error("Transcription error:", err);
      loading.style.display = "none";
      dz.style.display = "block";
      errBanner.style.display = "block";
      document.getElementById("cap-error-msg").innerText = 
        `Could not connect to AI Engine (${err.message}). Ensure background service is running on port 4001.`;
    }
  }

  function renderTranscript(data) {
    const t = data.transcript;
    // Strict R3 second-based formatting: 0.0s
    const durStr = `${Number(t.duration || 0).toFixed(1)}s`;
    const durEl = document.getElementById("cap-meta-dur");
    if (durEl) durEl.innerText = `⏱️ ${durStr}`;
    const wordsEl = document.getElementById("cap-meta-words");
    if (wordsEl) wordsEl.innerText = `📝 ${t.total_words} words`;
    const langEl = document.getElementById("cap-meta-lang");
    if (langEl) langEl.innerText = `🌐 ${(t.language || 'en').toUpperCase()}`;

    const txtBtn = document.getElementById("cap-btn-download-txt");
    if (txtBtn) txtBtn.href = data.downloads.txt;
    const pdfBtn = document.getElementById("cap-btn-download-pdf");
    if (pdfBtn) pdfBtn.href = data.downloads.pdf;

    const list = document.getElementById("cap-segments-container");
    if (!list) return;
    list.innerHTML = "";

    (t.segments || []).forEach((seg) => {
      const row = document.createElement("div");
      row.className = "cap-segment-row";
      
      const timeBadge = document.createElement("div");
      timeBadge.className = "cap-segment-time";
      // Strict R3 second-based interval format: 0.0s – 3.4s
      const sStart = Number(seg.start).toFixed(1);
      const sEnd = Number(seg.end).toFixed(1);
      timeBadge.innerText = `${sStart}s – ${sEnd}s`;
      timeBadge.style.cursor = "pointer";
      timeBadge.title = "Click to jump playback here";
      timeBadge.onclick = () => {
        if (audioElement) {
          audioElement.currentTime = seg.start;
          audioElement.play();
          document.getElementById("cap-preview-play-btn").innerHTML = "&#10074;&#10074;";
          startAnimationLoop();
        }
      };

      const textDiv = document.createElement("div");
      textDiv.className = "cap-segment-text";
      textDiv.innerText = seg.text;

      row.appendChild(timeBadge);
      row.appendChild(textDiv);
      list.appendChild(row);
    });
  }

  function togglePlayback() {
    if (!audioElement) {
      alert("Please import an audio file in the first tab to preview captions with speech.");
      return;
    }

    const btn = document.getElementById("cap-preview-play-btn");
    if (audioElement.paused) {
      audioElement.play();
      btn.innerHTML = "&#10074;&#10074;";
      startAnimationLoop();
    } else {
      audioElement.pause();
      btn.innerHTML = "&#9658;";
      cancelAnimationFrame(animFrame);
    }
  }

  function startAnimationLoop() {
    cancelAnimationFrame(animFrame);
    function tick() {
      updatePreviewFrame();
      if (audioElement && !audioElement.paused) {
        animFrame = requestAnimationFrame(tick);
      }
    }
    animFrame = requestAnimationFrame(tick);
  }

  function updatePreviewFrame() {
    if (!audioElement) return;

    const curTime = audioElement.currentTime;
    const dur = audioElement.duration || 1;
    const pct = (curTime / dur) * 100;

    const fill = document.getElementById("cap-progress-fill");
    if (fill) fill.style.width = `${pct}%`;
    const timeText = document.getElementById("cap-time-text");
    if (timeText) timeText.innerText = `${curTime.toFixed(1)}s / ${dur.toFixed(1)}s`;

    const previewBox = document.getElementById("cap-preview-text");
    const s = allStyles.find(item => item.id === currentStyle) || allStyles[0];
    if (!s || !previewBox) return;

    previewBox.className = `cap-preview-caption ${s.preview_class || ''}`;
    previewBox.removeAttribute("style");
    applyStyleObject(previewBox, s.css);

    if (!currentTranscript || !currentTranscript.segments) {
      previewBox.innerHTML = s.preview_html || `PREVIEW <span class="act">${s.name.toUpperCase()}</span> STYLE`;
      return;
    }

    let activeSeg = null;
    for (let seg of currentTranscript.segments) {
      if (curTime >= seg.start && curTime <= seg.end) {
        activeSeg = seg;
        break;
      }
    }

    if (!activeSeg) {
      activeSeg = currentTranscript.segments.find(seg => seg.start >= curTime) || currentTranscript.segments[0];
    }

    if (!activeSeg) return;

    const words = activeSeg.words;
    if (!words || words.length === 0) {
      const segText = s.uppercase ? activeSeg.text.toUpperCase() : activeSeg.text;
      previewBox.innerText = segText;
      return;
    }

    const wordIdx = words.findIndex(w => curTime >= w.start && curTime <= w.end);
    const chunkIdx = wordIdx >= 0 ? Math.floor(wordIdx / 4) : 0;
    const chunk = words.slice(chunkIdx * 4, chunkIdx * 4 + 4);

    const renderedWords = (chunk.length ? chunk : words.slice(0, 4)).map(w => {
      const isAct = curTime >= w.start && curTime <= w.end;
      const text = s.uppercase ? w.word.toUpperCase() : w.word;
      return isAct ? `<span class="act">${text}</span>` : text;
    });

    previewBox.innerHTML = renderedWords.join(" ");
    applyStyleObject(previewBox, s.css);
  }

  async function applyCaptionsToVideo() {
    if (!currentTranscript) {
      alert("Please import and transcribe an audio file first.");
      return;
    }

    try {
      // 1. Inject into AutoEditor timeline input directly
      const srtText = segmentsToSRT(currentTranscript.segments);
      const injected = injectCaptionsIntoEditor(srtText);

      // 2. Also generate ASS file
      const res = await fetch(`${API_BASE}/api/generate-ass`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          transcript: currentTranscript,
          style: currentStyle,
          width: 1920,
          height: 1080
        })
      });

      const data = await res.json();
      if (!data.ok) throw new Error(data.error);

      if (injected) {
        alert(`✨ Captions styled with "${currentStyle}" have been synchronized with your video editor timeline and preview!\n\nCaptions will now appear live in the video canvas and burn into final export.`);
      } else {
        alert(`Captions styled with "${currentStyle}" generated.\n\nFile saved: ${data.ass_path}`);
      }
      closeModal();

    } catch (err) {
      alert("Could not apply captions: " + err.message);
    }
  }

  // Global Event Delegation (useCapture = true catches clicks before any React stopPropagation)
  document.addEventListener("click", function(e) {
    const target = e.target;
    if (!target) return;

    // 1. Top Bar Auto Captions & Transcribe button
    const magicBtn = target.closest("#btn-auto-captions") || target.closest(".cap-magic-btn");
    if (magicBtn && !magicBtn.closest("#cap-modal-root")) {
      e.preventDefault();
      e.stopPropagation();
      openModal();
      return;
    }

    // 2. In-editor Create Automatic Captions button
    const editorBtn = target.closest("#btn-editor-auto-captions") || target.closest(".cap-ai-generate-btn");
    if (editorBtn) {
      e.preventDefault();
      e.stopPropagation();
      handleInEditorGenerateCaptions(editorBtn);
      return;
    }

    // 3. In-editor Browse All (64)... studio link
    const studioLink = target.closest("#btn-open-full-presets-studio") || target.closest(".cap-editor-studio-link");
    if (studioLink) {
      e.preventDefault();
      e.stopPropagation();
      openModal();
      switchTab(2);
      return;
    }

    // 4. Modal backdrop click to close
    if (target.id === "cap-modal-overlay") {
      closeModal();
      return;
    }

    // 5. Close button
    if (target.id === "cap-btn-close" || target.closest("#cap-btn-close")) {
      closeModal();
      return;
    }
  }, true);

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
