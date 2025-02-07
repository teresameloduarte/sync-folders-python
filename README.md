
# 📂 Sync Folders - Python  

A script to keep two folders **identical** by synchronizing files from **source → replica**.  

### ▶ How to Run  

```bash
python sync_folders.py source_test replica_test -i 120 -d -l sync.log
```

### ▶ Options:

🔹 -i 120 → Sync every 2 minutes (default: 60s)

🔹 -d → Delete files in the replica that don’t exist in the source

🔹 -l sync.log → Save actions to sync.log


### ▶ What It Does

✅ Copies new & updated files

✅ Deletes extra files in the replica (if -d is used)

✅ Logs all actions

