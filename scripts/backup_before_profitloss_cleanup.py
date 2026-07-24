import shutil
import os

os.makedirs("backup", exist_ok=True)

shutil.copy(
    "database/nifty100.db",
    "backup/nifty100_before_profitloss_cleanup.db"
)

print("Backup created successfully.")