import subprocess
result = subprocess.run("exit 1", shell=True, capture_output=True, text=True)
print(f"Return code: {result.returncode}")
print(f"Stdout: '{result.stdout}'")
print(f"Stderr: '{result.stderr}'")
