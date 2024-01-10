sun = 6
start = 19
end = 1

command = f"python image_interpolation.py --bpm 222 --step 0.51 --mult 3 --fps 222 --output ~/scratch/misc_images/sun_dance/sunkshift_sun{sun}_from{start}_to{end}.mp4 --images "

for i in range(start, end - 1, -1):
  command += f"~/scratch/misc_images/sun_dance/sun6k{i}.png "

print(command)
