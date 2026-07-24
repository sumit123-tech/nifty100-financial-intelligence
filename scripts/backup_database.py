import shutil

shutil.copy(
    "database/nifty100.db",
    "database/nifty100_backup_before_cleanup.db"
)

print("Database backup created successfully.")