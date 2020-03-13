// 摄像头初始化
$(document).ready(function () {
    const video = $('#webcam')[0];
    const overlay = $('#overlay')[0];
    const overlayCC = overlay.getContext('2d');
    const ctrack = new clm.tracker();
    ctrack.init();

    //裁剪眼部区域（通过特征点）
    function getEyesRectangle(positions) {
        const minX = positions[23][0] - 5;
        const maxX = positions[28][0] + 5;
        const minY = positions[24][1] - 5;
        const maxY = positions[26][1] + 5;

        const width = maxX - minX;
        const height = maxY - minY;

        return [minX, minY, width, height];
    }

    // 面部追踪
    function trackingLoop() {
        // Check if a face is detected, and if so, track it.
        requestAnimationFrame(trackingLoop);
        let currentPosition = ctrack.getCurrentPosition();

        overlayCC.clearRect(0, 0, 400, 300);
        if (currentPosition) {
            // Draw facial mask on overlay canvas:
            ctrack.draw(overlay);

            // Get the eyes rectangle and draw it in red:
            const eyesRect = getEyesRectangle(currentPosition);
            overlayCC.strokeStyle = 'red';
            overlayCC.strokeRect(eyesRect[0], eyesRect[1], eyesRect[2], eyesRect[3]);

            // The video might internally have a different size, so we need these
            // factors to rescale the eyes rectangle before cropping:
            const resizeFactorX = video.videoWidth / video.width;
            const resizeFactorY = video.videoHeight / video.height;

            // Crop the eyes from the video and paste them in the eyes canvas:
            const eyesCanvas = $('#eyes')[0];
            const eyesCC = eyesCanvas.getContext('2d');

            eyesCC.drawImage(
                video,
                eyesRect[0] * resizeFactorX,
                eyesRect[1] * resizeFactorY,
                eyesRect[2] * resizeFactorX,
                eyesRect[3] * resizeFactorY,
                0,
                0,
                eyesCanvas.width,
                eyesCanvas.height,
            );
        }
    }

    // 启动摄像头，和面部追踪
    function onStreaming(stream) {
        video.srcObject = stream;
        ctrack.start(video);
        trackingLoop();
    }

    navigator.mediaDevices
        .getUserMedia({
            video: true,
        })
        .then(onStreaming);

    // 获得鼠标位置坐标:
    // Track mouse movement:
    const mouse = {
        x: 0,
        y: 0,

        handleMouseMove: function (event) {
            // Get the mouse position and normalize it to [-1, 1]
            mouse.x = event.clientX;
            mouse.y = event.clientY;
        },
    }

    document.onmousemove = mouse.handleMouseMove;


//canvas数据处理
    function convertCanvasToImage(canvas) {
        var imagesrc = canvas.toDataURL("image/png");
        return imagesrc;
    }

//绑定到空格
    $('body').keyup(function (event) {
        // On space key:

        if (event.keyCode == 32) {
            // alert('空格');
            let src = convertCanvasToImage($('#eyes')[0]);
            $.ajax({
                url: "/home",    //请求的url地址
                dataType: "JSON",   //返回格式为json
                async: true,//请求是否异步，默认为异步，这也是ajax重要特性
                data: {
                    "img": src,
                    "label": mouse.x + '_' + mouse.y
                },    //参数值
                type: "POST",   //请求方式
                beforeSend: function () {
                    //请求前的处理
                },
                success: function (req) {
                    //请求成功时处理
                    console.log(req)
                },
                complete: function () {
                    //请求完成的处理
                },
                error: function () {
                    //请求出错处理
                }
            });
            event.preventDefault();
            return false;
        }
    });


    function moveTarget() {
        let src = convertCanvasToImage($('#eyes')[0]);
        $.ajax({
            url: "/learn",    //请求的url地址
            dataType: "JSON",   //返回格式为json
            async: true,//请求是否异步，默认为异步，这也是ajax重要特性
            data: {
                "img": src,
                "label": mouse.x + '_' + mouse.y
            },    //参数值
            type: "POST",   //请求方式
            beforeSend: function () {
                //请求前的处理
            },
            success: function (req) {
                //请求成功时处理

                const x = req.x;
                const y = req.y;

                // Move target there:
                const $target = $('#target');
                $target.css('left', x + 'px');
                $target.css('top', y + 'px');
            },
            complete: function () {
                //请求完成的处理
            },
            error: function () {
                //请求出错处理
            }
        });
        // event.preventDefault();


        return false;
    }

    $('#train').click(function () {
        // moveTarget()
        setInterval(moveTarget, 100);
    });
})
;
