// Injector PoC
// by Tyler Lafayette

class Injector {
    // debug controls whether or not debug messages will be seen.
    debug = false
    // cut will stop the draw function from requesting another animation frame when set to true.
    cut = false
    // CANVAS_ID is the id that the <canvas> element uses,
    // used to create a reference.
    CANVAS_ID = "market_overlay"
    // canvas contains a reference to the canvas element.
    canvas = null
    // context represents the context of the canvas.
    context = null
    // VIDEO_ID contains an id for the <video> element.
    VIDEO_ID = "video"
    // video contains a reference to the video element.
    video = null
    // solve contains the tracking solve points.
    solve = []
    // ICON_URL points to the icon URL.
    ICON_URL = "/static/tylerfolder/icon6.png"
    // ICON_SIZE defines how large the icon should be.
    ICON_SIZE = 100
    // drawIcon contains the icon image.
    drawIcon = null

    // init initializes the class by loading all initially required data.
    init = async _ => {
        // Create a reference to the canvas element.
        this.canvas = document.querySelector(`#${this.CANVAS_ID}`)
        if (!this.canvas) throw `could not select canvas #${this.CANVAS_ID}`

        this.context = this.canvas.getContext("2d")
        this.log("Selected canvas")

        // Create a reference to the video element.
        this.video = document.querySelector(`#${this.VIDEO_ID}`)
        if (!this.video) throw `could not select video #${this.VIDEO_ID}`

        // Create the event handlers for the video element.
        this.createVideoEventHandlers()
        this.log("Video selected and hooked")

        // Attempt to fetch the solve data.
        try {
            this.solve = await this.fetchSolve()
            this.log("Fetched solve")
        } catch (e) {
            throw e
        }

        this.canvasInit()
    }
    // fetchSolve fetches the solve json file.
    fetchSolve = async (filename = "/static/tylerfolder/solveTrack-fixed.json") => {
        // Create a fetch request to get the solve json file.
        const response = await fetch(`${filename}`)
        // Convert it to JSON and return it.
        return await response.json()
    }
    // log logs a message if this.debug is enabled.
    log = async message => !this.debug || console.log(`[Injector] ${message}`)
    // createVideoEventHandlers creates event handlers for all video events.
    createVideoEventHandlers = _ => {
        this.video.addEventListener("timeupdate", this.timeUpdate)
    }
    // timeUpdate is triggered by the video's time changing.
    // Temporarily deprecated in favor of requestAnimationFrame.
    timeUpdate = e => {}
    // canvasInit initializes the canvas system.
    canvasInit = _ => {
        // Create an Image for the icon.
        this.drawIcon = new Image()
        this.drawIcon.src = this.ICON_URL

        this.drawIcon.onload = this.draw
    }
    // draw renders the canvas with the tracked icons.
    draw = (timestamp = 0) => {
        const { currentTime } = this.video
        const currentTimeMs = Math.floor(currentTime * 1000)

        const [x, y] = this.returnTweenedFrameFromTimestamp(currentTimeMs)

        // Clear the canvas.
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height)

        // Draw the image.
        this.context.drawImage(
            this.drawIcon,
            x,
            y,
            this.ICON_SIZE,
            this.ICON_SIZE
        )

        // Request another animation frame (if this.cut has not been triggered).
        return this.cut || window.requestAnimationFrame(this.draw)
    }
    // returnTweenedFrameFromTimestamp returns the tweened x and y track coordinates from a timestamp.
    returnTweenedFrameFromTimestamp = timestamp => {

        //Sorted list of timestamp
        const tweenMap = this.solve.map(x => x.t).sort()
        
        this.log(`TweenMap : ${tweenMap}`)
        // Get the closest index that's lower than the timestamp.
        const lowerIndex = Object.keys(tweenMap).reduce((prev, curr) =>
            Math.abs(tweenMap[curr] - timestamp) <
                Math.abs(tweenMap[prev] - timestamp) &&
            tweenMap[curr] <= timestamp
                ? curr
                : prev
        )


        this.log(`lowerIndex : ${lowerIndex}`)

        // Get either the next value or the last element.
        const upperIndex = Math.min(lowerIndex + 1, tweenMap.length - 1)

        const lower = this.solve.filter(x => x.t == tweenMap[lowerIndex])[0]
        const upper = this.solve.filter(x => x.t == tweenMap[upperIndex])[0]

        if (lower.t == upper.t) return [lower.x, lower.y]

        // Find the progress to tween.
        const averageScale = upper.t - lower.t
        const progress = (timestamp - lower.t) / averageScale

        const x = lower.x + (upper.x - lower.x) * progress
        const y = lower.y + (upper.y - lower.y) * progress

        return [x, y]
    }
}

const injector = new Injector()
injector.debug = true

window.onload = injector.init