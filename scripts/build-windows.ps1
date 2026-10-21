$ErrorActionPreference = 'Stop'
$projectDir = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location -LiteralPath $projectDir
$pythonExe = Join-Path $projectDir '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $pythonExe)) { throw 'Run scripts/setup.ps1 first.' }
if (Get-Command uv -ErrorAction SilentlyContinue) {
    $env:UV_CACHE_DIR = Join-Path $projectDir '.runtime/uv-cache'
    uv pip install --python $pythonExe -r requirements-build.txt
} else { & $pythonExe -m pip install -r requirements-build.txt }
if ($LASTEXITCODE -ne 0) { throw 'Packaging dependency installation failed.' }
& $pythonExe scripts/fetch-cpu-engine.py
if ($LASTEXITCODE -ne 0) { throw 'CPU engine verification failed.' }
& $pythonExe scripts/collect-notices.py
if ($LASTEXITCODE -ne 0) { throw 'Could not collect redistribution notices.' }
& $pythonExe -m PyInstaller --noconfirm --distpath release --workpath .build Stonebound.spec
if ($LASTEXITCODE -ne 0) { throw 'The Windows build failed.' }
Copy-Item -LiteralPath 'PORTABLE-README.txt' -Destination 'release/READ-ME.txt'
Copy-Item -LiteralPath 'THIRD_PARTY_NOTICES.md' -Destination 'release/THIRD_PARTY_NOTICES.md'
New-Item -ItemType Directory -Force 'release/licenses' | Out-Null
Copy-Item -Path 'resources/licenses/*' -Destination 'release/licenses' -Recurse -Force
$campaignJson = & $pythonExe -c "import json; from stonebound.catalog import OPPONENTS, ITEMS; from stonebound.story import story_snapshot; s=story_snapshot([]); print(json.dumps(dict(opponents=len(OPPONENTS),items=len(ITEMS),chapters=len(s['chapters']),manga_pages=len(s['pages']))))"
if ($LASTEXITCODE -ne 0) { throw 'Could not read campaign metadata.' }
$buildInfo = [ordered]@{
    version = (Get-Content -LiteralPath package.json -Raw | ConvertFrom-Json).version
    file = 'Stonebound.exe'
    bytes = (Get-Item -LiteralPath release/Stonebound.exe).Length
    sha256 = (Get-FileHash -LiteralPath release/Stonebound.exe -Algorithm SHA256).Hash.ToLower()
    katrain_commit = 'f4981cf905cece90085ce4e3967415d0c16d525f'
    campaign = ($campaignJson | ConvertFrom-Json)
}
$buildInfo | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath release/BUILD-INFO.json -Encoding utf8
Compress-Archive -LiteralPath release/Stonebound.exe,release/READ-ME.txt,release/THIRD_PARTY_NOTICES.md,release/BUILD-INFO.json,release/licenses -DestinationPath release/Stonebound-Windows-x64.zip -Force
Write-Host 'Ready: release/Stonebound.exe and release/Stonebound-Windows-x64.zip'
