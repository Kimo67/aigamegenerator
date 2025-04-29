#!/usr/bin/env python3
"""
Script one-shot : crée un projet Easy-Model-Fusion 100 % fonctionnel
sur macOS Apple Silicon (M1/M2/M3) avec Python 3.12.

– Installe emf-cli
– Initialise le projet via python3.11
– Patche le SDK (torch/torchaudio >= 2.2 si besoin)
– Ajoute le modèle ‘segmind/tiny-sd’ avec votre token HF
– Installe diffusers/transformers/accelerate
– Génère une image de démo (generated.png)

! Le jeton HF est inscrit en dur ; ne partagez pas ce fichier.
"""

import json, os, platform, random, re, shutil, subprocess, sys, tarfile, tempfile, urllib.request
from pathlib import Path

# ------------------------------ réglages ---------------------------------
PROJECT      = "emf_image_app"
MODEL_ID = "runwayml/stable-diffusion-v1-5"               # dépôt public (mais token quand même)
HF_TOKEN     = "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"  # <- VOTRE TOKEN
PROMPTS      = [
    "un renard en aquarelle, style studio ghibli",
    "low-poly landscape, pastel colors, trending on artstation",
    "chat noir jouant du piano, style impressionniste",
    "a futuristic cityscape at dusk, vibrant neon lights",
]
# -------------------------------------------------------------------------

def run(cmd, **kw):
    print("  $", *cmd)
    subprocess.run(cmd, check=True, **kw)

def which(c): return shutil.which(c)

# -------- 1. install emf-cli ---------------------------------------------
def install_emf_cli():
    if which("emf-cli"):
        return
    sysn = {"darwin":"Darwin","linux":"Linux"}[platform.system().lower()]
    arch= {"arm64":"arm64","aarch64":"arm64","x86_64":"x86_64"}[platform.machine()]
    rel = json.load(urllib.request.urlopen(
            "https://api.github.com/repos/easy-model-fusion/emf-cli/releases/latest"))
    asset = next(a for a in rel["assets"] if a["name"]==f"emf-cli_{sysn}_{arch}.tar.gz")
    tmp   = tempfile.mkdtemp()
    tarf  = Path(tmp)/asset["name"]; urllib.request.urlretrieve(asset["browser_download_url"], tarf)
    with tarfile.open(tarf) as t: t.extractall(tmp)
    dst   = Path.home()/".local/bin/emf-cli"; dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(Path(tmp)/"emf-cli", dst); dst.chmod(0o755)
    print(f"→ emf-cli installé → {dst}")

# -------- 2. init via python3.11 -----------------------------------------
def init_project():
    if Path(PROJECT).exists():
        return
    py311 = which("python3.11")
    if not py311:
        sys.exit("❌  Installez Python 3.11 :  brew install python@3.11")
    tmpbin = Path(tempfile.mkdtemp()); (tmpbin/"python").symlink_to(py311)
    env = os.environ.copy(); env["PATH"] = f"{tmpbin}:{env['PATH']}"
    print("→ emf-cli init (python 3.11)…")
    run(["emf-cli","init",PROJECT], env=env)

# -------- 3. patch SDK torch>=2.2 ----------------------------------------
def patch_sdk():
    pyproj_files = [p for p in Path(PROJECT).rglob("pyproject.toml") if "torch==" in p.read_text()]
    if not pyproj_files:
        print("ℹ️  Aucun pyproject.toml à patcher.")
        return
    pyproj = pyproj_files[0]
    txt = pyproj.read_text()
    txt = re.sub(r"torch==\d+\.\d+\.\d+",      "torch>=2.2", txt)
    txt = re.sub(r"torchaudio==\d+\.\d+\.\d+", "torchaudio>=2.2", txt)
    pyproj.write_text(txt)
    print(f"🔧  {pyproj.relative_to(PROJECT)} patché (torch/torchaudio ≥ 2.2)")
    pip = Path(PROJECT)/".venv/bin/pip"
    run([pip,"install","-U","pip","setuptools","wheel"])
    run([pip,"install","-e",str(pyproj.parent),"diffusers","transformers","accelerate"])

# -------- 4. add model avec --access-token -------------------------------
def add_model():
    run([
        "emf-cli","model","add",MODEL_ID,"--yes",
        "--access-token",HF_TOKEN
    ], cwd=PROJECT)

# -------- 5. generate demo image -----------------------------------------
def generate_demo():
    act = Path(PROJECT)/".venv/bin/activate_this.py"
    if act.exists():
        exec(act.read_text(), {"__file__": str(act)})
    from diffusers import StableDiffusionPipeline
    prompt = random.choice(PROMPTS)
    print(f"→ Génération : « {prompt} »")
    pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, token=HF_TOKEN).to("cpu")
    img  = pipe(prompt, num_inference_steps=25).images[0]
    img.save("generated.png")
    print("✅  Image enregistrée → generated.png")

# ------------------------------ main -------------------------------------
if __name__ == "__main__":
    os.environ["HF_TOKEN"] = HF_TOKEN  # pour diffusers
    install_emf_cli()
    init_project()
    patch_sdk()
    add_model()
    print("✅  Projet EMF prêt – image de démo en cours…")
    generate_demo()
