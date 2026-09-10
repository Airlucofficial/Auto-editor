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

// =========================================================================
  // ENHANCED AUTOEDITOR STUDIO CONTROLLER & AUDIO/VISUAL ENGINE
  // =========================================================================

  // Global Application State for Enhanced Studio Features
  window._CAPTION_POS = window._CAPTION_POS || { x: 0.5, y: 0.85, scale: 1.0 };
  window._CURRENT_STYLE = window._CURRENT_STYLE || "classic";
  window._VOICEOVER_VOLUME = (window._VOICEOVER_VOLUME !== undefined) ? window._VOICEOVER_VOLUME : 1.0;
  window._SFX_ENABLED = false; // Opt-in only, strictly off by default
  window._SFX_VOLUME = (window._SFX_VOLUME !== undefined) ? window._SFX_VOLUME : 0.5;
  window._SELECTED_SFX = window._SELECTED_SFX || "auto"; // Default to Smart Auto
  window._CLIP_VOICE_SETTINGS = window._CLIP_VOICE_SETTINGS || {};
  let currentDrawerCategory = "all";
  let drawerSearchQuery = "";
  let isMonitorDrawerExpanded = false;
  let isSidebarDrawerExpanded = false;
  let lastSfxTriggerTime = -1;

  // 12 High Quality 44.1kHz Transition Sound Effects Catalog
  const SFX_CATALOG = [
    { id: "whoosh_fast", name: "Fast Whip Whoosh", icon: "💨", category: "motion", url: "/sfx/whoosh_fast.wav" },
    { id: "swoosh_smooth", name: "Cinematic Swoosh", icon: "🌊", category: "motion", url: "/sfx/swoosh_smooth.wav" },
    { id: "camera_click", name: "Camera Shutter", icon: "📸", category: "foley", url: "/sfx/camera_click.wav" },
    { id: "bubble_pop", name: "Bubble Pop", icon: "🫧", category: "retro", url: "/sfx/bubble_pop.wav" },
    { id: "cinematic_boom", name: "Cinematic Sub Boom", icon: "💥", category: "impact", url: "/sfx/cinematic_boom.wav" },
    { id: "digital_glitch", name: "Digital Glitch", icon: "⚡", category: "electronic", url: "/sfx/digital_glitch.wav" },
    { id: "gentle_chime", name: "Gentle Bell Chime", icon: "🔔", category: "ambient", url: "/sfx/gentle_chime.wav" },
    { id: "paper_turn", name: "Paper Turn", icon: "📄", category: "foley", url: "/sfx/paper_turn.wav" },
    { id: "snappy_switch", name: "Tactile Click", icon: "🔘", category: "foley", url: "/sfx/snappy_switch.wav" },
    { id: "impact_punch", name: "Punch Impact", icon: "🥊", category: "impact", url: "/sfx/impact_punch.wav" },
    { id: "cinematic_riser", name: "Tension Riser", icon: "📈", category: "motion", url: "/sfx/cinematic_riser.wav" },
    { id: "short_woosh", name: "Snappy Micro-Woosh", icon: "🌪️", category: "motion", url: "/sfx/short_woosh.wav" }
  ];

  // Helper to convert ASS hex color &H[AA]BBGGRR to standard CSS hex #RRGGBB
  function parseAssColor(assStr, defaultHex) {
    if (!assStr || typeof assStr !== "string") return defaultHex || "#ffffff";
    if (assStr.startsWith("#")) return assStr;
    const m = assStr.match(/&H(?:[0-9A-Fa-f]{2})?([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})&?/i);
    if (m) {
      const b = m[1], g = m[2], r = m[3];
      return `#${r}${g}${b}`;
    }
    return defaultHex || "#ffffff";
  }

  // Web Audio Context & SFX player
  const _sfxAudioCache = {};
  function playSFX(sfxId, volume) {
    if (!sfxId || sfxId === "none") return;
    const actualId = (sfxId === "auto") ? "whoosh_fast" : sfxId;
    const item = SFX_CATALOG.find(s => s.id === actualId);
    if (!item) return;
    const vol = (volume !== undefined) ? volume : (window._SFX_VOLUME !== undefined ? window._SFX_VOLUME : 0.5);
    try {
      let audio = _sfxAudioCache[actualId];
      if (!audio) {
        audio = new Audio(item.url);
        _sfxAudioCache[actualId] = audio;
      }
      audio.volume = Math.max(0, Math.min(1, vol));
      audio.currentTime = 0;
      audio.play().catch(() => {});
    } catch (e) {}
  }

  // Smart Auto-Selection for transition sound effect based on cut transition style
  function getSmartAutoSFX(transitionType) {
    const t = (transitionType || "").toLowerCase();
    if (t.includes("wipe")) return "whoosh_fast";
    if (t.includes("slide")) return "swoosh_smooth";
    if (t.includes("black")) return "cinematic_boom";
    if (t.includes("fade")) return "gentle_chime";
    if (t.includes("circle")) return "bubble_pop";
    if (t.includes("cut") || !t || t === "none") return "camera_click";
    return "whoosh_fast";
  }
  if (typeof window !== "undefined") {
    window._GET_SMART_SFX = getSmartAutoSFX;
  }

  // Web Audio Master Voiceover Volume Booster (0% to 200%) & Playback Engine
  let _voiceAudioCtx = null;
  let _voiceGainNode = null;
  let _voiceSourceNode = null;

  // Silent audio generator for running timeline without voiceover
  function createSilentAudioUrl(durationSec = 60) {
    try {
      const sampleRate = 8000;
      const numSamples = Math.ceil(sampleRate * Math.min(3600, durationSec || 60));
      const buffer = new ArrayBuffer(44 + numSamples * 2);
      const view = new DataView(buffer);
      view.setUint32(0, 0x52494646, false); // 'RIFF'
      view.setUint32(4, 36 + numSamples * 2, true);
      view.setUint32(8, 0x57415645, false); // 'WAVE'
      view.setUint32(12, 0x666d7420, false); // 'fmt '
      view.setUint32(16, 16, true);
      view.setUint16(20, 1, true); // PCM
      view.setUint16(22, 1, true); // Mono
      view.setUint32(24, sampleRate, true);
      view.setUint32(28, sampleRate * 2, true);
      view.setUint16(32, 2, true);
      view.setUint16(34, 16, true);
      view.setUint32(36, 0x64617461, false); // 'data'
      view.setUint32(40, numSamples * 2, true);
      const blob = new Blob([buffer], { type: 'audio/wav' });
      return URL.createObjectURL(blob);
    } catch (e) {
      return "";
    }
  }

  // Ensure audio is unmuted and AudioContext is resumed on user interaction
  function ensureEditorAudioReady() {
    const audioEl = window._VOICEOVER_AUDIO_EL || document.querySelector("audio");
    if (audioEl) {
      audioEl.muted = ((window._VOICEOVER_VOLUME !== undefined ? window._VOICEOVER_VOLUME : 1.0) <= 0);
      if (!audioEl.src || audioEl.src === window.location.href || audioEl.src.endsWith("/")) {
        if (!window._silentClockUrl) {
          window._silentClockUrl = createSilentAudioUrl(Math.max(60, window._TIMELINE_DURATION || 60));
        }
        audioEl.src = window._silentClockUrl;
      }
    }
    if (_voiceAudioCtx && _voiceAudioCtx.state === "suspended") {
      _voiceAudioCtx.resume().catch(() => {});
    }
  }

  if (typeof document !== "undefined") {
    document.addEventListener("click", ensureEditorAudioReady, { passive: true });
    document.addEventListener("keydown", (e) => {
      if (e.code === "Space" || e.code === "ArrowLeft" || e.code === "ArrowRight") {
        ensureEditorAudioReady();
      }
    }, { passive: true });
  }

  function setMasterVoiceVolume(v) {
    window._VOICEOVER_VOLUME = v;
    const audioEl = window._VOICEOVER_AUDIO_EL || document.querySelector("audio");
    if (!audioEl) return;
    try {
      audioEl.muted = (v <= 0);
      if (v <= 1.0) {
        audioEl.volume = Math.max(0, Math.min(1.0, v));
      } else {
        if (!_voiceAudioCtx) {
          const AudioCtx = window.AudioContext || window.webkitAudioContext;
          if (AudioCtx) _voiceAudioCtx = new AudioCtx();
        }
        if (_voiceAudioCtx && !_voiceSourceNode && !audioEl._hasVoiceSource) {
          audioEl._hasVoiceSource = true;
          _voiceSourceNode = _voiceAudioCtx.createMediaElementSource(audioEl);
          _voiceGainNode = _voiceAudioCtx.createGain();
          _voiceSourceNode.connect(_voiceGainNode);
          _voiceGainNode.connect(_voiceAudioCtx.destination);
        }
        if (_voiceGainNode) {
          if (_voiceAudioCtx.state === "suspended") {
            _voiceAudioCtx.resume().catch(() => {});
          }
          _voiceGainNode.gain.setValueAtTime(v, _voiceAudioCtx.currentTime);
          audioEl.volume = 1.0;
        } else {
          audioEl.volume = 1.0;
        }
      }
    } catch (e) {
      audioEl.volume = Math.max(0, Math.min(1.0, v));
    }
  }

  // -------------------------------------------------------------------------
  // Studio History Manager (Step Back / Step Forward / Reset to Default)
  // -------------------------------------------------------------------------
  const StudioHistory = {
    stack: [],
    index: -1,
    maxSize: 50,
    isApplying: false,

    capture() {
      return {
        style: window._CURRENT_STYLE || "classic",
        pos: { ...(window._CAPTION_POS || { x: 0.5, y: 0.85, scale: 1.0 }) },
        voiceVol: (window._VOICEOVER_VOLUME !== undefined) ? window._VOICEOVER_VOLUME : 1.0,
        sfxEnabled: !!window._SFX_ENABLED,
        sfxVol: (window._SFX_VOLUME !== undefined) ? window._SFX_VOLUME : 0.5,
        selectedSfx: window._SELECTED_SFX || "auto"
      };
    },

    push(label, isInitial = false) {
      if (this.isApplying) return;
      const snap = this.capture();
      if (!isInitial && this.index >= 0) {
        const prev = this.stack[this.index];
        if (JSON.stringify(prev) === JSON.stringify(snap)) return;
      }
      if (this.index < this.stack.length - 1) {
        this.stack = this.stack.slice(0, this.index + 1);
      }
      this.stack.push(snap);
      if (this.stack.length > this.maxSize) {
        this.stack.shift();
      }
      this.index = this.stack.length - 1;
      this.updateButtons();
    },

    stepBack() {
      // Step back React timeline history if available
      if (window._REACT_UNDO && window._REACT_CAN_UNDO && window._REACT_CAN_UNDO()) {
        window._REACT_UNDO();
      } else {
        const reactUndo = document.querySelector('.history button[aria-label="Undo"]');
        if (reactUndo && !reactUndo.disabled) {
          reactUndo.click();
        }
      }

      // Step back Studio history
      if (this.index > 0) {
        this.index--;
        this.apply(this.stack[this.index]);
      }
      this.updateButtons();
    },

    stepForward() {
      // Step forward React timeline history if available
      if (window._REACT_REDO && window._REACT_CAN_REDO && window._REACT_CAN_REDO()) {
        window._REACT_REDO();
      } else {
        const reactRedo = document.querySelector('.history button[aria-label="Redo"]');
        if (reactRedo && !reactRedo.disabled) {
          reactRedo.click();
        }
      }

      // Step forward Studio history
      if (this.index < this.stack.length - 1) {
        this.index++;
        this.apply(this.stack[this.index]);
      }
      this.updateButtons();
    },

    apply(snap) {
      if (!snap) return;
      this.isApplying = true;
      try {
        window._CURRENT_STYLE = snap.style;
        window._CAPTION_POS = { ...snap.pos };
        window._VOICEOVER_VOLUME = snap.voiceVol;
        window._SFX_ENABLED = snap.sfxEnabled;
        window._SFX_VOLUME = snap.sfxVol;
        window._SELECTED_SFX = snap.selectedSfx;

        if (window._SET_REACT_CAPTION_STYLE) {
          window._SET_REACT_CAPTION_STYLE(snap.style);
        }

        if (typeof updateMonitorBoxPosition === "function") {
          updateMonitorBoxPosition();
        }
        if (typeof syncAllUIControls === "function") {
          syncAllUIControls();
        }
        if (typeof window !== "undefined" && window._CANVAS_REDRAW) window._CANVAS_REDRAW();
      } finally {
        this.isApplying = false;
      }
    },

    resetToDefault() {
      this.isApplying = true;
      try {
        window._CURRENT_STYLE = "classic";
        window._CAPTION_POS = { x: 0.5, y: 0.85, scale: 1.0 };
        window._VOICEOVER_VOLUME = 1.0;
        window._SFX_ENABLED = false;
        window._SFX_VOLUME = 0.5;
        window._SELECTED_SFX = "auto";
        window._CLIP_VOICE_SETTINGS = {};

        if (window._SET_REACT_CAPTION_STYLE) {
          window._SET_REACT_CAPTION_STYLE("classic");
        }

        const clearMotionBtn = Array.from(document.querySelectorAll(".panel button")).find(b => b.innerText.trim() === "Clear");
        if (clearMotionBtn) clearMotionBtn.click();

        if (typeof updateMonitorBoxPosition === "function") {
          updateMonitorBoxPosition();
        }
        if (typeof syncAllUIControls === "function") {
          syncAllUIControls();
        }
        if (typeof window !== "undefined" && window._CANVAS_REDRAW) window._CANVAS_REDRAW();
      } finally {
        this.isApplying = false;
      }
      this.push("Reset to Default");
    },

    updateButtons() {
      const btnBack = document.getElementById("btn-step-back");
      const btnFwd = document.getElementById("btn-step-forward");
      const canReactUndo = window._REACT_CAN_UNDO ? window._REACT_CAN_UNDO() : (document.querySelector('.history button[aria-label="Undo"]:not(:disabled)') !== null);
      const canReactRedo = window._REACT_CAN_REDO ? window._REACT_CAN_REDO() : (document.querySelector('.history button[aria-label="Redo"]:not(:disabled)') !== null);

      if (btnBack) btnBack.disabled = (this.index <= 0 && !canReactUndo);
      if (btnFwd) btnFwd.disabled = (this.index >= this.stack.length - 1 && !canReactRedo);
    },

    init() {
      if (this.stack.length === 0) {
        this.push("Initial State", true);
      }
      this.updateButtons();
    }
  };

  // Sync all sliders, badges, and chips when state changes
  function syncAllUIControls() {
    syncSidebarPositionControls();

    // Voice Volume
    const voiceSlider = document.getElementById("cap-voice-vol-slider");
    const voiceVal = document.getElementById("cap-voice-vol-val");
    const vol = window._VOICEOVER_VOLUME !== undefined ? window._VOICEOVER_VOLUME : 1.0;
    if (voiceSlider) voiceSlider.value = vol;
    if (voiceVal) voiceVal.innerText = vol <= 0.01 ? "0% (Muted)" : `${Math.round(vol * 100)}%`;
    setMasterVoiceVolume(vol);

    // SFX Settings
    const chkSfx = document.getElementById("chk-enable-sfx");
    const sfxBody = document.getElementById("cap-sfx-body");
    const sfxVolSlider = document.getElementById("slider-sfx-vol");
    const sfxVolVal = document.getElementById("val-sfx-vol");
    if (chkSfx) chkSfx.checked = !!window._SFX_ENABLED;
    if (sfxBody) sfxBody.style.display = window._SFX_ENABLED ? "block" : "none";
    if (sfxVolSlider) sfxVolSlider.value = window._SFX_VOLUME !== undefined ? window._SFX_VOLUME : 0.5;
    if (sfxVolVal) sfxVolVal.innerText = `${Math.round((window._SFX_VOLUME || 0.5) * 100)}%`;

    // Active Style Chips & Cards
    const curStyle = window._CURRENT_STYLE || "classic";
    const sObj = allStyles.find(item => item.id === curStyle) || allStyles[0];
    const activeLabel = document.getElementById("cap-active-style-name");
    if (activeLabel && sObj) activeLabel.innerText = sObj.name;

    document.querySelectorAll(".cap-preset-chip, .cap-monitor-chip").forEach(chip => {
      chip.classList.toggle("is-active", chip.getAttribute("data-style") === curStyle);
    });
    document.querySelectorAll(".cap-drawer-card").forEach(card => {
      card.classList.toggle("selected", card.getAttribute("data-style") === curStyle);
    });

    // SFX Active Chips
    const curSfx = window._SELECTED_SFX || "auto";
    document.querySelectorAll(".cap-sfx-chip").forEach(chip => {
      chip.classList.toggle("is-active", chip.getAttribute("data-sfx") === curSfx);
    });

    StudioHistory.updateButtons();
  }

  // -------------------------------------------------------------------------
  // Live Audio Playback Watcher (Sync Master Volume & Trigger Transition SFX)
  // -------------------------------------------------------------------------
  function setupAudioPlaybackWatchers() {
    const audioEl = document.querySelector('audio');
    if (!audioEl || audioEl._hasSfxWatcher) return;
    audioEl._hasSfxWatcher = true;

    setMasterVoiceVolume(window._VOICEOVER_VOLUME !== undefined ? window._VOICEOVER_VOLUME : 1.0);

    audioEl.addEventListener('play', () => {
      setMasterVoiceVolume(window._VOICEOVER_VOLUME !== undefined ? window._VOICEOVER_VOLUME : 1.0);
    });

    // Precise cut watcher during playback
    audioEl.addEventListener('timeupdate', () => {
      if (!window._SFX_ENABLED) return;
      const curTime = audioEl.currentTime;

      // 1. Direct inspection from exposed window._TIMELINE_CLIPS
      const clips = window._TIMELINE_CLIPS || [];
      const transMap = window._TIMELINE_TRANSITIONS || {};

      if (clips.length > 1) {
        for (let i = 1; i < clips.length; i++) {
          const cutSec = clips[i].start;
          if (cutSec > 0.05 && Math.abs(curTime - cutSec) < 0.22) {
            if (Math.abs(lastSfxTriggerTime - cutSec) > 0.7) {
              lastSfxTriggerTime = cutSec;
              const cutTransition = transMap[clips[i].name] || "wipeleft";
              const sfxId = (window._SELECTED_SFX && window._SELECTED_SFX !== "auto") ? window._SELECTED_SFX : getSmartAutoSFX(cutTransition);
              playSFX(sfxId, window._SFX_VOLUME);
              break;
            }
          }
        }
      } else {
        // Fallback: DOM inspection of cut buttons
        const cutButtons = document.querySelectorAll('.tl__cuts button.cut');
        const audioDur = audioEl.duration || 1;
        cutButtons.forEach(btn => {
          const leftPctStr = btn.style.left;
          if (leftPctStr && leftPctStr.includes('%')) {
            const cutSec = (parseFloat(leftPctStr) / 100) * audioDur;
            if (cutSec > 0.05 && Math.abs(curTime - cutSec) < 0.25) {
              if (Math.abs(lastSfxTriggerTime - cutSec) > 0.7) {
                lastSfxTriggerTime = cutSec;
                const title = btn.getAttribute('title') || '';
                const autoSfx = getSmartAutoSFX(title);
                playSFX(window._SELECTED_SFX || autoSfx, window._SFX_VOLUME);
              }
            }
          }
        });
      }
    });
  }

  // -------------------------------------------------------------------------
  // Canvas Caption Drawing Hook: 100% Visual Fidelity for all 64 Styles
  // -------------------------------------------------------------------------
  window._DRAW_CAPTION = function(ctx, text, width, height, styleKey, fontSize, lineHeight, currentTime, cues) {
    const activeKey = window._CURRENT_STYLE || styleKey || "classic";
    const s = allStyles.find(item => item.id === activeKey) || allStyles[0];
    if (!s) return false;

    // Use placeholder text if no active caption cue is playing so user can place and resize on monitor
    const isPlaceholder = !text;
    const displayText = text || (window._SHOW_CAPTION_PREVIEW ? (s.name.toUpperCase() + " CAPTION") : "[ CAPTION PLACEMENT ]");

    const pos = window._CAPTION_POS || { x: 0.5, y: 0.85, scale: 1.0 };
    const fontScale = pos.scale || 1.0;
    const finalFontSize = Math.max(14, Math.round(fontSize * fontScale));
    const fontFam = (s.css && s.css.fontFamily) || s.font || '"CaptionFont", system-ui, sans-serif';
    const isUpper = !!s.uppercase;
    const rawText = isUpper ? displayText.toUpperCase() : displayText;

    const maxChars = Math.max(8, Math.floor(0.9 * width / (0.58 * finalFontSize)));
    const words = rawText.split(/\s+/).filter(Boolean);
    const lines = [];
    let curLine = "";
    for (const w of words) {
      const testLine = curLine ? `${curLine} ${w}` : w;
      if (curLine && testLine.length > maxChars) {
        lines.push(curLine);
        curLine = w;
      } else {
        curLine = testLine;
      }
    }
    if (curLine) lines.push(curLine);

    const lineCount = lines.length || 1;
    const lineSpacing = lineHeight > 0 ? lineHeight : 1.22;

    const centerX = (pos.x !== undefined ? pos.x : 0.5) * width;
    const targetY = (pos.y !== undefined ? pos.y : 0.85) * height;
    const totalBlockHeight = lineCount * finalFontSize * lineSpacing;
    const startY = targetY - totalBlockHeight / 2 + finalFontSize * 0.8;

    ctx.save();
    ctx.font = `${s.bold ? 'bold ' : '700 '}${finalFontSize}px ${fontFam}`;
    ctx.textAlign = "center";
    ctx.textBaseline = "alphabetic";

    // Precise Colors
    const primaryColor = (s.css && s.css.color) || parseAssColor(s.primary_color, "#ffffff");
    const activeColor = (s.css && s.css.activeColor) || parseAssColor(s.active_color, "#facc15");
    const outlineColor = parseAssColor(s.outline_color, "#000000");
    const strokeWidth = s.outline ? Math.max(2.5, s.outline * 1.3 * (finalFontSize / 44)) : Math.max(2, finalFontSize / 7);

    // Active word index calculation
    let activeWordIdx = -1;
    if (!isPlaceholder && currentTime !== undefined) {
      const cueList = cues || window._CAPTION_CUES || [];
      const curCue = cueList.find(c => currentTime >= c.start && currentTime <= c.end);
      if (curCue) {
        const dur = Math.max(0.05, curCue.end - curCue.start);
        const prog = Math.max(0, Math.min(0.999, (currentTime - curCue.start) / dur));
        activeWordIdx = Math.floor(prog * words.length);
      }
    } else if (isPlaceholder) {
      activeWordIdx = 0; // Highlight first word in preview mode
    }

    let maxLineWidth = 0;
    for (let i = 0; i < lineCount; i++) {
      const w = ctx.measureText(lines[i]).width;
      if (w > maxLineWidth) maxLineWidth = w;
    }

    // Boxed / Pill background
    const hasBox = (s.css && s.css.background) || s.category === "boxed_pill" || s.animation_type === "box_pill";
    if (hasBox) {
      const boxPadX = 0.40 * finalFontSize;
      const boxPadY = 0.20 * finalFontSize;
      const boxBg = (s.css && s.css.background) || parseAssColor(s.back_color, "rgba(0, 0, 0, 0.75)");
      ctx.fillStyle = boxBg;
      for (let i = 0; i < lineCount; i++) {
        const lineW = ctx.measureText(lines[i]).width;
        const lineY = startY + i * finalFontSize * lineSpacing;
        const boxX = centerX - lineW / 2 - boxPadX;
        const boxY = lineY - finalFontSize * 0.85 - boxPadY;
        const boxW = lineW + boxPadX * 2;
        const boxH = finalFontSize * 1.05 + boxPadY * 2;
        ctx.beginPath();
        if (typeof ctx.roundRect === "function") {
          ctx.roundRect(boxX, boxY, boxW, boxH, 8);
        } else {
          ctx.rect(boxX, boxY, boxW, boxH);
        }
        ctx.fill();
      }
    }

    // Neon Glow & Shadows
    if (s.category === "neon_glow") {
      ctx.shadowColor = activeColor;
      ctx.shadowBlur = Math.max(12, finalFontSize * 0.40);
    } else if (s.shadow) {
      ctx.shadowColor = "rgba(0, 0, 0, 0.85)";
      ctx.shadowBlur = s.shadow * 2.5;
      ctx.shadowOffsetX = s.shadow;
      ctx.shadowOffsetY = s.shadow;
    }

    // Word-by-word drawing with active highlights & bounce pop
    let globalWordCounter = 0;
    for (let i = 0; i < lineCount; i++) {
      const lineText = lines[i];
      const lineWords = lineText.split(/\s+/).filter(Boolean);
      const lineY = startY + i * finalFontSize * lineSpacing;
      const lineTotalW = ctx.measureText(lineText).width;
      let curX = centerX - lineTotalW / 2;

      for (let j = 0; j < lineWords.length; j++) {
        const wordStr = lineWords[j];
        const wordW = ctx.measureText(wordStr).width;
        const spaceW = ctx.measureText(" ").width;
        const wordCenterX = curX + wordW / 2;
        const isWordActive = (globalWordCounter === activeWordIdx);

        ctx.save();
        if (isWordActive && (s.animation_type === "bounce_pop" || s.category === "viral_shorts")) {
          // Bouncy scale pop
          ctx.translate(wordCenterX, lineY);
          ctx.scale(1.08, 1.08);
          ctx.translate(-wordCenterX, -lineY);
        }

        // Active Boxed Pill Highlight Background
        if (isWordActive && s.category === "boxed_pill") {
          const pillBg = (s.css && s.css.activeBg) || activeColor;
          ctx.fillStyle = pillBg;
          const pPadX = 0.20 * finalFontSize;
          const pPadY = 0.12 * finalFontSize;
          ctx.beginPath();
          if (typeof ctx.roundRect === "function") {
            ctx.roundRect(curX - pPadX, lineY - finalFontSize * 0.85 - pPadY, wordW + pPadX * 2, finalFontSize * 1.05 + pPadY * 2, 6);
          } else {
            ctx.rect(curX - pPadX, lineY - finalFontSize * 0.85 - pPadY, wordW + pPadX * 2, finalFontSize * 1.05 + pPadY * 2);
          }
          ctx.fill();
        }

        // Stroke Outline
        ctx.lineJoin = "round";
        ctx.miterLimit = 2;
        ctx.lineWidth = strokeWidth;
        ctx.strokeStyle = outlineColor;
        ctx.strokeText(wordStr, wordCenterX, lineY);

        // Fill Text
        ctx.fillStyle = isWordActive ? activeColor : primaryColor;
        ctx.fillText(wordStr, wordCenterX, lineY);
        ctx.restore();

        curX += wordW + spaceW;
        globalWordCounter++;
      }
    }

    ctx.restore();

    // Update the on-monitor interactive placement and resize box
    updateMonitorOverlayBox(centerX, targetY, maxLineWidth + finalFontSize * 0.6, totalBlockHeight + finalFontSize * 0.4, width, height);

    return true;
  };

  // -------------------------------------------------------------------------
  // On-Monitor Draggable & Resizable Caption Bounding Box (Req 2)
  // -------------------------------------------------------------------------
  function updateMonitorOverlayBox(cx, cy, bw, bh, canvasW, canvasH) {
    const box = document.getElementById("cap-monitor-box");
    const overlay = document.getElementById("cap-monitor-overlay");
    const canvas = document.querySelector(".viewer__canvas");
    if (!box || !overlay || !canvas) return;

    const frame = overlay.parentElement;
    if (!frame) return;

    const frameRect = frame.getBoundingClientRect();
    const canvasRect = canvas.getBoundingClientRect();
    if (!frameRect.width || !canvasRect.width) return;

    const scaleX = canvasRect.width / canvasW;
    const scaleY = canvasRect.height / canvasH;

    const cssCenterX = canvasRect.left - frameRect.left + (cx * scaleX);
    const cssCenterY = canvasRect.top - frameRect.top + (cy * scaleY);
    const cssW = Math.max(80, bw * scaleX);
    const cssH = Math.max(36, bh * scaleY);

    if (!box._isDragging && !box._isResizing) {
      box.style.left = `${cssCenterX - cssW / 2}px`;
      box.style.top = `${cssCenterY - cssH / 2}px`;
      box.style.width = `${cssW}px`;
      box.style.height = `${cssH}px`;
      box.style.display = "block";
    }

    const badge = document.getElementById("cap-monitor-badge");
    if (badge) {
      const xPct = Math.round((window._CAPTION_POS.x || 0.5) * 100);
      const yPct = Math.round((window._CAPTION_POS.y || 0.85) * 100);
      const scPct = Math.round((window._CAPTION_POS.scale || 1.0) * 100);
      badge.innerText = `Caption · X: ${xPct}% · Y: ${yPct}% · Size: ${scPct}%`;
    }
  }

  function updateMonitorBoxPosition() {
    const box = document.getElementById("cap-monitor-box");
    const overlay = document.getElementById("cap-monitor-overlay");
    const canvas = document.querySelector(".viewer__canvas");
    if (!box || !overlay) return;

    const frame = overlay.parentElement;
    if (!frame) return;

    const frameRect = frame.getBoundingClientRect();
    const canvasRect = canvas ? canvas.getBoundingClientRect() : frameRect;
    if (!canvasRect.width || !frameRect.width) return;

    const scale = (window._CAPTION_POS && window._CAPTION_POS.scale) || 1.0;
    const posX = (window._CAPTION_POS && window._CAPTION_POS.x !== undefined) ? window._CAPTION_POS.x : 0.5;
    const posY = (window._CAPTION_POS && window._CAPTION_POS.y !== undefined) ? window._CAPTION_POS.y : 0.85;

    const boxW = Math.max(120, Math.min(canvasRect.width * 0.9, 240 * scale));
    const boxH = Math.max(38, Math.min(canvasRect.height * 0.5, 60 * scale));

    const offsetLeft = canvas ? (canvasRect.left - frameRect.left) : 0;
    const offsetTop = canvas ? (canvasRect.top - frameRect.top) : 0;

    const centerX = offsetLeft + (posX * canvasRect.width);
    const centerY = offsetTop + (posY * canvasRect.height);

    box.style.width = `${Math.round(boxW)}px`;
    box.style.height = `${Math.round(boxH)}px`;
    box.style.left = `${Math.round(centerX - boxW / 2)}px`;
    box.style.top = `${Math.round(centerY - boxH / 2)}px`;
    box.style.display = "block";

    const badge = document.getElementById("cap-monitor-badge");
    if (badge) {
      badge.innerText = `Caption · X: ${Math.round(posX * 100)}% · Y: ${Math.round(posY * 100)}% · Size: ${Math.round(scale * 100)}%`;
    }
  }

  function injectMonitorCaptionBox() {
    const frame = document.querySelector(".viewer__frame");
    if (!frame || document.getElementById("cap-monitor-overlay")) return;

    frame.style.position = "relative";

    const overlay = document.createElement("div");
    overlay.id = "cap-monitor-overlay";
    overlay.className = "cap-monitor-overlay";

    overlay.innerHTML = `
      <div id="cap-monitor-box" class="cap-monitor-box" style="display: block;" title="Drag anywhere to reposition caption. Drag handles to resize.">
        <div class="cap-monitor-badge" id="cap-monitor-badge">Caption · X: 50% · Y: 85% · Size: 100%</div>
        <div class="cap-handle cap-handle-nw" data-handle="nw"></div>
        <div class="cap-handle cap-handle-ne" data-handle="ne"></div>
        <div class="cap-handle cap-handle-sw" data-handle="sw"></div>
        <div class="cap-handle cap-handle-se" data-handle="se"></div>
        <div class="cap-handle cap-handle-n" data-handle="n"></div>
        <div class="cap-handle cap-handle-s" data-handle="s"></div>
        <div class="cap-handle cap-handle-w" data-handle="w"></div>
        <div class="cap-handle cap-handle-e" data-handle="e"></div>
      </div>
    `;

    frame.appendChild(overlay);
    updateMonitorBoxPosition();

    const box = overlay.querySelector("#cap-monitor-box");
    let isDragging = false;
    let isResizing = false;
    let activeHandle = null;
    let startX = 0, startY = 0;
    let initialBoxLeft = 0, initialBoxTop = 0, initialBoxW = 0, initialBoxH = 0;
    let initialPosX = 0.5, initialPosY = 0.85, initialScale = 1.0;

    box.addEventListener("pointerdown", (e) => {
      const handle = e.target.getAttribute("data-handle");
      const canvas = document.querySelector(".viewer__canvas");
      if (!canvas) return;
      const cRect = canvas.getBoundingClientRect();
      const fRect = frame.getBoundingClientRect();

      startX = e.clientX;
      startY = e.clientY;
      initialBoxLeft = parseFloat(box.style.left) || ((cRect.left - fRect.left) + (cRect.width * 0.5 - 120));
      initialBoxTop = parseFloat(box.style.top) || ((cRect.top - fRect.top) + (cRect.height * 0.85 - 30));
      initialBoxW = parseFloat(box.style.width) || 240;
      initialBoxH = parseFloat(box.style.height) || 60;

      initialPosX = (window._CAPTION_POS && window._CAPTION_POS.x !== undefined) ? window._CAPTION_POS.x : 0.5;
      initialPosY = (window._CAPTION_POS && window._CAPTION_POS.y !== undefined) ? window._CAPTION_POS.y : 0.85;
      initialScale = (window._CAPTION_POS && window._CAPTION_POS.scale) || 1.0;

      window._IS_PLACING_CAPTION = true;

      if (handle) {
        isResizing = true;
        box._isResizing = true;
        activeHandle = handle;
      } else {
        isDragging = true;
        box._isDragging = true;
        box.classList.add("is-dragging");
      }
      e.stopPropagation();

      const onPointerMove = (ev) => {
        const deltaX = ev.clientX - startX;
        const deltaY = ev.clientY - startY;

        if (isDragging) {
          const newLeft = initialBoxLeft + deltaX;
          const newTop = initialBoxTop + deltaY;
          box.style.left = `${newLeft}px`;
          box.style.top = `${newTop}px`;

          const offsetLeft = cRect.left - fRect.left;
          const offsetTop = cRect.top - fRect.top;
          const centerBoxX = newLeft + initialBoxW / 2 - offsetLeft;
          const centerBoxY = newTop + initialBoxH / 2 - offsetTop;

          const normX = Math.max(0.05, Math.min(0.95, centerBoxX / cRect.width));
          const normY = Math.max(0.05, Math.min(0.95, centerBoxY / cRect.height));

          window._CAPTION_POS.x = normX;
          window._CAPTION_POS.y = normY;

          syncSidebarPositionControls();
          if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
        } else if (isResizing) {
          const dyNorm = deltaY / cRect.height;
          const scaleDelta = (activeHandle.includes("n") ? -dyNorm : dyNorm) * 2.2;
          const newScale = Math.max(0.35, Math.min(2.8, initialScale + scaleDelta));
          window._CAPTION_POS.scale = newScale;

          const wRatio = newScale / initialScale;
          box.style.width = `${Math.max(60, initialBoxW * wRatio)}px`;
          box.style.height = `${Math.max(28, initialBoxH * wRatio)}px`;

          syncSidebarPositionControls();
          if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
        }
      };

      const onPointerUp = () => {
        isDragging = false;
        isResizing = false;
        box._isDragging = false;
        box._isResizing = false;
        box.classList.remove("is-dragging");
        window._IS_PLACING_CAPTION = false;
        window.removeEventListener("pointermove", onPointerMove);
        window.removeEventListener("pointerup", onPointerUp);

        // Push state to StudioHistory
        StudioHistory.push("Reposition Caption");
        if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
      };

      window.addEventListener("pointermove", onPointerMove);
      window.addEventListener("pointerup", onPointerUp);
    });

    window.addEventListener("resize", () => {
      updateMonitorBoxPosition();
    });
  }

  function syncSidebarPositionControls() {
    const posXRange = document.getElementById("cap-pos-x-range");
    const posYRange = document.getElementById("cap-pos-y-range");
    const scaleRange = document.getElementById("cap-scale-range");
    const posXVal = document.getElementById("cap-pos-x-val");
    const posYVal = document.getElementById("cap-pos-y-val");
    const scaleVal = document.getElementById("cap-scale-val");

    const xPct = Math.round((window._CAPTION_POS.x || 0.5) * 100);
    const yPct = Math.round((window._CAPTION_POS.y || 0.85) * 100);
    const scPct = Math.round((window._CAPTION_POS.scale || 1.0) * 100);

    if (posXRange) posXRange.value = window._CAPTION_POS.x || 0.5;
    if (posYRange) posYRange.value = window._CAPTION_POS.y || 0.85;
    if (scaleRange) scaleRange.value = window._CAPTION_POS.scale || 1.0;
    if (posXVal) posXVal.innerText = `${xPct}%`;
    if (posYVal) posYVal.innerText = `${yPct}%`;
    if (scaleVal) scaleVal.innerText = `${scPct}%`;

    const badge = document.getElementById("cap-monitor-badge");
    if (badge) {
      badge.innerText = `Caption · X: ${xPct}% · Y: ${yPct}% · Size: ${scPct}%`;
    }
  }

  // -------------------------------------------------------------------------
  // 1. Caption Styles Bar on Video Monitor Window (Req 1)
  // -------------------------------------------------------------------------
  function injectMonitorCaptionStylesBar() {
    const viewer = document.querySelector(".viewer");
    if (!viewer || document.getElementById("cap-monitor-styles-bar")) return;

    const bar = document.createElement("div");
    bar.id = "cap-monitor-styles-bar";
    bar.className = "cap-monitor-styles-bar";

    bar.innerHTML = `
      <div class="cap-monitor-bar-inner">
        <span class="cap-monitor-bar-label">✨ Caption Styles:</span>
        <div class="cap-monitor-chips-row" id="cap-monitor-chips-container">
          <!-- Populated dynamically -->
        </div>
        <button type="button" class="cap-monitor-expand-btn ${isMonitorDrawerExpanded ? 'is-expanded' : ''}" id="btn-monitor-expand-styles">
          <span id="txt-monitor-expand">${isMonitorDrawerExpanded ? 'Collapse' : 'All 64 Styles'}</span>
          <span class="cap-arrow-icon">▼</span>
        </button>
      </div>
      <div class="cap-monitor-drawer ${isMonitorDrawerExpanded ? 'is-open' : ''}" id="cap-monitor-drawer">
        <div class="cap-drawer-controls">
          <input type="text" class="cap-drawer-search" id="cap-monitor-search-input" placeholder="🔍 Search 64 styles (e.g. Hormozi, Neon, TikTok, Bouncy...)" value="${drawerSearchQuery}">
          <div class="cap-drawer-categories" id="cap-monitor-categories-container">
            <!-- Populated dynamically -->
          </div>
        </div>
        <div class="cap-drawer-grid" id="cap-monitor-grid-container">
          <!-- Populated dynamically -->
        </div>
      </div>
    `;

    // Insert directly beneath the video canvas inside .viewer
    const transport = viewer.querySelector(".transport");
    if (transport) {
      viewer.insertBefore(bar, transport);
    } else {
      viewer.appendChild(bar);
    }

    const toggleBtn = bar.querySelector("#btn-monitor-expand-styles");
    toggleBtn.onclick = () => {
      isMonitorDrawerExpanded = !isMonitorDrawerExpanded;
      toggleBtn.classList.toggle("is-expanded", isMonitorDrawerExpanded);
      const drawer = document.getElementById("cap-monitor-drawer");
      if (drawer) drawer.classList.toggle("is-open", isMonitorDrawerExpanded);
      const txt = document.getElementById("txt-monitor-expand");
      if (txt) txt.innerText = isMonitorDrawerExpanded ? "Collapse" : "All 64 Styles";
    };

    const searchInp = bar.querySelector("#cap-monitor-search-input");
    searchInp.oninput = (e) => {
      drawerSearchQuery = e.target.value.toLowerCase().trim();
      renderAllStyleGrids();
    };

    renderMonitorChips();
    renderAllCategories();
    renderAllStyleGrids();
  }

  function renderMonitorChips() {
    const container = document.getElementById("cap-monitor-chips-container");
    if (!container) return;
    const curStyle = window._CURRENT_STYLE || "classic";
    container.innerHTML = FEATURED_EDITOR_PRESETS.map(p => {
      const isAct = (p.id === curStyle);
      return `<button type="button" class="cap-monitor-chip ${isAct ? 'is-active' : ''}" data-style="${p.id}">${p.label}</button>`;
    }).join("");

    container.querySelectorAll(".cap-monitor-chip").forEach(chip => {
      chip.onclick = () => selectStyle(chip.getAttribute("data-style"));
    });
  }

  // -------------------------------------------------------------------------
  // Expandable 64 Caption Styles in Editor Sidebar (Req 1)
  // -------------------------------------------------------------------------
  function injectSidebarCaptionStyles() {
    const capPanel = document.querySelector(".panel.captions");
    if (!capPanel || document.getElementById("cap-editor-presets-container")) return;

    const presetsSection = document.createElement("div");
    presetsSection.className = "cap-editor-presets-section";
    presetsSection.id = "cap-editor-presets-container";

    const cur = allStyles.find(s => s.id === (window._CURRENT_STYLE || "classic")) || allStyles[0];

    presetsSection.innerHTML = `
      <div class="cap-editor-presets-head">
        <span class="cap-editor-presets-title">✨ Caption Styles (64 Presets)</span>
        <button type="button" class="cap-expand-arrow-btn ${isSidebarDrawerExpanded ? 'is-expanded' : ''}" id="cap-btn-expand-styles">
          <span id="cap-expand-btn-text">${isSidebarDrawerExpanded ? 'Collapse List' : 'All 64 Styles'}</span>
          <span class="cap-arrow-icon">▼</span>
        </button>
      </div>
      <div class="cap-active-indicator">
        <span class="cap-active-label">Active Style:</span>
        <span class="cap-active-value" id="cap-active-style-name">${cur.name}</span>
      </div>
      <div class="cap-editor-chips" id="cap-featured-chips-container">
        <!-- Populated dynamically -->
      </div>
      <div class="cap-presets-drawer ${isSidebarDrawerExpanded ? 'is-open' : ''}" id="cap-presets-drawer">
        <input type="text" class="cap-drawer-search" id="cap-drawer-search-input" placeholder="🔍 Search 64 styles (e.g. Hormozi, Neon, TikTok, Bouncy...)" value="${drawerSearchQuery}">
        <div class="cap-drawer-categories" id="cap-drawer-categories-container">
          <!-- Populated dynamically -->
        </div>
        <div class="cap-drawer-grid" id="cap-drawer-grid-container">
          <!-- Populated dynamically -->
        </div>
      </div>
    `;

    // Inject prominently into the captions panel
    const capBody = capPanel.querySelector(".cap-body");
    if (capBody) {
      capBody.insertBefore(presetsSection, capBody.firstChild);
    } else {
      capPanel.appendChild(presetsSection);
    }

    const expandBtn = presetsSection.querySelector("#cap-btn-expand-styles");
    expandBtn.onclick = () => {
      isSidebarDrawerExpanded = !isSidebarDrawerExpanded;
      expandBtn.classList.toggle("is-expanded", isSidebarDrawerExpanded);
      const drawer = document.getElementById("cap-presets-drawer");
      if (drawer) drawer.classList.toggle("is-open", isSidebarDrawerExpanded);
      const txt = document.getElementById("cap-expand-btn-text");
      if (txt) txt.innerText = isSidebarDrawerExpanded ? "Collapse List" : "All 64 Styles";
    };

    const searchInp = presetsSection.querySelector("#cap-drawer-search-input");
    searchInp.oninput = (e) => {
      drawerSearchQuery = e.target.value.toLowerCase().trim();
      renderAllStyleGrids();
    };

    renderSidebarChips();
    renderAllCategories();
    renderAllStyleGrids();
    injectSidebarPositionControls(presetsSection);
  }

  function renderSidebarChips() {
    const container = document.getElementById("cap-featured-chips-container");
    if (!container) return;
    const curStyle = window._CURRENT_STYLE || "classic";
    container.innerHTML = FEATURED_EDITOR_PRESETS.map(p => {
      const isAct = (p.id === curStyle);
      return `<button type="button" class="cap-preset-chip ${isAct ? 'is-active' : ''}" data-style="${p.id}">${p.label}</button>`;
    }).join("");

    container.querySelectorAll(".cap-preset-chip").forEach(chip => {
      chip.onclick = () => selectStyle(chip.getAttribute("data-style"));
    });
  }

  function renderAllCategories() {
    ["cap-drawer-categories-container", "cap-monitor-categories-container"].forEach(cId => {
      const container = document.getElementById(cId);
      if (!container) return;
      container.innerHTML = CATEGORY_TABS.map(cat => `
        <button type="button" class="cap-drawer-pill ${cat.id === currentDrawerCategory ? 'active' : ''}" data-cat="${cat.id}">
          ${cat.name}
        </button>
      `).join("");
      container.querySelectorAll(".cap-drawer-pill").forEach(btn => {
        btn.onclick = () => {
          currentDrawerCategory = btn.getAttribute("data-cat");
          renderAllCategories();
          renderAllStyleGrids();
        };
      });
    });
  }

  function renderAllStyleGrids() {
    const filtered = allStyles.filter(s => {
      const matchCat = currentDrawerCategory === "all" || s.category === currentDrawerCategory;
      const matchSearch = !drawerSearchQuery ||
        s.name.toLowerCase().includes(drawerSearchQuery) ||
        (s.category_label || "").toLowerCase().includes(drawerSearchQuery) ||
        (s.description || "").toLowerCase().includes(drawerSearchQuery);
      return matchCat && matchSearch;
    });

    ["cap-drawer-grid-container", "cap-monitor-grid-container"].forEach(gId => {
      const container = document.getElementById(gId);
      if (!container) return;
      const curStyle = window._CURRENT_STYLE || "classic";
      container.innerHTML = filtered.map(s => {
        const isSel = (s.id === curStyle);
        const pHtml = s.preview_html || `<span>${s.name.toUpperCase()}</span>`;
        const pClass = s.preview_class || "preview-default";
        const inlineStyle = (s.css && s.css.fontFamily) ? `font-family: ${s.css.fontFamily};` : "";
        return `
          <div class="cap-drawer-card ${isSel ? 'selected' : ''}" data-style="${s.id}">
            <div class="cap-drawer-card-preview ${pClass}" style="${inlineStyle}">
              ${pHtml}
            </div>
            <div class="cap-drawer-card-footer">
              <div class="cap-drawer-card-name" title="${s.name}">${s.name}</div>
              <div class="cap-drawer-card-cat">${s.category_label || s.category}</div>
            </div>
          </div>
        `;
      }).join("");

      container.querySelectorAll(".cap-drawer-card").forEach(card => {
        card.onclick = () => selectStyle(card.getAttribute("data-style"));
      });
    });
  }

  function selectStyle(styleId) {
    if (!styleId) return;
    window._CURRENT_STYLE = styleId;
    window._SHOW_CAPTION_PREVIEW = true;
    currentStyle = styleId;

    if (window._SET_REACT_CAPTION_STYLE) {
      window._SET_REACT_CAPTION_STYLE(styleId);
    }
    if (window._SET_REACT_CAPTIONS_ON) {
      window._SET_REACT_CAPTIONS_ON(true);
    }

    updateMonitorBoxPosition();
    syncAllUIControls();
    if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();

    const s = allStyles.find(item => item.id === styleId);
    StudioHistory.push(`Select Style: ${s ? s.name : styleId}`);
  }

  function injectSidebarPositionControls(parent) {
    if (document.getElementById("cap-pos-controls-container")) return;

    const posWrap = document.createElement("div");
    posWrap.id = "cap-pos-controls-container";
    posWrap.className = "cap-pos-controls-wrap";
    posWrap.innerHTML = `
      <div class="mini-h" style="margin-top: 14px;">Caption Placement & Position</div>
      <div class="cap-pos-row">
        <button type="button" class="cap-pos-preset-btn" id="btn-pos-top">⬆ Top (15%)</button>
        <button type="button" class="cap-pos-preset-btn" id="btn-pos-center">↔ Center (50%)</button>
        <button type="button" class="cap-pos-preset-btn is-active" id="btn-pos-bottom">⬇ Bottom (85%)</button>
      </div>
      <div class="mini-h">Vertical Position (Y)</div>
      <label class="trdur">
        <input type="range" min="0.05" max="0.95" step="0.02" value="${window._CAPTION_POS.y || 0.85}" id="cap-pos-y-range">
        <span class="trdur__val" id="cap-pos-y-val">${Math.round((window._CAPTION_POS.y || 0.85)*100)}%</span>
      </label>
      <div class="mini-h" style="margin-top: 6px;">Horizontal Position (X)</div>
      <label class="trdur">
        <input type="range" min="0.05" max="0.95" step="0.02" value="${window._CAPTION_POS.x || 0.5}" id="cap-pos-x-range">
        <span class="trdur__val" id="cap-pos-x-val">${Math.round((window._CAPTION_POS.x || 0.5)*100)}%</span>
      </label>
      <div class="mini-h" style="margin-top: 6px;">Caption Size / Scale</div>
      <label class="trdur">
        <input type="range" min="0.4" max="2.5" step="0.05" value="${window._CAPTION_POS.scale || 1.0}" id="cap-scale-range">
        <span class="trdur__val" id="cap-scale-val">${Math.round((window._CAPTION_POS.scale || 1.0)*100)}%</span>
      </label>
    `;

    parent.appendChild(posWrap);

    posWrap.querySelector("#btn-pos-top").onclick = () => {
      window._CAPTION_POS.y = 0.15;
      updateMonitorBoxPosition();
      syncSidebarPositionControls();
      if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
      StudioHistory.push("Position: Top");
    };
    posWrap.querySelector("#btn-pos-center").onclick = () => {
      window._CAPTION_POS.y = 0.50;
      updateMonitorBoxPosition();
      syncSidebarPositionControls();
      if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
      StudioHistory.push("Position: Center");
    };
    posWrap.querySelector("#btn-pos-bottom").onclick = () => {
      window._CAPTION_POS.y = 0.85;
      updateMonitorBoxPosition();
      syncSidebarPositionControls();
      if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
      StudioHistory.push("Position: Bottom");
    };

    posWrap.querySelector("#cap-pos-y-range").oninput = (e) => {
      window._CAPTION_POS.y = parseFloat(e.target.value);
      updateMonitorBoxPosition();
      syncSidebarPositionControls();
      if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
    };
    posWrap.querySelector("#cap-pos-y-range").onchange = () => StudioHistory.push("Adjust Y Position");

    posWrap.querySelector("#cap-pos-x-range").oninput = (e) => {
      window._CAPTION_POS.x = parseFloat(e.target.value);
      updateMonitorBoxPosition();
      syncSidebarPositionControls();
      if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
    };
    posWrap.querySelector("#cap-pos-x-range").onchange = () => StudioHistory.push("Adjust X Position");

    posWrap.querySelector("#cap-scale-range").oninput = (e) => {
      window._CAPTION_POS.scale = parseFloat(e.target.value);
      updateMonitorBoxPosition();
      syncSidebarPositionControls();
      if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
    };
    posWrap.querySelector("#cap-scale-range").onchange = () => StudioHistory.push("Adjust Caption Size");
  }

  // -------------------------------------------------------------------------
  // 3. Full View / Fullscreen Monitor Button (Req 3)
  // -------------------------------------------------------------------------
  function injectFullViewButton() {
    const transport = document.querySelector(".transport");
    if (!transport || document.getElementById("btn-toggle-fullview")) return;

    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "btn-fullview";
    btn.id = "btn-toggle-fullview";
    btn.innerHTML = `<span>⛶</span><span>Full View</span>`;
    btn.title = "View monitor screen in full view / fullscreen";

    btn.onclick = toggleFullView;

    const historyDiv = transport.querySelector(".history");
    if (historyDiv) {
      transport.insertBefore(btn, historyDiv);
    } else {
      transport.appendChild(btn);
    }

    // Also listen to Esc key and fullscreenchange to exit cleanly
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        const viewer = document.querySelector(".viewer");
        if (viewer && viewer.classList.contains("viewer--fullview")) {
          toggleFullView();
        }
      }
    });

    document.addEventListener("fullscreenchange", () => {
      if (!document.fullscreenElement) {
        const viewer = document.querySelector(".viewer");
        if (viewer && viewer.classList.contains("viewer--fullview")) {
          viewer.classList.remove("viewer--fullview");
          const exitBtn = document.getElementById("btn-exit-fullview");
          if (exitBtn) exitBtn.style.display = "none";
          updateMonitorBoxPosition();
          if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
        }
      }
    });
  }

  function toggleFullView() {
    const viewer = document.querySelector(".viewer");
    if (!viewer) return;

    const isFull = viewer.classList.contains("viewer--fullview");
    if (!isFull) {
      viewer.classList.add("viewer--fullview");
      let exitBtn = document.getElementById("btn-exit-fullview");
      if (!exitBtn) {
        exitBtn = document.createElement("button");
        exitBtn.id = "btn-exit-fullview";
        exitBtn.className = "btn-exit-fullview";
        exitBtn.innerHTML = "✕ Exit Full View";
        exitBtn.onclick = toggleFullView;
        document.body.appendChild(exitBtn);
      }
      exitBtn.style.display = "block";
      try {
        if (document.documentElement.requestFullscreen) {
          document.documentElement.requestFullscreen().catch(() => {});
        }
      } catch (e) {}
    } else {
      viewer.classList.remove("viewer--fullview");
      const exitBtn = document.getElementById("btn-exit-fullview");
      if (exitBtn) exitBtn.style.display = "none";
      try {
        if (document.fullscreenElement && document.exitFullscreen) {
          document.exitFullscreen().catch(() => {});
        }
      } catch (e) {}
    }
    updateMonitorBoxPosition();
    if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
  }

  function initLayoutCustomizationSystem() {
    window._LAYOUT_CONFIG = layoutConfig;
    window._APPLY_WORKSPACE_PRESET = applyWorkspacePreset;
    window._TOGGLE_EXPAND_PREVIEW = toggleExpandPreview;
    window._INJECT_LAYOUT_SPLITTERS = injectLayoutSplitters;
    window._INJECT_EXPAND_PREVIEW = injectExpandPreviewButton;
    window._INJECT_WORKSPACE_PRESETS = injectWorkspacePresets;
    window._INJECT_LAYOUT_MENU = injectLayoutMenu;
    window._INIT_PLAYHEAD = initTimelinePlayheadController;
    window._WATCH_EDITOR_UI = watchEditorUI;
    applyLayoutStyles();
  }

  // -------------------------------------------------------------------------
  // 4. Voice File & Master Voiceover Volume Control (Req 4)
  // -------------------------------------------------------------------------
  function injectVoiceoverVolumeControl() {
    const transport = document.querySelector(".transport");
    if (!transport || document.getElementById("cap-voice-vol-container")) return;

    const wrap = document.createElement("div");
    wrap.id = "cap-voice-vol-container";
    wrap.className = "cap-voice-vol-wrap";
    wrap.title = "Master Voiceover Volume: Adjust volume from 0% to 200%";

    const vol = window._VOICEOVER_VOLUME !== undefined ? window._VOICEOVER_VOLUME : 1.0;
    const volPct = Math.round(vol * 100);

    wrap.innerHTML = `
      <span class="cap-voice-vol-label">🔊 Voice</span>
      <input type="range" min="0" max="2" step="0.05" value="${vol}" class="cap-voice-vol-slider" id="cap-voice-vol-slider" />
      <span class="cap-voice-vol-val" id="cap-voice-vol-val">${volPct}%</span>
      <button type="button" class="cap-voice-file-btn" id="btn-pick-voice-file" title="Import or replace voiceover audio file">📁 Voice File</button>
    `;

    const slider = wrap.querySelector("#cap-voice-vol-slider");
    const valLabel = wrap.querySelector("#cap-voice-vol-val");
    const fileBtn = wrap.querySelector("#btn-pick-voice-file");

    slider.oninput = (e) => {
      const v = parseFloat(e.target.value);
      setMasterVoiceVolume(v);
      valLabel.innerText = v <= 0.01 ? "0% (Muted)" : `${Math.round(v * 100)}%`;
    };

    slider.onchange = () => {
      StudioHistory.push(`Set Voice Volume: ${Math.round(window._VOICEOVER_VOLUME * 100)}%`);
    };

    fileBtn.onclick = () => {
      const nativeAudioInput = document.querySelector('.bar__io input[accept*="audio"]');
      if (nativeAudioInput) {
        nativeAudioInput.click();
      } else {
        openModal();
        switchTab(1);
      }
    };

    const timeDiv = transport.querySelector(".time");
    if (timeDiv && timeDiv.nextSibling) {
      transport.insertBefore(wrap, timeDiv.nextSibling);
    } else {
      transport.appendChild(wrap);
    }
  }

  // -------------------------------------------------------------------------
  // 5. Undo, Redo (Step Back / Step Forward) & Reset to Default (Req 5)
  // -------------------------------------------------------------------------
  function injectResetAndStepButtons() {
    const transport = document.querySelector(".transport");
    if (!transport || document.getElementById("cap-studio-history-group")) return;

    const history = transport.querySelector(".history");
    if (!history) return;

    const group = document.createElement("div");
    group.id = "cap-studio-history-group";
    group.className = "cap-history-group";

    group.innerHTML = `
      <button type="button" class="cap-step-btn" id="btn-step-back" title="Go back one step (Undo)">↶ Step Back</button>
      <button type="button" class="cap-step-btn" id="btn-step-forward" title="Go forward one step (Redo)">↷ Step Forward</button>
      <button type="button" class="cap-reset-btn" id="btn-reset-default" title="Reset all styles, pace, audio, and captions back to default">↺ Reset to Default</button>
    `;

    group.querySelector("#btn-step-back").onclick = () => StudioHistory.stepBack();
    group.querySelector("#btn-step-forward").onclick = () => StudioHistory.stepForward();
    group.querySelector("#btn-reset-default").onclick = () => {
      if (confirm("Reset caption style, placement, audio volume, and transitions back to default settings?")) {
        StudioHistory.resetToDefault();
      }
    };

    history.appendChild(group);
    StudioHistory.init();
  }

  // -------------------------------------------------------------------------
  // 6. Video Clip AI Voice Removal (Keep SFX & Clicks) (Req 6)
  // -------------------------------------------------------------------------
  function injectClipVoiceRemovalCard() {
    const modalVol = document.querySelector(".modal__vol");
    if (!modalVol || document.getElementById("clip-voice-removal-container")) return;

    const card = document.createElement("div");
    card.id = "clip-voice-removal-container";
    card.className = "clip-voice-remover-card";

    card.innerHTML = `
      <div class="clip-voice-remover-head">
        <div class="clip-voice-remover-title">
          <span>🎤</span>
          <span>AI Voice Removal</span>
        </div>
        <label class="cap-sfx-optin">
          <input type="checkbox" id="chk-remove-clip-voice" />
          <span>Remove Voice</span>
        </label>
      </div>
      <div class="clip-voice-remover-hint">
        Attenuates speech formants using multi-band AI filters while preserving click transients, foley, and ambient SFX.
      </div>
      <div id="clip-voice-slider-wrap" style="display: none; margin-top: 8px;">
        <div class="mini-h">Voice Volume Level</div>
        <label class="trdur">
          <input type="range" min="0" max="1" step="0.05" value="0.0" id="slider-clip-voice-vol" />
          <span class="trdur__val" id="val-clip-voice-vol">0% (Muted)</span>
        </label>
        <div style="display: flex; gap: 8px; margin-top: 8px;">
          <button type="button" class="cap-magic-btn" id="btn-process-vocal-remove" style="padding: 6px 12px; font-size: 11px;">
            <span>⚡</span><span>Process with AI Engine</span>
          </button>
        </div>
        <div id="clip-vocal-status-badge" class="clip-voice-remover-badge" style="display: none;">
          ✨ AI Voice Removed · Clicks & Foley Preserved
        </div>
      </div>
    `;

    modalVol.parentNode.insertBefore(card, modalVol.nextSibling);

    const chk = card.querySelector("#chk-remove-clip-voice");
    const sliderWrap = card.querySelector("#clip-voice-slider-wrap");
    const slider = card.querySelector("#slider-clip-voice-vol");
    const valLabel = card.querySelector("#val-clip-voice-vol");
    const procBtn = card.querySelector("#btn-process-vocal-remove");
    const statusBadge = card.querySelector("#clip-vocal-status-badge");

    let audioCtx = null;
    let sourceNode = null;
    let filterBands = [];

    function setupWebAudioNotch(videoEl, attenuationDb) {
      if (!videoEl) return;
      try {
        if (!audioCtx) {
          audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (!sourceNode && !videoEl._hasSourceNode) {
          videoEl._hasSourceNode = true;
          sourceNode = audioCtx.createMediaElementSource(videoEl);
          
          // Formant notch filters: 300Hz, 1050Hz, 2200Hz, 3300Hz
          const freqs = [300, 1050, 2200, 3300];
          filterBands = freqs.map(f => {
            const filt = audioCtx.createBiquadFilter();
            filt.type = "peaking";
            filt.frequency.value = f;
            filt.Q.value = 1.4;
            filt.gain.value = attenuationDb;
            return filt;
          });

          let prev = sourceNode;
          filterBands.forEach(f => {
            prev.connect(f);
            prev = f;
          });
          prev.connect(audioCtx.destination);
        } else if (filterBands.length) {
          filterBands.forEach(f => {
            f.gain.value = attenuationDb;
          });
        }
      } catch (e) {}
    }

    chk.onchange = () => {
      sliderWrap.style.display = chk.checked ? "block" : "none";
      const modalVideo = document.querySelector(".modal video");
      if (chk.checked) {
        setupWebAudioNotch(modalVideo, -28.0);
        if (statusBadge) statusBadge.style.display = "block";
      } else {
        setupWebAudioNotch(modalVideo, 0.0);
        if (statusBadge) statusBadge.style.display = "none";
      }
    };

    slider.oninput = (e) => {
      const v = parseFloat(e.target.value);
      valLabel.innerText = v <= 0.05 ? "0% (Muted)" : `${Math.round(v * 100)}%`;
      const att = -32.0 * (1.0 - v);
      const modalVideo = document.querySelector(".modal video");
      setupWebAudioNotch(modalVideo, att);
    };

    procBtn.onclick = async () => {
      const modalVideo = document.querySelector(".modal video");
      if (!modalVideo || !modalVideo.src) {
        alert("No active video clip selected in modal.");
        return;
      }
      procBtn.disabled = true;
      procBtn.innerHTML = `<span>⏳</span><span>Processing AI speech removal...</span>`;

      try {
        const vVol = parseFloat(slider.value) || 0.0;
        const blob = await fetch(modalVideo.src).then(r => r.blob());
        const formData = new FormData();
        formData.append("file", blob, "clip.mp4");
        formData.append("vocal_volume", vVol);

        const res = await fetch(`${API_BASE}/api/vocal-remove`, {
          method: "POST",
          body: formData
        });
        const data = await res.json();
        if (!data.ok) throw new Error(data.error || "Vocal removal failed");

        procBtn.innerHTML = `<span>✓</span><span>Voice Removed & Foley Preserved!</span>`;
        procBtn.style.background = "#10b981";
        if (statusBadge) {
          statusBadge.innerHTML = `✓ Clean Foley & Clicks Audio generated (${data.id}.wav) &middot; <a href="${data.audio_url}" download="foley_clean_${data.id}.wav" style="color:#38bdf8;text-decoration:underline;font-weight:700;">Download Audio</a>`;
          statusBadge.style.display = "block";
        }
      } catch (err) {
        alert("Vocal removal error: " + err.message);
        procBtn.disabled = false;
        procBtn.innerHTML = `<span>⚡</span><span>Process with AI Engine</span>`;
      }
    };
  }

  // -------------------------------------------------------------------------
  // 7. Transition Sound Effects with Smart Auto-Selection (Req 7)
  // -------------------------------------------------------------------------
  function injectTransitionSoundEffects() {
    const transPanel = document.querySelector(".panel.transitions");
    if (!transPanel || document.getElementById("cap-sfx-panel-container")) return;

    const sfxSection = document.createElement("div");
    sfxSection.id = "cap-sfx-panel-container";
    sfxSection.className = "cap-sfx-section";

    const allSfxItems = [
      { id: "auto", name: "✨ Smart Auto (Dynamic)", icon: "✨", category: "smart" },
      ...SFX_CATALOG
    ];

    sfxSection.innerHTML = `
      <div class="cap-sfx-head">
        <div class="cap-sfx-title">
          <span>🔊</span>
          <span>Transition Sound Effects</span>
        </div>
        <label class="cap-sfx-optin" title="Enable sound effects for video transitions">
          <input type="checkbox" id="chk-enable-sfx" ${window._SFX_ENABLED ? 'checked' : ''} />
          <span>Use sound effects</span>
        </label>
      </div>
      <div class="cap-sfx-body" id="cap-sfx-body" style="display: ${window._SFX_ENABLED ? 'block' : 'none'};">
        <div class="cap-sfx-smart-badge">
          <span>⚡</span>
          <span>Smart Auto-Select: Active (Chooses optimal sound per cut)</span>
        </div>
        <div class="mini-h">Sound Effect Volume</div>
        <label class="trdur">
          <input type="range" min="0" max="1" step="0.05" value="${window._SFX_VOLUME || 0.5}" id="slider-sfx-vol" />
          <span class="trdur__val" id="val-sfx-vol">${Math.round((window._SFX_VOLUME || 0.5)*100)}%</span>
        </label>
        <div class="mini-h" style="margin-top: 8px;">Sound Effects Library (Click ▶ to preview, click chip to select)</div>
        <div class="cap-sfx-grid" id="cap-sfx-grid-container">
          ${allSfxItems.map(s => `
            <div class="cap-sfx-chip ${s.id === (window._SELECTED_SFX || 'auto') ? 'is-active' : ''}" data-sfx="${s.id}">
              <span>${s.icon} ${s.name}</span>
              <button type="button" class="cap-sfx-play-btn" data-play="${s.id}" title="Preview sound">▶</button>
            </div>
          `).join("")}
        </div>
      </div>
    `;

    transPanel.appendChild(sfxSection);

    const chk = sfxSection.querySelector("#chk-enable-sfx");
    const body = sfxSection.querySelector("#cap-sfx-body");
    const volSlider = sfxSection.querySelector("#slider-sfx-vol");
    const volVal = sfxSection.querySelector("#val-sfx-vol");

    chk.onchange = () => {
      window._SFX_ENABLED = chk.checked;
      body.style.display = chk.checked ? "block" : "none";
      if (chk.checked) {
        playSFX(window._SELECTED_SFX || "auto", window._SFX_VOLUME);
      }
      StudioHistory.push(chk.checked ? "Enable Sound Effects" : "Disable Sound Effects");
    };

    volSlider.oninput = (e) => {
      window._SFX_VOLUME = parseFloat(e.target.value);
      volVal.innerText = `${Math.round(window._SFX_VOLUME * 100)}%`;
    };
    volSlider.onchange = () => StudioHistory.push("Adjust SFX Volume");

    sfxSection.querySelectorAll(".cap-sfx-chip").forEach(chip => {
      chip.onclick = (e) => {
        if (e.target.classList.contains("cap-sfx-play-btn")) return;
        const sfxId = chip.getAttribute("data-sfx");
        window._SELECTED_SFX = sfxId;
        sfxSection.querySelectorAll(".cap-sfx-chip").forEach(c => c.classList.remove("is-active"));
        chip.classList.add("is-active");
        playSFX(sfxId, window._SFX_VOLUME);
        StudioHistory.push(`Select SFX: ${sfxId}`);
      };
    });

    sfxSection.querySelectorAll(".cap-sfx-play-btn").forEach(btn => {
      btn.onclick = (e) => {
        e.stopPropagation();
        const sfxId = btn.getAttribute("data-play");
        playSFX(sfxId, window._SFX_VOLUME);
      };
    });
  }

/* === ADVANCED RESPONSIVE LAYOUT & PLAYHEAD CONTROLLER === */
  // -------------------------------------------------------------------------
  // 1. Interactive Professional Timeline Playhead Scrubber
  // -------------------------------------------------------------------------
  let isPlayheadDragging = false;

  function initTimelinePlayheadController() {
    const track = document.querySelector(".tl__track");
    const playhead = document.querySelector(".tl__playhead");
    if (!track || !playhead) return;

    const grip = playhead.querySelector(".tl__playhead-grip");
    if (!grip) return;

    if (grip._hasPlayheadController) return;
    grip._hasPlayheadController = true;

    playhead.style.pointerEvents = "auto";
    grip.style.pointerEvents = "auto";

    const getTotalDuration = () => {
      return window._TIMELINE_TOTAL_DURATION || 
             (window._VOICEOVER_AUDIO_EL && window._VOICEOVER_AUDIO_EL.duration) || 
             (window._TIMELINE_CLIPS && window._TIMELINE_CLIPS.length && 
              window._TIMELINE_CLIPS[window._TIMELINE_CLIPS.length - 1].start + 
              window._TIMELINE_CLIPS[window._TIMELINE_CLIPS.length - 1].duration) || 30.0;
    };

    const getTrackClips = () => {
      return window._TIMELINE_CLIPS || [];
    };

    const isSnappingEnabled = () => {
      const snapBtn = document.getElementById("cap-tl-btn-snap");
      return !snapBtn || snapBtn.classList.contains("is-active");
    };

    const computeTimeFromClientX = (clientX) => {
      const rect = track.getBoundingClientRect();
      if (!rect || rect.width <= 0) return 0;
      const ratio = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
      let targetSec = ratio * getTotalDuration();

      if (isSnappingEnabled()) {
        const clips = getTrackClips();
        const snapThresholdSec = 0.18;
        for (const clip of clips) {
          if (clip.start !== undefined && Math.abs(clip.start - targetSec) <= snapThresholdSec) {
            targetSec = clip.start;
            break;
          }
          if (clip.start !== undefined && clip.duration !== undefined) {
            const cutEnd = clip.start + clip.duration;
            if (Math.abs(cutEnd - targetSec) <= snapThresholdSec) {
              targetSec = cutEnd;
              break;
            }
          }
        }
      }
      return Math.max(0, Math.min(getTotalDuration(), targetSec));
    };

    const updatePlayheadVisuals = (sec) => {
      const total = getTotalDuration();
      if (total <= 0) return;
      const pct = Math.max(0, Math.min(100, (sec / total) * 100));
      playhead.style.left = pct + "%";

      const tcDisplay = document.getElementById("cap-tl-timecode-display");
      const min = Math.floor(sec / 60);
      const s = Math.floor(sec % 60);
      const frac = Math.floor((sec % 1) * 30);
      const pad = (n) => String(n).padStart(2, "0");
      if (tcDisplay) {
        tcDisplay.innerText = pad(Math.floor(min / 60)) + ":" + pad(min % 60) + ":" + pad(s) + ":" + pad(frac);
      }

      const timeNowEl = document.querySelector(".time__now");
      if (timeNowEl) {
        timeNowEl.innerText = pad(min) + ":" + pad(s) + "." + Math.floor((sec % 1) * 10);
      }
    };

    const performSeek = (sec) => {
      updatePlayheadVisuals(sec);

      if (window._SEEK_TO) {
        window._SEEK_TO(sec);
      } else if (window._VOICEOVER_AUDIO_EL) {
        window._VOICEOVER_AUDIO_EL.currentTime = sec;
      }

      if (window._TRIGGER_CANVAS_DRAW) {
        window._TRIGGER_CANVAS_DRAW();
      }
    };

    const onPointerDown = (e) => {
      if (e.button !== 0 && e.pointerType === "mouse") return;
      e.preventDefault();
      e.stopPropagation();

      isPlayheadDragging = true;
      document.body.classList.add("is-playhead-dragging");
      playhead.classList.add("is-dragging");
      grip.classList.add("is-dragging");

      try {
        grip.setPointerCapture(e.pointerId);
      } catch (err) {}

      const sec = computeTimeFromClientX(e.clientX);
      performSeek(sec);

      const onPointerMove = (moveEvt) => {
        if (!isPlayheadDragging) return;
        moveEvt.preventDefault();
        const moveSec = computeTimeFromClientX(moveEvt.clientX);
        performSeek(moveSec);
      };

      const onPointerUp = (upEvt) => {
        if (!isPlayheadDragging) return;
        isPlayheadDragging = false;
        document.body.classList.remove("is-playhead-dragging");
        playhead.classList.remove("is-dragging");
        grip.classList.remove("is-dragging");

        try {
          grip.releasePointerCapture(upEvt.pointerId);
        } catch (err) {}

        window.removeEventListener("pointermove", onPointerMove, true);
        window.removeEventListener("pointerup", onPointerUp, true);
        window.removeEventListener("pointercancel", onPointerUp, true);

        const finalSec = computeTimeFromClientX(upEvt.clientX);
        performSeek(finalSec);
      };

      window.addEventListener("pointermove", onPointerMove, true);
      window.addEventListener("pointerup", onPointerUp, true);
      window.addEventListener("pointercancel", onPointerUp, true);
    };

    grip.addEventListener("pointerdown", onPointerDown, { passive: false });
    playhead.addEventListener("pointerdown", onPointerDown, { passive: false });

    // Scrubbing on ruler
    const ruler = document.querySelector(".tl__ruler");
    if (ruler && !ruler._hasScrubBridge) {
      ruler._hasScrubBridge = true;
      ruler.addEventListener("pointerdown", (e) => {
        if (e.target.closest(".tl__playhead") || e.target.closest(".tl__playhead-grip")) return;
        const sec = computeTimeFromClientX(e.clientX);
        performSeek(sec);
      }, true);
    }

    // Scrubbing on captions lane
    const capLane = document.getElementById("cap-tl-captions-lane");
    if (capLane && !capLane._hasScrubBridge) {
      capLane._hasScrubBridge = true;
      capLane.addEventListener("pointerdown", (e) => {
        if (e.target.closest(".cap-tl-cue-pill") || e.target.closest("#btn-tl-quick-captions") || e.target.closest(".tl__playhead")) return;
        const sec = computeTimeFromClientX(e.clientX);
        performSeek(sec);
      }, true);
    }
  }

  // -------------------------------------------------------------------------
  // 2. Fully Customizable Layout Configuration System
  // -------------------------------------------------------------------------
  const LAYOUT_STORAGE_KEY = "autoeditor_layout_config_v2";

  let layoutConfig = {
    sideWidth: 330,
    viewerHeightPct: 58,
    isLocked: false,
    isExpandedPreview: false,
    sidebarPos: "right",
    timelinePos: "bottom",
    panels: {
      preview: true,
      timeline: true,
      export: true,
      transitions: true,
      voice: true,
      speed: true
    },
    activePreset: "default"
  };

  try {
    const saved = localStorage.getItem(LAYOUT_STORAGE_KEY);
    if (saved) {
      const parsed = JSON.parse(saved);
      layoutConfig = Object.assign({}, layoutConfig, parsed);
    }
  } catch (e) {}

  function saveLayoutConfig() {
    try {
      localStorage.setItem(LAYOUT_STORAGE_KEY, JSON.stringify(layoutConfig));
    } catch (e) {}
  }

  function applyLayoutStyles() {
    const editor = document.querySelector(".editor");
    if (!editor) return;

    document.documentElement.style.setProperty("--editor-side-width", layoutConfig.sideWidth + "px");
    document.documentElement.style.setProperty("--editor-viewer-height", layoutConfig.viewerHeightPct + "%");
    document.documentElement.style.setProperty("--editor-tl-height", (100 - layoutConfig.viewerHeightPct) + "%");

    if (layoutConfig.sidebarPos === "left") {
      editor.classList.add("layout--sidebar-left");
    } else {
      editor.classList.remove("layout--sidebar-left");
    }

    if (layoutConfig.timelinePos === "top") {
      editor.classList.add("layout--timeline-top");
    } else {
      editor.classList.remove("layout--timeline-top");
    }

    if (layoutConfig.isLocked) {
      editor.classList.add("layout--locked");
    } else {
      editor.classList.remove("layout--locked");
    }

    if (layoutConfig.isExpandedPreview) {
      editor.classList.add("editor--expand-preview");
    } else {
      editor.classList.remove("editor--expand-preview");
    }

    // Panel visibility
    const viewer = document.querySelector(".viewer");
    if (viewer) viewer.style.display = layoutConfig.panels.preview ? "flex" : "none";

    const tl = document.querySelector(".tl");
    if (tl) tl.style.display = layoutConfig.panels.timeline ? "flex" : "none";

    const exportPanel = document.querySelector(".panel.export");
    if (exportPanel) exportPanel.style.display = layoutConfig.panels.export ? "block" : "none";

    const transPanel = document.querySelector(".panel.transitions");
    if (transPanel) transPanel.style.display = layoutConfig.panels.transitions ? "block" : "none";

    const voiceWrap = document.getElementById("cap-voice-vol-container");
    if (voiceWrap) voiceWrap.style.display = layoutConfig.panels.voice ? "flex" : "none";

    const speedPill = document.getElementById("cap-auto-speed-pill");
    if (speedPill) speedPill.style.display = layoutConfig.panels.speed ? "flex" : "none";

    // Update Lock button UI
    const lockBtn = document.getElementById("btn-toggle-lock-layout");
    if (lockBtn) {
      lockBtn.classList.toggle("is-locked", layoutConfig.isLocked);
      lockBtn.innerHTML = layoutConfig.isLocked ? "<span>🔒</span><span>Layout Locked</span>" : "<span>🔓</span><span>Layout Unlocked</span>";
      lockBtn.title = layoutConfig.isLocked ? "Layout is locked to prevent accidental changes (Click to unlock)" : "Click to lock current layout";
    }

    // Update Expand Preview button
    const expBtn = document.getElementById("btn-expand-preview-main") || document.getElementById("btn-toggle-fullview");
    if (expBtn) {
      expBtn.classList.toggle("is-active", layoutConfig.isExpandedPreview);
      expBtn.innerHTML = layoutConfig.isExpandedPreview ? "<span>🗗</span><span>Restore View</span>" : "<span>⛶</span><span>Expand Preview</span>";
    }

    let banner = document.getElementById("cap-expanded-preview-banner");
    if (!banner && layoutConfig.isExpandedPreview) {
      banner = document.createElement("div");
      banner.id = "cap-expanded-preview-banner";
      banner.className = "cap-expanded-preview-banner";
      banner.innerHTML = `
        <span>⛶ Large Preview Active (Timeline Docked Below)</span>
        <button type="button" class="cap-expanded-preview-exit-btn" id="btn-exit-expanded-preview">Restore (Esc)</button>
      `;
      document.body.appendChild(banner);
      banner.querySelector("#btn-exit-expanded-preview").onclick = toggleExpandPreview;
    }
    if (banner) {
      banner.classList.toggle("is-visible", !!layoutConfig.isExpandedPreview);
    }
    if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
  }

  // -------------------------------------------------------------------------
  // 3. Resizable Splitters (Horizontal & Vertical)
  // -------------------------------------------------------------------------
  function injectLayoutSplitters() {
    const editor = document.querySelector(".editor");
    if (!editor) return;

    const main = editor.querySelector(".main");
    const side = editor.querySelector(".side");
    if (!main || !side) return;

    // Horizontal Splitter between Main and Side
    let splitH = document.getElementById("editor-splitter-h");
    if (!splitH) {
      splitH = document.createElement("div");
      splitH.id = "editor-splitter-h";
      splitH.className = "editor-splitter editor-splitter--h";
      splitH.title = "Drag to resize sidebar width | Click arrow to collapse";

      const colBtn = document.createElement("button");
      colBtn.type = "button";
      colBtn.className = "splitter-collapse-btn";
      colBtn.id = "btn-splitter-collapse-side";
      colBtn.innerHTML = "◀";
      colBtn.title = "Collapse / Expand Sidebar";
      colBtn.onclick = (e) => {
        e.stopPropagation();
        side.classList.toggle("is-collapsed");
        colBtn.innerHTML = side.classList.contains("is-collapsed") ? "▶" : "◀";
        if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
      };
      splitH.appendChild(colBtn);

      editor.insertBefore(splitH, side);

      splitH.onpointerdown = (e) => {
        if (layoutConfig.isLocked || e.target === colBtn) return;
        e.preventDefault();
        splitH.setPointerCapture(e.pointerId);
        splitH.classList.add("is-active");

        const editorRect = editor.getBoundingClientRect();

        const onMove = (moveEvt) => {
          let newWidth = 0;
          if (layoutConfig.sidebarPos === "left") {
            newWidth = moveEvt.clientX - editorRect.left;
          } else {
            newWidth = editorRect.right - moveEvt.clientX;
          }
          newWidth = Math.max(220, Math.min(650, newWidth));
          layoutConfig.sideWidth = Math.round(newWidth);
          document.documentElement.style.setProperty("--editor-side-width", layoutConfig.sideWidth + "px");
          if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
        };

        const onUp = (upEvt) => {
          try { splitH.releasePointerCapture(upEvt.pointerId); } catch(err){}
          splitH.classList.remove("is-active");
          window.removeEventListener("pointermove", onMove);
          window.removeEventListener("mousemove", onMove);
          window.removeEventListener("pointerup", onUp);
          window.removeEventListener("mouseup", onUp);
          saveLayoutConfig();
          if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
        };

        window.addEventListener("pointermove", onMove);
        window.addEventListener("mousemove", onMove);
        window.addEventListener("pointerup", onUp);
        window.addEventListener("mouseup", onUp);
      };
    }

    // Vertical Splitter between Viewer and Timeline
    const viewer = main.querySelector(".viewer");
    const tl = main.querySelector(".tl");
    if (!viewer || !tl) return;

    let splitV = document.getElementById("editor-splitter-v");
    if (!splitV) {
      splitV = document.createElement("div");
      splitV.id = "editor-splitter-v";
      splitV.className = "editor-splitter editor-splitter--v";
      splitV.title = "Drag to resize Video Preview and Timeline heights";

      main.insertBefore(splitV, tl);

      splitV.onpointerdown = (e) => {
        if (layoutConfig.isLocked) return;
        e.preventDefault();
        splitV.setPointerCapture(e.pointerId);
        splitV.classList.add("is-active");

        const mainRect = main.getBoundingClientRect();

        const onMove = (moveEvt) => {
          let offsetY = moveEvt.clientY - mainRect.top;
          if (layoutConfig.timelinePos === "top") {
            offsetY = mainRect.bottom - moveEvt.clientY;
          }
          let pct = (offsetY / mainRect.height) * 100;
          pct = Math.max(30, Math.min(82, pct));
          layoutConfig.viewerHeightPct = Math.round(pct);
          document.documentElement.style.setProperty("--editor-viewer-height", layoutConfig.viewerHeightPct + "%");
          document.documentElement.style.setProperty("--editor-tl-height", (100 - layoutConfig.viewerHeightPct) + "%");
          if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
        };

        const onUp = (upEvt) => {
          try { splitV.releasePointerCapture(upEvt.pointerId); } catch(err){}
          splitV.classList.remove("is-active");
          window.removeEventListener("pointermove", onMove);
          window.removeEventListener("mousemove", onMove);
          window.removeEventListener("pointerup", onUp);
          window.removeEventListener("mouseup", onUp);
          saveLayoutConfig();
          if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
        };

        window.addEventListener("pointermove", onMove);
        window.addEventListener("mousemove", onMove);
        window.addEventListener("pointerup", onUp);
        window.addEventListener("mouseup", onUp);
      };
    }
  }

  // -------------------------------------------------------------------------
  // 4. CapCut-Style Expand Video Preview Mode
  // -------------------------------------------------------------------------
  function toggleExpandPreview() {
    layoutConfig.isExpandedPreview = !layoutConfig.isExpandedPreview;
    applyLayoutStyles();
    saveLayoutConfig();

    if (window._CANVAS_REDRAW) {
      setTimeout(window._CANVAS_REDRAW, 50);
    }
  }

  function injectExpandPreviewButton() {
    const transport = document.querySelector(".transport");
    if (!transport) return;

    let btn = document.getElementById("btn-expand-preview-main");
    if (!btn) {
      btn = document.createElement("button");
      btn.type = "button";
      btn.id = "btn-expand-preview-main";
      btn.className = "btn-expand-preview";
      btn.innerHTML = layoutConfig.isExpandedPreview ? "<span>🗗</span><span>Restore View</span>" : "<span>⛶</span><span>Expand Preview</span>";
      btn.title = "Expand Video Preview to fill screen (Keeps Timeline docked for editing)";
      btn.onclick = toggleExpandPreview;

      // Replace or augment old fullview button
      const oldBtn = document.getElementById("btn-toggle-fullview");
      if (oldBtn) {
        oldBtn.replaceWith(btn);
      } else {
        const historyDiv = transport.querySelector(".history");
        if (historyDiv) {
          transport.insertBefore(btn, historyDiv);
        } else {
          transport.appendChild(btn);
        }
      }
    }

    // Keyboard shortcut Esc or Ctrl+Enter to toggle
    if (!window._hasExpandShortcut) {
      window._hasExpandShortcut = true;
      document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && layoutConfig.isExpandedPreview) {
          toggleExpandPreview();
        } else if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
          toggleExpandPreview();
        }
      });
    }
  }

  // -------------------------------------------------------------------------
  // 5. Workspace Presets Bar & Lock Layout Controls in Header
  // -------------------------------------------------------------------------
  function applyWorkspacePreset(presetId) {
    layoutConfig.activePreset = presetId;
    layoutConfig.isExpandedPreview = false;

    const side = document.querySelector(".side");
    if (side) side.classList.remove("is-collapsed");

    if (presetId === "preview_focus") {
      layoutConfig.viewerHeightPct = 74;
      layoutConfig.sideWidth = 240;
      layoutConfig.panels.export = false;
      layoutConfig.panels.transitions = false;
    } else if (presetId === "timeline_focus") {
      layoutConfig.viewerHeightPct = 44;
      layoutConfig.sideWidth = 320;
      layoutConfig.panels.export = true;
      layoutConfig.panels.transitions = true;
    } else if (presetId === "captions_focus") {
      layoutConfig.viewerHeightPct = 55;
      layoutConfig.sideWidth = 380;
      layoutConfig.panels.export = true;
      layoutConfig.panels.transitions = true;
    } else if (presetId === "export_focus") {
      layoutConfig.viewerHeightPct = 52;
      layoutConfig.sideWidth = 420;
      layoutConfig.panels.export = true;
      layoutConfig.panels.transitions = true;
    } else { // default
      layoutConfig.viewerHeightPct = 58;
      layoutConfig.sideWidth = 330;
      layoutConfig.panels.preview = true;
      layoutConfig.panels.timeline = true;
      layoutConfig.panels.export = true;
      layoutConfig.panels.transitions = true;
    }

    applyLayoutStyles();
    saveLayoutConfig();
    updateWorkspacePresetButtons();
  }

  function updateWorkspacePresetButtons() {
    document.querySelectorAll(".cap-ws-btn").forEach(btn => {
      const id = btn.getAttribute("data-preset");
      btn.classList.toggle("is-active", id === layoutConfig.activePreset);
    });
  }

  function injectWorkspacePresets() {
    const bar = document.querySelector(".bar");
    if (!bar) return;

    let wsBar = document.getElementById("cap-workspace-bar");
    if (!wsBar) {
      wsBar = document.createElement("div");
      wsBar.id = "cap-workspace-bar";
      wsBar.className = "cap-workspace-bar";
      wsBar.innerHTML = `
        <button type="button" class="cap-ws-btn" data-preset="preview_focus" title="Maximized Video Preview with compact editing timeline">🎬 Large Preview</button>
        <button type="button" class="cap-ws-btn" data-preset="timeline_focus" title="Expanded multi-track timeline focus">⚡ Timeline</button>
        <button type="button" class="cap-ws-btn" data-preset="captions_focus" title="Caption studio with preset selector focus">🎨 Captions</button>
        <button type="button" class="cap-ws-btn" data-preset="export_focus" title="Export settings & transition mixing focus">🚀 Export</button>
        <button type="button" class="cap-ws-btn" data-preset="default" title="Reset to default balanced workspace">⚙️ Default</button>
      `;

      wsBar.querySelectorAll(".cap-ws-btn").forEach(b => {
        b.onclick = () => applyWorkspacePreset(b.getAttribute("data-preset"));
      });

      const barActions = bar.querySelector(".bar__actions");
      if (barActions) {
        bar.insertBefore(wsBar, barActions);
      } else {
        bar.appendChild(wsBar);
      }
    }

    updateWorkspacePresetButtons();
  }

  function injectLayoutMenu() {
    const barActions = document.querySelector(".bar__actions");
    if (!barActions || document.getElementById("btn-toggle-lock-layout")) return;

    // 1. Lock Layout Button
    const lockBtn = document.createElement("button");
    lockBtn.type = "button";
    lockBtn.id = "btn-toggle-lock-layout";
    lockBtn.className = "btn-lock-layout";
    lockBtn.innerHTML = layoutConfig.isLocked ? "<span>🔒</span><span>Layout Locked</span>" : "<span>🔓</span><span>Layout Unlocked</span>";
    lockBtn.title = "Lock/Unlock editor panel sizes and positions";
    lockBtn.onclick = () => {
      layoutConfig.isLocked = !layoutConfig.isLocked;
      applyLayoutStyles();
      saveLayoutConfig();
    };

    // 2. Layout & Panels Dropdown Button
    const menuBtn = document.createElement("button");
    menuBtn.type = "button";
    menuBtn.id = "btn-toggle-layout-menu";
    menuBtn.className = "btn-layout-menu-toggle";
    menuBtn.innerHTML = "<span>📐</span><span>Panels ▾</span>";
    menuBtn.title = "Show/hide individual panels and customize workspace arrangement";

    let dropdown = document.getElementById("cap-layout-dropdown");
    if (!dropdown) {
      dropdown = document.createElement("div");
      dropdown.id = "cap-layout-dropdown";
      dropdown.className = "cap-layout-dropdown";
      dropdown.style.display = "none";
      dropdown.innerHTML = `
        <div class="cap-layout-dropdown-h">
          <span>Visible Panels</span>
          <span style="font-size:10px; color:#00f5d4;">CUSTOMIZE</span>
        </div>
        <label class="cap-panel-toggle-item">
          <span>🎬 Video Preview Window</span>
          <input type="checkbox" id="chk-panel-preview" ${layoutConfig.panels.preview ? "checked" : ""} />
        </label>
        <label class="cap-panel-toggle-item">
          <span>⚡ Multi-Track Timeline</span>
          <input type="checkbox" id="chk-panel-timeline" ${layoutConfig.panels.timeline ? "checked" : ""} />
        </label>
        <label class="cap-panel-toggle-item">
          <span>🚀 Export & Format Panel</span>
          <input type="checkbox" id="chk-panel-export" ${layoutConfig.panels.export ? "checked" : ""} />
        </label>
        <label class="cap-panel-toggle-item">
          <span>✨ Transitions & Mix Panel</span>
          <input type="checkbox" id="chk-panel-transitions" ${layoutConfig.panels.transitions ? "checked" : ""} />
        </label>
        <label class="cap-panel-toggle-item">
          <span>🔊 Voice Volume Controls</span>
          <input type="checkbox" id="chk-panel-voice" ${layoutConfig.panels.voice ? "checked" : ""} />
        </label>
        <label class="cap-panel-toggle-item">
          <span>⚡ Auto-Speed Sync Badge</span>
          <input type="checkbox" id="chk-panel-speed" ${layoutConfig.panels.speed ? "checked" : ""} />
        </label>

        <div class="cap-layout-dropdown-h" style="margin-top:8px;">
          <span>Rearrange Layout</span>
        </div>
        <div class="cap-layout-opt-row">
          <span>Sidebar Position:</span>
          <select id="sel-sidebar-pos">
            <option value="right" ${layoutConfig.sidebarPos === "right" ? "selected" : ""}>Right Side</option>
            <option value="left" ${layoutConfig.sidebarPos === "left" ? "selected" : ""}>Left Side</option>
          </select>
        </div>
        <div class="cap-layout-opt-row">
          <span>Timeline Position:</span>
          <select id="sel-timeline-pos">
            <option value="bottom" ${layoutConfig.timelinePos === "bottom" ? "selected" : ""}>Bottom</option>
            <option value="top" ${layoutConfig.timelinePos === "top" ? "selected" : ""}>Top</option>
          </select>
        </div>

        <button type="button" class="cap-layout-reset-btn" id="btn-reset-layout-default">Reset to Default Layout</button>
      `;

      document.body.appendChild(dropdown);

      // Checkbox listeners
      const bindToggle = (chkId, key) => {
        const chk = dropdown.querySelector(chkId);
        if (chk) {
          chk.onchange = (e) => {
            layoutConfig.panels[key] = e.target.checked;
            applyLayoutStyles();
            saveLayoutConfig();
          };
        }
      };
      bindToggle("#chk-panel-preview", "preview");
      bindToggle("#chk-panel-timeline", "timeline");
      bindToggle("#chk-panel-export", "export");
      bindToggle("#chk-panel-transitions", "transitions");
      bindToggle("#chk-panel-voice", "voice");
      bindToggle("#chk-panel-speed", "speed");

      // Position Selectors
      const selSide = dropdown.querySelector("#sel-sidebar-pos");
      if (selSide) {
        selSide.onchange = (e) => {
          layoutConfig.sidebarPos = e.target.value;
          applyLayoutStyles();
          saveLayoutConfig();
        };
      }

      const selTl = dropdown.querySelector("#sel-timeline-pos");
      if (selTl) {
        selTl.onchange = (e) => {
          layoutConfig.timelinePos = e.target.value;
          applyLayoutStyles();
          saveLayoutConfig();
        };
      }

      // Reset
      dropdown.querySelector("#btn-reset-layout-default").onclick = () => {
        applyWorkspacePreset("default");
        dropdown.style.display = "none";
      };
    }

    menuBtn.onclick = (e) => {
      e.stopPropagation();
      dropdown.classList.toggle("is-open");
      if (dropdown.classList.contains("is-open")) {
        const rect = menuBtn.getBoundingClientRect();
        dropdown.style.top = (rect.bottom + 8) + "px";
        dropdown.style.right = (window.innerWidth - rect.right) + "px";
      }
    };

    document.addEventListener("click", (e) => {
      if (!dropdown.contains(e.target) && e.target !== menuBtn) {
        dropdown.classList.remove("is-open");
      }
    });

    const expBtn = document.getElementById("btn-capcut-header-export");
    if (expBtn) {
      barActions.insertBefore(lockBtn, expBtn);
      barActions.insertBefore(menuBtn, expBtn);
    } else {
      barActions.appendChild(lockBtn);
      barActions.appendChild(menuBtn);
    }
  }

  // -------------------------------------------------------------------------
  // 6. Responsive Player Transport Bar Formatting
  // -------------------------------------------------------------------------
  function formatResponsiveTransportBar() {
    const transport = document.querySelector(".transport");
    if (!transport || transport._isFormatted) return;
    transport._isFormatted = true;

    // Wrap elements if needed to ensure no overlaps
    transport.style.flexWrap = "wrap";
    transport.style.alignItems = "center";
  }



    // -------------------------------------------------------------------------
  // Main UI Watcher & Periodic Injection Loop
  // -------------------------------------------------------------------------
  function watchEditorUI() {
    initTimelinePlayheadController();
    initLayoutCustomizationSystem();
    injectLayoutSplitters();
    injectExpandPreviewButton();
    injectWorkspacePresets();
    injectLayoutMenu();
    formatResponsiveTransportBar();
    applyLayoutStyles();

    removeUnwantedLinks();
    ensureModal();
    injectHeaderButton();
    injectAutoSpeedBadge();
    updateTimelineSpeedBadges();
    setupAudioPlaybackWatchers();

    // CapCut Desktop Video Editor UI/UX Overhaul
    injectWindowExpandButton();
    injectHeaderExportButton();
    injectHeaderProjectInfo();
    injectCapCutTimelineToolbar();
    updateCapCutTimecode();
    injectCapCutMultiTrackGutter();
    injectCapCutCaptionsTimelineLane();
    injectCapCutSFXTimelineLane();
    enhanceOnboardingScreen();
    injectAspectControls();
    ensureEditorAudioReady();

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

    // 2. Inject 64 styles into both monitor window and sidebar
    injectMonitorCaptionStylesBar();
    injectSidebarCaptionStyles();

    // 3. Inject on-monitor draggable & resizable caption box
    injectMonitorCaptionBox();

    // 4. Inject Full View button in transport bar
    injectFullViewButton();

    // 5. Inject Master Voiceover Volume slider
    injectVoiceoverVolumeControl();

    // 6. Inject Step Undo/Redo & Reset to Default
    injectResetAndStepButtons();

    // 7. Inject Video Clip AI Voice Removal card into clip modal
    injectClipVoiceRemovalCard();

    // 8. Inject Transition Sound Effects section with Smart Auto-Selection
    injectTransitionSoundEffects();
  }


  
  
  
  // === CAPCUT DESKTOP VIDEO EDITOR CONTROLLER OVERHAUL ===
  // 0. 9:16 Vertical Video Editing & Screen Recording Mode
  function setProjectAspect(aspect) {
    if (window._SET_ASPECT) {
      window._SET_ASPECT(aspect);
    }
    const select = document.querySelector('.ctrl select');
    if (select && select.value !== aspect) {
      select.value = aspect;
      select.dispatchEvent(new Event('change', { bubbles: true }));
    }
    applyAspectUI(aspect);
    if (window._CANVAS_REDRAW) {
      window._CANVAS_REDRAW();
    }
  }

  function applyAspectUI(aspect) {
    const isVert = (aspect === "9:16");
    const editor = document.querySelector(".editor");
    if (editor) {
      editor.classList.toggle("cap-vertical-mode", isVert);
    }
    if (typeof document !== "undefined") {
      document.body.classList.toggle("cap-vertical-mode", isVert);
    }

    const aspectBtn = document.getElementById("btn-aspect-toggle");
    if (aspectBtn) {
      aspectBtn.classList.toggle("is-vertical", isVert);
      aspectBtn.innerHTML = isVert 
        ? `<span>🖥️</span><span>16:9 Landscape</span>`
        : `<span>📱</span><span>9:16 Vertical</span>`;
      aspectBtn.title = isVert 
        ? "Switch to 16:9 Landscape YouTube Widescreen Mode" 
        : "Switch to 9:16 Vertical Shorts/Reels/TikTok Video Mode";
    }

    const pill = document.querySelector(".cap-header-project-pill");
    if (pill) {
      pill.innerHTML = isVert 
        ? `<span>📱</span><span>AutoEditor Pro &middot; 9:16 1080×1920 (Vertical)</span>`
        : `<span>🎬</span><span>AutoEditor Pro &middot; 1080p 30fps</span>`;
    }

    const ratioPill = document.getElementById("btn-ratio-pill");
    if (ratioPill) {
      ratioPill.innerHTML = isVert ? `<span>📱</span><span>9:16</span>` : `<span>🖥️</span><span>16:9</span>`;
    }
  }

  function injectAspectControls() {
    const barActions = document.querySelector(".bar__actions");
    if (barActions) {
      let aspectBtn = document.getElementById("btn-aspect-toggle");
      if (!aspectBtn) {
        aspectBtn = document.createElement("button");
        aspectBtn.type = "button";
        aspectBtn.id = "btn-aspect-toggle";
        aspectBtn.className = "cap-aspect-toggle-btn";
        aspectBtn.innerHTML = `<span>📱</span><span>9:16 Vertical</span>`;
        aspectBtn.title = "Switch to 9:16 Vertical Video Mode (Shorts / Reels / TikTok)";
        aspectBtn.onclick = () => {
          const current = (window._GET_ASPECT ? window._GET_ASPECT() : window._ASPECT) || "16:9";
          const next = (current === "9:16") ? "16:9" : "9:16";
          setProjectAspect(next);
        };

        const expandBtn = document.getElementById("btn-window-expand");
        if (expandBtn) {
          barActions.insertBefore(aspectBtn, expandBtn);
        } else {
          barActions.appendChild(aspectBtn);
        }
      }
    }

    // Transport ratio pill
    const transport = document.querySelector(".transport");
    if (transport && !document.getElementById("btn-ratio-pill")) {
      const ratioPill = document.createElement("button");
      ratioPill.type = "button";
      ratioPill.id = "btn-ratio-pill";
      ratioPill.className = "cap-ratio-pill";
      ratioPill.title = "Toggle Aspect Ratio (16:9 Landscape ↔ 9:16 Vertical)";
      ratioPill.innerHTML = `<span>🖥️</span><span>16:9</span>`;
      ratioPill.onclick = () => {
        const current = (window._GET_ASPECT ? window._GET_ASPECT() : window._ASPECT) || "16:9";
        const next = (current === "9:16") ? "16:9" : "9:16";
        setProjectAspect(next);
      };

      const fullViewBtn = document.getElementById("btn-fullscreen-toggle");
      if (fullViewBtn) {
        transport.insertBefore(ratioPill, fullViewBtn);
      } else {
        transport.appendChild(ratioPill);
      }
    }

    // Sync from Inspector select
    const select = document.querySelector('.ctrl select');
    if (select && !select._hasAspectSync) {
      select._hasAspectSync = true;
      select.addEventListener("change", (e) => {
        applyAspectUI(e.target.value);
        if (window._SET_ASPECT) {
          window._SET_ASPECT(e.target.value);
        }
        if (window._CANVAS_REDRAW) {
          window._CANVAS_REDRAW();
        }
      });
      if (select.value === "9:16") {
        applyAspectUI("9:16");
      }
    }
  }

  // 1. Expand / Fullscreen Window Toggle Button
  function injectWindowExpandButton() {
    const barActions = document.querySelector(".bar__actions");
    if (!barActions) return;

    let btn = document.getElementById("btn-window-expand");
    if (!btn) {
      btn = document.createElement("button");
      btn.type = "button";
      btn.id = "btn-window-expand";
      btn.className = "cap-window-expand-btn";
      btn.title = "Expand / Fullscreen Editor Window";
      btn.innerHTML = `<span style="font-size:13px;">⛶</span><span>Expand Window</span>`;

      btn.onclick = () => {
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen().catch(() => {});
          btn.innerHTML = `<span style="font-size:13px;">🗗</span><span>Restore Window</span>`;
          btn.title = "Restore Window (Esc)";
        } else {
          document.exitFullscreen().catch(() => {});
          btn.innerHTML = `<span style="font-size:13px;">⛶</span><span>Expand Window</span>`;
          btn.title = "Expand / Fullscreen Editor Window";
        }
      };

      document.addEventListener("fullscreenchange", () => {
        if (document.fullscreenElement) {
          btn.innerHTML = `<span style="font-size:13px;">🗗</span><span>Restore Window</span>`;
          btn.title = "Restore Window (Esc)";
        } else {
          btn.innerHTML = `<span style="font-size:13px;">⛶</span><span>Expand Window</span>`;
          btn.title = "Expand / Fullscreen Editor Window";
        }
      });
    }

    const expBtn = document.getElementById("btn-capcut-header-export");
    if (expBtn && btn.nextSibling !== expBtn) {
      barActions.insertBefore(btn, expBtn);
    } else if (!expBtn && btn.parentElement !== barActions) {
      barActions.appendChild(btn);
    }
  }

  // 2. CapCut Header Export Button
  function injectHeaderExportButton() {
    const barActions = document.querySelector(".bar__actions");
    if (!barActions || document.getElementById("btn-capcut-header-export")) return;

    const expBtn = document.createElement("button");
    expBtn.type = "button";
    expBtn.id = "btn-capcut-header-export";
    expBtn.className = "cap-header-export-btn";
    expBtn.title = "Export Rendered MP4 Video with Subtitles & Audio";
    expBtn.innerHTML = `<span>🚀</span><span>Export Video</span>`;

    expBtn.onclick = () => {
      const renderBtn = document.querySelector(".render:not(.build)");
      if (renderBtn) {
        renderBtn.click();
      } else {
        alert("Please import storyboard media and build the timeline first.");
      }
    };

    barActions.appendChild(expBtn);
  }

  // 3. CapCut Header Project Info & Aspect Ratio
  function injectHeaderProjectInfo() {
    const bar = document.querySelector(".bar");
    if (!bar || document.getElementById("cap-header-project-info")) return;

    const brand = bar.querySelector(".brand");
    const barActions = bar.querySelector(".bar__actions");
    if (!brand || !barActions) return;

    const info = document.createElement("div");
    info.id = "cap-header-project-info";
    info.className = "cap-header-center";
    info.innerHTML = `
      <span class="cap-header-project-pill" title="Current Video Project Preset">
        <span>🎬</span>
        <span>AutoEditor Pro &middot; 1080p 30fps</span>
      </span>
    `;

    bar.insertBefore(info, barActions);
  }

  // 4. CapCut Timeline Control Toolbar
  function injectCapCutTimelineToolbar() {
    const tl = document.querySelector(".tl");
    if (!tl || document.getElementById("cap-timeline-toolbar")) return;

    const rulerRow = tl.querySelector(".tl__row--ruler");
    if (!rulerRow) return;

    const toolbar = document.createElement("div");
    toolbar.id = "cap-timeline-toolbar";
    toolbar.className = "cap-tl-toolbar";

    toolbar.innerHTML = `
      <div class="cap-tl-tools-left">
        <span class="cap-tl-timecode" id="cap-tl-timecode-display">00:00:00:00</span>
        <span class="cap-tl-divider"></span>
        <button type="button" class="cap-tl-tool-btn" id="cap-tl-btn-split" title="Split clip at playhead position">
          <span>✂️</span><span>Split</span>
        </button>
        <button type="button" class="cap-tl-tool-btn" id="cap-tl-btn-delete" title="Delete selected clip">
          <span>🗑️</span><span>Delete</span>
        </button>
        <button type="button" class="cap-tl-tool-btn" id="cap-tl-btn-undo" title="Step Back / Undo (Ctrl+Z)">
          <span>↶</span><span>Undo</span>
        </button>
        <button type="button" class="cap-tl-tool-btn" id="cap-tl-btn-redo" title="Step Forward / Redo (Ctrl+Y)">
          <span>↷</span><span>Redo</span>
        </button>
        <button type="button" class="cap-tl-tool-btn is-active" id="cap-tl-btn-snap" title="Magnetic Snapping">
          <span>🧲</span><span>Snap</span>
        </button>
        <span class="cap-tl-badge-speed" title="Clips automatically scale to voiceover slots">⚡ Auto-Speed: 100% Sync</span>
      </div>
      <div class="cap-tl-tools-right">
        <span class="cap-tl-zoom-label">🔍 Zoom:</span>
        <button type="button" class="cap-tl-zoom-btn" id="cap-tl-zoom-out" title="Zoom Out">−</button>
        <input type="range" id="cap-tl-zoom-slider" min="0.5" max="3.0" step="0.1" value="1.0" title="Timeline scale" />
        <button type="button" class="cap-tl-zoom-btn" id="cap-tl-zoom-in" title="Zoom In">+</button>
        <button type="button" class="cap-tl-zoom-fit-btn" id="cap-tl-zoom-fit" title="Fit Timeline to Window">↔ Fit</button>
      </div>
    `;

    tl.insertBefore(toolbar, rulerRow);

    // Zoom Controls
    const zoomSlider = toolbar.querySelector("#cap-tl-zoom-slider");
    const zoomOut = toolbar.querySelector("#cap-tl-zoom-out");
    const zoomIn = toolbar.querySelector("#cap-tl-zoom-in");
    const zoomFit = toolbar.querySelector("#cap-tl-zoom-fit");

    const applyZoom = (val) => {
      const clamped = Math.max(0.5, Math.min(3.0, val));
      zoomSlider.value = clamped;
      if (clamped === 1.0) {
        tl.style.removeProperty("--tl-min");
      } else {
        const baseW = tl.clientWidth || 1000;
        tl.style.setProperty("--tl-min", `${Math.round(baseW * clamped)}px`);
      }
    };

    zoomSlider.oninput = (e) => applyZoom(parseFloat(e.target.value));
    zoomOut.onclick = () => applyZoom(parseFloat(zoomSlider.value) - 0.25);
    zoomIn.onclick = () => applyZoom(parseFloat(zoomSlider.value) + 0.25);
    zoomFit.onclick = () => applyZoom(1.0);

    // Undo / Redo
    toolbar.querySelector("#cap-tl-btn-undo").onclick = () => {
      if (window._REACT_UNDO) window._REACT_UNDO();
      else StudioHistory.undo();
    };
    toolbar.querySelector("#cap-tl-btn-redo").onclick = () => {
      if (window._REACT_REDO) window._REACT_REDO();
      else StudioHistory.redo();
    };

    // Split / Delete
    toolbar.querySelector("#cap-tl-btn-split").onclick = () => {
      const activeCut = document.querySelector(".cut.is-sel") || document.querySelector(".cut:hover");
      if (activeCut) {
        activeCut.click();
      } else {
        const cuts = document.querySelectorAll(".cut");
        if (cuts.length > 0) {
          cuts[0].click();
        } else {
          const clip = document.querySelector(".clip.is-active") || document.querySelector(".clip");
          if (clip) clip.click();
        }
      }
    };

    toolbar.querySelector("#cap-tl-btn-delete").onclick = () => {
      // 1. If modal open, click danger delete
      const modalDel = document.querySelector(".modal .mbtn--danger");
      if (modalDel) {
        modalDel.click();
        return;
      }
      // 2. If clip active, remove
      const selClip = document.querySelector(".clip.is-selected") || document.querySelector(".clip.is-active");
      if (selClip) {
        const removeBtn = selClip.querySelector(".clip__x") || selClip.querySelector("button");
        if (removeBtn) {
          removeBtn.click();
          return;
        }
        selClip.click();
      }
    };
  }

  // 5. Update Timecode Display in Timeline Toolbar
  function updateCapCutTimecode() {
    const tc = document.getElementById("cap-tl-timecode-display");
    if (!tc) return;
    const timeNowEl = document.querySelector(".time__now");
    if (timeNowEl && timeNowEl.innerText) {
      const raw = timeNowEl.innerText.trim();
      let parts = raw.split(":");
      let min = 0, sec = 0, frac = 0;
      if (parts.length === 2) {
        min = parseInt(parts[0], 10) || 0;
        let secParts = parts[1].split(".");
        sec = parseInt(secParts[0], 10) || 0;
        frac = secParts[1] ? parseInt(secParts[1], 10) : 0;
      }
      const pad = (n) => String(n).padStart(2, "0");
      tc.innerText = `${pad(Math.floor(min / 60))}:${pad(min % 60)}:${pad(sec)}:${pad(frac * 3)}`;
    }
  }

  // 6. CapCut Multi-Track Gutter Headers
  function injectCapCutMultiTrackGutter() {
    const gutter = document.querySelector(".tl__row:not(.tl__row--ruler):not(.tl__row--cuts) .tl__gutter");
    if (!gutter) return;

    // Track 1: Subtitles Track Gutter Tag
    let subTag = document.getElementById("cap-tl-tag-subtitles");
    if (!subTag) {
      subTag = document.createElement("div");
      subTag.id = "cap-tl-tag-subtitles";
      subTag.className = "tl__tag tl__tag--subtitles";
      subTag.title = "Subtitles & Synchronized Captions Track";
      subTag.innerHTML = `
        <div class="cap-tag-main">
          <span class="cap-tag-icon">💬</span>
          <span class="cap-tag-label">Subtitles</span>
        </div>
        <div class="cap-tag-actions">
          <button type="button" class="cap-track-btn cap-btn-cue-vis" title="Toggle Subtitles Visibility">👁️</button>
          <button type="button" class="cap-track-btn" title="Lock Subtitles Track">🔒</button>
        </div>
      `;
      gutter.insertBefore(subTag, gutter.firstChild);

      const visBtn = subTag.querySelector(".cap-btn-cue-vis");
      if (visBtn) {
        visBtn.onclick = (e) => {
          e.stopPropagation();
          window._SHOW_CAPTION_PREVIEW = !window._SHOW_CAPTION_PREVIEW;
          if (window._CANVAS_REDRAW) window._CANVAS_REDRAW();
          visBtn.style.opacity = window._SHOW_CAPTION_PREVIEW ? "1" : "0.35";
        };
      }
    }

    // Track 2: Video Track Gutter Tag
    const vTag = gutter.querySelector(".tl__tag:not(.tl__tag--audio):not(.tl__tag--subtitles):not(.tl__tag--sfx)");
    if (vTag) {
      if (!vTag.querySelector(".cap-tag-main")) {
        vTag.id = "cap-tl-tag-video";
        vTag.className = "tl__tag tl__tag--video";
        vTag.innerHTML = `
          <div class="cap-tag-main">
            <span class="cap-tag-icon">🎬</span>
            <span class="cap-tag-label">Video</span>
          </div>
          <div class="cap-tag-actions">
            <button type="button" class="cap-track-btn" title="Toggle Video Visibility">👁️</button>
            <button type="button" class="cap-track-btn" title="Lock Video Track">🔒</button>
          </div>
        `;
        vTag.title = "Video Visuals & Motion Track (1080p)";
      }
    }

    // Track 3: Audio Track Gutter Tag
    const aTag = gutter.querySelector(".tl__tag--audio:not(.tl__tag--subtitles):not(.tl__tag--sfx)");
    if (aTag) {
      if (!aTag.querySelector(".cap-tag-main")) {
        aTag.id = "cap-tl-tag-audio";
        aTag.innerHTML = `
          <div class="cap-tag-main">
            <span class="cap-tag-icon">🎵</span>
            <span class="cap-tag-label">Audio</span>
          </div>
          <div class="cap-tag-actions">
            <button type="button" class="cap-track-btn cap-btn-aud-mute" title="Mute/Unmute Audio">🔊</button>
            <button type="button" class="cap-track-btn" title="Lock Audio Track">🔒</button>
          </div>
        `;
        aTag.title = "Master Voiceover Track (48kHz)";

        const muteBtn = aTag.querySelector(".cap-btn-aud-mute");
        if (muteBtn) {
          muteBtn.onclick = (e) => {
            e.stopPropagation();
            const aud = window._VOICEOVER_AUDIO_EL || document.querySelector("audio");
            if (aud) {
              aud.muted = !aud.muted;
              muteBtn.innerText = aud.muted ? "🔇" : "🔊";
              muteBtn.title = aud.muted ? "Unmute Audio" : "Mute Audio";
            }
          };
        }
      }
    }

    // Track 4: Transition SFX Gutter Tag
    let sfxTag = document.getElementById("cap-tl-tag-sfx");
    if (window._SFX_ENABLED) {
      if (!sfxTag) {
        sfxTag = document.createElement("div");
        sfxTag.id = "cap-tl-tag-sfx";
        sfxTag.className = "tl__tag tl__tag--sfx";
        sfxTag.title = "Transition SFX Markers Track";
        sfxTag.innerHTML = `
          <div class="cap-tag-main">
            <span class="cap-tag-icon">🔔</span>
            <span class="cap-tag-label">SFX</span>
          </div>
          <div class="cap-tag-actions">
            <button type="button" class="cap-track-btn" title="SFX Active">🔊</button>
            <button type="button" class="cap-track-btn" title="Lock SFX Track">🔒</button>
          </div>
        `;
        gutter.appendChild(sfxTag);
      }
      sfxTag.style.display = "flex";
    } else {
      if (sfxTag) sfxTag.style.display = "none";
    }
  }

  // 7. CapCut Subtitle / Captions Timeline Lane
  function injectCapCutCaptionsTimelineLane() {
    const tlTrack = document.querySelector(".tl__track");
    if (!tlTrack) return;

    const videoLane = tlTrack.querySelector(".tl__lane--video");
    if (!videoLane) return;

    let capLane = document.getElementById("cap-tl-captions-lane");
    if (!capLane) {
      capLane = document.createElement("div");
      capLane.id = "cap-tl-captions-lane";
      capLane.className = "cap-tl-captions-lane";
      capLane.title = "Synchronized Subtitle Track";
      tlTrack.insertBefore(capLane, videoLane);
    }

    const cues = window._CAPTION_CUES || (currentTranscript && currentTranscript.segments);
    const totalDuration = (currentTranscript && currentTranscript.duration) || 
      (window._TIMELINE_CLIPS && window._TIMELINE_CLIPS.length && 
       window._TIMELINE_CLIPS[window._TIMELINE_CLIPS.length - 1].start + 
       window._TIMELINE_CLIPS[window._TIMELINE_CLIPS.length - 1].duration) || 30.0;

    if (cues && cues.length > 0) {
      if (capLane.dataset.cueCount !== String(cues.length)) {
        capLane.dataset.cueCount = String(cues.length);
        capLane.innerHTML = "";
        cues.forEach((cue) => {
          const pill = document.createElement("div");
          pill.className = "cap-tl-cue-pill";
          const leftPct = Math.max(0, (cue.start / totalDuration) * 100);
          const widthPct = Math.max(1.5, ((cue.end - cue.start) / totalDuration) * 100);
          pill.style.left = `${leftPct}%`;
          pill.style.width = `${widthPct}%`;
          pill.title = `${cue.start.toFixed(1)}s – ${cue.end.toFixed(1)}s: ${cue.text}`;
          pill.innerHTML = `<span>💬</span><span>${cue.text}</span>`;
          pill.onclick = (e) => {
            e.stopPropagation();
            if (audioElement) {
              audioElement.currentTime = cue.start;
              audioElement.play();
            }
          };
          capLane.appendChild(pill);
        });
      }
    } else {
      if (!capLane.querySelector(".cap-tl-empty-track")) {
        capLane.dataset.cueCount = "0";
        capLane.innerHTML = `
          <div class="cap-tl-empty-track" title="Click to auto-generate subtitles with Whisper AI">
            <span class="cap-tl-empty-icon">💬</span>
            <span class="cap-tl-empty-text">Captions Track &middot;</span>
            <button type="button" class="cap-tl-empty-btn" id="btn-tl-quick-captions">+ Auto Captions</button>
          </div>
        `;
        const quickBtn = capLane.querySelector("#btn-tl-quick-captions");
        if (quickBtn) {
          quickBtn.onclick = (e) => {
            e.stopPropagation();
            handleInEditorGenerateCaptions(quickBtn);
          };
        }
      }
    }
  }

  // 8. CapCut SFX Timeline Lane
  function injectCapCutSFXTimelineLane() {
    const tlTrack = document.querySelector(".tl__track");
    if (!tlTrack) return;

    const audioLane = tlTrack.querySelector(".tl__lane--audio");
    if (!audioLane) return;

    let sfxLane = document.getElementById("cap-tl-sfx-lane");
    if (!window._SFX_ENABLED) {
      if (sfxLane) sfxLane.style.display = "none";
      return;
    }

    if (!sfxLane) {
      sfxLane = document.createElement("div");
      sfxLane.id = "cap-tl-sfx-lane";
      sfxLane.className = "cap-tl-sfx-lane";
      sfxLane.title = "Transition SFX Markers Track";
      tlTrack.appendChild(sfxLane);
    }
    sfxLane.style.display = "block";

    const clips = window._TIMELINE_CLIPS || [];
    if (clips.length > 1 && sfxLane.childElementCount !== (clips.length - 1)) {
      sfxLane.innerHTML = "";
      const totalDuration = clips[clips.length - 1].start + clips[clips.length - 1].duration || 30.0;
      for (let i = 1; i < clips.length; i++) {
        const cutSec = clips[i].start;
        const pill = document.createElement("div");
        pill.className = "cap-tl-sfx-pill";
        const leftPct = (cutSec / totalDuration) * 100;
        pill.style.left = `${leftPct}%`;
        const sfxName = (window._SELECTED_SFX && window._SELECTED_SFX !== "auto") ? window._SELECTED_SFX : "whoosh";
        pill.title = `Cut at ${cutSec.toFixed(1)}s &middot; SFX: ${sfxName}`;
        pill.innerHTML = `<span>🔔</span><span>${sfxName}</span>`;
        pill.onclick = (e) => {
          e.stopPropagation();
          playSFX(sfxName, window._SFX_VOLUME);
        };
        sfxLane.appendChild(pill);
      }
    }
  }

  // 9. Enhance Step 1 Automatic Onboarding UI
  function enhanceOnboardingScreen() {
    const onboard = document.querySelector(".onboard");
    if (!onboard) return;

    const h = onboard.querySelector(".onboard__h");
    if (h && !h.dataset.capcutEnhanced) {
      h.dataset.capcutEnhanced = "true";
      h.innerText = "Sync Voiceover to Storyboard Visuals, Automatically.";
    }

    const dzList = onboard.querySelectorAll(".dz");
    if (dzList.length >= 2) {
      const dzAudio = dzList[0];
      const bodyAudio = dzAudio.querySelector(".dz__body");
      if (bodyAudio && !bodyAudio.querySelector(".dz-browse-btn")) {
        const btnAudio = document.createElement("span");
        btnAudio.className = "dz-browse-btn";
        btnAudio.innerText = "📁 Choose Audio File (MP3 / WAV)";
        bodyAudio.appendChild(btnAudio);
      }

      const dzMedia = dzList[1];
      const bodyMedia = dzMedia.querySelector(".dz__body");
      if (bodyMedia && !bodyMedia.querySelector(".dz-browse-btn")) {
        const btnMedia = document.createElement("span");
        btnMedia.className = "dz-browse-btn";
        btnMedia.innerText = "📁 Choose Images & Video Clips";
        bodyMedia.appendChild(btnMedia);
      }
    }

    const buildBtn = onboard.querySelector(".render.build");
    if (buildBtn && !buildBtn.innerText.includes("CapCut")) {
      buildBtn.innerText = "⚡ Build Automatic Timeline & Open CapCut Studio →";
      buildBtn.title = "Build synchronized timeline and open CapCut editor";
    }
  }


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
        if (typeof window !== "undefined") window._COMPANION_ONLINE = true;
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
      if (typeof window !== "undefined") window._COMPANION_ONLINE = false;
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
          style: (window._CURRENT_STYLE || currentStyle),
          width: 1920,
          height: 1080,
          pos_x: (window._CAPTION_POS ? window._CAPTION_POS.x : 0.5),
          pos_y: (window._CAPTION_POS ? window._CAPTION_POS.y : 0.85),
          font_scale: (window._CAPTION_POS ? window._CAPTION_POS.scale : 1.0)
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

  
    // -------------------------------------------------------------------------
  // 7. Instant Demo Storyboard Timeline Builder (for Quickstart & E2E Testing)
  // -------------------------------------------------------------------------
  window.__BUILD_DEMO_TIMELINE = async function() {
    console.log("Generating demo media and building timeline...");

    // 1. Synthetic WAV Audio (15 seconds, 440Hz beep)
    const sampleRate = 16000;
    const duration = 15;
    const numSamples = sampleRate * duration;
    const buffer = new ArrayBuffer(44 + numSamples * 2);
    const view = new DataView(buffer);

    const writeString = (offset, string) => {
      for (let i = 0; i < string.length; i++) view.setUint8(offset + i, string.charCodeAt(i));
    };
    writeString(0, 'RIFF');
    view.setUint32(4, 36 + numSamples * 2, true);
    writeString(8, 'WAVE');
    writeString(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, 1, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * 2, true);
    view.setUint16(32, 2, true);
    view.setUint16(34, 16, true);
    writeString(36, 'data');
    view.setUint32(40, numSamples * 2, true);

    for (let i = 0; i < numSamples; i++) {
      const t = i / sampleRate;
      const s = Math.sin(2 * Math.PI * 440 * t) * 0.3 * (t % 2 < 1 ? 1 : 0.2);
      view.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }
    const audioBlob = new Blob([buffer], { type: 'audio/wav' });
    const audioFile = new File([audioBlob], 'voiceover_demo.wav', { type: 'audio/wav' });

    // 2. Synthetic Storyboard Images
    const createDemoImage = (filename, label, color) => {
      const canvas = document.createElement('canvas');
      canvas.width = 1280;
      canvas.height = 720;
      const ctx = canvas.getContext('2d');
      const grad = ctx.createLinearGradient(0, 0, 1280, 720);
      grad.addColorStop(0, color);
      grad.addColorStop(1, '#090a0f');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 1280, 720);

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 50px system-ui, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(label, 640, 360);
      ctx.font = '22px monospace';
      ctx.fillStyle = '#00f5d4';
      ctx.fillText(filename, 640, 420);

      return new Promise(resolve => {
        canvas.toBlob(blob => {
          resolve(new File([blob], filename, { type: 'image/png' }));
        }, 'image/png');
      });
    };

    const img1 = await createDemoImage('0-00_intro_scene.png', 'Scene 1: Introduction (0:00)', '#1e3a8a');
    const img2 = await createDemoImage('0-05_features_showcase.png', 'Scene 2: Core Features (0:05)', '#065f46');
    const img3 = await createDemoImage('0-10_final_callout.png', 'Scene 3: Final Callout (0:10)', '#831843');

    // 3. Populate File Inputs
    const audioInput = document.querySelectorAll('input[type="file"][accept*="audio"]')[0];
    if (audioInput) {
      const dtAudio = new DataTransfer();
      dtAudio.items.add(audioFile);
      audioInput.files = dtAudio.files;
      audioInput.dispatchEvent(new Event('change', { bubbles: true }));
    }

    const mediaInput = document.querySelectorAll('input[type="file"][accept*="image"]')[0];
    if (mediaInput) {
      const dtMedia = new DataTransfer();
      dtMedia.items.add(img1);
      dtMedia.items.add(img2);
      dtMedia.items.add(img3);
      mediaInput.files = dtMedia.files;
      mediaInput.dispatchEvent(new Event('change', { bubbles: true }));
    }

    // 4. Poll until build button is enabled, then click
    let attempts = 0;
    const clickInterval = setInterval(() => {
      attempts++;
      const buildBtn = document.querySelector('.render.build');
      if (buildBtn && !buildBtn.disabled) {
        clearInterval(clickInterval);
        buildBtn.click();
        console.log("Successfully clicked Build timeline!");
      } else if (attempts > 40) {
        clearInterval(clickInterval);
      }
    }, 150);
  };

  // Check URL param ?demo=1
  if (typeof window !== "undefined" && window.location && window.location.search && window.location.search.includes("demo=1")) {
    window.addEventListener("load", () => {
      setTimeout(() => {
        if (window.__BUILD_DEMO_TIMELINE) window.__BUILD_DEMO_TIMELINE();
      }, 600);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
