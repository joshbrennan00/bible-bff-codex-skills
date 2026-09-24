import importlib.util, pathlib, shutil, tempfile, unittest, wave
ROOT=pathlib.Path(__file__).resolve().parents[1]
S=ROOT/'.agents/skills/uploading-speaker-stories-into-vercel/scripts'
def load(name):
    spec=importlib.util.spec_from_file_location(name,S/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
match=load('match');audio=load('convert_audio')
class Tests(unittest.TestCase):
    def test_ambiguous_exact_is_held(self):
        m=match.Matcher([{'story_id':'demo-a','title':'The Journey'},{'story_id':'demo-b','title':'The Journey'}])
        self.assertIsNone(m.best('The Journey.mp3')[0])
    def test_alias_and_editor_prefix(self):
        m=match.Matcher([{'story_id':'demo-a','title':'The Call of Abraham','aliases':['Call of Abram']}],['editor','edit'])
        self.assertEqual(m.best('Editor Edit Call of Abram.mp3')[0],'demo-a')
    def test_longest_match(self):
        m=match.Matcher([{'story_id':'short','title':'The Journey'},{'story_id':'long','title':'The Journey to the Mountain'}])
        self.assertEqual(m.best('Finished The Journey to the Mountain REDO.mp3')[0],'long')
    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg unavailable')
    def test_conversion_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            src=pathlib.Path(d)/'source.wav';dst=pathlib.Path(d)/'result.mp3'
            with wave.open(str(src),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(44100);w.writeframes(b'\x00\x00'*44100)
            result=audio.convert(src,dst);self.assertLess(abs(result['output_seconds']-1),.25)
            with self.assertRaises(FileExistsError):audio.convert(src,dst)
if __name__=='__main__':unittest.main()
