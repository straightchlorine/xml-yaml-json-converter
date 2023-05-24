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

        pyinstaller --onefile --noconsole markupconverter.py -n markupconverter.exe 2>&1 | Out-Null

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

choco install -y vcbuildtools
choco install -y qt5

CheckModuleInstalled -module PyQt5

GenerateExecutable
