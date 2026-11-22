#!/usr/bin/env bash
# 探测操作系统界面语言，输出 HUD 应使用的显示语言代号：
#   zh-CN  简体中文
#   zh-TW  繁體中文
#   en     英文
# 优先级：HUD_LANG 环境变量 > 系统界面语言 > en
# 支持系统：macOS / Windows（Git Bash、MSYS2、Cygwin）/ Linux / WSL / HarmonyOS（手机、平板、PC）
# 用法：bash scripts/detect-language.sh
set -u

norm() { printf '%s' "$1" | tr 'A-Z' 'a-z' | tr '_' '-'; }

# 空值、C、POSIX 之类都视为「没有可用语言」
usable() {
  case "$(norm "$1")" in
    ''|c|posix|c-utf-8|c-utf8|none) return 1 ;;
  esac
  return 0
}

classify() {
  case "$(norm "$1")" in
    zh-cn*|zh-hans*|zh-sg*|zh*cn*) echo "zh-CN" ;;
    zh-tw*|zh-hk*|zh-mo*|zh-hant*|zh*tw*|zh*hk*|zh*hant*) echo "zh-TW" ;;
    en*) echo "en" ;;
    *) echo "" ;;
  esac
}

emit() {
  local out
  out="$(classify "$1")"
  if [ -n "$out" ]; then echo "$out"; else echo "en"; fi
}

# 1. 显式指定（auto / system / 默认 视为未指定）
if usable "${HUD_LANG:-}" && ! printf '%s' "${HUD_LANG:-}" | grep -qiE '^(auto|system|auto-detect|默认|自动)$'; then
  emit "$HUD_LANG"
  exit 0
fi

raw=""
os="$(uname -s 2>/dev/null || echo unknown)"

case "$os" in
  Darwin)
    # macOS：AppleLocale 形如 zh_CN / en_US；取不到则回退 AppleLanguages
    raw="$(defaults read -g AppleLocale 2>/dev/null || true)"
    if ! usable "$raw"; then
      raw="$(defaults read -g AppleLanguages 2>/dev/null \
        | tr -d ' \n"' | sed 's/^(//; s/)$//' | cut -d, -f1 || true)"
    fi
    ;;

  MINGW*|MSYS*|CYGWIN*)
    # Windows + Git Bash / MSYS2 / Cygwin
    raw="$(powershell.exe -NoProfile -Command "(Get-Culture).Name" 2>/dev/null \
      || powershell -NoProfile -Command "(Get-Culture).Name" 2>/dev/null || true)"
    ;;

  *)
    # 鸿蒙 / OpenHarmony（手机、平板、PC）：语言存在 param 里，不走 locale 环境变量
    if command -v param >/dev/null 2>&1; then
      for k in persist.sys.locale const.product.locale persist.sys.language; do
        v="$(param get "$k" 2>/dev/null || true)"
        if usable "$v" && [ "$v" != "Unknown" ]; then raw="$v"; break; fi
      done
    fi

    # WSL：借用 Windows 的区域设置
    if ! usable "$raw" && { [ -n "${WSL_DISTRO_NAME:-}" ] || grep -qi microsoft /proc/version 2>/dev/null; }; then
      raw="$(powershell.exe -NoProfile -Command "(Get-Culture).Name" 2>/dev/null || true)"
    fi

    # 常规 Linux / 容器：环境变量 → 系统配置文件 → localectl
    if ! usable "$raw"; then
      for v in "${LC_ALL:-}" "${LC_MESSAGES:-}" "${LANG:-}"; do
        if usable "$v"; then raw="$v"; break; fi
      done
    fi
    if ! usable "$raw" && [ -n "${LANGUAGE:-}" ]; then
      raw="${LANGUAGE%%,*}"        # GNU gettext，取第一个
    fi
    if ! usable "$raw" && [ -r /etc/locale.conf ]; then
      raw="$(sed -n 's/^[[:space:]]*LANG[[:space:]]*=[[:space:]]*//p' /etc/locale.conf 2>/dev/null | head -1)"
    fi
    if ! usable "$raw" && [ -r /etc/default/locale ]; then
      raw="$(sed -n 's/^[[:space:]]*LANG[[:space:]]*=[[:space:]]*//p' /etc/default/locale 2>/dev/null | head -1)"
    fi
    if ! usable "$raw" && command -v localectl >/dev/null 2>&1; then
      raw="$(localectl status 2>/dev/null | sed -n 's/.*System Locale:[[:space:]]*LANG=\([^[:space:]]*\).*/\1/p' | head -1)"
    fi
    ;;
esac

if ! usable "$raw"; then
  emit "${LANG:-en}"
  exit 0
fi

emit "$raw"
