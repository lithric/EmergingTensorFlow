(async function pragmaMain() {
//#region preset
function getUserMediaSupported() {
    return !!(navigator.mediaDevices?.getUserMedia);
}

const video = document.getElementById('webcam');
const liveView = document.getElementById('liveView');
const demosSection = document.getElementById('demos');
const enableWebcamButton = document.getElementById('webcamButton');
//#endregion

async function main() {
    getUserMediaSupported() ?
    enableWebcamButton.addEventListener('click',enableCam):
    console.warn('getUserMedia() is not supported by your browser');
    /** @param {MouseEvent} event*/
     async function enableCam(event) {
        model && (
        event.target.classList.add('removed'),
        video.srcObject = await navigator.mediaDevices.getUserMedia({video: true}),
        video.addEventListener('loadeddata',predictWebcam)
        )
    }
    var children = [];
    async function predictWebcam() {
        /**@type {Array<import("@tensorflow-models/coco-ssd").DetectedObject>} */
        const predictions = await model.detect(video);
        for (let child of children) {
            liveView.removeChild(child);
        }
        children.splice(0);

        for (let prediction of predictions) {
            if(prediction.score <= 0.50) break;
            const $p = createElement("p",{
                innerText:`${prediction.class} - with ${Math.round(prediction.score*100)} % confidence`,
                style: {
                    marginLeft: prediction.bbox[0]+'px',
                    marginTop: prediction.bbox[1]-10+'px',
                    width: prediction.bbox[2]-10+'px',
                    top: 0,
                    left: 0,
                }
            });
            const $highlighter = createElement("div",{
                className: 'highlighter',
                style: {
                    left: prediction.bbox[0]+'px',
                    top: prediction.bbox[1]+'px',
                    width: prediction.bbox[2]+'px',
                    height: prediction.bbox[3]+'px',
                }
            });
            liveView.appendChild($highlighter);
            liveView.appendChild($p);
            children.push($highlighter);
            children.push($p);
        }

        window.requestAnimationFrame(predictWebcam);
    }
}

// Store the resulting model in the global scope of our app.
var model;
model = await cocoSsd.load();
demosSection.classList.remove('invisible');

main();

})();