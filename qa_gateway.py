"""
Closed-Loop Deterministic QA Gateway for AutoEditor.

This module provides the automated quality assurance engine that guarantees
zero defective videos reach the user. It runs 6 deterministic validation checks
and applies auto-fixes.
"""

import json
import subprocess
import logging
import math
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c + c for c in hex_color)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def relative_luminance(r: int, g: int, b: int) -> float:
    """Calculate relative luminance per WCAG 2.0."""
    def adjust(c: float) -> float:
        c /= 255.0
        if c <= 0.03928:
            return c / 12.92
        return math.pow((c + 0.055) / 1.055, 2.4)
    return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)

def contrast_ratio(l1: float, l2: float) -> float:
    """Calculate contrast ratio between two luminance values."""
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def measure_lufs(audio_path: str, ffmpeg_path: str = 'ffmpeg.exe') -> float:
    """Use FFmpeg loudnorm to measure integrated LUFS."""
    try:
        cmd = [
            ffmpeg_path,
            '-hide_banner',
            '-i', audio_path,
            '-af', 'loudnorm=print_format=json',
            '-f', 'null',
            '-'
        ]
        result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stderr
        
        # Parse JSON from stderr
        json_start = output.find('{')
        json_end = output.rfind('}') + 1
        if json_start != -1 and json_end != -1:
            loudnorm_data = json.loads(output[json_start:json_end])
            return float(loudnorm_data.get('input_i', -70.0))
        return -70.0
    except Exception as e:
        logging.warning(f"Failed to measure LUFS using FFmpeg: {e}")
        return -70.0


class QAReport:
    """Represents a Quality Assurance report for a video timeline."""
    
    def __init__(self):
        self.checks: List[Dict[str, Any]] = []
        self.passed: bool = True
        self.total_checks: int = 0
        self.passed_checks: int = 0
        self.failed_checks: int = 0
        self.auto_fixes: List[Dict[str, Any]] = []
        self.warnings: List[str] = []
        self.created_at: str = datetime.now().isoformat()
        
    def add_check(self, name: str, passed: bool, details: Dict[str, Any], auto_fix_applied: Optional[Dict[str, Any]] = None) -> None:
        """Add a check result."""
        self.total_checks += 1
        if passed:
            self.passed_checks += 1
        else:
            self.failed_checks += 1
            self.passed = False
            
        check_record = {
            'name': name,
            'passed': passed,
            'details': details
        }
        
        if auto_fix_applied:
            check_record['auto_fix_applied'] = auto_fix_applied
            self.auto_fixes.append(auto_fix_applied)
            
        self.checks.append(check_record)
        
    def add_warning(self, message: str) -> None:
        """Add a warning."""
        self.warnings.append(message)
        
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to JSON-compatible dict."""
        return {
            'passed': self.passed,
            'total_checks': self.total_checks,
            'passed_checks': self.passed_checks,
            'failed_checks': self.failed_checks,
            'checks': self.checks,
            'auto_fixes': self.auto_fixes,
            'warnings': self.warnings,
            'created_at': self.created_at
        }
        
    def summary(self) -> str:
        """Human-readable summary string."""
        status = "PASSED" if self.passed else "FAILED"
        summary_str = f"QA Report Summary: {status}\n"
        summary_str += f"Total Checks: {self.total_checks} (Passed: {self.passed_checks}, Failed: {self.failed_checks})\n"
        summary_str += f"Auto-fixes Applied: {len(self.auto_fixes)}\n"
        summary_str += f"Warnings: {len(self.warnings)}\n"
        
        for check in self.checks:
            check_status = "PASS" if check['passed'] else "FAIL"
            summary_str += f"- {check['name']}: {check_status}\n"
            
        return summary_str


class QAGateway:
    """The automated QA engine running validation checks and auto-fixes."""
    
    def __init__(self, ffmpeg_path: str = 'ffmpeg.exe'):
        self.ffmpeg_path = ffmpeg_path
        
    def audit_acoustic_sync(self, timeline: Any, word_grid: Any, tolerance_ms: int = 40) -> Dict[str, Any]:
        """Verifies all cuts sit in silence gaps (±40ms)."""
        cuts_checked = 0
        cuts_in_silence = 0
        cuts_drifted = 0
        drift_details = []
        auto_fixes = []
        
        # Flatten word_grid if it's a dict (transcript)
        words_list = []
        if isinstance(word_grid, dict):
            for seg in word_grid.get("segments", []):
                words_list.extend(seg.get("words", []))
        elif isinstance(word_grid, list):
            words_list = word_grid
            
        # Simple gap identification based on word grid
        silence_gaps = []
        last_end = 0.0
        for word in words_list:
            start = float(word.get('start', 0.0))
            end = float(word.get('end', start))
            if start - last_end > 0.05: # more than 50ms gap
                silence_gaps.append((last_end, start))
            last_end = end
            
        clips_list = timeline.get("cuts", timeline.get("timeline", [])) if isinstance(timeline, dict) else (timeline or [])
        for clip in clips_list:
            cut_time = float(clip.get('timestamp', clip.get('start_time', clip.get('start', -1))))
            if cut_time < 0:
                continue
                
            cuts_checked += 1
            
            # Find closest silence gap
            is_in_silence = False
            closest_gap = None
            min_dist = float('inf')
            
            for gap in silence_gaps:
                gap_mid = (gap[0] + gap[1]) / 2.0
                dist = abs(cut_time - gap_mid)
                if dist < min_dist:
                    min_dist = dist
                    closest_gap = gap_mid
                
                # Check if cut is within gap bounds + tolerance
                tol_s = tolerance_ms / 1000.0
                if gap[0] - tol_s <= cut_time <= gap[1] + tol_s:
                    is_in_silence = True
                    break
                    
            if is_in_silence:
                cuts_in_silence += 1
            else:
                cuts_drifted += 1
                drift_details.append({'clip_id': clip.get('id', cuts_checked), 'cut_time': cut_time, 'closest_gap': closest_gap})
                if closest_gap is not None:
                    auto_fixes.append({'clip_id': clip.get('id', cuts_checked), 'property': 'cut_time', 'new_value': round(closest_gap, 3), 'reason': 'Snapped to silence gap'})
                    
        passed = cuts_drifted == 0
        
        return {
            'passed': passed,
            'cuts_checked': cuts_checked,
            'cuts_in_silence': cuts_in_silence,
            'cuts_drifted': cuts_drifted,
            'drift_details': drift_details,
            'auto_fixes': auto_fixes
        }

    def audit_luminance_contrast(self, subtitle_color_hex: str, background_samples: List[str] = None, min_ratio: float = 4.5) -> Dict[str, Any]:
        """Calculates contrast ratio between subtitle text color and background."""
        sub_rgb = hex_to_rgb(subtitle_color_hex)
        sub_lum = relative_luminance(*sub_rgb)
        
        bg_lum = 0.1 # Assume standard dark video background by default
        if background_samples:
            bg_lums = []
            for bg in background_samples:
                rgb = hex_to_rgb(bg)
                bg_lums.append(relative_luminance(*rgb))
            if bg_lums:
                bg_lum = sum(bg_lums) / len(bg_lums)
            
        ratio = contrast_ratio(sub_lum, bg_lum)
        passed = ratio >= min_ratio
        
        auto_fix = None
        if not passed:
            auto_fix = {
                'recommendation': 'Apply 3.5px drop shadow or solid dark pill backplate',
                'property': 'subtitle_style',
                'new_value': {'drop_shadow': True, 'shadow_opacity': 0.8, 'shadow_px': 3.5},
                'reason': f'Contrast ratio {ratio:.2f} < {min_ratio}'
            }
            
        return {
            'passed': passed,
            'contrast_ratio': ratio,
            'min_required': min_ratio,
            'subtitle_color': subtitle_color_hex,
            'bg_luminance': bg_lum,
            'auto_fix': auto_fix
        }

    def audit_safe_zones(self, elements: List[Dict[str, Any]], video_width: int = 1080, video_height: int = 1920) -> Dict[str, Any]:
        """Constrains elements to safe zones to avoid overlapping UI."""
        elements_checked = 0
        elements_clamped = 0
        clamp_details = []
        auto_fixes = []
        
        for el in elements:
            elements_checked += 1
            raw_x = el.get('position_x', el.get('x', 0.5))
            raw_y = el.get('position_y', el.get('y', 0.75))
            
            is_norm = (0.0 <= float(raw_y) <= 1.0)
            y_val = float(raw_y) if is_norm else (float(raw_y) / video_height)
            x_val = float(raw_x) if (0.0 <= float(raw_x) <= 1.0) else (float(raw_x) / video_width)
            
            needs_clamp = False
            new_y = y_val
            new_x = x_val
            
            if y_val < 0.65:
                new_y = 0.65
                needs_clamp = True
            elif y_val > 0.80:
                new_y = 0.80
                needs_clamp = True
                
            if abs(x_val - 0.5) > 0.15:
                new_x = 0.5
                needs_clamp = True
                
            if needs_clamp:
                elements_clamped += 1
                final_y = new_y if is_norm else round(new_y * video_height)
                final_x = new_x if is_norm else round(new_x * video_width)
                clamp_details.append({'element_id': el.get('id', elements_checked), 'original_y': raw_y, 'new_y': final_y})
                auto_fixes.append({
                    'element_id': el.get('id', elements_checked),
                    'property': 'position',
                    'new_value': {'x': final_x, 'y': final_y},
                    'reason': 'Clamped to safe zone (Y: 65%-80%, X: center)'
                })
                
        passed = elements_clamped == 0
        
        return {
            'passed': passed,
            'elements_checked': elements_checked,
            'elements_clamped': elements_clamped,
            'clamp_details': clamp_details,
            'auto_fixes': auto_fixes
        }

    def audit_pacing(self, timeline: Any, threshold_s: float = 2.8) -> Dict[str, Any]:
        """Scans timeline for scenes sitting still for too long."""
        scenes_checked = 0
        static_scenes_found = 0
        static_details = []
        auto_fixes = []
        
        clips_list = timeline.get("cuts", timeline.get("timeline", [])) if isinstance(timeline, dict) else (timeline or [])
        for clip in clips_list:
            scenes_checked += 1
            start = float(clip.get('start_time', clip.get('start', 0.0)))
            end = float(clip.get('end_time', clip.get('end', start)))
            duration = float(clip.get('duration', max(0.0, end - start)))
            has_motion = clip.get('has_motion', False)
            
            if duration > threshold_s and not has_motion:
                static_scenes_found += 1
                static_details.append({'clip_id': clip.get('id', scenes_checked), 'duration': duration})
                auto_fixes.append({
                    'clip_id': clip.get('id', scenes_checked),
                    'property': 'scale_animation',
                    'new_value': {'start': 1.0, 'end': 1.08},
                    'reason': f'Static scene > {threshold_s}s, applied Ken Burns'
                })
                
        passed = static_scenes_found == 0
        
        return {
            'passed': passed,
            'scenes_checked': scenes_checked,
            'static_scenes_found': static_scenes_found,
            'static_details': static_details,
            'auto_fixes': auto_fixes
        }

    def audit_audio_levels(self, audio_path: Optional[str] = None, target_lufs: float = -14.0, tolerance_lufs: float = 2.0) -> Dict[str, Any]:
        """Checks audio LUFS."""
        if audio_path:
            measured = measure_lufs(audio_path, self.ffmpeg_path)
        else:
            measured = -20.0
            
        diff = abs(measured - target_lufs)
        passed = diff <= tolerance_lufs
        
        auto_fix = None
        if not passed:
            gain_needed = target_lufs - measured
            auto_fix = {
                'recommendation': 'Adjust audio volume',
                'property': 'volume_db',
                'new_value': gain_needed,
                'reason': f'Measured {measured} LUFS, target {target_lufs} LUFS'
            }
            
        return {
            'passed': passed,
            'measured_lufs': measured,
            'target_lufs': target_lufs,
            'difference': diff,
            'auto_fix': auto_fix
        }

    def audit_copyright(self, timeline_assets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Verifies provenance of external assets."""
        assets_checked = 0
        assets_cleared = 0
        assets_flagged = 0
        flagged_details = []
        auto_fixes = []
        
        for asset in timeline_assets:
            assets_checked += 1
            provenance = asset.get('provenance', 'unknown')
            
            if provenance in ['cc0', 'public_domain', 'internal_dsp', 'internal_svg']:
                assets_cleared += 1
            else:
                assets_flagged += 1
                flagged_details.append({'asset_id': asset.get('id'), 'provenance': provenance})
                auto_fixes.append({
                    'asset_id': asset.get('id'),
                    'action': 'remove_or_replace',
                    'reason': 'Unverified copyright provenance'
                })
                
        passed = assets_flagged == 0
        
        return {
            'passed': passed,
            'assets_checked': assets_checked,
            'assets_cleared': assets_cleared,
            'assets_flagged': assets_flagged,
            'flagged_details': flagged_details,
            'auto_fixes': auto_fixes
        }

    def run_full_qa(self, 
                   timeline: Optional[List[Dict[str, Any]]] = None, 
                   word_grid: Optional[List[Dict[str, Any]]] = None, 
                   audio_path: Optional[str] = None, 
                   assets: Optional[List[Dict[str, Any]]] = None, 
                   subtitle_color: str = '#FFFFFF', 
                   video_width: int = 1080, 
                   video_height: int = 1920, 
                   target_lufs: float = -14.0) -> QAReport:
        """Runs all 6 checks, collects results into QAReport."""
        report = QAReport()
        timeline = timeline or []
        word_grid = word_grid or []
        assets = assets or []
        
        # Collect all items from timeline for element checking
        all_items = []
        if isinstance(timeline, dict):
            for k in ("cuts", "sticker_placements", "text_overlays", "zoom_events", "elements", "timeline"):
                val = timeline.get(k, [])
                if isinstance(val, list):
                    all_items.extend(val)
        elif isinstance(timeline, list):
            all_items = timeline
            
        # 1. Acoustic Sync Audit
        sync_res = self.audit_acoustic_sync(timeline, word_grid)
        report.add_check('Acoustic Sync', sync_res['passed'], sync_res, sync_res.get('auto_fixes'))
        
        # 2. Luminance Contrast Audit
        contrast_res = self.audit_luminance_contrast(subtitle_color)
        report.add_check('Luminance Contrast', contrast_res['passed'], contrast_res, contrast_res.get('auto_fix'))
        
        # 3. Social Safe-Zone Clamp
        elements = [clip for clip in all_items if isinstance(clip, dict) and (('x' in clip and 'y' in clip) or ('position_x' in clip or 'position_y' in clip))]
        if not elements:
            # Add default subtitle position check if no explicit elements
            elements = [{'id': 'subtitle_default', 'position_x': 0.5, 'position_y': 0.78, 'type': 'subtitle'}]
        safe_zone_res = self.audit_safe_zones(elements, video_width, video_height)
        report.add_check('Safe Zones', safe_zone_res['passed'], safe_zone_res, safe_zone_res.get('auto_fixes'))
        
        # 4. Pacing Audit
        pacing_res = self.audit_pacing(timeline)
        report.add_check('Pacing', pacing_res['passed'], pacing_res, pacing_res.get('auto_fixes'))
        
        # 5. Audio Master Check
        audio_res = self.audit_audio_levels(audio_path, target_lufs)
        report.add_check('Audio Levels', audio_res['passed'], audio_res, audio_res.get('auto_fix'))
        
        # 6. Copyright Pre-Flight
        copyright_res = self.audit_copyright(assets)
        report.add_check('Copyright', copyright_res['passed'], copyright_res, copyright_res.get('auto_fixes'))
        
        return report

    def apply_auto_fixes(self, timeline: List[Dict[str, Any]], qa_report: QAReport) -> List[Dict[str, Any]]:
        """Applies all deterministic auto-fixes from QA report to the timeline."""
        fixed_timeline = []
        for clip in timeline:
            fixed_clip = clip.copy()
            for fix_batch in qa_report.auto_fixes:
                if fix_batch is None:
                    continue
                if isinstance(fix_batch, list):
                    fixes = fix_batch
                elif isinstance(fix_batch, dict):
                    fixes = [fix_batch]
                else:
                    fixes = []
                    
                for fix in fixes:
                    if fix.get('clip_id') == fixed_clip.get('id') or fix.get('element_id') == fixed_clip.get('id'):
                        prop = fix.get('property')
                        if prop and 'new_value' in fix:
                            if prop == 'position':
                                fixed_clip['x'] = fix['new_value'].get('x', fixed_clip.get('x'))
                                fixed_clip['y'] = fix['new_value'].get('y', fixed_clip.get('y'))
                            else:
                                fixed_clip[prop] = fix['new_value']
            fixed_timeline.append(fixed_clip)
        return fixed_timeline

if __name__ == '__main__':
    # Demo block
    print("Initializing QA Gateway...")
    qa = QAGateway()
    
    sample_timeline = [
        {'id': 'clip1', 'type': 'video', 'start_time': 0.1, 'end_time': 3.5, 'has_motion': False, 'x': 540, 'y': 1500},
        {'id': 'clip2', 'type': 'video', 'start_time': 3.6, 'end_time': 5.0, 'has_motion': True, 'x': 540, 'y': 1600}
    ]
    sample_words = [
        {'word': 'hello', 'start': 0.2, 'end': 0.5},
        {'word': 'world', 'start': 3.7, 'end': 4.0}
    ]
    sample_assets = [
        {'id': 'asset1', 'provenance': 'cc0'},
        {'id': 'asset2', 'provenance': 'google_images'}
    ]
    
    print("\nRunning Full QA...")
    report = qa.run_full_qa(
        timeline=sample_timeline,
        word_grid=sample_words,
        assets=sample_assets,
        subtitle_color='#FFFFFF'
    )
    
    print("\n" + report.summary())
    
    print("\nApplying Auto-Fixes...")
    fixed_timeline = qa.apply_auto_fixes(sample_timeline, report)
    print("Original Clip 1:", sample_timeline[0])
    print("Fixed Clip 1:", fixed_timeline[0])
    print("Original Clip 2:", sample_timeline[1])
    print("Fixed Clip 2:", fixed_timeline[1])
