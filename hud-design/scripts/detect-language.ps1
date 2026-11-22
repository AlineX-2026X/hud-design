# 探测 Windows 界面语言，输出 HUD 应使用的显示语言代号：zh-CN / zh-TW / en
# 优先级：HUD_LANG 环境变量 > 系统界面语言 > en
# 用法（cmd 或 PowerShell，无需 Git Bash）：
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\detect-language.ps1
param([string]$HudLang = $env:HUD_LANG)

$ErrorActionPreference = 'SilentlyContinue'

function Get-Normalized([string]$s) {
    if ([string]::IsNullOrWhiteSpace($s)) { return '' }
    return ($s -replace '_', '-').ToLower()
}

function Get-Code([string]$s) {
    $n = Get-Normalized $s
    if ($n -match '^zh-(cn|hans|sg)' -or $n -match '^zh.*cn') { return 'zh-CN' }
    if ($n -match '^zh-(tw|hk|mo|hant)' -or $n -match '^zh.*(tw|hk)') { return 'zh-TW' }
    if ($n -match '^en') { return 'en' }
    return ''
}

function Get-SystemLanguage {
    $candidates = @()
    # 1) 显示语言覆盖（Win10 / Win11 优先）
    $override = Get-WinUILanguageOverride
    if ($override) { $candidates += $override.Name }
    # 2) .NET 当前 UI 区域
    $candidates += [System.Globalization.CultureInfo]::CurrentUICulture.Name
    # 3) 用户首选语言列表（注册表）
    $langs = (Get-ItemProperty 'HKCU:\Control Panel\International\User Profile' -Name Languages).Languages
    if ($langs -and $langs.Count -gt 0) { $candidates += $langs[0] }
    # 4) 当前区域设置
    $candidates += [System.Globalization.CultureInfo]::CurrentCulture.Name

    foreach ($c in $candidates) {
        $code = Get-Code $c
        if ($code) { return $code }
    }
    return 'en'
}

if (-not [string]::IsNullOrWhiteSpace($HudLang)) {
    $n = Get-Normalized $HudLang
    if ($n -notmatch '^(auto|system|auto-detect|自动|默认)$') {
        $code = Get-Code $HudLang
        if ($code) { Write-Output $code; exit 0 }
    }
}

Write-Output (Get-SystemLanguage)
exit 0
