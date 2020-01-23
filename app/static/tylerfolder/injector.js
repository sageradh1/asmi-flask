// Injector PoC
// by Tyler Lafayette

// import VideoWrapper from "./VideoWrapper"
// import Tweener from "./utils/Tweener"
// import Converter from "./utils/Converter"
// import CanvasDraw from "./canvas/CanvasDraw"
// import Animator from "./canvas/Animator"
// import Modal from "./modals/Modal"

const EXAMPLE_VIDEOS = [
	[
		"solveTrack-fixed.json",
		"video.mp4",
		{
			name: "Dark Blue Shirt",
			image:
				"https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcQad2_iVMNhLWP0oCo0sG_rEUgb0aDKnL4-SXzpbl-NxsnsWPOKUqrE0fTNf3Mk2IOpDr5Rmz3G4xZNZnSYNrlUMc6kQCkXcF8JfNtAGBJiVp7HmncU0WzCqw&usqp=CAc",
			price: 29.99,
		},
	],
	[
		"track2.json",
		"video2.mp4",
		{
			name: "Men's Torrentshell Jacket",
			image:
				"https://eu.patagonia.com/dis/dw/image/v2/ABBM_PRD/on/demandware.static/-/Sites-patagonia-master/default/dwe6ea0083/images/hi-res/83802_BLK.jpg?sw=750&sh=750&sm=fit&sfrm=png",
			price: 140.0,
		},
	],
	[
		"track3.json",
		"video3.mp4",
		{
			name: "Honor Lace White Dress",
			image:
				"https://cdn-images.farfetch-contents.com/13/94/20/58/13942058_18699281_300.jpg",
			price: 380.0,
		},
	],
	[
		"track4.json",
		"video4.mp4",
		{
			name:
				"Nike Men's Hypercool Compression Long Sleeve Top 2.0 - Volt Green/Black",
			image:
				"https://s1.thcdn.com/productimg/0/960/960/05/10928605-1404897650-358544.jpg",
			price: 46.99,
		},
	],
	[
		"track5.json",
		"video5.mp4",
		{
			name: 'LTT "Stealth" Hoodie',
			image:
				"https://cdn.shopify.com/s/files/1/0058/4538/5314/products/LMG_Black_Hoodie-21_1800x1800.jpg?v=1571597691",
			price: 59.99,
		},
	],
]

const findGetParameter = parameterName => {
	var result = null,
		tmp = []
	location.search
		.substr(1)
		.split("&")
		.forEach(function(item) {
			tmp = item.split("=")
			if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1])
		})
	return result
}

// Container contains simple dependencies.
class Container {
	animator = null
}

class Injector {
	// debug controls whether or not debug messages will be seen.
	debug = false
	// cut will stop the draw function from requesting another animation frame when set to true.
	cut = false
	// STAGE_ID contains an id for the stage.
	STAGE_ID = "stage"
	// stage contains a reference to the stage element.
	stage = null
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
	// videoWrapper is an instance of the VideoWrapper class.
	videoWrapper = null
	// interactionOverlay contains a reference to the interaction overlay element.
	interactionOverlay = null
	// INTERACTION_ID contains an id for the interaction overlay element.
	INTERACTION_ID = "interaction_overlay"
	// solve contains the tracking solve points.
	solve = []
	// ICON_URL points to the icon URL.
	ICON_URL = "icon6.png"
	// ICON_SIZE defines how large the icon should be.
	ICON_SIZE = 70
	// drawIcon contains the icon image.
	drawIcon = null
	// tweener contains the Tweener class.
	tweener = null
	// canvasDrawer contains the CanvasDraw class.
	canvasDrawer = null
	// enableClicks blocks click handlers when true.
	enableClicks = false
	// hoveredActive reflects whether or not the icon is hovered over.
	hoveredActive = false
	// animator contains an Animator class.
	animator = null
	// container contains the Container.
	container = null

	getSelection = _ => {
		if (findGetParameter("video"))
			return EXAMPLE_VIDEOS[parseInt(findGetParameter("video"))]

		return EXAMPLE_VIDEOS[0]
	}

	// init initializes the class by loading all initially required data.
	init = async _ => {
		this.container = new Container()

		// Create a reference to the stage.
		this.stage = document.querySelector(`#${this.STAGE_ID}`)
		if (!this.stage) throw `could not select stage #${this.STAGE_ID}`
		// Register the mouse event handlers to the stage.
		this.registerClickHandlers()

		// Create a reference to the interaction overlay.
		this.interactionOverlay = document.querySelector(
			`#${this.INTERACTION_ID}`
		)
		if (!this.interactionOverlay)
			throw `could not select stage #${this.INTERACTION_ID}`

		// Create a reference to the canvas element.
		this.canvas = document.querySelector(`#${this.CANVAS_ID}`)
		if (!this.canvas) throw `could not select canvas #${this.CANVAS_ID}`

		this.context = this.canvas.getContext("2d")
		this.log("Selected canvas")

		// Create a reference to the video element.
		this.video = document.querySelector(`#${this.VIDEO_ID}`)
		if (!this.video) throw `could not select video #${this.VIDEO_ID}`

		this.videoWrapper = new VideoWrapper(this.video)

		this.log("Video selected and hooked")

		this.video.addEventListener("loadedmetadata", e => {
			// Change the canvas width and height to match the video.
			this.canvas.width = this.video.videoWidth
			this.canvas.height = this.video.videoHeight
		})

		this.video.src = this.getSelection()[1]

		document.querySelector("#selector").innerHTML = `${EXAMPLE_VIDEOS.map(
			(item, i) =>
				`<a style="padding:8px" href="?video=${i}"><button>Video ${i +
					1}</button></a>`
		).join("")}`

		// Attempt to fetch the solve data.
		try {
			this.solve = await this.fetchSolve(this.getSelection()[0])
			this.tweener = new Tweener(this.solve)
			this.log("Fetched solve")
		} catch (e) {
			throw e
		}

		this.canvasDrawer = new CanvasDraw(
			this.canvas,
			this.context,
			this.videoWrapper,
			this.tweener,
			this.container,
			this.ICON_URL,
			this.ICON_SIZE
		)

		this.canvasDrawer.start()
	}
	// registerClickHandlers registers the mouse events to the stage.
	registerClickHandlers = _ => {
		this.stage.addEventListener("mousemove", this.stageHover)
		this.stage.addEventListener("click", this.stageClick)
	}
	// overIcon returns whether or not a mouse event object is hovered over the icon.
	overIcon = e => {
		// Get the relative x and y coordinates of the click.
		const { x, y } = this.coordinate(e, this.stage)

		// Map the x and y values to the corresponding values on the video.
		const [relX, relY] = [
			(x / this.stage.offsetWidth) * this.canvas.width,
			(y / this.stage.offsetHeight) * this.canvas.height,
		]

		const { currentTime } = this.video
		const currentTimeMs = Math.floor(currentTime * 1000)

		// Find the current location of the target.
		const [targetX, targetY] = this.tweener.getTweenedKeyframeAtTime(
			currentTimeMs
		)

		// Get the bottom right bound of the icon.
		const [targetXMax, targetYMax] = [targetX, targetY].map(
			x => x + this.ICON_SIZE
		)

		if (targetXMax - relX < 0 || targetYMax - relY < 0) return false

		// Return if the click was outside the range of the icon.
		if (
			targetXMax - relX > this.ICON_SIZE ||
			targetYMax - relY > this.ICON_SIZE
		)
			return false

		return true
	}
	stageHover = e => {
		const prevState = this.hoveredActive

		if (!this.overIcon(e)) {
			this.hoveredActive = false

			this.stage.style.cursor = "default"

			if (!prevState) return

			if (!this.container.animator) return

			this.container.animator = new Animator(
				Date.now(),
				300,
				this.container.animator.getCurrentValue(Date.now()),
				true
			)

			return
		}

		this.hoveredActive = true
		if (!prevState) {
			this.container.animator = new Animator(Date.now(), 300, 0, false)
		}

		this.stage.style.cursor = "pointer"
	}
	stageClick = e => {
		if (!this.overIcon(e)) return

		// Actions from here will be executed if icon is clicked.

		// Prevent the click from interacting with another element.
		e.preventDefault()

		this.video.pause()

		const modal = new Modal(this.interactionOverlay, {
			data: this.getSelection()[2],
		})

		modal.build()
		modal.display()
	}
	// coordinate gets the relative client x and y positions for a mouse
	// event based on screen position.
	coordinate = (e, target) => {
		const { x, y } = target.getBoundingClientRect()

		return {
			x: e.clientX - x,
			y: e.clientY - y,
		}
	}
	// fetchSolve fetches the solve json file.
	fetchSolve = async (filename = "track4.json", convert = false) => {
		// Create a fetch request to get the solve json file.
		const response = await fetch(`${filename}`)

		// If enabled, convert from the raw model format.
		if (convert || filename.includes("raw"))
			return Converter.convert(await response.json())

		// Convert it to JSON and return it.
		return await response.json()
	}
	// log logs a message if this.debug is enabled.
	log = async message => !this.debug || console.log(`[Injector] ${message}`)
}

// VideoWrapper wraps around a <video> element and abstracts certain
// functions.

class VideoWrapper {
	// _video references the actual <video> element.
	_video = null

	constructor(_video) {
		this._video = _video
	}
	// getCurrentTimeMs returns the current video time in ms.
	getCurrentTimeMs = _ => Math.floor(this._video.currentTime * 1000)
}

// Converter converts from the model data to canvas-render-supported JSON.

class Converter {
	static convert = input => {
		const [first] = input

		return first["TimeStamp"].map(({ timeInMilliSec, x, y }) => ({
			t: timeInMilliSec,
			x,
			y,
		}))
	}
}

// Tweener interpolates between two keyframes in a motion tracked data set.

class Tweener {
	// data holds keyframe data.
	data = null

	constructor(data) {
		if (!data.length > 0) throw "data must be of length 1 or more"
		this.data = data
	}
	// getTweenedKeyframeAtTime returns an x and y coordinate by tweening
	// two keyframes based on the timestamp provided.
	getTweenedKeyframeAtTime = timestamp => {
		const tweenMap = this.data.map(x => x.t).sort()

		// Get the closest index that's lower than the timestamp.
		const lowerIndex = Object.keys(tweenMap).reduce((prev, curr) =>
			Math.abs(tweenMap[curr] - timestamp) <
				Math.abs(tweenMap[prev] - timestamp) &&
			tweenMap[curr] <= timestamp
				? curr
				: prev
		)

		// Get either the next value or the last element.
		const upperIndex = Math.min(lowerIndex + 1, tweenMap.length - 1)

		const lower = this.data.filter(x => x.t == tweenMap[lowerIndex])[0]
		const upper = this.data.filter(x => x.t == tweenMap[upperIndex])[0]

		if (lower.t == upper.t) return [lower.x, lower.y]

		// Find the progress to tween.
		const averageScale = upper.t - lower.t
		const progress = (timestamp - lower.t) / averageScale

		const x = lower.x + (upper.x - lower.x) * progress
		const y = lower.y + (upper.y - lower.y) * progress

		// Return the tweened x and y values.
		return [x, y]
	}
}

// Modal displays a modal over the video.

class Modal {
	// mountPoint is where the modal will mount.
	mountPoint = null
	// options contains options to be used in rendering the modal.
	options = {}
	// _element contains the element reference for the modal.
	_element = null
	// _container contains the inner container element of the modal.
	_container = null

	// SHIRT_IMAGE is a placeholder shirt image for the checkout concept.
	SHIRT_IMAGE =
		"https://eu.patagonia.com/dis/dw/image/v2/ABBM_PRD/on/demandware.static/-/Sites-patagonia-master/default/dwe6ea0083/images/hi-res/83802_BLK.jpg?sw=750&sh=750&sm=fit&sfrm=png"

	constructor(mountPoint, options = {}) {
		if (!mountPoint)
			throw "a valid element is required for the first argument"
		this.mountPoint = mountPoint
		this.options = options
		this._element = document.createElement("div")
		this._element.classList.add("marketing-modal")
	}
	// build builds the modal element.
	build = _ => {
		const dimmer = document.createElement("div")
		dimmer.classList.add("marketing-dimmer")
		this._element.append(dimmer)

		this._container = document.createElement("div")
		this._container.classList.add("marketing-container")
		this._element.append(this._container)

		const wrapper = document.createElement("div")
		wrapper.classList.add("marketing-wrapper")

		// General layout
		wrapper.innerHTML = `
			<div class="header">
				<span class="header-text">Checkout</span>
			</div>
			<span class="section-header">Items</span>
			<div class="product-description">
				<div class="product-image-wrapper">
					<div class="product-image" style="background-image: url('${this.options.data.image}')"></div>
				</div>
				<div class="item-details">
					<span class="title">${this.options.data.name}</span>
					<span class="price">$${this.options.data.price}</span>
				</div>
			</div>
			<span class="section-header">Payment</span>
			<div class="payment-details">
				<div class="visa-icon"></div>
				<span class="last-four">1049</span>
			</div>
			<div class="interaction-wrapper">
				<button class="marketing-payment" id="pay">Checkout</button>
			</div>
		`

		this._container.append(wrapper)
	}
	simulatePay = e => {
		const { target } = e
		target.disabled = true
		target.classList.add("processing")
		target.innerText = "Processing..."

		// Fake API delay
		setTimeout(() => {
			target.classList.remove("processing")
			target.innerText = "Thank you!"

			setTimeout(this.close, 1000)
		}, 1500)
	}
	// display displays the modal element.
	display = _ => {
		this.mountPoint.append(this._element)

		document
			.getElementById("pay")
			.addEventListener("click", this.simulatePay)
	}
	// close closes the modal.
	close = _ => {
		this._element.classList.add("going-away")
		setTimeout(() => this.mountPoint.removeChild(this._element), 300)
	}
}

// CanvasDraw draws icons over videos using an HTML5 canvas.

class CanvasDraw {
	// canvas references the canvas used to draw on.
	canvas = null
	// context has the context of the canvas.
	context = null
	// videoWrapper contains a reference to the VideoWrapper object to be used.
	videoWrapper = null
	// tweener contains a Tweener with a dataset loaded.
	tweener = null
	// aniamtorRequest is a function to get the parent Animator.
	container = null
	// iconURL contains a URL to the icon's image file.
	iconURL = "icon6.png"
	// cut is a killswitch for the animation drawing.
	cut = false
	// iconSize contains the size of the icon to draw.
	iconSize = 100

	// drawIcon is the Image class for rendering over the video.
	drawIcon = null

	constructor(
		canvas,
		context,
		videoWrapper,
		tweener,
		container,
		iconURL = "icon6.png",
		iconSize = 100
	) {
		this.canvas = canvas
		this.context = canvas.getContext("2d")
		this.videoWrapper = videoWrapper
		this.tweener = tweener
		this.container = container
		this.iconURL = iconURL
		this.iconSize = iconSize
	}
	// init initializes the drawer and creates all the dependencies.
	init = _ => {
		// Create an Image for the icon.
		this.drawIcon = new Image()
		this.drawIcon.src = this.iconURL

		this.drawIcon.onload = this.draw
	}
	// start starts the animation process.
	start = _ => this.init()
	// stop stops the drawing process.
	stop = _ => (this.cut = false)
	// draw renders the canvas with the tracked icons.
	draw = (timestamp = 0, lastVideoTime = 0) => {
		const currentTimeMs = this.videoWrapper.getCurrentTimeMs()

		// If the video is paused, skip the redraw.
		if (currentTimeMs == lastVideoTime)
			return this.scheduleRedraw(currentTimeMs)

		const [x, y] = this.tweener.getTweenedKeyframeAtTime(currentTimeMs)

		// Clear the canvas.
		this.context.clearRect(0, 0, this.canvas.width, this.canvas.height)

		const { animator } = this.container
		if (animator) {
			this.context.globalAlpha =
				0.7 + 0.3 * (1 - animator.getCurrentValue(Date.now()))
		}

		// Draw the image.
		this.context.drawImage(
			this.drawIcon,
			x,
			y,
			this.iconSize,
			this.iconSize
		)

		this.context.globalAlpha = 1

		// Request another animation frame (if this.cut has not been triggered).
		return this.scheduleRedraw(currentTimeMs)
	}
	// scheduleRedraw schedules the next redraw with requestAnimationFrame.
	scheduleRedraw = (currentTimeMs = 0) =>
		this.cut ||
		window.requestAnimationFrame(timestamp =>
			this.draw(timestamp, currentTimeMs)
		)
}

// import Injector from "./Injector"

const injector = new Injector()
injector.debug = true

window.onload = injector.init