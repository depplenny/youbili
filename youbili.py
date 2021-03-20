import os
import re
import sys
import glob
from translate import Translator


with open('key.txt') as file: 
    lines = file.readlines()

for line in lines:
  if not '#' in line:
    key = line.strip();

translator = Translator(provider='microsoft', to_lang='zh', secret_access_key=key)


def vid_down(url):
  os.system("youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' --write-thumbnail --write-auto-sub {}".format(url))


def vtt2srt(file_src_path):

  file_tar_path = file_src_path.replace('.en.vtt','.en.srt')

  file_src = open(file_src_path)
  file_tar = open(file_tar_path, 'w')

  content_src = file_src.readlines()
  # if subtitle's duration is less than 1 second, ignore it
  timestamp = [ (i, x) for i, x in enumerate(content_src) if ' --> ' in x]
  timestamp_reduced = []
  for i, x in timestamp:
    start_time = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+',x)[0]
    end_time = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+',x)[1]
    start_time = re.split(':|\.',start_time)
    end_time = re.split(':|\.',end_time)

    if start_time[2]!=end_time[2]:
      timestamp_reduced.append((i,x))

  j=1 # caption number in srt
  for i, x in timestamp_reduced:
    if content_src[i+1].strip()!='':
      # write caption number
      file_tar.write(str(j) + '\n')
      j+=1
      # write timestamp
      file_tar.write(x.replace('.',','))
      # skip next line, it's redundant for youtube's auto generated subtitle
      if not ('align:start' in x):
        file_tar.write(content_src[i+1].strip() + ' ')
      # write next next line
      next_next_line = content_src[i+2].strip()
      if next_next_line!='':
        new_next_next_line = re.sub('<[0-9]+:[0-9]+:[0-9]+\.[0-9]+>|<c>|</c>','',next_next_line)
        if len(next_next_line.split())!=1:
          file_tar.write(new_next_next_line + '\n\n')
        else:
          file_tar.write(new_next_next_line + '优比利\n\n')
      else:
        file_tar.write('\n\n')

  file_src.close()
  file_tar.close()
  os.remove(file_src_path)



def en2cn(file_src_path):
  file_tar_path = file_src_path.replace('.en.srt','.中英字幕.srt')
  
  file_src = open(file_src_path)
  file_tar = open(file_tar_path, 'w')

  content_src = file_src.readlines()
  
  timestamp = [ i for i, x in enumerate(content_src) if ' --> ' in x]

  # true if it's youtube's auto generated subtitle

  is_auto = 'align:start' in content_src[timestamp[0]]
  j=1

  if is_auto:
    for i in range(0,len(timestamp),2):
      # write caption number
      file_tar.write(str(j) + '\n')
      # write timestamp
      # if there are odd number of timestamps, and this is the last timestamp
      if i == len(timestamp)-1:
        file_tar.write(content_src[timestamp[i]])
      else:
        start_time = re.findall('[0-9]+:[0-9]+:[0-9]+,[0-9]+', content_src[timestamp[i]])[0]
        end_time = re.findall('[0-9]+:[0-9]+:[0-9]+,[0-9]+', content_src[timestamp[i+1]])[1]
        timestamp_new = start_time + ' --> ' + end_time + '\n';
        file_tar.write(timestamp_new)
      # wirite line
      # if there are odd number of timestamps, and this is the last timestamp
      if i == len(timestamp)-1:
        line_en = content_src[timestamp[i]+1].strip()
        line_cn = translator.translate(line_en)
        print(j,line_cn)
        file_tar.write(line_cn + '\n')
        file_tar.write(line_en + '\n\n')
        j+=1
      else:
        line_en = content_src[timestamp[i]+1].strip() + ' ' + content_src[timestamp[i+1]+1].strip()
        line_cn = translator.translate(line_en)
        print(j,line_cn)
        file_tar.write(line_cn + '\n')
        file_tar.write(line_en + '\n\n')
        j+=1

  else:
    for i in range(len(timestamp)):
      # write caption(subtitle) number
      file_tar.write(str(j) + '\n')
      # write timestamp
      file_tar.write(content_src[timestamp[i]])
      # write line
      line_en = content_src[timestamp[i]+1].strip()
      line_cn = translator.translate(line_en)
      print(j,line_cn)
      file_tar.write(line_cn + '\n')
      file_tar.write(line_en + '\n\n')
      j+=1
      

  file_src.close()
  file_tar.close()
  os.remove(file_src_path)


def burn_in_sub(inp_vid, inp_sub):
  out_vid = inp_vid.replace('.mp4', '.sub.mp4')
  os.system("""ffmpeg -i '{}' -filter_complex "subtitles='{}':force_style='BackColour=&H80000000,BorderStyle=4,Fontsize=14'" '{}'""".format(inp_vid, inp_sub, out_vid))  
  os.remove(inp_vid)
  os.remove(inp_sub)


if __name__ == '__main__':
  os.makedirs('outputs/', exist_ok=True) 
  os.chdir('outputs/')



  if len(sys.argv) == 2:
    print('youtube-dl starts:')
    vid_down(str(sys.argv[1]))

    file_src_paths = glob.glob('*.en.vtt')
    for path in file_src_paths:
      print('vtt2srt starts:')
      vtt2srt(path)  

    file_src_paths = glob.glob('*.en.srt')
    for path in file_src_paths:
      print('en2cn starts:')
      en2cn(path)
  else:
    sub_paths = glob.glob('*.中英字幕.srt')
    for path in sub_paths:
      print('burn_in_sub starts:')

      sub_path = path
      img_path = path.replace('.中英字幕.srt','.jpg')
      img_path2 = path.replace('.中英字幕.srt','.webp')
      mp4_path = path.replace('.中英字幕.srt','.mp4')

      os.rename(sub_path, sub_path.replace("'", ''))
      if os.path.exists(img_path):
        os.rename(img_path, img_path.replace("'", ''))
      if os.path.exists(img_path2):
        os.rename(img_path2, img_path2.replace("'", ''))
      os.rename(mp4_path, mp4_path.replace("'", ''))
      
      burn_in_sub(mp4_path.replace("'", ''), sub_path.replace("'", ''))


  os.chdir('../')
    

