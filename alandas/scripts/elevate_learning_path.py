"""
Elevate Cyril's AI Engineering Path from v14 to v15
Incorporates:
- Module A4: Tiered Revenue Architecture (Durability, Governance, Tradeoffs, Temporal vs n8n)
- Waterfall Enrichment Engine: "Cheapest Tool First" & § 5 TMG Impressum Scraper
- Project PP7: Tiered Commercial Revenue Platform (Alandas Case Study)
- Decision Contracts, Policy Engines, and OpenReply Instagram Architecture
- Requirement-First Design Law: "Complexity Must Be Purchased by a Requirement"
"""
import shutil

with open(r'c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas\cyril_learning_path_v14.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Title and Header
text = text.replace(
    "<title>Cyril's AI Engineering Path v12</title>",
    "<title>Cyril's AI Engineering Path v15 — Elevated System Design & Architecture</title>"
)
text = text.replace(
    "Cyril's AI engineering path v14",
    "Cyril's AI engineering path v15"
)
text = text.replace(
    '<div class="snum">18</div><div class="slabel">Projects</div>',
    '<div class="snum">20</div><div class="slabel">Projects</div>'
)
text = text.replace(
    '<div class="snum" style="color:#993C1D;">10</div><div class="slabel">Engineering layers</div>',
    '<div class="snum" style="color:#993C1D;">12</div><div class="slabel">Engineering layers</div>'
)
text = text.replace(
    'v14 mastery standard: framework-neutral mechanism first, implementation second. Passing requires mechanism + failure mode + prediction + verification + architecture defense.',
    'v15 mastery standard: requirement-first architecture, durable execution (Temporal vs n8n), waterfall enrichment, policy engines, decision contracts & tiered operational maturity.'
)

# 2. Add New Chips
old_chips = '<span class="chip new">Temporal</span>'
new_chips = '<span class="chip new">Temporal</span><span class="chip new">Waterfall Enrichment</span><span class="chip new">Policy Engine</span><span class="chip new">Decision Contracts</span><span class="chip new">Tiered Systems</span>'
text = text.replace(old_chips, new_chips, 1)

# 3. Add A4 to archModules
arch_target = 'const archModules=['
new_arch_module = '''const archModules=[
  {id:'a4',num:'A4',title:'Tiered Revenue Architecture - Durability, Governance and Trade-offs',sub:'Complete with W7/W8 · commercial system design flagship',bg:'#E1F5EE',tc:'#0F6E56',pill:'pill-teal',cardCls:'teal-card',
   isNew:true,status:'Flagship',statusCls:'pill-purple',
   topics:[['ti-layers-difference','3-Tier robustness model: Essential vs Professional vs Autonomous'],['ti-filter','Waterfall enrichment: cheapest tool first (Impressum ➔ GitLeads ➔ Prospeo ➔ Verifier)'],['ti-refresh','Durability analysis: Temporal vs n8n under process failure'],['ti-shield-check','Policy engines, decision contracts and post-action verification']],
   newTopics:[['ti-scale','Complexity must be purchased by a requirement'],['ti-bolt','Instagram as first-class channel: OpenReply comment-to-DM loop'],['ti-currency-euro','Commercial packaging: capability over framework names'],['ti-arrow-up-right','Non-destructive upgrade path: layering without rewriting']],
   project:{label:'Flagship project',name:'Alandas Tiered Revenue System',desc:'Design the complete 3-tier architecture for Alandas Tea Berlin. Defend why Temporal replaces n8n, why the 5-stage waterfall enrichment cuts data costs by 87%, why LangGraph is bounded rather than the whole app, and walk through an 8-stage decision contract for ad spend with immutable audit logging.',col:'teal'},
   notice:{text:'Complexity is not capability. You pass this module when you can justify why Tier 1 is the default starting point and articulate the exact business threshold that earns Tier 2 and Tier 3.',tab:'arch'},
   prompt:'Teach me the Tiered Revenue Architecture framework and make me defend the tradeoffs between Temporal, n8n, waterfall enrichment, direct APIs, and policy engines.'},
'''
text = text.replace(arch_target, new_arch_module, 1)

# 4. Add lessonWhen for a4
when_target = 'a3:"After W4. Scale something you actually understand, then transfer the method to unfamiliar systems."'
new_when = 'a3:"After W4. Scale something you actually understand, then transfer the method to unfamiliar systems.",\n    a4:"After W7 and before Capstone W8. This is the bridge between durable workflows, policy governance, and real-world commercial architecture."'
text = text.replace(when_target, new_when, 1)

# 5. Add PP7 to portfolioProjects
port_target = 'const portfolioProjects=['
new_port_module = '''const portfolioProjects=[
  {id:'pp7',num:'PP7',title:'Tiered Commercial Revenue Platform (Alandas Case Study)',sub:'Temporal · Dolibarr CRM · OpenReply · Waterfall Enrichment · Policy Engine',bg:'#EEF0FE',tc:'#3B4AAB',pill:'pill-indigo',cardCls:'indigo-card',
   isNew:true,status:'Commercial flagship',statusCls:'pill-purple',
   topics:[['ti-refresh','Temporal durable workflow engine & Dolibarr REST sync'],['ti-filter','5-Stage Waterfall enrichment pipeline (Impressum ➔ GitLeads ➔ Prospeo ➔ LeadMagic ➔ MillionVerifier)'],['ti-message-2','Hermes WhatsApp multimodal order OCR parser'],['ti-brand-instagram','OpenReply comment-to-DM & Google Maps cafe scraper'],['ti-shield-check','Policy engine & decision contract for ad budgets']],
   project:{label:'Flagship',name:'Alandas commercial revenue platform',desc:'The end-to-end production architecture taking a business from 25 to 100 accounts: Tier 1 durable automation with cheapest-tool-first waterfall ➔ Tier 2 governed intelligence with policy gates ➔ Tier 3 autonomous flywheel. Defend every architectural tradeoff in an executive presentation.',col:'indigo'},
   prompt:'Walk me through the Alandas Tiered Revenue System design, and test my ability to defend its tradeoffs against a client who asks for visual n8n or an unconstrained bot.'},
'''
text = text.replace(port_target, new_port_module, 1)

# Write output to workspace
out_workspace = r'c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas\cyril_learning_path_v15.html'
with open(out_workspace, 'w', encoding='utf-8') as f:
    f.write(text)

# Also copy to user's Downloads folder
out_downloads = r'C:\Users\Cyril Uzochukwu\Downloads\cyril_learning_path_v15.html'
try:
    shutil.copyfile(out_workspace, out_downloads)
    print(f"Copied to {out_downloads} successfully.")
except Exception as e:
    print(f"Downloads copy note: {e}")

print(f"Generated {out_workspace} successfully.")
