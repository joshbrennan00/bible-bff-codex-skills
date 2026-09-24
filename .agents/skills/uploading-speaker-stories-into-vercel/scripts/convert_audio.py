"""Convert an approved local recording without trimming or changing content."""
import argparse, json, math, subprocess
from pathlib import Path

def duration(path):
    result=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(path)],check=True,capture_output=True,text=True)
    value=float(json.loads(result.stdout)['format']['duration'])
    if not math.isfinite(value) or value<=0:raise ValueError('Invalid audio duration')
    return value

def convert(source,target):
    source=Path(source).resolve();target=Path(target).resolve()
    if not source.is_file():raise ValueError('Source must be a local file')
    if target.suffix.lower()!='.mp3':raise ValueError('Destination must end in .mp3')
    if target.exists():raise FileExistsError('Refusing to overwrite destination')
    before=duration(source);target.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(source),'-codec:a','libmp3lame','-b:a','192k',str(target)],check=True)
    after=duration(target)
    if abs(before-after)>.25:raise ValueError('Duration mismatch; hold output for review')
    return {'source_seconds':before,'output_seconds':after,'output':str(target),'codec':'libmp3lame','bitrate':'192k'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('target');a=p.parse_args()
    print(json.dumps(convert(a.source,a.target),indent=2))
