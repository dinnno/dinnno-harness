#!/usr/bin/env bash
# 시각화를 ~/Workspace/vis/<프로젝트>/<날짜>/ 에 보관용으로 저장한다.
# PNG(정지) + MP4(움직임) + 원본을 같은 이름으로 남기고 NOTES.md에 기록한다.
set -euo pipefail

VIS_ROOT="${VIS_ROOT:-$HOME/Workspace/vis}"
CHROME="${CHROME:-google-chrome}"
project=""; slug=""; caption=""; source_note=""; date_dir="$(date +%F)"
record=0; fps=24; win="1600,1000"; wait_ms=3000
srcs=()

usage() {
  cat <<'EOF'
사용법: vis-save.sh --slug SLUG [옵션] 소스...

  --slug S           파일 이름이 될 짧은 영문 kebab-case (필수)
  --caption "..."    이 그림이 보여주는 사실 한 줄. 제목이 아니라 읽어낸 내용.
  --source "..."     재현 정보: 스크립트 · config · seed · commit
  --project P        기본값은 cwd로 추정 (~/Workspace/<이것>/...)
  --date YYYY-MM-DD  기본값 오늘
  --record SEC       HTML 애니메이션을 SEC초 화면 녹화해 mp4로. 화면에 창이 잠깐 뜬다.
  --fps N            프레임 시퀀스·녹화 fps (기본 24)
  --window W,H       HTML 렌더 크기 (기본 1600,1000)
  --wait MS          HTML 캡처 전 렌더 대기 (기본 3000, plotly/three.js는 늘려라)

소스: .html .png .jpg .svg .pdf .mp4 .webm .mov .avi .gif,
      또는 번호순 PNG/JPG 프레임이 든 디렉토리
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --slug) slug="$2"; shift 2;;
    --caption) caption="$2"; shift 2;;
    --source) source_note="$2"; shift 2;;
    --project) project="$2"; shift 2;;
    --date) date_dir="$2"; shift 2;;
    --record) record="$2"; shift 2;;
    --fps) fps="$2"; shift 2;;
    --window) win="$2"; shift 2;;
    --wait) wait_ms="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    -*) echo "모르는 옵션: $1" >&2; usage >&2; exit 2;;
    *) srcs+=("$1"); shift;;
  esac
done

[[ -n $slug ]] || { echo "--slug 가 필요하다" >&2; exit 2; }
[[ ${#srcs[@]} -gt 0 ]] || { echo "소스를 하나 이상 달라" >&2; exit 2; }
[[ $slug =~ ^[a-z0-9][a-z0-9-]*$ ]] || { echo "--slug 는 소문자 kebab-case 여야 한다: $slug" >&2; exit 2; }

if [[ -z $project ]]; then
  case "$PWD/" in
    "$HOME/Workspace/"*) project="$(printf '%s' "${PWD#"$HOME"/Workspace/}" | cut -d/ -f1)";;
    *) project="$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null | xargs -r basename || true)"; project="${project:-$(basename "$PWD")}";;
  esac
fi

DEST="$VIS_ROOT/$project/$date_dir"
mkdir -p "$DEST"
NOTES="$DEST/NOTES.md"

# 같은 날 같은 slug가 이미 있으면 -2, -3 으로 (png/mp4/html이 같은 base를 공유한다)
base_taken() { local b="$1" f; for f in "$DEST"/*; do [[ -e $f ]] || continue; [[ "$(basename "$f")" == "$b."* ]] && return 0; done; return 1; }
base="$slug"; n=2
while base_taken "$base"; do base="$slug-$n"; n=$((n+1)); done

saved=(); origs=()
note() { echo "  $*"; }

# 같은 호출 안에서 두 소스가 같은 출력 경로를 노리면 뒤엣것이 앞엣것을 조용히 덮어쓴다.
# 주 산출물이면 멈추고, 파생물(영상 첫 프레임 png 같은 것)이면 건너뛴다.
claim() { # $1=경로 $2=primary|derived → 쓸 수 있으면 0
  local path="$1" kind="$2" s
  for s in "${saved[@]}"; do
    [[ $s == "$path" ]] || continue
    [[ $kind == derived ]] && return 1
    echo "출력 이름이 겹친다: $(basename "$path") — 소스마다 --slug 를 따로 주고 호출을 나눠라" >&2
    exit 1
  done
  return 0
}

file_uri() { python3 -c 'import sys,pathlib;print(pathlib.Path(sys.argv[1]).resolve().as_uri())' "$1"; }

html_to_png() { # $1=abs html  $2=out png
  "$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
    --window-size="$win" --virtual-time-budget="$wait_ms" \
    --screenshot="$2" "$(file_uri "$1")" >/dev/null 2>&1
  [[ -s $2 ]]
}

html_to_mp4() { # $1=abs html  $2=out mp4  $3=secs — 실제 화면에 창을 띄워 녹화한다
  local url out="$2" secs="$3" tmpd geom w h x y scr pid i before line wid rc=0
  url="$(file_uri "$1")"
  [[ -n ${DISPLAY:-} ]] || { note "DISPLAY 없음 — mp4 건너뜀"; return 1; }
  command -v xwininfo >/dev/null || { note "xwininfo 없음 — mp4 건너뜀"; return 1; }
  before="$(xwininfo -root -tree 2>/dev/null | grep -oE '0x[0-9a-f]+' | sort -u)"
  tmpd="$(mktemp -d)"
  "$CHROME" --user-data-dir="$tmpd" --no-first-run --no-default-browser-check \
    --new-window --app="$url" --window-size=1280,800 >/dev/null 2>&1 &
  pid=$!
  for i in $(seq 60); do
    line="$(xwininfo -root -tree 2>/dev/null | grep -F "$(basename "$1")" | while IFS= read -r l; do
              wid="$(printf '%s' "$l" | grep -oE '0x[0-9a-f]+' | head -1)"
              grep -qx "$wid" <<<"$before" || { printf '%s\n' "$l"; break; }
            done | head -1)"
    geom="$(printf '%s' "$line" | grep -oE '[0-9]+x[0-9]+\+[0-9]+\+[0-9]+' | head -1 || true)"
    [[ -n $geom ]] && break
    sleep 0.25
  done
  if [[ -z $geom ]]; then
    note "이번에 띄운 창을 찾지 못했다 — mp4 건너뜀"
    kill "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true; rm -rf "$tmpd" 2>/dev/null || true
    return 1
  fi
  w="${geom%%x*}"; geom="${geom#*x}"; h="${geom%%+*}"; geom="${geom#*+}"; x="${geom%%+*}"; y="${geom#*+}"
  w=$(( w / 2 * 2 )); h=$(( h / 2 * 2 ))   # libx264는 짝수 해상도를 요구한다
  scr="$DISPLAY"; [[ $scr == *.* ]] || scr="$scr.0"
  sleep 1   # 첫 페인트가 끝난 뒤부터 녹화
  ffmpeg -y -hide_banner -loglevel error -f x11grab -framerate "$fps" \
    -video_size "${w}x${h}" -i "$scr+$x,$y" -t "$secs" \
    -c:v libx264 -preset veryfast -pix_fmt yuv420p "$out" || rc=$?
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true      # 크롬이 프로필을 놓은 뒤에 지운다
  rm -rf "$tmpd" 2>/dev/null || true
  if (( rc != 0 )) || [[ ! -s $out ]]; then
    rm -f "$out"                       # 잘린 파일을 성공 산출물로 남기지 않는다
    note "녹화 실패 (ffmpeg rc=$rc)"; return 1
  fi
  return 0
}

first_frame() { # $1=영상 경로 → 대표 png. 이미 png가 있으면 건너뛴다.
  claim "$DEST/$base.png" derived || return 0
  ffmpeg -y -hide_banner -loglevel error -i "$1" -frames:v 1 "$DEST/$base.png" 2>/dev/null \
    && { saved+=("$DEST/$base.png"); note "첫 프레임 → $base.png"; }
  return 0
}

for src in "${srcs[@]}"; do
  [[ -e $src ]] || { echo "없는 경로: $src" >&2; exit 1; }
  abs="$(cd "$(dirname "$src")" && pwd)/$(basename "$src")"
  origs+=("$abs")
  low="$(printf '%s' "${src##*.}" | tr '[:upper:]' '[:lower:]')"

  if [[ -d $src ]]; then
    # 프레임 시퀀스 디렉토리 → mp4
    ext=""
    compgen -G "$src/*.png" >/dev/null && ext=png
    [[ -z $ext ]] && compgen -G "$src/*.jpg" >/dev/null && ext=jpg
    [[ -n $ext ]] || { echo "디렉토리에 png/jpg 프레임이 없다: $src" >&2; exit 1; }
    claim "$DEST/$base.mp4" primary
    ffmpeg -y -hide_banner -loglevel error -framerate "$fps" \
      -pattern_type glob -i "$src/*.$ext" \
      -c:v libx264 -preset veryfast -pix_fmt yuv420p "$DEST/$base.mp4"
    saved+=("$DEST/$base.mp4"); note "프레임 시퀀스 → $base.mp4"
    first_frame "$DEST/$base.mp4"
    continue
  fi

  case "$low" in
    html|htm)
      claim "$DEST/$base.html" primary
      cp "$abs" "$DEST/$base.html"; saved+=("$DEST/$base.html"); note "복사 → $base.html"
      if claim "$DEST/$base.png" primary && html_to_png "$abs" "$DEST/$base.png"; then
        saved+=("$DEST/$base.png"); note "HTML → $base.png"
      else
        note "PNG 렌더 실패 (--wait 를 늘려 보라)"
      fi
      if [[ $record != 0 ]]; then
        claim "$DEST/$base.mp4" primary
        html_to_mp4 "$abs" "$DEST/$base.mp4" "$record" && { saved+=("$DEST/$base.mp4"); note "화면 녹화 → $base.mp4"; }
      fi
      ;;
    png|jpg|jpeg|svg|pdf|webp)
      claim "$DEST/$base.$low" primary
      cp "$abs" "$DEST/$base.$low"; saved+=("$DEST/$base.$low"); note "복사 → $base.$low"
      ;;
    mp4)
      claim "$DEST/$base.mp4" primary
      cp "$abs" "$DEST/$base.mp4"; saved+=("$DEST/$base.mp4"); note "복사 → $base.mp4"
      first_frame "$abs"
      ;;
    gif|webm|mov|avi|mkv)
      claim "$DEST/$base.mp4" primary
      ffmpeg -y -hide_banner -loglevel error -i "$abs" \
        -c:v libx264 -preset veryfast -pix_fmt yuv420p \
        -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" "$DEST/$base.mp4"
      saved+=("$DEST/$base.mp4"); note "$low → $base.mp4"
      if [[ $low == gif ]] && claim "$DEST/$base.gif" primary; then
        cp "$abs" "$DEST/$base.gif"; saved+=("$DEST/$base.gif")
      fi
      first_frame "$abs"
      ;;
    *)
      echo "다룰 줄 모르는 형식: .$low ($src)" >&2; exit 1;;
  esac
done

join() { local sep="$1" out="" x; shift; for x in "$@"; do out+="${out:+$sep}$x"; done; printf '%s' "$out"; }
names=(); for f in "${saved[@]}"; do names+=("$(basename "$f")"); done

{
  [[ -s $NOTES ]] || printf '# %s — %s\n' "$project" "$date_dir"
  printf '\n## %s\n' "$base"
  [[ -n $caption ]] && printf '%s\n' "$caption"
  printf '\n%s\n' "- 파일: $(join ', ' "${names[@]}")"
  [[ -n $source_note ]] && printf '%s\n' "- 출처: $source_note"
  printf '%s\n' "- 원본: $(join ' · ' "${origs[@]}")"
} >> "$NOTES"

echo
echo "저장 위치: $DEST"
printf '  %s\n' "${names[@]}"
echo "  NOTES.md 갱신"
