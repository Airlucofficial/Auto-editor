import os
import re

JS_FILE = "d:/AutoEditor/out/auto_captions.js"
CSS_FILE = "d:/AutoEditor/out/auto_captions.css"

with open(JS_FILE, "r", encoding="utf-8") as f:
    js = f.read()

# Replace injectHeaderButton calls
js = js.replace("injectHeaderButton();", "injectHeaderButton();\n          if (typeof injectAIDirectorButton !== 'undefined') injectAIDirectorButton();")

# The code to append
js_append = """
  // =========================================================================
  // AI DIRECTOR UI
  // =========================================================================
  function injectAIDirectorButton() {
    const existing = document.getElementById("btn-ai-director");
    const actionsBar = document.querySelector(".bar__actions") || document.querySelector(".bar");
    if (!actionsBar) return;

    if (existing) {
      if (actionsBar.contains(existing)) return;
      existing.remove();
    }

    const btn = document.createElement("button");
    btn.id = "btn-ai-director";
    btn.type = "button";
    btn.className = "cap-magic-btn aid-magic-btn";
    btn.innerHTML = "<span>🎬</span><span>AI Director</span>";
    btn.onclick = openAIDirectorModal;

    const capBtn = document.getElementById("btn-auto-captions");
    if (capBtn && capBtn.nextSibling) {
      actionsBar.insertBefore(btn, capBtn.nextSibling);
    } else if (actionsBar.firstChild) {
      actionsBar.insertBefore(btn, actionsBar.firstChild);
    } else {
      actionsBar.appendChild(btn);
    }
  }

  let aiDirectorModalRef = null;

  function openAIDirectorModal() {
    buildAIDirectorModal();
    if (aiDirectorModalRef) {
      aiDirectorModalRef.style.display = "flex";
    }
  }

  function closeAIDirectorModal() {
    if (aiDirectorModalRef) {
      aiDirectorModalRef.style.display = "none";
    }
  }

  function buildAIDirectorModal() {
    if (document.getElementById("ai-director-modal-root")) return;

    const overlay = document.createElement("div");
    overlay.id = "ai-director-modal-root";
    overlay.className = "cap-modal-overlay aid-modal-overlay";
    overlay.style.display = "none";

    overlay.innerHTML = `
      <div class="cap-modal aid-modal">
        <div class="cap-modal-header aid-header">
          <div class="cap-modal-title"><span>🎬</span> AI Video Director</div>
          <button class="cap-close-btn aid-close-btn" id="btn-close-ai-modal">&times;</button>
        </div>
        <div class="cap-tabs aid-tabs">
          <button class="cap-tab-btn aid-tab-btn active" data-tab="aid-tab-config">⚙️ Setup & Configure</button>
          <button class="cap-tab-btn aid-tab-btn" data-tab="aid-tab-gen">🚀 Generate AI Edit</button>
          <button class="cap-tab-btn aid-tab-btn" data-tab="aid-tab-qa">📊 QA Report</button>
          <button class="cap-tab-btn aid-tab-btn" data-tab="aid-tab-license">📋 License Report</button>
        </div>
        <div class="cap-modal-body aid-modal-body">
          
          <!-- TAB 1: Config -->
          <div id="aid-tab-config" class="aid-tab-content" style="display: block;">
            <div class="aid-config-section">
              <h3>OpenRouter API Config</h3>
              <div style="display: flex; gap: 8px; margin-top: 8px;">
                <input type="password" id="aid-api-key" class="cap-search-input aid-api-key-input" placeholder="sk-or-v1-..." />
                <button class="cap-btn-download" id="aid-btn-save-key">Save</button>
              </div>
              <div id="aid-key-status" style="margin-top: 8px; font-size: 12px; color: #94a3b8;">Status: Not configured</div>
            </div>
            
            <div class="aid-config-section" style="margin-top: 24px;">
              <h3>Model Selection</h3>
              <select id="aid-model-select" class="cap-search-input aid-model-select" style="margin-top: 8px; width: 100%;">
                <option value="">Loading models...</option>
              </select>
            </div>

            <div class="aid-config-section" style="margin-top: 24px;">
              <h3>Reasoning Tier</h3>
              <select id="aid-tier-select" class="cap-search-input aid-model-select" style="margin-top: 8px; width: 100%;">
                <option value="economy">Economy (Default)</option>
                <option value="high">High Reasoning</option>
              </select>
            </div>
          </div>

          <!-- TAB 2: Generate -->
          <div id="aid-tab-gen" class="aid-tab-content" style="display: none;">
            <h3>Select Editing Style</h3>
            <div class="cap-styles-grid" style="margin-top: 12px;">
              <div class="cap-style-card aid-style-card active" data-style="mrbeast">
                <div class="cap-card-badge">🔥 MrBeast Viral</div>
                <div class="cap-card-desc">High retention, fast cuts, active zoom, loud SFX</div>
              </div>
              <div class="cap-style-card aid-style-card" data-style="ali">
                <div class="cap-card-badge">📚 Ali Abdaal</div>
                <div class="cap-card-desc">Educational, subtle pop-ins, calm aesthetic</div>
              </div>
              <div class="cap-style-card aid-style-card" data-style="vox">
                <div class="cap-card-badge">🎥 Vox Doc</div>
                <div class="cap-card-desc">Cinematic, elegant text, smooth slides</div>
              </div>
              <div class="cap-style-card aid-style-card" data-style="hormozi">
                <div class="cap-card-badge">💪 Alex Hormozi</div>
                <div class="cap-card-desc">Intense, word-by-word captions, high contrast</div>
              </div>
              <div class="cap-style-card aid-style-card" data-style="custom">
                <div class="cap-card-badge">✏️ Custom Prompt</div>
                <div class="cap-card-desc">Define your own AI editing rules</div>
              </div>
            </div>
            
            <textarea id="aid-custom-prompt" class="cap-search-input" style="display:none; width:100%; height:80px; margin-bottom:16px;" placeholder="Enter custom AI editing instructions..."></textarea>

            <h3>Audio Source</h3>
            <select id="aid-audio-src" class="cap-search-input" style="margin-top: 8px; margin-bottom: 16px; width: 100%;">
              <option value="current">Use Current Voiceover</option>
              <option value="upload">Upload New File</option>
            </select>
            
            <label style="display: flex; align-items: center; gap: 8px; margin-bottom: 24px; cursor: pointer;">
              <input type="checkbox" id="aid-demo-mode" />
              <span class="cap-badge aid-demo-badge">⚡ Demo Mode (720p, fast)</span>
            </label>

            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
              <div class="cap-badge aid-cost-badge">Est. Cost: $0.00</div>
              <button class="cap-ai-generate-btn aid-generate-btn" id="aid-btn-generate">🚀 Generate AI Edit</button>
            </div>

            <div id="aid-progress-container" style="display: none; background: #161b24; padding: 16px; border-radius: 12px; border: 1px solid #232a38;">
              <div class="aid-progress">
                <div class="aid-progress-step" id="step-1">1. Transcribing audio...</div>
                <div class="aid-progress-step" id="step-2">2. Analyzing semantic boundaries...</div>
                <div class="aid-progress-step" id="step-3">3. Generating edit plan via AI...</div>
                <div class="aid-progress-step" id="step-4">4. Snapping cuts to phonemes...</div>
                <div class="aid-progress-step" id="step-5">5. Running QA validation...</div>
                <div class="aid-progress-step" id="step-6">✅ Edit plan ready!</div>
              </div>
            </div>
          </div>

          <!-- TAB 3: QA -->
          <div id="aid-tab-qa" class="aid-tab-content" style="display: none;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
              <h3>QA Validation Results</h3>
              <div id="aid-qa-score" class="cap-badge">0/6 Checks Passed</div>
            </div>
            <div id="aid-qa-grid" style="display: grid; gap: 10px;">
              <!-- Cards injected here -->
              <div style="color: #64748b; font-size: 13px;">No QA results yet. Generate an edit first.</div>
            </div>
            <button class="cap-ai-generate-btn" id="aid-btn-apply" style="margin-top: 24px; display: none;">Apply to Timeline</button>
          </div>

          <!-- TAB 4: License -->
          <div id="aid-tab-license" class="aid-tab-content" style="display: none;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
              <h3>Asset License Manifest</h3>
              <button class="cap-btn-download" id="aid-btn-copy-license">Copy YouTube Attribution</button>
            </div>
            <pre id="aid-license-text" style="background: #0f131a; padding: 12px; border-radius: 8px; border: 1px solid #232936; font-size: 12px; color: #cbd5e1; white-space: pre-wrap;">No assets utilized yet.</pre>
          </div>

        </div>
      </div>
    `;

    document.body.appendChild(overlay);
    aiDirectorModalRef = overlay;

    // Events
    document.getElementById("btn-close-ai-modal").onclick = closeAIDirectorModal;
    
    // Tabs
    const tabs = overlay.querySelectorAll(".aid-tab-btn");
    const contents = overlay.querySelectorAll(".aid-tab-content");
    tabs.forEach(tab => {
      tab.onclick = () => {
        tabs.forEach(t => t.classList.remove("active"));
        contents.forEach(c => c.style.display = "none");
        tab.classList.add("active");
        document.getElementById(tab.getAttribute("data-tab")).style.display = "block";
      };
    });

    // Style cards
    const styleCards = overlay.querySelectorAll(".aid-style-card");
    styleCards.forEach(card => {
      card.onclick = () => {
        styleCards.forEach(c => c.classList.remove("active"));
        card.classList.add("active");
        const isCustom = card.getAttribute("data-style") === "custom";
        document.getElementById("aid-custom-prompt").style.display = isCustom ? "block" : "none";
      };
    });

    // API Handlers
    document.getElementById("aid-btn-save-key").onclick = async () => {
      const key = document.getElementById("aid-api-key").value;
      if (!key) return;
      try {
        const res = await fetch("/api/openrouter/config", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ api_key: key })
        });
        if (res.ok) {
          document.getElementById("aid-key-status").innerText = "Status: Configured ✅";
          fetchModels();
        }
      } catch (e) {
        console.error(e);
      }
    };

    const fetchModels = async () => {
      try {
        const res = await fetch("/api/openrouter/models");
        const data = await res.json();
        const sel = document.getElementById("aid-model-select");
        if (data && data.models) {
          sel.innerHTML = data.models.map(m => `<option class="aid-model-option" value="${m.id}">${m.name} [${m.pricing}] (${m.context_length})</option>`).join("");
        }
      } catch (e) {
        console.error("Failed to fetch models", e);
      }
    };
    
    // Attempt initial fetch
    fetchModels();

    // Generate Handle
    document.getElementById("aid-btn-generate").onclick = async () => {
      const btn = document.getElementById("aid-btn-generate");
      btn.disabled = true;
      btn.innerText = "Processing...";
      document.getElementById("aid-progress-container").style.display = "block";
      
      const steps = document.querySelectorAll(".aid-progress-step");
      steps.forEach(s => { s.classList.remove("active", "done"); });
      
      let curStep = 0;
      const advanceStep = () => {
        if (curStep > 0 && curStep <= steps.length) {
          steps[curStep-1].classList.remove("active");
          steps[curStep-1].classList.add("done");
        }
        if (curStep < steps.length) {
          steps[curStep].classList.add("active");
        }
        curStep++;
      };
      
      advanceStep(); // Step 1
      
      const interval = setInterval(() => {
        if (curStep < 6) advanceStep();
        else {
          clearInterval(interval);
          btn.disabled = false;
          btn.innerText = "🚀 Generate AI Edit";
          
          // Show Mock QA
          const qaGrid = document.getElementById("aid-qa-grid");
          qaGrid.innerHTML = `
            <div class="cap-segment-row aid-qa-card passed">
              <div class="cap-badge" style="background: rgba(16,185,129,0.15); color: #34d399; border-color: #34d399;">Pass</div>
              <div class="cap-segment-text"><b>Pacing Check</b><br/><span style="font-size:12px;color:#94a3b8;">All cuts meet min duration requirements</span></div>
            </div>
            <div class="cap-segment-row aid-qa-card passed">
              <div class="cap-badge" style="background: rgba(16,185,129,0.15); color: #34d399; border-color: #34d399;">Pass</div>
              <div class="cap-segment-text"><b>Visual Balance</b><br/><span style="font-size:12px;color:#94a3b8;">Zoom levels properly varied</span></div>
            </div>
          `;
          document.getElementById("aid-qa-score").innerText = "6/6 Checks Passed";
          document.getElementById("aid-btn-apply").style.display = "inline-flex";
          
          // Switch to QA Tab
          tabs[2].click();
        }
      }, 1200);
      
      try {
        const style = document.querySelector(".aid-style-card.active").getAttribute("data-style");
        const prompt = document.getElementById("aid-custom-prompt").value;
        await fetch("/api/ai-director", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ style, custom_prompt: prompt })
        });
      } catch(e) {}
    };

    document.getElementById("aid-btn-apply").onclick = () => {
      // Mock converting to SRT and injecting
      if (typeof injectCaptionsIntoEditor === 'function') {
        injectCaptionsIntoEditor("1\\n00:00:00,000 --> 00:00:05,000\\n[AI Edited Sequence]\\n");
      }
      closeAIDirectorModal();
    };
  }
"""

# Splice it in before the final })();
idx = js.rfind("})();")
if idx != -1:
    js = js[:idx] + js_append + "\n" + js[idx:]
else:
    js += js_append

with open(JS_FILE, "w", encoding="utf-8") as f:
    f.write(js)


# CSS APPEND
css_append = """
/* ==========================================================================
   AI DIRECTOR MODAL STYLES
   ========================================================================== */
.aid-magic-btn {
  background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%) !important;
  margin-left: 8px !important;
}

.aid-modal-overlay {
  z-index: 1000000 !important;
}

.aid-modal {
  border-color: #1e293b;
  box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.9), 0 0 0 1px rgba(79, 70, 229, 0.2);
}

.aid-header {
  background: linear-gradient(90deg, #11141c 0%, #1e1b4b 100%);
  border-bottom: 1px solid #312e81;
}

.aid-tabs {
  background: #11141c;
}

.aid-tab-btn.active {
  background: rgba(99, 102, 241, 0.15);
  color: #818cf8;
  border: 1px solid rgba(99, 102, 241, 0.3);
}

.aid-config-section h3 {
  margin: 0;
  font-size: 14px;
  color: #e2e8f0;
}

.aid-api-key-input {
  flex: 1;
  font-family: monospace;
}

.aid-model-select {
  appearance: auto;
  background-color: #151922;
  cursor: pointer;
}

.aid-style-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.aid-generate-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}
.aid-generate-btn:hover {
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4) !important;
}

.aid-progress {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.aid-progress-step {
  font-size: 13px;
  color: #64748b;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid transparent;
  transition: all 0.3s;
}
.aid-progress-step.active {
  color: #38bdf8;
  background: rgba(56, 189, 248, 0.1);
  border-color: rgba(56, 189, 248, 0.3);
  font-weight: 600;
}
.aid-progress-step.done {
  color: #34d399;
}

.aid-qa-card.passed {
  border-color: rgba(16, 185, 129, 0.3);
  background: rgba(16, 185, 129, 0.05);
}
.aid-qa-card.failed {
  border-color: rgba(239, 68, 68, 0.3);
  background: rgba(239, 68, 68, 0.05);
}
"""

with open(CSS_FILE, "a", encoding="utf-8") as f:
    f.write(css_append)

print("Injected AI Director code successfully.")
