ffmpeg \
  -framerate 15 \
  -pattern_type glob \
  -i "/Users/Hu/Downloads/output/*.JPG" \
  -s:v 2400x1800 \
  -c:v libx264 \
  -crf 17 \
  -pix_fmt yuv420p \
  timelapse.mp4