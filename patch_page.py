#!/usr/bin/env python3
"""
Comprehensive, exact patch for out/_next/static/chunks/app/page-f2b7366e605a20db.js:
1. Exposes window._CANVAS_REDRAW and window._TRIGGER_CANVAS_DRAW.
2. Direct 64-style canvas caption rendering in tu callback with window._DRAW_CAPTION and preview support.
3. Exposes React's caption setters and timeline history functions to window.
4. Exposes window._TIMELINE_CLIPS and window._TIMELINE_TRANSITIONS for accurate cut detection.
5. Injects audio pre-mixing (/api/mix-audio) for voiceover volume & transition SFX.
6. Injects post-render caption burning (/api/burn-captions) for custom 64 styles and placement.
"""

file_path = "out/_next/static/chunks/app/page-f2b7366e605a20db.js"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Idempotency check: if already patched and scope integrity is preserved, exit cleanly
if (
    "window._CANVAS_REDRAW" in text
    and "};let eL=(0,l.useCallback)" in text
    and "window._SET_REACT_CAPTION_STYLE" in text
    and "window._SET_ASPECT" in text
):
    print("Page chunk is already patched and scope integrity is verified.")
    exit(0)

# 1. Canvas Redraw hook
s_redraw = "(0,l.useEffect)(()=>{eP.current=tu},[tu])"
assert s_redraw in text, "s_redraw target not found"
r_redraw = "(0,l.useEffect)(()=>{eP.current=tu;if(typeof window!==\"undefined\"){window._CANVAS_REDRAW=()=>eP.current&&eP.current(eI.current);window._TRIGGER_CANVAS_DRAW=window._CANVAS_REDRAW}},[tu])"
text = text.replace(s_redraw, r_redraw, 1)

# 2. Canvas tu caption drawing block
start_tu = "if(ef&&ep&&ep.length){let t=function(e,t){if(!e)return"
end_tu = "(l,t,s,i,eg,Math.round(i*(eN>0?eN:b[eb]||b.md)),ey)}"
idx1 = text.find(start_tu)
assert idx1 != -1, "start_tu not found"
idx2 = text.find(end_tu, idx1)
assert idx2 != -1, "end_tu not found"
old_tu_block = text[idx1:idx2 + len(end_tu)]

new_tu_block = (
    'if((ef&&ep&&ep.length)||(typeof window!=="undefined"&&(window._SHOW_CAPTION_PREVIEW||window._CAPTIONS_ON||window._IS_PLACING_CAPTION))){'
    'let t=(ep&&ep.length)?function(e,t){if(!e)return"";for(let a=0;a<e.length;a++)if(t>=e[a].start&&t<e[a].end)return e[a].text;return""}(ep,e):"";'
    'if(!t&&typeof window!=="undefined"&&(window._SHOW_CAPTION_PREVIEW||window._IS_PLACING_CAPTION||(!ep||!ep.length)))t="Sample Caption Text";'
    'let _drawn=false;'
    'if(typeof window!=="undefined"&&window._DRAW_CAPTION){'
    '_drawn=window._DRAW_CAPTION(l,t,s,i,(window._CURRENT_STYLE||eg),Math.round(i*(eN>0?eN:b[eb]||b.md)),ey,e,ep);'
    '}'
    'if(!_drawn&&t){'
    '!function(e,t,a,n,l,s,i){if(!t)return;let r=g[l]||g.classic,o=function(e,t){let a=String(e).replace(/\\s+/g," ").trim();if(!a)return[];if(a.length<=t)return[a];let n=a.split(" "),l=[],s="";for(let e of n){let a=s?"".concat(s," ").concat(e):e;s&&a.length>t?(l.push(s),s=e):s=a}return s&&l.push(s),l}(t,Math.max(8,Math.floor(.9*a/(.58*s)))),c=o.length,d=i>0?i:y(r);e.save(),e.font="700 ".concat(s,\'px "CaptionFont", system-ui, sans-serif\'),e.textAlign="center",e.textBaseline="alphabetic";for(let t=0;t<c;t++){let l=o[t],i=N(n,s,c,t,d)+.82*s;if(r.box){let t=e.measureText(l).width,n=.38*s,o=.12*s,c=i-.78*s-o,d=.98*s+2*o;e.fillStyle=r.box,e.fillRect((a-t)/2-n,c,t+2*n,d)}r.stroke&&(e.lineJoin="round",e.miterLimit=2,e.lineWidth=Math.max(2,s/7),e.strokeStyle=r.stroke,e.strokeText(l,a/2,i)),e.fillStyle=r.fill,e.fillText(l,a/2,i)}e.restore()}(l,t,s,i,eg,Math.round(i*(eN>0?eN:b[eb]||b.md)),ey)'
    '}'
    '}'
)
text = text[:idx1] + new_tu_block + text[idx1 + len(old_tu_block):]

# 3. Expose React setters and history functions to window
s_hist = "{slots:eE,transitionsByName:eR}=eN,"
assert s_hist in text, "s_hist target not found"
r_hist = (
    "{slots:eE,transitionsByName:eR}=eN;if(typeof window!==\"undefined\"){"
    "window._SET_REACT_CAPTION_STYLE=ee;"
    "window._SET_REACT_CAPTIONS_ON=q;"
    "window._REACT_UNDO=ek;"
    "window._REACT_REDO=eC;"
    "window._REACT_CAN_UNDO=()=>eM;"
    "window._REACT_CAN_REDO=()=>eS;"
    "window._CAPTIONS_ON=Y;"
    "};let "
)
text = text.replace(s_hist, r_hist, 1)

# Child component cues ref
s_child_ref = "ez=(0,l.useRef)(null);"
assert s_child_ref in text, "s_child_ref target not found"
r_child_ref = "ez=(0,l.useRef)(null);if(typeof window!==\"undefined\"){window._CAPTION_CUES=ep;}"
text = text.replace(s_child_ref, r_child_ref, 1)

# 4. Expose timeline clips and transitions
s_clips = "clips:e4,imageEls:e1,"
if s_clips in text:
    r_clips = "clips:(typeof window!==\"undefined\"?(window._TIMELINE_CLIPS=e4,window._TIMELINE_TRANSITIONS=eR,e4):e4),imageEls:e1,"
    text = text.replace(s_clips, r_clips, 1)

# 4b. Expose aspect ratio state and setter to window
t_aspect = "aspect:v,setAspect:b,fps:y,setFps:_,renderQuality:N,setRenderQuality:k"
if t_aspect in text:
    r_aspect = "aspect:(typeof window!==\"undefined\"?(window._ASPECT=v,window._SET_ASPECT=b,window._TIMELINE_DURATION=p,v):v),setAspect:b,fps:y,setFps:_,renderQuality:N,setRenderQuality:k"
    text = text.replace(t_aspect, r_aspect, 1)

# 4c. Expose voiceover audio element reference to window
t_audio = '(0,n.jsx)("audio",{ref:eE,src:s,hidden:!0})'
if t_audio in text:
    r_audio = '(0,n.jsx)("audio",{ref:(el)=>{eE.current=el;if(typeof window!=="undefined"){window._VOICEOVER_AUDIO_EL=el;}},src:s,hidden:!0})'
    text = text.replace(t_audio, r_audio, 1)

# 4d. Video element unmuted & DOM attachment for reliable audio output
t_video = 'n.src=a.url,n.muted=!0,n.playsInline=!0,n.preload="auto"'
if t_video in text:
    r_video = 'n.src=a.url,n.muted=!1,n.playsInline=!0,n.preload="auto";n.style.cssText="position:fixed;width:1px;height:1px;opacity:0.001;pointer-events:none;bottom:0;left:0;z-index:-999";if(typeof document!=="undefined"&&!document.getElementById("v_"+t)){n.id="v_"+t;document.body.appendChild(n)};'
    text = text.replace(t_video, r_video, 1)


# 5. Render spec caller parameters
s_render_call = "captions:r,captionStyle:Q,captionSize:et,captionLineHeight:en,captionFontScale:es,onProgress:ep"
assert s_render_call in text, "s_render_call target not found"
r_render_call = (
    "captions:r,captionStyle:(window._CURRENT_STYLE||Q),captionSize:et,captionLineHeight:en,"
    "captionFontScale:(window._CAPTION_POS?window._CAPTION_POS.scale:es),"
    "captionPosX:(window._CAPTION_POS?window._CAPTION_POS.x:void 0),"
    "captionPosY:(window._CAPTION_POS?window._CAPTION_POS.y:void 0),"
    "voiceVolume:window._VOICEOVER_VOLUME,sfxEnabled:window._SFX_ENABLED,sfxVolume:window._SFX_VOLUME,onProgress:ep"
)
text = text.replace(s_render_call, r_render_call, 1)

# 6. Audio pre-mix in async function m(e)
s_m_audio = "let M=new FormData;for(let[e,t]of(M.append(\"spec\",JSON.stringify({clips:a,width:i,height:r,fps:c,transitions:m,transitionDuration:h,motions:p,motionAmount:f,trims:x,volumes:g,speeds:v,fadeIn:b,fadeOut:j,captions:y,captionStyle:_,captionSize:N,captionLineHeight:w,captionFontScale:k})),M.append(\"audio\",s,s.name)"
assert s_m_audio in text, "s_m_audio target not found"
r_m_audio = (
    'if(typeof window!=="undefined"&&(window._VOICEOVER_VOLUME!==1||window._SFX_ENABLED)){'
    'try{'
    'let mixForm=new FormData;'
    'mixForm.append("audio",s,s.name);'
    'mixForm.append("voice_volume",window._VOICEOVER_VOLUME!==void 0?window._VOICEOVER_VOLUME:1);'
    'mixForm.append("sfx_volume",window._SFX_VOLUME!==void 0?window._SFX_VOLUME:.5);'
    'let sfxEvents=[];'
    'if(window._SFX_ENABLED&&a&&a.length>1){'
    'for(let i=1;i<a.length;i++){'
    'let cutSec=a[i].start;'
    'let transType=(m&&m[a[i].name])||"wipeleft";'
    'let sfxId=(window._SELECTED_SFX&&window._SELECTED_SFX!=="auto")?window._SELECTED_SFX:((window._GET_SMART_SFX&&window._GET_SMART_SFX(transType))||"whoosh_fast");'
    'sfxEvents.push({file:sfxId+".wav",timestamp:cutSec});'
    '}'
    '}'
    'mixForm.append("sfx_events",JSON.stringify(sfxEvents));'
    'let mixResp=await fetch("http://localhost:4001/api/mix-audio",{method:"POST",body:mixForm});'
    'if(mixResp.ok){'
    'let mixData=await mixResp.json();'
    'if(mixData.audio_url){'
    'let mixedBlob=await fetch(mixData.audio_url).then(e=>e.blob());'
    's=new File([mixedBlob],s.name,{type:s.type||"audio/wav"});'
    '}'
    '}'
    '}catch(e){console.warn("Audio pre-mix fallback:",e)}'
    '}'
    'let M=new FormData;for(let[e,t]of(M.append("spec",JSON.stringify({clips:a,width:i,height:r,fps:c,transitions:m,transitionDuration:h,motions:p,motionAmount:f,trims:x,volumes:g,speeds:v,fadeIn:b,fadeOut:j,captions:(typeof window!=="undefined"&&window._COMPANION_ONLINE?null:y),captionStyle:(typeof window!=="undefined"?window._CURRENT_STYLE||_:_),captionSize:N,captionLineHeight:w,captionFontScale:(typeof window!=="undefined"&&window._CAPTION_POS?window._CAPTION_POS.scale:k),captionPosX:(typeof window!=="undefined"&&window._CAPTION_POS?window._CAPTION_POS.x:void 0),captionPosY:(typeof window!=="undefined"&&window._CAPTION_POS?window._CAPTION_POS.y:void 0),voiceVolume:(typeof window!=="undefined"?window._VOICEOVER_VOLUME:1),sfxEnabled:(typeof window!=="undefined"?window._SFX_ENABLED:!1),sfxVolume:(typeof window!=="undefined"?window._SFX_VOLUME:.5)})),M.append("audio",s,s.name)'
)
text = text.replace(s_m_audio, r_m_audio, 1)

# 7. Post-render caption burn in async function m(e)
s_m_return = "let{jobId:S}=await t.json();return await d(S,C)"
assert s_m_return in text, "s_m_return target not found"
r_m_return = (
    'let{jobId:S}=await t.json();'
    'let _resBlob=await d(S,C);'
    'if(typeof window!=="undefined"&&(window._CAPTIONS_ON||(y&&y.length))){'
    'try{'
    'let burnForm=new FormData;'
    'burnForm.append("video",_resBlob,"rendered.mp4");'
    'let transcriptToBurn=y||window._CAPTION_CUES||[];'
    'if(transcriptToBurn&&transcriptToBurn.length){'
    'let assResp=await fetch("http://localhost:4001/api/generate-ass",{'
    'method:"POST",headers:{"Content-Type":"application/json"},'
    'body:JSON.stringify({'
    'transcript:transcriptToBurn,'
    'style:(window._CURRENT_STYLE||_),'
    'width:i,height:r,'
    'pos_x:(window._CAPTION_POS?window._CAPTION_POS.x:.5),'
    'pos_y:(window._CAPTION_POS?window._CAPTION_POS.y:.85),'
    'font_scale:(window._CAPTION_POS?window._CAPTION_POS.scale:1)'
    '})});'
    'if(assResp.ok){'
    'let assData=await assResp.json();'
    'burnForm.append("ass_content",assData.ass_content);'
    'let burnResp=await fetch("http://localhost:4001/api/burn-captions",{method:"POST",body:burnForm});'
    'if(burnResp.ok){'
    'let burnData=await burnResp.json();'
    'if(burnData.video_url){'
    'let burnedVid=await fetch(burnData.video_url);'
    'if(burnedVid.ok)_resBlob=await burnedVid.blob()'
    '}'
    '}'
    '}'
    '}'
    '}catch(e){console.warn("Caption burn fallback:",e)}'
    '}'
    'return _resBlob'
)
text = text.replace(s_m_return, r_m_return, 1)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully applied comprehensive patch to page-f2b7366e605a20db.js!")
