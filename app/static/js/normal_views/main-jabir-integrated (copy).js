var player = (function () {
  //Namespace todo lo que esta aqui dentro es privado
  var play = document.getElementById("play"),
    fullscreen = document.getElementById("expand"),
    playlist = document.getElementById("playlist"),
    audioVolume = document.getElementById("audioVolume"),
    progress = document.getElementById("progress"),
    start = document.getElementById("start"),
    finish = document.getElementById("finish"),
    preload = document.getElementById("preload");

  var mediaPlayer, // global para que los listener sepan el estado a modificar
    currentTrack = "0", // que video se esta reproduciendo ahora.
    videos,
    videoNodes;

  play.addEventListener("click", (e) => {
    if (mediaPlayer.paused || mediaPlayer.ended) {
      e.target.setAttribute("class", "fas fa-pause");
      mediaPlayer.play();
    } else {
      mediaPlayer.pause();
      e.target.setAttribute("class", "fas fa-play");
    }
  });

  audioVolume.addEventListener("click", (e) => {
    if (mediaPlayer.muted) {
      e.target.setAttribute("class", "fas fa-volume-up");
      mediaPlayer.muted = !mediaPlayer.muted;
    } else {
      e.target.setAttribute("class", "fas fa-volume-off");
      mediaPlayer.muted = !mediaPlayer.muted;
    }
  });

  // fullscreen.addEventListener("click", () => {
  //     if      (mediaPlayer.requestFullscreen)        mediaPlayer.requestFullscreen();
  //     else if (mediaPlayer.webkitRequestFullscreen)  mediaPlayer.webkitRequestFullscreen();
  //     else if (mediaPlayer.mozRequestFullScreen)     mediaPlayer.mozRequestFullScreen();
  //     else if (mediaPlayer.msRequestFullscreen)      mediaPlayer.msRequestFullscreen();
  // });

  playlist.addEventListener("click", function (e) {
    var target = e.target;

    if (target.id != "playlist") {
      var id = target.closest(".video").id,
        el = target.closest(".video");

      preload.classList.add("lds-ring");
      higlight(id, currentTrack.toString());
      set(videos[id].source);
      window.injector.init(videos[id].current_video_json);
      mediaPlayer.addEventListener("canplay", videoIsReady);
    }
  });

  function set(video) {
    mediaPlayer.src = video;
  }
  /**
   * @param {*} e
   */
  function handleProgress(e) {
    var minutes = Math.floor(mediaPlayer.currentTime / 60),
      seconds = Math.floor(mediaPlayer.currentTime - minutes * 60),
      x = minutes < 10 ? "0" + minutes : minutes,
      y = seconds < 10 ? "0" + seconds : seconds;

    progress.style.width =
      Number((this.currentTime / this.duration) * 100) + "%";
    start.textContent = x + " : " + y;
  }

  /**
   *
   * @param {*} event
   */
  function togglePlay(event) {
    event.preventDefault();
    if (mediaPlayer.paused || mediaPlayer.ended) mediaPlayer.play();
    else mediaPlayer.pause();
  }

  /**
   * Create
   * @param {object} itemList
   * @returns un Nodo que representa el objeto siendo pasado
   * Rturns a Node representation of the object
   */
  function create(itemList) {
    var div = document.createElement("div"),
      imageContainer = document.createElement("div"),
      videoIformation = document.createElement("div"),
      img = document.createElement("img"),
      title = document.createElement("p"),
      duration = document.createElement("span");

    // div.onclick= reload(itemList.videoid);
    // div.onclick=  function (videoid){
    //     window.location.href = '/viewvideos?videoid='+videoid;
    // }

    div.setAttribute("onclick","reload("+itemList.videoid+")");

    div.setAttribute("id", itemList.videoid);
    // div.setAttribute("id", 11);
    
    div.setAttribute("class", "video");

    imageContainer.setAttribute("class", "video-imagen");
    img.setAttribute("src", itemList.thumbnailurl);
    imageContainer.appendChild(img);
    div.appendChild(imageContainer);

    videoIformation.setAttribute("class", "video-information");
    title.textContent = itemList.videoname;
    duration.textContent = itemList.duration;
    videoIformation.appendChild(duration);
    videoIformation.appendChild(title);


    div.appendChild(videoIformation);

    return div;
  }


  /**
   * Recibe un array de objetos y devuelve su representacion en un Nodos HTML
   * Returns an Node Collection
   * @param {playlist : arreglo de objetos}
   */
  function loadList(playlist) {
    var domPlayList = document.getElementById("playlist"),
      fragmentList = document.createDocumentFragment();

    for (let video of playlist) fragmentList.appendChild(create(video));

    domPlayList.appendChild(fragmentList);
    videoNodes = document.querySelectorAll(
      ".video"
    ); /* Hace disponible los nodos para manipular Una vex cargados */
  }

  function videoIsReady(event) {
    preload.classList.remove("lds-ring");
    mediaPlayer.play();
  }

  function higlight(current, lastTrack) {
    if (lastTrack) {
      videoNodes[lastTrack].classList.remove("playing");
      videoNodes[current].classList.add("playing");
    } else {
      videoNodes[current].classList.add("playing");
    }
    currentTrack = current;
  }

  var getVideos = function () {
    //carga los videos por primera vez
    // getJSON('source/videos.json', function(response){
    //     videos = response;
    //     loadList(videos)
    //     higlight(currentTrack);
    // });
    videos = window.myjson.side_playlist_info;
    console.log(videos)
    loadList(videos);
    higlight(currentTrack);
  };

  /************************************
   * xmlHtppRequest del json local
   *************************************/
  function getJSON(url, callback) {
    var request = new XMLHttpRequest();
    request.open("GET", url, true);

    request.onload = function () {
      if (request.status >= 200 && request.status < 400) {
        var data = JSON.parse(request.responseText);
        callback(data);
      }
    };

    request.onerror = function () {
      // There was a connection error of some sort
      console.error("there was an error");
    };

    request.send();
  }
  /**************************
   * Public
   *******************/
  return {
    init: function () {
      //configura el reproductor por primera vez, previene algun cambio en el css
      mediaPlayer = document.getElementById("video");
      mediaPlayer.controls = false;
      mediaPlayer.muted = true;
      getVideos();
      //cuando el video pueda reproducirse elimina el preloader css
      mediaPlayer.addEventListener("canplay", videoIsReady);
      mediaPlayer.addEventListener("timeupdate", handleProgress);
      mediaPlayer.addEventListener("click", togglePlay);
    },
  };
})();
