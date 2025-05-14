#!/usr/bin/env python3
"""
Easy‑Model‑Fusion + DreamShaper‑8 (Stable Diffusion 1.5)
– Mac Apple‑Silicon / WSL / Linux (GPU ou CPU)

• Installe emf-cli
• Initialise projet
• Patche torch>=2.2, installe diffusers/accelerate
• Télécharge le modèle public « Lykon/dreamshaper‑8 »
• Génère un fond VN 1280×720
"""

import json, os, platform, random, re, shutil, subprocess, sys, tarfile, tempfile, urllib.request
from pathlib import Path

# ---------------- configuration ----------------
PROJECT  = "emf_image_app"
MODEL_ID = "Lykon/dreamshaper-8"
STEPS, GUIDANCE = 30, 7.5
# -----------------------------------------------

def run(cmd, **kw):
    print("  $", *cmd); subprocess.run(cmd, check=True, **kw)

def which(x): return shutil.which(x)

# 1. Installe emf-cli ---------------------------
def install_emf_cli():
    if which("emf-cli"): return
    sysn={"darwin":"Darwin","linux":"Linux"}[platform.system().lower()]
    arch={"arm64":"arm64","aarch64":"arm64","x86_64":"x86_64"}[platform.machine()]
    rel=json.load(urllib.request.urlopen("https://api.github.com/repos/easy-model-fusion/emf-cli/releases/latest"))
    asset=next(a for a in rel["assets"] if a["name"]==f"emf-cli_{sysn}_{arch}.tar.gz")
    tmp=tempfile.mkdtemp(); tarf=Path(tmp)/asset["name"]
    urllib.request.urlretrieve(asset["browser_download_url"], tarf)
    with tarfile.open(tarf) as t: t.extractall(tmp)
    dst=Path.home()/".local/bin/emf-cli"; dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(Path(tmp)/"emf-cli", dst); dst.chmod(0o755)

# 2. Init projet via python3.11 -----------------
def init_project():
    if Path(PROJECT).exists(): return
    py311=which("python3.11") or sys.exit("brew install python@3.11 requis")
    tbin=Path(tempfile.mkdtemp()); (tbin/"python").symlink_to(py311)
    env=os.environ | {"PATH":f"{tbin}:{os.getenv('PATH')}"}
    run(["emf-cli","init",PROJECT], env=env)

# 3. Patch SDK + maj diffusers ------------------
def patch_sdk():
    py=next((p for p in Path(PROJECT).rglob("pyproject.toml") if "torch==" in p.read_text()),None)
    if py: py.write_text(re.sub(r"torch==\\d+\\.\\d+\\.\\d+","torch>=2.2",py.read_text()))
    pip=Path(PROJECT)/".venv/bin/pip"
    run([pip,"install","-U","diffusers[torch]>=0.27","accelerate>=0.27","transformers>=4.40"])

# 4. Ajoute le modèle ---------------------------
def add_model():
    env=os.environ.copy(); env.pop("HF_TOKEN",None)
    res=subprocess.run(["emf-cli","model","add",MODEL_ID,"--yes"], cwd=PROJECT, env=env)
    if res.returncode not in (0,1): res.check_returncode()

# 5. Génération fond VN -------------------------
def generate_background(prompt: str) -> str:
    act = Path(PROJECT) / ".venv/bin/activate_this.py"
    if act.exists():
        exec(act.read_text(), {"__file__": str(act)})

    import torch
    from diffusers import StableDiffusionPipeline, EulerAncestralDiscreteScheduler

    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

    pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float32, safety_checker=None)
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
    pipe.to(device)
    pipe.enable_attention_slicing()

    img = pipe(prompt, num_inference_steps=STEPS, guidance_scale=GUIDANCE, height=600, width=800).images[0]
    output_path = Path.cwd() / "generated.png"
    img.save(output_path)
    print(f"✅ {output_path.name} sauvegardée")
    return str(output_path.resolve())

# ------------------- main ----------------------
if __name__ == "__main__":
    #---------------- INITIALISATION D'EMF + INSTALLATION DU MODELE SI PAS DEJA LA --------------
    install_emf_cli()
    init_project()
    patch_sdk()
    add_model()
    print("✅ EMF prêt – génération…")


    vn_text = (
    "$TIME — Le vent tiède de $SEASON effleure les cheveux de $MC_NAME tandis qu’iel "
    "remonte l’avenue de $CITY. Les néons du café \"$PLACE_NAME\" commencent à s’allumer, "
    "diffusant une lueur rose sur les vitrines. Plus loin, le vieux temple shinto "
    "parsemé de pétales de cerisier semble veiller silencieusement.\n\n"
    "$MC_NAME (pensée) : «  $INNER_THOUGHT  »\n\n"
    "Au même instant, $FRIEND_NAME surgit à l’angle, essoufflé·e, un dossier serré "
    "contre sa poitrine.\n\n"
    "$FRIEND_NAME : «  $MC_NAME ! Tu ne vas pas croire ce que j’ai découvert...  »"
    )

    prompt = (
    f"visual novel background, {vn_text}, "
    "wide scenic establishing shot, 1280x720, ultra‑detailed, atmospheric anime art, "
    "soft cinematic lighting, vibrant colours, high resolution"
    )
    #Génération fond
    path = generate_background(prompt)
    print("Chemin absolu :", path)


