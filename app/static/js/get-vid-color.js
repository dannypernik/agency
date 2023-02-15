// Adapted from https://reustle.org/reading-html5-video-data

// Main elements
// var body = document.getElementsByTagName('body')[0];
// var current_rgb = document.getElementById('current_rgb');
var my_video = document.getElementById('welcome-vid');
var my_canvas = document.getElementById('my-canvas');
var my_canvas_context = my_canvas.getContext('2d', { willReadFrequently: true });
var rgb_min = [20, 72, 92]
var rgb_brighten = [20, 20, 20]


var update_bg = function(){
  // If the video isn't playing, don't loop
  if(my_video.ended){
    document.getElementById('pause-play').classList.add('paused');
    return false; 
  }
  else if(my_video.paused) {
    return false;
  }

  // Draw the current frame of the video onto the hidden canvas
  my_canvas_context.drawImage(my_video, 0, 0, window.innerWidth/2, window.innerHeight/2);

  // Pull the image data from the canvas
  var frame_data = my_canvas_context.getImageData(0, 0, window.innerWidth/2, window.innerHeight/2).data;

  // Get the length of the data, divide that by 4 to get the number of pixels
  // then divide that by 100 so we check the color of every 100th pixel
  var frame_data_length = (frame_data.length / 4) / 100;

  // Loop through the raw image data, adding the rgb of every 4th pixel to rgb_sums
  var pixel_count = 0;
  var rgb_sums = [0, 0, 0];
  for(var i = 0; i < frame_data_length; i += 4){
    rgb_sums[0] += frame_data[i*4];
    rgb_sums[1] += frame_data[i*4+1];
    rgb_sums[2] += frame_data[i*4+2];
    pixel_count++;
  }

  // Get the inverse of the frame's average color, make adjustments to brightest and darkest values
  rgb_sums[0] = Math.max(Math.floor(255 + rgb_brighten[0] - rgb_sums[0]/pixel_count), rgb_min[0]);
  rgb_sums[1] = Math.max(Math.floor(255 + rgb_brighten[1] - rgb_sums[1]/pixel_count), rgb_min[1]);
  rgb_sums[2] = Math.max(Math.floor(255 + rgb_brighten[2] - rgb_sums[2]/pixel_count), rgb_min[2]);

  // Set the background color to the new color
  var new_rgb = 'rgb(' + rgb_sums.join(',') + ')';
  document.documentElement.style.setProperty('--dynamic-color', new_rgb );

  // Repeat every 1/10th of a second
  setTimeout(update_bg, 100);
}

var init = function(){
  // Update the size of the canvas to match the video
  my_canvas.width = window.innerWidth/2;
  my_canvas.height = window.innerHeight/2;
  // Start updating the bg color
  update_bg();
}

document.addEventListener("DOMContentLoaded", init);
my_video.addEventListener('play', init);