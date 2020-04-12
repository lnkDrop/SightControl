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
        // 检查是否检测到脸部，如果有，请对其进行跟踪。
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
    const mouse = {
        x: 0,
        y: 0,

        handleMouseMove: function (event) {
            // client得到相对坐标(浏览器中)
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

        if (event.keyCode == 32) {
            let img = convertCanvasToImage($('#eyes')[0]);
            $.ajax({
                url: "/home",    //请求的url地址
                dataType: "JSON",   //返回格式为json
                async: true,//请求是否异步，默认为异步
                data: {
                    "img": img,  //传送图片的base64数据
                    "label": mouse.x + '_' + mouse.y //传送鼠标位置数据
                },
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

    //传输当前眼部数据到后台，并获取预测位置数据将其实施绘制到屏幕
    function moveTarget() {
        let img = convertCanvasToImage($('#eyes')[0]);
        $.ajax({
            url: "/learn",
            dataType: "JSON",
            async: true,
            data: {
                "img": img,
                "label": mouse.x + '_' + mouse.y
            },
            type: "POST",
            beforeSend: function () {
                //请求前的处理
            },
            success: function (req) {
                //请求成功时获取预测数据req(获取到的json数据)

                const x = req.x;
                const y = req.y;

                // 移动:
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

    //按下train开始预测
    $('#train').click(function () {
        setInterval(moveTarget, 100);
    });
})
;
