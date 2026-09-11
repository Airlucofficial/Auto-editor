import os
import json
import subprocess
import uuid
from datetime import datetime
from typing import List, Dict, Tuple, Any, Optional

def distill_style_profile(reference_videos: List[str], output_path: str, llm_client=None) -> Dict[str, Any]:
    """Main entry point. Analyzes reference videos and compiles a .dna.json profile."""
    # Simplified version, normally would analyze videos and use LLM
    profile = {
        "profile_name": "custom_profile",
        "display_name": "Custom Profile",
        "description": "Distilled from reference videos",
        "version": "1.0",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "hook_phase": {
            "duration_s": 5.0,
            "asl_range": [0.8, 1.4],
            "acceleration": "exponential",
            "cadence_formula": "L_i = L_0 * exp(-k * t)",
            "visual_density": "high",
            "sfx_triggers": ["cinematic_boom", "impact_punch"]
        },
        "buildup_phase": {
            "asl_range": [2.5, 3.5],
            "overlay_triggers": ["noun", "metric", "statistic", "proper_noun"],
            "pacing": "stable",
            "sfx_triggers": ["swoosh_smooth", "gentle_chime"]
        },
        "climax_phase": {
            "punch_zoom": 1.15,
            "sfx": "cinematic_boom",
            "transition": "whip",
            "asl_range": [0.6, 1.2]
        },
        "typography": {
            "font": "Montserrat Black",
            "position_y": 0.78,
            "position_x": 0.50,
            "style_key": "bold",
            "shadow_px": 3.5,
            "min_contrast_ratio": 4.5
        },
        "pacing": {
            "boredom_threshold_s": 2.8,
            "jcut_offset_ms": -80,
            "optical_flow_min_pct": 12,
            "ken_burns_scale": 1.08
        },
        "sound_design": {
            "ducking_db": -18,
            "ducking_freq_range": [1000, 4000],
            "vocal_target_lufs": -14,
            "sfx_volume_db": -6,
            "jcut_audio_lead_ms": -80
        },
        "asset_preferences": {
            "sticker_style": "flat_modern",
            "icon_set": "lucide",
            "overlay_opacity": 0.85
        }
    }
    if output_path:
        save_profile(profile, output_path)
    return profile

def generate_mosaic_grid(video_path: str, scene_start: float, scene_duration: float = 10.0, grid_size: int = 4) -> str:
    """Uses FFmpeg to extract keyframes across a scene, stitches them into a contact sheet PNG."""
    output_path = f"mosaic_{uuid.uuid4().hex[:8]}.png"
    fps = (grid_size * grid_size) / scene_duration
    
    cmd = [
        "ffmpeg.exe",
        "-ss", str(scene_start),
        "-t", str(scene_duration),
        "-i", video_path,
        "-vf", f"fps={fps},scale=320:-1,tile={grid_size}x{grid_size}",
        "-y",
        output_path
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error generating mosaic: {e}")
        return ""
        
    return output_path

def analyze_pacing(video_path: str) -> Dict[str, Any]:
    """Uses FFmpeg scene detection to find cuts and computes pacing metrics."""
    cmd = [
        "ffmpeg.exe",
        "-i", video_path,
        "-filter:v", "select='gt(scene,0.3)',showinfo",
        "-f", "null",
        "-"
    ]
    
    # In a real implementation, we would parse ffmpeg stderr for showinfo output
    # Here we simulate the return structure
    return {
        "total_duration": 60.0,
        "cut_count": 15,
        "average_shot_length": 4.0,
        "cut_timestamps": [4.0, 8.5, 12.1, 15.0],
        "pacing_curve": [4.0, 3.5], # ASL per 30s window
        "hook_asl": 1.2
    }

def build_state_machine(pacing_data: Dict[str, Any], total_duration: float) -> Dict[str, Any]:
    """Constructs editorial Finite State Machine."""
    return {
        "states": ["hook", "build_up", "climax"],
        "transitions": {
            "hook_to_buildup": 5.0,
            "buildup_to_climax": total_duration * 0.8
        },
        "hook_phase": {
            "duration": 5.0,
            "cadence": "L_i = L_0 * e^(-k*t)",
            "asl_range": [0.8, 1.4]
        },
        "concept_build_up": {
            "start": 5.0,
            "end": total_duration * 0.8,
            "asl_range": [2.5, 3.5]
        },
        "climax_phase": {
            "start": total_duration * 0.8,
            "end": total_duration,
            "actions": ["rapid_cuts", "punch_zoom", "high_impact_sound"]
        }
    }

def apply_jcut_offset(timeline: List[Dict[str, Any]], offset_ms: int = -80) -> List[Dict[str, Any]]:
    """Shifts audio events to precede visual cuts by offset_ms (J-cut anticipation effect)"""
    new_timeline = []
    offset_s = offset_ms / 1000.0
    for event in timeline:
        new_event = dict(event)
        # Handle both ms and second representations, and audio or cut events
        if "start_ms" in new_event:
            new_event["start_ms"] = max(0, new_event["start_ms"] + offset_ms)
        if "timestamp" in new_event and new_event.get("type") in ("audio", "sfx", "cut"):
            new_event["timestamp"] = max(0.0, round(new_event["timestamp"] + offset_s, 3))
        new_timeline.append(new_event)
    return new_timeline

def detect_static_scenes(timeline: List[Dict[str, Any]], threshold_s: float = 2.8) -> List[Dict[str, Any]]:
    """Scans timeline for scenes exceeding threshold without motion."""
    static_scenes = []
    for scene in timeline:
        start = float(scene.get("start", 0))
        end = float(scene.get("end", start))
        duration = float(scene.get("duration", max(0.0, end - start)))
        if duration > threshold_s and not scene.get("motion_detected", False):
            static_scenes.append({
                "start": start,
                "end": end,
                "duration": duration,
                "suggested_fix": "add_broll_or_punch_in"
            })
    return static_scenes

def inject_ken_burns(scene: Dict[str, Any], scale_from: float = 1.0, scale_to: float = 1.08) -> Dict[str, Any]:
    """Returns modified scene with subtle zoom punch-in parameters"""
    new_scene = dict(scene)
    new_scene["effects"] = new_scene.get("effects", [])
    new_scene["effects"].append({
        "type": "ken_burns",
        "scale_from": scale_from,
        "scale_to": scale_to
    })
    return new_scene

def clamp_safe_zones(elements: List[Dict[str, Any]], y_range: Tuple[float, float] = (0.65, 0.80), x_center: float = 0.50) -> List[Dict[str, Any]]:
    """Constrains subtitle/sticker coordinates within eye-line safe zones"""
    clamped = []
    for el in elements:
        new_el = dict(el)
        # Handle position_y or y
        if "position_y" in new_el:
            new_el["position_y"] = max(y_range[0], min(y_range[1], float(new_el["position_y"])))
        elif "y" in new_el:
            new_el["y"] = max(y_range[0], min(y_range[1], float(new_el["y"])))
        # Handle position_x or x
        if "position_x" in new_el:
            new_el["position_x"] = x_center
        elif "x" in new_el:
            new_el["x"] = x_center
        clamped.append(new_el)
    return clamped

def load_profile(profile_path: str) -> Dict[str, Any]:
    """Load a .dna.json profile from disk or profile name"""
    if not profile_path:
        return {}
    if os.path.exists(profile_path) and os.path.isfile(profile_path):
        with open(profile_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Try relative to storage/profiles
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base_dir, "storage", "profiles", profile_path),
        os.path.join(base_dir, "storage", "profiles", f"{profile_path}.dna.json"),
        os.path.join("storage", "profiles", profile_path),
        os.path.join("storage", "profiles", f"{profile_path}.dna.json"),
    ]
    for c in candidates:
        if os.path.exists(c) and os.path.isfile(c):
            with open(c, "r", encoding="utf-8") as f:
                return json.load(f)
                
    # Search factory profile
    try:
        return get_factory_profile(profile_path)
    except Exception:
        return {}

def save_profile(profile_data: Dict[str, Any], output_path: str) -> None:
    """Save a .dna.json profile"""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=2)

def list_profiles(profiles_dir: str = 'storage/profiles') -> List[Dict[str, Any]]:
    """List all available profiles with metadata"""
    profiles = []
    if not os.path.exists(profiles_dir):
        return profiles
    for filename in os.listdir(profiles_dir):
        if filename.endswith('.dna.json'):
            path = os.path.join(profiles_dir, filename)
            try:
                data = load_profile(path)
                profiles.append({
                    "filename": filename,
                    "profile_name": data.get("profile_name", ""),
                    "display_name": data.get("display_name", ""),
                    "version": data.get("version", "")
                })
            except Exception:
                pass
    return profiles

def get_factory_profile(name: str) -> Dict[str, Any]:
    """Get a built-in factory profile by name"""
    profiles_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'storage', 'profiles')
    expected_path = os.path.join(profiles_dir, f"{name}.dna.json")
    if os.path.exists(expected_path):
        return load_profile(expected_path)
    # Search by profile_name inside
    for filename in os.listdir(profiles_dir):
        if filename.endswith('.dna.json'):
            path = os.path.join(profiles_dir, filename)
            try:
                data = load_profile(path)
                if data.get("profile_name") == name:
                    return data
            except Exception:
                pass
    raise FileNotFoundError(f"Profile {name} not found.")
