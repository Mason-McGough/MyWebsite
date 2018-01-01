var container;
var container_id = "WebGL-Canvas";
var scene, camera, renderer, seafloor;
var lights = [];
var spheres = [];
var mouse = {x: 0, y: 0};

var isMouseOverCanvas = false;
var PI = Math.PI;

var useCameraBob = true;
var n_spheres = 200;
var sphereSpeed = 0.1;
var sphereSpread = 400;
var sphereOscillationAmplitude = 0.002;
var sphereTimeScale = 0.001;
var seafloorBobAmplitude = 0.05;
var seafloorBobTimeScale = 0.0005;
var sphereYBounds = [-sphereSpread/2, sphereSpread/2];

init();
window.addEventListener( 'resize', onWindowResize, false );
container.addEventListener('mouseover', onEventMouseOverCanvas, false);
container.addEventListener('mouseout', onEventMouseLeftCanvas, false);
container.addEventListener('mousemove', onEventGetMouseCoordinates, false);

function init() {
    container = document.getElementById(container_id);
    
    camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 1, 2000);
    camera.position.set(0, 0, 200);
    scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x000310, 1, 2*sphereSpread);
    
    // add audio to scene
    // var listener = new THREE.AudioListener();
    // camera.add(listener);
    // var sound = new THREE.Audio(listener);
    // var audioLoader = new THREE.AudioLoader();
    // audioLoader.load(audio_url, function(buffer) {
    //     sound.setBuffer(buffer);
    //     sound.setLoop(true);
    //     sound.setVolume(0.5);
    //     sound.play();
    // });
    
    // load seafloor
    var loadManager = HorseLoader();
    var loader = new THREE.FBXLoader(loadManager);
    loader.load(seafloor_url, function(object) {
        seafloor = object;
        seafloor.scale.set(sphereSpread/8, sphereSpread/8, sphereSpread/8);
        seafloor.position.y = -sphereSpread/2-50;
        scene.add(seafloor);
    }, loadManager.onProgress, loadManager.onError);
    
    // assign background cube
    var path = cubemap_url;
    var format = ".jpg";
    var urls = [ 
                    path + 'posx' + format, path + 'negx' + format,
                    path + 'posy' + format, path + 'negy' + format,
                    path + 'posz' + format, path + 'negz' + format
                ];
    var textureCube = new THREE.CubeTextureLoader().load(urls);
    textureCube.format = THREE.RGBFormat;
    
    // ambient lighting
    var light = new THREE.AmbientLight(0x888888, 1.0);
    light.position.set(0, 1, 0);
    lights.push(light);
    scene.add(light);
    
    // renderer
    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0x000310);
    renderer.sortObjects = false;
    container.appendChild(renderer.domElement);
    
    // adding spheres
    var geometry = new THREE.SphereBufferGeometry( 10, 15, 15 );
    // iridescent shader material
    var shader = THREE.FresnelShader;
    var uniforms = THREE.UniformsUtils.clone(shader.uniforms);
    uniforms["tCube"].value = textureCube;
    var material = new THREE.ShaderMaterial({
        uniforms: uniforms,
        vertexShader: shader.vertexShader,
        fragmentShader: shader.fragmentShader
    });
    for (i = 0; i < n_spheres; i++) {
        //let material = new THREE.MeshPhongMaterial({color: 0x00ddf7});
        var object = new THREE.Mesh(geometry, material);
        
        randomlyDistribute(object);
        
        // assign random scale
        let randScale = Math.random();
        object.scale.set(randScale + 0.5, randScale + 0.5, randScale + 0.5);
        object.trueScale = randScale;
        
        // assign random oscillation amplitudes
        object.xOscillation = Math.random();
        object.zOscillation = 1 - object.xOscillation;
        scene.add( object );
        spheres.push(object);
    }
    
    animate();
}

function onWindowResize(){
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, window.innerHeight);
}

function randomlyDistribute(object) {
    var noSpawnRadius = 20;
    var singleDistribute = function(radius) {
        var randnum = Math.random() - 0.5;
        var sign = Math.sign(randnum);
        var dist = sign*(Math.abs(randnum)*(sphereSpread-radius) + radius);
        return dist;
    };
    object.position.x = singleDistribute(noSpawnRadius);
    object.position.y = singleDistribute(0);
    object.position.z = singleDistribute(noSpawnRadius);
}

function onEventMouseOverCanvas() {
    isMouseOverCanvas = true;
    console.log("ENTERED!");
}

function onEventMouseLeftCanvas() {
    isMouseOverCanvas = false;
}

function moveSpheres() {
    let timer = sphereTimeScale*Date.now();
    
    for (let i = 0; i < spheres.length; i++) {
        let sphere = spheres[i];
        
        // change position
        sphere.position.x += sphereOscillationAmplitude*sphere.xOscillation*Math.sin(timer + i*1.1)*Math.abs(sphere.position.y);
        sphere.position.z += sphereOscillationAmplitude*sphere.zOscillation*Math.sin(timer + i*1.1)*Math.abs(sphere.position.y);
        sphere.position.y += sphereSpeed;
        
        // change size according to position
        let newScale = sphere.trueScale*(1 - Math.abs(sphere.position.y)/sphereYBounds[1]);
        sphere.scale.set(newScale, newScale, newScale);
        
        // clamp position to sphereYBounds
        if (sphere.position.y < sphereYBounds[0]) {
            sphere.position.y = sphereYBounds[1];
        } else if (sphere.position.y > sphereYBounds[1]) {
            sphere.position.y = sphereYBounds[0];
        }
    }
}

function bobObject(object, bobTimeScale, bobAmplitude) {
    if (!object) { return; } // leave if object does not exist
    let timer = bobTimeScale*Date.now();
    object.position.y += bobAmplitude*Math.sin(timer);
}

function animate() {
    requestAnimationFrame(animate);
    
    moveSpheres();
    if (useCameraBob) {
        bobObject(seafloor, seafloorBobTimeScale, seafloorBobAmplitude);
    }
    
    renderer.render(scene, camera);
}