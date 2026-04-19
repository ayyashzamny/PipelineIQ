$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ollamaHome = Join-Path $projectRoot ".ollama-home"
$ollamaModels = Join-Path $projectRoot ".ollama-models"
$ollamaExe = Join-Path $projectRoot "ollama-standalone\\ollama.exe"

if (-not (Test-Path $ollamaExe)) {
    throw "Ollama binary not found at $ollamaExe"
}

New-Item -ItemType Directory -Force -Path $ollamaHome | Out-Null
New-Item -ItemType Directory -Force -Path $ollamaModels | Out-Null

$env:HOME = $ollamaHome
$env:USERPROFILE = $ollamaHome
$env:OLLAMA_MODELS = $ollamaModels
$env:OLLAMA_HOST = "127.0.0.1:11434"

# Clear the broken localhost:9 proxy used in this environment.
$proxyVars = @("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "GIT_HTTP_PROXY", "GIT_HTTPS_PROXY")
foreach ($proxyVar in $proxyVars) {
    $currentValue = (Get-Item "Env:$proxyVar" -ErrorAction SilentlyContinue).Value
    if ($currentValue -eq "http://127.0.0.1:9") {
        Remove-Item "Env:$proxyVar" -ErrorAction SilentlyContinue
    }
}

& $ollamaExe @args
