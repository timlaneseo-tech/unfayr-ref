#!/bin/bash
# usage: run_one.sh <iter> <eval_id> <arm: skill|baseline>
ITER=$1; ID=$2; ARM=$3
REPO=/c/Users/TimLane/unfayr-ref
NAME=$(python -c "import json;e=[x for x in json.load(open('$REPO/evals/evals.json'))['evals'] if x['id']==$ID][0];print(e['name'])")
DIR="$TEMP/ref-bench/$ITER/$ID-$NAME-$ARM"
rm -rf "$DIR"; mkdir -p "$DIR/evals/files"
python - "$REPO" "$ID" "$DIR" <<'PY'
import json,shutil,sys,os
repo,i,d=sys.argv[1],int(sys.argv[2]),sys.argv[3]
e=[x for x in json.load(open(os.path.join(repo,'evals/evals.json')))['evals'] if x['id']==i][0]
for f in e['files']: shutil.copy(os.path.join(repo,f),os.path.join(d,f))
open(os.path.join(d,'.prompt.txt'),'w',encoding='utf-8').write(e['prompt'])
PY
if [ "$ARM" = skill ]; then mkdir -p "$DIR/.claude/skills"; cp -r "$REPO/ref" "$DIR/.claude/skills/ref"; rm -rf "$DIR/.claude/skills/ref/scripts/__pycache__"; fi
# snapshot of inputs for diffing
(cd "$DIR" && find . -type f -not -path './.claude/*' | sort | xargs md5sum > "$DIR/../$ID-$ARM.before.md5")
START=$(date +%s)
cd "$DIR"
timeout 600 claude -p "$(cat .prompt.txt)" --model sonnet --output-format text --setting-sources project,local --strict-mcp-config --dangerously-skip-permissions > "$DIR/../$ID-$ARM.transcript.txt" 2>&1
RC=$?
END=$(date +%s)
echo "rc=$RC seconds=$((END-START))" > "$DIR/../$ID-$ARM.meta.txt"
