function HorseLoader() {
	var manager = new THREE.LoadingManager();
	manager.onProgress = function(xhr) {
		if (xhr.lengthComputable) {
			var percentComplete = xhr.loaded/xhr.total*100;
			console.log(Math.round(percentComplete, 2) + '% downloaded');
		}
	};
	manager.onError = function(xhr) {
		console.error(xhr);
	};
	return manager;
}

function onEventGetMouseCoordinates(event) {
	/*  Stores mouse coordinates in a global 'mouse' variable. Variable mouse must exist.
		The origin is roughly the center of the screen.
	
		Example usage:
		var mouse;
		document.addEventListener('mousemove', onEventGetMouseCoordinates, false);
	*/
	event.preventDefault();
	
	mouse.x = (event.clientX / window.innerWidth)*2 - 1;
	mouse.y = -(event.clientY / window.innerHeight)*2 + 1;
}

