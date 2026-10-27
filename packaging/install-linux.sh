#!/bin/sh
set -eu
SOURCE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TARGET="$HOME/.local/opt/amerika-social"
mkdir -p "$TARGET" "$HOME/.local/share/applications" "$HOME/.local/share/metainfo" "$HOME/.local/bin"
# Copies files without deleting unrelated user data. No root privileges are needed.
cp -R "$SOURCE"/. "$TARGET"/
chmod +x "$TARGET/MakkSocial"
ln -sf "$TARGET/MakkSocial" "$HOME/.local/bin/MakkSocial"
ln -sf "$TARGET/MakkSocial" "$HOME/.local/bin/makk-social"
for size in 16 32 48 64 128 256 512; do
  mkdir -p "$HOME/.local/share/icons/hicolor/${size}x${size}/apps"
  cp "$TARGET/_internal/assets/vigiltech/icons/social-$size.png" "$HOME/.local/share/icons/hicolor/${size}x${size}/apps/amerika-social.png"
done
[ -f "$SOURCE/amerika-social.metainfo.xml" ] && cp "$SOURCE/amerika-social.metainfo.xml" "$HOME/.local/share/metainfo/amerika-social.metainfo.xml"
command -v gtk-update-icon-cache >/dev/null 2>&1 && gtk-update-icon-cache -q -t "$HOME/.local/share/icons/hicolor" || true
sed "s|Exec=MakkSocial|Exec=\"$TARGET/MakkSocial\"|" "$SOURCE/amerika-social.desktop" > "$HOME/.local/share/applications/amerika-social.desktop"
printf '%s\n' 'Installed Vigil Social for the current user.'
