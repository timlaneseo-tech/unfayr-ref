import sys,json,glob,os
# usage: trace.py <projects_dir_glob> <out_file>
lines=[]
for f in sorted(glob.glob(os.path.join(sys.argv[1],'*.jsonl'))):
  for l in open(f,encoding='utf-8'):
    try:o=json.loads(l)
    except:continue
    c=(o.get('message') or {}).get('content')
    if isinstance(c,list):
      for b in c:
        if isinstance(b,dict) and b.get('type')=='tool_use':
          i=b['input']; s=i.get('skill') or i.get('command') or i.get('file_path') or i.get('pattern') or ''
          s=str(s).replace('\n',' ')[:200]
          lines.append(f"{b['name']}: {s}")
open(sys.argv[2],'w',encoding='utf-8').write(f"Tool calls ({len(lines)}), extracted from the headless session log:\n"+'\n'.join(lines)+'\n')
print(len(lines))
