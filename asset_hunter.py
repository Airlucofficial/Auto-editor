import json
import os
import urllib.request
import urllib.parse
import urllib.error
import re
from typing import List, Dict, Any, Optional
from datetime import datetime

class AssetHunter:
    """
    An autonomous asset retrieval agent that searches ONLY copyright-safe repositories.
    Zero unfiltered web crawling.
    """

    def __init__(self, storage_dir: str = 'storage/assets', config_path: str = 'storage/openrouter_config.json'):
        """
        Initialize the AssetHunter with storage directory and config.
        
        Args:
            storage_dir (str): Directory to store downloaded assets.
            config_path (str): Path to configuration file containing API keys.
        """
        self.storage_dir = storage_dir
        self.config_path = config_path
        self.headers = {'User-Agent': 'AutoEditor/1.0 (https://github.com/Airlucofficial/Auto-editor)'}
        self.timeout = 10.0
        
        os.makedirs(self.storage_dir, exist_ok=True)
        
        self.api_keys = self._load_config()

    def _load_config(self) -> Dict[str, str]:
        """Load API keys from config file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _make_request(self, url: str, headers: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        """Helper to make HTTP GET request and return JSON."""
        req_headers = self.headers.copy()
        if headers:
            req_headers.update(headers)
        
        req = urllib.request.Request(url, headers=req_headers)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                if response.status == 200:
                    data = response.read()
                    return json.loads(data.decode('utf-8'))
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
            print(f"Request failed for {url}: {e}")
        return None

    def search_openverse(self, query: str, license_filter: str = 'cc0,pdm', media_type: str = 'image', max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search Openverse API for CC0/Public Domain media.
        
        Args:
            query (str): Search query.
            license_filter (str): Licenses to filter by.
            media_type (str): Type of media (image, audio).
            max_results (int): Max number of results to return.
            
        Returns:
            List[Dict]: List of asset dictionaries.
        """
        base_url = f"https://api.openverse.org/v1/{media_type}s/"
        params = {
            'q': query,
            'license': license_filter,
            'page_size': max_results
        }
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        data = self._make_request(url)
        results = []
        
        if data and 'results' in data:
            for item in data['results']:
                results.append({
                    'url': item.get('url'),
                    'title': item.get('title'),
                    'license': item.get('license'),
                    'attribution': item.get('attribution'),
                    'source': 'openverse',
                    'thumbnail_url': item.get('thumbnail')
                })
                
        return results

    def search_iconify(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search Iconify API for MIT/Apache-2.0 icons.
        
        Args:
            query (str): Search query.
            limit (int): Max number of results.
            
        Returns:
            List[Dict]: List of icon dictionaries.
        """
        base_url = "https://api.iconify.design/search"
        params = {
            'query': query,
            'limit': limit
        }
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        data = self._make_request(url)
        results = []
        
        if data and 'icons' in data:
            for icon_str in data['icons']:
                parts = icon_str.split(':')
                if len(parts) == 2:
                    prefix, name = parts
                    svg_url = f"https://api.iconify.design/{prefix}/{name}.svg"
                    results.append({
                        'prefix': prefix,
                        'name': name,
                        'svg_url': svg_url,
                        'license': 'mit/apache2', # Iconify is generally open source
                        'source': 'iconify'
                    })
                    
        return results

    def search_pexels(self, query: str, per_page: int = 5) -> List[Dict[str, Any]]:
        """
        Search Pexels API for commercial-safe stock photos.
        Requires PEXELS_API_KEY in config.
        
        Args:
            query (str): Search query.
            per_page (int): Number of results per page.
            
        Returns:
            List[Dict]: List of photo dictionaries.
        """
        api_key = self.api_keys.get('PEXELS_API_KEY')
        if not api_key:
            return []
            
        base_url = "https://api.pexels.com/v1/search"
        params = {
            'query': query,
            'per_page': per_page
        }
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        headers = {'Authorization': api_key}
        data = self._make_request(url, headers=headers)
        results = []
        
        if data and 'photos' in data:
            for item in data['photos']:
                results.append({
                    'url': item.get('url'),
                    'photographer': item.get('photographer'),
                    'src_urls': item.get('src', {}),
                    'source': 'pexels',
                    'license': 'pexels_license'
                })
                
        return results

    def search_pixabay(self, query: str, per_page: int = 5) -> List[Dict[str, Any]]:
        """
        Search Pixabay API for zero-attribution stock media.
        Requires PIXABAY_API_KEY in config.
        
        Args:
            query (str): Search query.
            per_page (int): Number of results per page.
            
        Returns:
            List[Dict]: List of media dictionaries.
        """
        api_key = self.api_keys.get('PIXABAY_API_KEY')
        if not api_key:
            return []
            
        base_url = "https://pixabay.com/api/"
        params = {
            'key': api_key,
            'q': query,
            'per_page': per_page,
            'safesearch': 'true'
        }
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        data = self._make_request(url)
        results = []
        
        if data and 'hits' in data:
            for item in data['hits']:
                results.append({
                    'url': item.get('largeImageURL'),
                    'tags': item.get('tags'),
                    'preview_url': item.get('previewURL'),
                    'source': 'pixabay',
                    'license': 'pixabay_license'
                })
                
        return results

    def extract_visual_entities(self, transcript_text: Any) -> List[Dict[str, Any]]:
        """
        Extract visual entities from transcript text using simple NLP heuristics.
        
        Args:
            transcript_text: The transcript text (str), list of chunks/segments, or transcript dict.
            
        Returns:
            List[Dict]: List of extracted entities.
        """
        entities = []
        if isinstance(transcript_text, dict):
            text = transcript_text.get("text", "")
            if not text and "segments" in transcript_text:
                text = " ".join([s.get("text", "") for s in transcript_text.get("segments", [])])
            transcript_text = text
        elif isinstance(transcript_text, list):
            parts = []
            for item in transcript_text:
                if isinstance(item, dict):
                    parts.append(item.get("text", item.get("word", "")))
                else:
                    parts.append(str(item))
            transcript_text = " ".join(parts)
        elif not isinstance(transcript_text, str):
            transcript_text = str(transcript_text or "")
            
        # Simple keywords indicating visual concepts
        visual_keywords = ['chart', 'icon', 'graph', 'arrow', 'warning', 'logo', 'button', 'badge']
        
        words = transcript_text.split()
        for i, word in enumerate(words):
            clean_word = re.sub(r'[^a-zA-Z0-9]', '', word.lower())
            
            # Check for visual keywords
            if clean_word in visual_keywords:
                entities.append({
                    'entity': clean_word,
                    'type': 'icon' if clean_word in ['icon', 'arrow', 'badge'] else 'graphic',
                    'context': ' '.join(words[max(0, i-3):min(len(words), i+4)]),
                    'timestamp_hint': i # Simplified timestamp hint based on word index
                })
            
            # Check for capitalized nouns (potential subjects)
            elif word.istitle() and len(clean_word) > 2:
                entities.append({
                    'entity': clean_word,
                    'type': 'subject',
                    'context': ' '.join(words[max(0, i-3):min(len(words), i+4)]),
                    'timestamp_hint': i
                })
                
        return entities

    def download_asset(self, url: str, filename: str) -> str:
        """
        Download an asset to the storage directory.
        
        Args:
            url (str): URL of the asset.
            filename (str): Name to save the file as.
            
        Returns:
            str: Local path to the downloaded asset.
        """
        local_path = os.path.join(self.storage_dir, filename)
        
        req = urllib.request.Request(url, headers=self.headers)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response, open(local_path, 'wb') as out_file:
                out_file.write(response.read())
            return local_path
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return ""

    def resolve_assets(self, entities: List[Dict[str, Any]], prefer_svg: bool = True) -> List[Dict[str, Any]]:
        """
        Resolve and download assets for given entities from safe sources.
        
        Args:
            entities (List[Dict]): List of extracted entities.
            prefer_svg (bool): Whether to prioritize SVGs/icons.
            
        Returns:
            List[Dict]: List of resolved asset dictionaries with local paths.
        """
        resolved_assets = []
        
        for i, entity in enumerate(entities):
            query = entity['entity']
            downloaded = False
            
            if prefer_svg or entity.get('type') == 'icon':
                # Try Iconify
                icon_results = self.search_iconify(query, limit=1)
                if icon_results:
                    icon = icon_results[0]
                    filename = f"icon_{i}_{icon['name']}.svg"
                    local_path = self.download_asset(icon['svg_url'], filename)
                    if local_path:
                        resolved_assets.append({
                            'entity': query,
                            'local_path': local_path,
                            'source': 'iconify',
                            'license': icon['license'],
                            'attribution': f"{icon['prefix']}/{icon['name']} via Iconify"
                        })
                        downloaded = True
                        
            if not downloaded:
                # Try Openverse
                ov_results = self.search_openverse(query, max_results=1)
                if ov_results:
                    img = ov_results[0]
                    filename = f"ov_{i}_{query}.jpg"
                    local_path = self.download_asset(img['url'], filename)
                    if local_path:
                        resolved_assets.append({
                            'entity': query,
                            'local_path': local_path,
                            'source': 'openverse',
                            'license': img['license'],
                            'attribution': img.get('attribution', 'Openverse Public Domain')
                        })
                        downloaded = True
                        
            if not downloaded:
                # Try Pixabay as fallback
                pb_results = self.search_pixabay(query, per_page=1)
                if pb_results:
                    img = pb_results[0]
                    filename = f"pb_{i}_{query}.jpg"
                    local_path = self.download_asset(img['url'], filename)
                    if local_path:
                        resolved_assets.append({
                            'entity': query,
                            'local_path': local_path,
                            'source': 'pixabay',
                            'license': img['license'],
                            'attribution': 'Pixabay License (No attribution required)'
                        })
                        
        return resolved_assets

    def create_license_record(self, asset_path: str, source: str, license_type: str, attribution: str = '', url: str = '') -> Dict[str, Any]:
        """Create a per-asset provenance record."""
        return {
            'asset_path': asset_path,
            'source': source,
            'license_type': license_type,
            'attribution': attribution,
            'url': url,
            'timestamp': datetime.now().isoformat()
        }

    def compile_license_manifest(self, timeline_assets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compile full LICENSE_MANIFEST.json from all assets used in a timeline."""
        manifest = {
            'generated_at': datetime.now().isoformat(),
            'assets': []
        }
        
        for asset in timeline_assets:
            manifest['assets'].append(self.create_license_record(
                asset.get('local_path', ''),
                asset.get('source', ''),
                asset.get('license', ''),
                asset.get('attribution', ''),
                asset.get('url', '')
            ))
            
        return manifest

    def save_license_manifest(self, manifest: Dict[str, Any], output_path: str = 'storage/LICENSE_MANIFEST.json'):
        """Write manifest to disk."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=4)

    def generate_youtube_attribution(self, manifest: Dict[str, Any]) -> str:
        """Generate ready-to-paste YouTube description attribution text for CC-BY 4.0 assets."""
        attribution_lines = ["--- Media Attributions ---"]
        for item in manifest.get('assets', []):
            if 'cc-by' in item.get('license_type', '').lower() or item.get('attribution'):
                attr = item.get('attribution', '')
                if attr:
                    attribution_lines.append(f"- {attr}")
        return "\n".join(set(attribution_lines))

if __name__ == '__main__':
    # Demo block
    print("Initializing AssetHunter...")
    hunter = AssetHunter(storage_dir='storage/demo_assets')
    
    print("\nExtracting entities from text...")
    text = "Look at this chart showing the trend. Also note the warning icon in the corner."
    entities = hunter.extract_visual_entities(text)
    print("Entities:", json.dumps(entities, indent=2))
    
    print("\nResolving assets...")
    resolved = hunter.resolve_assets(entities)
    print(f"Resolved {len(resolved)} assets.")
    
    manifest = hunter.compile_license_manifest(resolved)
    hunter.save_license_manifest(manifest, 'storage/demo_assets/LICENSE_MANIFEST.json')
    print("\nGenerated Youtube Attribution:")
    print(hunter.generate_youtube_attribution(manifest))
