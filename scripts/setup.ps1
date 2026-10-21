$ErrorActionPreference = 'Stop'
$projectDir = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location -LiteralPath $projectDir
$revision = 'f4981cf905cece90085ce4e3967415d0c16d525f'
$sourceDir = Join-Path $projectDir 'vendor/katrain'
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Install Git for Windows, then run setup again.' }
if (-not (Test-Path -LiteralPath (Join-Path $sourceDir '.git'))) {
    git clone --no-checkout https://github.com/sanderland/katrain.git $sourceDir
    if ($LASTEXITCODE -ne 0) { throw 'Could not download KaTrain.' }
    git -C $sourceDir checkout --detach $revision
    if ($LASTEXITCODE -ne 0) { throw 'Could not check out the pinned KaTrain revision.' }
}
$actualRevision = git -C $sourceDir rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $actualRevision -ne $revision) {
    throw "The KaTrain checkout must be at $revision. Your checkout was left unchanged."
}
$env:UV_PYTHON_INSTALL_DIR = Join-Path $projectDir '.runtime/python'
$env:UV_CACHE_DIR = Join-Path $projectDir '.runtime/uv-cache'
$pythonExe = Join-Path $projectDir '.venv/Scripts/python.exe'
if (Get-Command uv -ErrorAction SilentlyContinue) {
    if (-not (Test-Path -LiteralPath $pythonExe)) {
        uv venv --python 3.12 --managed-python .venv
        if ($LASTEXITCODE -ne 0) { throw 'Could not prepare Python 3.12.' }
    }
    uv pip install --python $pythonExe -r requirements.txt
} else {
    if (-not (Test-Path -LiteralPath $pythonExe)) {
        if (-not (Get-Command py -ErrorAction SilentlyContinue)) { throw 'Install Python 3.12 or uv, then run setup again.' }
        py -3.12 -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw 'Python 3.12 is needed. Install it or install uv.' }
    }
    & $pythonExe -m pip install -r requirements.txt
}
if ($LASTEXITCODE -ne 0) { throw 'Could not install the KaTrain core dependencies.' }
& $pythonExe scripts/fetch-cpu-engine.py
if ($LASTEXITCODE -ne 0) { throw 'Could not prepare the CPU engine.' }
Write-Host 'Stonebound is ready. Open Start-Stonebound.cmd to play.'
