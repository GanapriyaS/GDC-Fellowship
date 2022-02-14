var c = document.getElementById("canvas");
var ctx = c.getContext("2d");
let drawLine = (ctx, startX, startY, endX, endY) => {
  ctx.beginPath();
  ctx.moveTo(startX, startY);
  ctx.lineTo(endX, endY);
  ctx.stroke();
};

ctx.beginPath();
ctx.arc(250, 50, 25, 0, 2 * Math.PI);
ctx.stroke();
ctx.beginPath();
drawLine(ctx, 250, 75, 250, 200);
drawLine(ctx, 250, 100, 200, 75);
drawLine(ctx, 250, 100, 300, 75);
drawLine(ctx, 250, 125, 200, 150);
drawLine(ctx, 250, 125, 300, 150);

// --------------------------------------------------------------------------------

var c1 = document.getElementById("canvas1");
var ctx1 = c1.getContext("2d");
let drawCircle = (
  centerX,
  centerY,
  radius,
  startingAngle,
  endingAngle,
  color
) => {
  ctx1.beginPath();
  ctx1.arc(centerX, centerY, radius, startingAngle, endingAngle);

  ctx1.fillStyle = color;
  ctx1.fill();
  ctx1.stroke();
};
ctx1.beginPath();
ctx1.arc(100, 80, 70, 0, 2 * Math.PI);
ctx1.stroke();

// eyes
function getRndInteger(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
let drawEyes = (radius, color) => {
  // left eye // right eye
  drawCircle(120, 50, radius, 0, 2 * Math.PI, color);
  drawCircle(80, 50, radius, 0, 2 * Math.PI, color);
};

// Nose
let drawNose = (type) => {
  if (type == "crooked") {
    drawLine(ctx1, 100, 70, 90, 90);
    drawLine(ctx1, 90, 90, 110, 90);
  } else {
    drawCircle(100, 90, 10, 0, Math.PI, "transparent");
    drawLine(ctx1, 100, 70, 110, 90);
    drawLine(ctx1, 100, 70, 90, 90);
  }
};

// Mouth
let drawMouth = (expression) => {
  if (expression == "happy") {
    drawCircle(100, 100, 20, 0, Math.PI, "transparent");
  } else if (expression == "suprise") {
    drawCircle(100, 120, 10, 0, 2 * Math.PI, "transparent");
  } else {
    drawLine(ctx1, 80, 110, 120, 110);
  }
};

let drawRandomFace = () => {
  let eyeRadius = getRndInteger(1, 20);
  let color = ["Green", "red", "orange", "violet"][getRndInteger(0, 3)];
  drawEyes(eyeRadius, color);
  drawNose("crooked");
  drawMouth("happy");
};

drawRandomFace();

// ------------------------------------------------------------------------

var c2 = document.getElementById("canvas2");
var ctx2 = c2.getContext("2d");

let callbackFun = (src, callback) => {
  var img = document.createElement("img");

  img.onload = () => callback(img);
  img.src = src;
};
callbackFun("./images/idle/1.png", (img) => {
  ctx2.drawImage(img, 0, 0, 300, 160);
});

// -----------------------------------------------------------------

var c3 = document.getElementById("canvas3");
var ctx3 = c3.getContext("2d");

let imageno = (frameno, animation) =>
  "./images/" + animation + "/" + frameno + ".png";

let loadImages = (callback) => {
  let images = [];
  let count = 8;
  [1, 2, 3, 4, 5, 6, 7, 8].forEach((item) => {
    callbackFun(imageno(item, "idle"), (img) => {
      images[item - 1] = img;
      count -= count;
      if (count === 0) {
        callback(images);
      }
    });
  });
};

let animate = (ctx3, images, callback) => {
  images.forEach((item, index) => {
    setTimeout(() => {
      ctx3.clearRect(0, 0, 500, 500);
      ctx3.drawImage(item, 0, 0, 300, 160);
    }, index * 100);
  });
  setTimeout(callback, images.length * 100);
};

loadImages((images) => {
  animate(ctx3, images, () => console.log("Done"));
});

// ------------------------------------------------------------------------

var c4 = document.getElementById("canvas4");
var ctx4 = c4.getContext("2d");

let frames = {
  idle: [1, 2, 3, 4, 5, 6, 7, 8],
  kick: [1, 2, 3, 4, 5, 6, 7],
  punch: [1, 2, 3, 4, 5, 6, 7],
  block: [1, 2, 3, 4, 5, 6, 7, 8, 9],
  forward: [1, 2, 3, 4, 5, 6],
  backward: [1, 2, 3, 4, 5, 6],
};

let loadImages1 = (callback) => {
  let images = {
    idle: [],
    kick: [],
    punch: [],
    backward: [],
    forward: [],
    block: [],
  };
  let count = 0;
  ["kick", "idle", "punch", "forward", "backward", "block"].forEach(
    (animation) => {
      let animFrame = frames[animation];
      count += animFrame.length;

      animFrame.forEach((item) => {
        callbackFun(imageno(item, animation), (img) => {
          images[animation][item - 1] = img;
          count -= count;
          if (count === 0) {
            callback(images);
          }
        });
      });
    }
  );
};

let animate1 = (ctx4, images, animation, callback) => {
  images[animation].forEach((item, index) => {
    setTimeout(() => {
      ctx4.clearRect(0, 0, 500, 500);
      ctx4.drawImage(item, 0, 0, 300, 160);
    }, index * 200);
  });
  setTimeout(callback, images[animation].length * 300);
};

loadImages1((images) => {
  console.log(images);
  let animate = "idle";
  let aux = () => animate1(ctx4, images, animate, aux);
  aux();
  document.getElementById("kick").onclick = () => {
    animate = "kick";
  };
  document.getElementById("push").onclick = () => {
    animate = "punch";
  };
});

// ------------------------------------------------------------------

var c5 = document.getElementById("canvas5");
var ctx5 = c5.getContext("2d");

loadImages1((images) => {
  let queue = [];

  let aux = () => {
    let select;
    if (queue.length === 0) {
      select = "idle";
    } else {
      select = queue.shift();
    }
    animate1(ctx5, images, select, aux);
  };
  aux();
  document.getElementById("kick1").onclick = () => {
    queue.push("kick");
  };
  document.getElementById("punch1").onclick = () => {
    queue.push("punch");
  };
  document.getElementById("forward").onclick = () => {
    queue.push("forward");
  };
  document.getElementById("backward").onclick = () => {
    queue.push("backward");
  };
  document.getElementById("block").onclick = () => {
    queue.push("block");
  };
  document.addEventListener("keydown", function (event) {
    const key = event.key;
    if (key === "ArrowRight") queue.push("kick");
    if (key === "ArrowLeft") queue.push("punch");
    if (key === "ArrowUp") queue.push("forward");
    if (key === "ArrowDown") queue.push("backward");
    if (key === "Enter") queue.push("block"); // "ArrowRight", "ArrowLeft", "ArrowUp", or "ArrowDown"
  });
});
