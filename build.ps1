function CheckPipInstalled {
    if (Test-Path (Get-Command pip -ErrorAction SilentlyContinue)) {
        Write-Host "pip is installed."
    } else {
        Write-Host "pip is not installed, proceeding to installation..."
        python -m ensurepip --upgrade
    }
}

function CheckModuleInstalled {
    param(
        [string]$module,
        [string]$import = ""
    )

    if ([string]::IsNullOrWhiteSpace($import)) {
        $import = $module
    }

    try {
        Import-Module $import -ErrorAction Stop | Out-Null
        Write-Host "$module is installed, skipping the installation."
    } catch {
        Write-Host "$module is not installed, proceeding to installation..."
        pip install $module
    }
}

function GenerateExecutable {
    if (Test-Path "./dist/markupconverter.exe") {
        Write-Host "Executable present, skipping the generation."
    } else {
        Write-Host "Proceeding to generation of an executable..."

        pyinstaller.exe --onefile --noconsole markupconverter.py

        if ($LASTEXITCODE -eq 0) {
            Write-Host "Generation finished successfully."
        } else {
            Write-Host "Failed to generate executable."
        }
    }
}

# Required modules
CheckPipInstalled
CheckModuleInstalled -module pyinstaller -import PyInstaller
CheckModuleInstalled -module xmltodict
CheckModuleInstalled -module pyyaml -import yaml

# installing chocolatey
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
}

# getting the dependencies
choco install -y qt5-default

CheckModuleInstalled -module PyQt5

GenerateExecutable
