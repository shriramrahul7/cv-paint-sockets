let video = document.querySelector("#VideoElement");
let canvas =  document.querySelector("#Canvas");
let ctx = canvas.getContext('2d');
let output = document.querySelector('#output')
let socket = io('http://localhost:5000');
//TODO: Flask URL  

navigator.mediaDevices.getUserMedia({video: true})
.then(function(stream) {
    video.srcObject = stream;
    requestAnimationFrame(loop);
})
.catch(function(err) {
    print(err.message);
});

const loop = () => {
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight 
    ctx.drawImage(video, 0, 0)

    if (socket){
        socket.emit('newFrame', canvas.toDataURL());

        socket.on('disp_img', (uri)=> {
            output.src = uri;
        })
    }

    requestAnimationFrame(loop)
}