(function(vjs) {

	// define some reasonable defaults
	var defaults = {
		image: '',
		destination: '#'
	};
	// plugin initializer
	var logobrand = function(options) {
		var settings = videojs.util.mergeOptions(defaults, options), player = this;
		var link = document.createElement("a");
			link.id = "vjs-logobrand-image-destination";
			link.href = settings.destination;
			link.target = "_blank";
		var image = document.createElement('img');
			image.id = 'vjs-logobrand-image';
			//image.style.height = settings.height;
			//image.style.width = settings.width;
			image.src = settings.image;
		link.appendChild(image);
		player.el().appendChild(link);
		
		this.loadImage = function(src){
			document.getElementById("vjs-logobrand-image").src=src;
		};
		this.setDestination = function(href){
			document.getElementById("vjs-logobrand-image-destination").href = href;
		};
		return this;
	};	
	// register the plugin with video.js
	vjs.plugin('logobrand', logobrand);

}(window.videojs));
video = document.querySelector('video'),

			// save a reference to the video.js player for that element
			player = videojs(video);

			// initialize the plugin with some custom options:
			player.logobrand({
				//height: "32px",
				//width: "32px",
				image: "http://www.videojs.com/img/logo.png",
				destination: "http://www.videojs.com/"
			});
	
	
