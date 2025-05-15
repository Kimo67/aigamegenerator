#!/usr/bin/env python3

import json, os, platform, random, re, shutil, subprocess, sys, tarfile, tempfile, urllib.request
from pathlib import Path

# ---------------- configuration ----------------
PROJECT  = "emf_image_app"
MODEL_ID = "Lykon/dreamshaper-8"
STEPS, GUIDANCE = 30, 7.5
HF_TOKEN  = "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"
# -----------------------------------------------

def run(cmd, **kw):
    print("  $", *cmd); subprocess.run(cmd, check=True, **kw)

def which(x): return shutil.which(x)

# 1. Installe emf-cli ---------------------------
def install_emf_cli():
    if shutil.which("emf-cli"):
        return

    url = "https://github.com/easy-model-fusion/emf-cli/archive/refs/tags/v0.0.3.tar.gz"
    tmp = tempfile.mkdtemp()
    tarf = Path(tmp) / "emf-cli.tar.gz"
    urllib.request.urlretrieve(url, tarf)

    with tarfile.open(tarf) as t:
        t.extractall(tmp)

    src_dir = next(Path(tmp).glob("emf-cli-*"))
    os.chdir(src_dir)

    subprocess.run(["make", "build"], check=True)

    bin_path = src_dir / "bin" / "emf-cli"
    if not bin_path.exists():
        raise RuntimeError("Binaire emf-cli non trouvé après compilation.")

    for target_dir in [Path("/usr/local/bin"), Path.home() / ".local/bin"]:
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            dst = target_dir / "emf-cli"
            shutil.move(str(bin_path), dst)
            dst.chmod(0o755)
            print(f"✅ emf-cli installé dans : {dst}")
            return
        except PermissionError:
            continue

    raise RuntimeError("❌ Impossible d’installer emf-cli (droits insuffisants)")

# 2. Initialise le projet sans venv ------------------
def init_project():
    if Path(PROJECT).exists(): return
    run(["emf-cli", "init", PROJECT])

# 3. Patch torch>=2.2 et installe dépendances globales
def patch_sdk():
    pyproject = next((p for p in Path(PROJECT).rglob("pyproject.toml") if "torch==" in p.read_text()), None)
    if pyproject:
        pyproject.write_text(re.sub(r"torch==\d+\.\d+\.\d+", "torch>=2.2", pyproject.read_text()))

    run([sys.executable, "-m", "pip", "install", "-U",
         "torch>=2.2",
         "diffusers[torch]>=0.27",
         "accelerate>=0.27",
         "transformers>=4.40"
    ])

# 4. Ajoute le modèle avec token
def add_model():
    env = os.environ.copy()
    env.pop("HF_TOKEN", None)
    res = subprocess.run([
        "emf-cli", "model", "add", MODEL_ID,
        "--yes", "--access-token", HF_TOKEN
    ], cwd=PROJECT, env=env)
    if res.returncode not in (0, 1):
        res.check_returncode()

# 5. Génération d'une image depuis prompt
def generate_background(prompt: str) -> str:
    import torch
    from diffusers import StableDiffusionPipeline, EulerAncestralDiscreteScheduler

    task = (
        f"visual novel background, {prompt}, "
        "wide scenic establishing shot, 1280x720, ultra‑detailed, atmospheric anime art, "
        "soft cinematic lighting, vibrant colours, high resolution"
    )

    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

    pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float32, safety_checker=None)
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
    pipe.to(device)
    pipe.enable_attention_slicing()

    img = pipe(task, num_inference_steps=STEPS, guidance_scale=GUIDANCE, height=600, width=800).images[0]

    output_path = Path("/backend/backend") / "generated.png"
    img.save(output_path)
    print(f"✅ {output_path.name} sauvegardée")
    return str(output_path.resolve())

# ------------------- main ----------------------
if __name__ == "__main__":
    install_emf_cli()
    init_project()
    patch_sdk()
    add_model()
    print("✅ EMF prêt – génération…")

    prompt = (
        "$TIME — Le vent tiède de $SEASON effleure les cheveux de $MC_NAME tandis qu’iel "
        "remonte l’avenue de $CITY. Les néons du café \"$PLACE_NAME\" commencent à s’allumer, "
        "diffusant une lueur rose sur les vitrines. Plus loin, le vieux temple shinto "
        "parsemé de pétales de cerisier semble veiller silencieusement.\n\n"
        "$MC_NAME (pensée) : «  $INNER_THOUGHT  »\n\n"
        "Au même instant, $FRIEND_NAME surgit à l’angle, essoufflé·e, un dossier serré "
        "contre sa poitrine.\n\n"
        "$FRIEND_NAME : «  $MC_NAME ! Tu ne vas pas croire ce que j’ai découvert...  »"
    )

    # path = generate_background(prompt)
    # print("Chemin absolu :", path)
