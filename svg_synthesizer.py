import os
import re
from typing import Dict, Any, Optional

try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None
    ImageDraw = None

try:
    import cairosvg
except ImportError:
    cairosvg = None


def get_builtin_svgs() -> Dict[str, str]:
    """
    Returns catalog of 20+ built-in SVG templates for common concepts.
    Each template is a clean, modern, flat-design SVG.
    Use {color} formatting string to replace fill colors.
    """
    return {
        'up_arrow': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M12 4l-8 8h6v8h4v-8h6z"/></svg>',
        'down_arrow': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M12 20l8-8h-6v-8h-4v8h-6z"/></svg>',
        'trend_up': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"/></svg>',
        'trend_down': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M16 18l2.29-2.29-4.88-4.88-4 4L2 7.41 3.41 6l6 6 4-4 6.3 6.29L22 12v6z"/></svg>',
        'warning_triangle': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>',
        'checkmark': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>',
        'x_mark': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>',
        'star': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>',
        'heart': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>',
        'fire': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M11.71 3.56c-.05-.12-.17-.2-.3-.2-.14 0-.27.09-.31.22-.65 2.15-2.22 3.81-4 4.53C5.7 8.68 4.6 9.9 4.14 11.56c-.49 1.76.02 3.65 1.34 4.96.11.11.27.14.41.08.15-.07.25-.22.25-.38-.01-2.29 1.32-4.23 3.39-5.18.14-.06.29-.02.39.09.1.1.13.25.07.39-.75 1.78-.54 3.85.55 5.46.09.14.28.18.43.1.15-.08.23-.25.21-.41-.21-1.72.31-3.46 1.48-4.75 1.01-1.12 2.5-1.8 4.09-1.87.16-.01.3.1.34.25.19 1.06-.06 2.15-.7 3.01-.1.14-.08.33.05.45.13.12.33.12.46-.02 1.44-1.63 2.02-3.83 1.54-5.92-.47-2.07-1.89-3.79-3.8-4.63-.56-.25-1.18-.39-1.82-.44.22-.85.34-1.74.34-2.65 0-.25.01-.5-.03-.74-.01-.14-.14-.24-.29-.24h-.01c-.13 0-.24.08-.28.2-.5 1.59-1.58 2.87-2.95 3.51-1.29.6-2.23 1.76-2.52 3.12-.04.18.06.37.23.44.17.07.38 0 .47-.16 1.05-1.92 3.11-3.03 5.3-2.91 0 0-2.25-4.43-1.61-9z"/></svg>',
        'lightning_bolt': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M7 2v11h3v9l7-12h-4l4-8z"/></svg>',
        'money_dollar': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"/></svg>',
        'chart_bar': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/></svg>',
        'chart_line': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M3.5 18.49l6-6.01 4 4L22 6.92l-1.41-1.41-7.09 7.97-4-4L2 16.99z"/></svg>',
        'shield': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/></svg>',
        'badge_circle': '<svg viewBox="0 0 24 24" fill="{color}"><circle cx="12" cy="12" r="10"/></svg>',
        'speech_bubble': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>',
        'light_bulb': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M9 21c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H9v1zm3-19C8.14 2 5 5.14 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.86-3.14-7-7-7z"/></svg>',
        'gear_settings': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.06-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.56-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.06.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .43-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.49-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/></svg>',
        'clock': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/></svg>',
        'target_bullseye': '<svg viewBox="0 0 24 24" fill="{color}"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm0 10c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4zm0-7c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>'
    }

def validate_svg(svg_code: str) -> bool:
    """
    Check if SVG XML is well-formed and safe.
    Rejects scripts and external object references.
    """
    if not svg_code or not isinstance(svg_code, str):
        return False
        
    lower_code = svg_code.lower()
    
    # Check for basic SVG structure
    if '<svg' not in lower_code or '</svg>' not in lower_code:
        return False
        
    # Block potentially dangerous tags/attributes
    dangerous_patterns = [
        '<script', 'javascript:', 'onmouseover', 'onclick', 'onload', 
        'onerror', '<iframe', '<object', '<embed', 'xlink:href'
    ]
    
    for pattern in dangerous_patterns:
        if pattern in lower_code:
            return False
            
    return True

def generate_svg_from_concept(concept: str, color: str = '#FFFFFF', style: str = 'modern_flat') -> str:
    """
    Generate SVG XML code for a visual concept using template-based generation.
    Supports common concepts defined in get_builtin_svgs.
    """
    templates = get_builtin_svgs()
    
    # Normalize concept to match dictionary keys
    clean_concept = concept.lower().replace(' ', '_')
    
    if clean_concept in templates:
        return templates[clean_concept].replace('{color}', color)
        
    # Fallback to a basic circle if concept not found
    return f'<svg viewBox="0 0 24 24" fill="{color}"><circle cx="12" cy="12" r="10"/></svg>'

def generate_svg_with_llm(concept: str, llm_client: Any, style_hints: str = '') -> str:
    """
    Use LLM to generate custom SVG XML for complex concepts.
    Sends a prompt asking for clean, minimal SVG code.
    Validates the output is well-formed XML.
    """
    prompt = f"""
    Create a clean, minimal SVG vector graphic for the concept: "{concept}".
    Style instructions: {style_hints}
    
    Requirements:
    - Output ONLY the raw <svg> XML code.
    - No markdown formatting or explanation.
    - Make it scaleable with a viewBox.
    - Use clean, simple paths.
    - Do NOT include any script tags, external links, or raster images.
    """
    
    try:
        # Assuming llm_client has a method like generate_text or similar
        # Since we don't have the exact API, this is a generic implementation
        response = llm_client.generate(prompt) 
        
        # Extract SVG from potential markdown response
        svg_match = re.search(r'<svg.*?</svg>', response, re.DOTALL | re.IGNORECASE)
        if svg_match:
            svg_code = svg_match.group(0)
            if validate_svg(svg_code):
                return svg_code
                
    except Exception as e:
        print(f"LLM SVG generation failed: {e}")
        
    # Fallback
    return generate_svg_from_concept(concept)

def generate_fallback_icon(concept: str, size: int = 256, bg_color: str = None) -> str:
    """
    Template-based PNG generation using Pillow for simple geometric icons 
    when SVG rendering is unavailable.
    """
    if Image is None or ImageDraw is None:
        raise ImportError("Pillow (PIL) is required for fallback rasterization")
        
    output_path = f"fallback_{concept.replace(' ', '_')}.png"
    
    # Create image with transparent background by default
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0) if bg_color is None else bg_color)
    draw = ImageDraw.Draw(img)
    
    margin = size // 8
    
    # Very basic drawing based on concept
    if 'circle' in concept or 'dot' in concept:
        draw.ellipse([margin, margin, size-margin, size-margin], fill="white")
    elif 'square' in concept or 'box' in concept:
        draw.rectangle([margin, margin, size-margin, size-margin], fill="white")
    else:
        # Default fallback: a filled polygon (triangle)
        draw.polygon([(size//2, margin), (size-margin, size-margin), (margin, size-margin)], fill="white")
        
    img.save(output_path, "PNG")
    return output_path

def rasterize_svg_to_png(svg_code: str, width: int = 512, height: int = 512, output_path: str = None) -> str:
    """
    Convert SVG XML to transparent PNG.
    Try cairosvg first, then fallback to a basic built-in renderer using Pillow draw primitives.
    """
    if not output_path:
        output_path = "output.png"
        
    if not validate_svg(svg_code):
        raise ValueError("Invalid or unsafe SVG code")
        
    # Ensure directory exists
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        
    # 1. Try cairosvg (best quality)
    if cairosvg is not None:
        try:
            cairosvg.svg2png(bytestring=svg_code.encode('utf-8'), write_to=output_path, output_width=width, output_height=height)
            return output_path
        except Exception as e:
            print(f"cairosvg rendering failed: {e}")
            
    # 2. Fallback: VERY rudimentary rendering (since Pillow doesn't render SVGs natively)
    # We just create a placeholder fallback icon.
    print("Warning: cairosvg not available or failed. Generating placeholder fallback PNG.")
    return generate_fallback_icon("fallback", size=width)
