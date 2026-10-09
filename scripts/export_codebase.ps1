# PAIMANA AI - PowerShell Codebase Text Bundler

$rootDir = (Get-Item $PSScriptRoot).Parent.FullName
$bundlePath = Join-Path $rootDir "PAIMANA_AI_CODE_BUNDLE.txt"

$includeExtensions = @(".py", ".jsx", ".js", ".json", ".html", ".css", ".md", ".bat", ".ps1", ".txt", ".rules")
$excludeDirs = @("node_modules", "__pycache__", ".git", ".venv", "venv", "dist", ".pytest_cache", ".idea", ".vscode")

Write-Host "======================================================================" -ForegroundColor Green
Write-Host "   PAIMANA AI - Codebase Text Bundler (PowerShell)" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green

$allFiles = Get-ChildItem -Path $rootDir -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
    $file = $_
    $rel = $file.FullName.Substring($rootDir.Length + 1)
    $ext = $file.Extension.ToLower()
    
    $skip = $false
    foreach ($ex in $excludeDirs) {
        if ($rel -like "*$ex*") { $skip = $true; break }
    }
    if ($file.Name -eq "package-lock.json" -or $file.Name -eq "PAIMANA_AI_CODE_BUNDLE.txt" -or $file.Name.EndsWith(".db")) { $skip = $true }

    -not $skip -and ($includeExtensions -contains $ext -or $file.Name.StartsWith("."))
}

$sb = [System.Text.StringBuilder]::new()
[void]$sb.AppendLine("================================================================================")
[void]$sb.AppendLine("PAIMANA AI - COMPLETE SOURCE CODE AND SPECIFICATION BUNDLE")
[void]$sb.AppendLine("Generated On: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
[void]$sb.AppendLine("Total Files: $($allFiles.Count)")
[void]$sb.AppendLine("================================================================================")
[void]$sb.AppendLine("")

$idx = 1
foreach ($f in $allFiles) {
    $rel = $f.FullName.Substring($rootDir.Length + 1).Replace("\", "/")
    [void]$sb.AppendLine("================================================================================")
    [void]$sb.AppendLine("FILE $idx/$($allFiles.Count): $rel")
    [void]$sb.AppendLine("================================================================================")
    [void]$sb.AppendLine("")
    try {
        $content = [System.IO.File]::ReadAllText($f.FullName)
        [void]$sb.AppendLine($content)
    } catch {
        [void]$sb.AppendLine("[Could not read file]")
    }
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("")
    $idx++
}

[System.IO.File]::WriteAllText($bundlePath, $sb.ToString())
Write-Host "[OK] Text bundle generated directly in project root at: $bundlePath" -ForegroundColor Green
