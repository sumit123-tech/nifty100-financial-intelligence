import yaml

with open(
    "config/screener_presets.yaml",
    "r",
    encoding="utf-8"
) as f:

    presets = yaml.safe_load(f)

print(presets)