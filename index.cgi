#!/bin/sh

#
# Modified Version with help from google gemini to improve problems present in old script.
#


printf "Content-Type: text/html\r\n\r\n"

# Root folder that users are allowed to browse (adjust to your target directory)
BASE_DIR="$(cd .. && pwd)"

# Extract path after SCRIPT_NAME (e.g., /cgi-bin/list.sh/photos/2026 -> /photos/2026)
RAW_PATH="${REQUEST_URI#"$SCRIPT_NAME"}"
# Strip query string if present
RAW_PATH="${RAW_PATH%%\?*}"

# URL-decode basic %XX sequences (e.g., %20 -> space)
url_decode() {
  printf '%b' "$(printf '%s' "$1" | sed 's/+/ /g; s/%\([0-9A-Fa-f][0-9A-Fa-f]\)/\\x\1/g')"
}

# HTML-escape text for safe display
html_escape() {
  printf '%s' "$1" | sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g' -e 's/"/\&quot;/g'
}

# URL-encode path segments safely
url_encode_path() {
  awk '
    BEGIN {
      for (i = 0; i < 256; i++) ord[sprintf("%c", i)] = i
    }
    {
      out = ""
      n = split($0, chars, "")
      for (i = 1; i <= n; i++) {
        c = chars[i]
        if (c ~ /[A-Za-z0-9._~\/-]/ || c == " ") {
          if (c == " ") out = out "%20"
          else out = out c
        } else {
          out = out sprintf("%%%02X", ord[c])
        }
      }
      print out
    }
  '
}

REL_PATH="$(url_decode "$RAW_PATH")"
# Normalize slashes and reject ".." traversal segments
CLEAN_REL=""
OLD_IFS="$IFS"
IFS='/'
for seg in $REL_PATH; do
  case "$seg" in
    ""|".") ;;
    "..")
      # Step up one segment if possible
      CLEAN_REL="${CLEAN_REL%/*}"
      [ "$CLEAN_REL" = "$seg" ] && CLEAN_REL=""
      ;;
    *)
      CLEAN_REL="$CLEAN_REL/$seg"
      ;;
  esac
done
IFS="$OLD_IFS"

TARGET_DIR="$BASE_DIR$CLEAN_REL"

# Verify TARGET_DIR exists and stays inside BASE_DIR
if [ ! -d "$TARGET_DIR" ]; then
  TARGET_DIR="$BASE_DIR"
  CLEAN_REL=""
fi

DISPLAY_REL="${CLEAN_REL#/}"
[ -z "$DISPLAY_REL" ] && DISPLAY_REL="/" || DISPLAY_REL="/$DISPLAY_REL"
ESC_DISPLAY_REL="$(html_escape "$DISPLAY_REL")"

cat << EOH
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Gruppo&family=Roboto+Mono:ital,wght@0,100..700;1,100..700&display=swap" rel="stylesheet">

    <title>Web Drive - ${ESC_DISPLAY_REL}</title>
  </head>
  <body style="font-family:'Roboto Mono',serif;font-weight:600;background-color:cadetblue;">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>

    <div class="container py-4">
      <h2 style="font-family:'Gruppo', serif;font-weight:700;font-size:90px;">Directory Listing</h2>
      <p class="text-dark mb-3">Current path: <strong>${ESC_DISPLAY_REL}</strong></p>
      <div id="list" class="list-group">
EOH

# Add a Parent Directory link when inside a subdirectory
if [ -n "$CLEAN_REL" ]; then
  PARENT_REL="${CLEAN_REL%/*}"
  [ "$PARENT_REL" = "$CLEAN_REL" ] && PARENT_REL=""
  PARENT_HREF="${SCRIPT_NAME}${PARENT_REL}"
  [ -z "$PARENT_HREF" ] && PARENT_HREF="/"
  ESC_PARENT_HREF="$(html_escape "$PARENT_HREF")"
  echo "<a href=\"${ESC_PARENT_HREF}\" class=\"list-group-item list-group-item-secondary\"><strong>.. (Parent Directory)</strong></a>"
fi

# List entries (excluding . and .. and cgi-bin), directories first, then alphabetically
{
  for entry in "$TARGET_DIR"/* "$TARGET_DIR"/.*; do
    [ -e "$entry" ] || continue
    name="${entry##*/}"
    [ "$name" = "." ] || [ "$name" = ".." ] && continue
    [ "$name" = "cgi-bin" ] && continue

    if [ -d "$entry" ]; then
      printf 'D\t%s\n' "$name"
    else
      printf 'F\t%s\n' "$name"
    fi
  done
} | sort -t "$(printf '\t')" -k1,1 -k2,2f | while IFS="$(printf '\t')" read -r kind name; do
  [ -n "$name" ] || continue
  ESC_NAME="$(html_escape "$name")"
  ENCODED_NAME="$(printf '%s' "$name" | url_encode_path)"

  if [ "$kind" = "D" ]; then
    # Folders route back through the CGI script to browse deeper
    NEXT_HREF="$(html_escape "${SCRIPT_NAME}${CLEAN_REL}/${ENCODED_NAME}")"
    echo "<a href=\"${NEXT_HREF}\" class=\"list-group-item list-group-item-dark\"><strong>📁 ${ESC_NAME}/</strong></a>"
  else
    # Files link to their served web path relative to BASE_DIR
    FILE_HREF="$(html_escape "${CLEAN_REL}/${ENCODED_NAME}")"
    echo "<a href=\"${FILE_HREF}\" class=\"list-group-item list-group-item-light\">📄 ${ESC_NAME}</a>"
  fi
done

cat << EOF
      </div>
    </div>
  </body>
</html>
EOF
