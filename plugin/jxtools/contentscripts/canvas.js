var canvas_inject = function () {

    (function () {
        const shift = {
            'r': 0,
            'g': 0,
            'b': 0,
            'a': [[canvas]],
            //'a': Math.floor(68 * 255)+1
        };
        const toBlobOrigion = HTMLCanvasElement.prototype.toBlob;
        const toDataURLOrigion = HTMLCanvasElement.prototype.toDataURL;
        const getImageDataOrigion = CanvasRenderingContext2D.prototype.getImageData;
        const toStringOrigion = Function.prototype.toString;
        //
        var noisify = function (canvas, context) {
            const width = canvas.width, height = canvas.height;
            const imageData = getImageDataOrigion.apply(context, [0, 0, width, height]);
            for (let i = 0; i < height; i++) {
                for (let j = 0; j < width; j++) {
                    const n = ((i * (width * 4)) + (j * 4));
                    if (imageData.data[n + 0] + shift.r > 0) {
                        imageData.data[n + 0] = imageData.data[n + 0] + shift.r;
                    }
                    if (imageData.data[n + 1] + shift.r > 0) {
                        imageData.data[n + 1] = imageData.data[n + 1] + shift.g;
                    }
                    if (imageData.data[n + 2] + shift.r > 0) {
                        imageData.data[n + 2] = imageData.data[n + 2] + shift.b;
                    }
                    if (imageData.data[n + 3] + shift.r > 0) {
                        imageData.data[n + 3] = imageData.data[n + 3] + shift.a;
                    }
                }
            }
            context.putImageData(imageData, 0, 0);
        };
        //
        Object.defineProperty(HTMLCanvasElement.prototype, "toBlob", {
            "value": function toBlob(a) {
                var context = this.getContext("2d");
                if (!context) {
                    context = this.getContext("experimental-webgl", { preserveDrawingBuffer: true });
                    if (context) {
                        return toBlobOrigion.apply(this, arguments);
                    }
                }
                else {
                    noisify(this);
                    return toBlobOrigion.apply(this, arguments);
                }
            }
        });
        //
        Object.defineProperty(HTMLCanvasElement.prototype, "toDataURL", {
            "value": function toDataURL() {
                var context = this.getContext("2d");
                if (!context) {
                    context = this.getContext("experimental-webgl", { preserveDrawingBuffer: true });
                    if (context) {
                        return toDataURLOrigion.apply(this, arguments);
                    }
                }
                else {
                    noisify(this, context);
                    return toDataURLOrigion.apply(this, arguments);
                }
            }
        });
        //
        //Object.defineProperty(CanvasRenderingContext2D.prototype, "getImageData", {
        //    "value": function getImageData(a, b, c, d) {
        //        noisify(this.canvas, this);
        //        return getImageDataOrigion.apply(this, arguments);
        //    }
        //});
        Object.defineProperty(Function.prototype, "toString", {
            "value": function toString() {
                if (this.name && this.name === "toBlob") {
                    return "function toBlob() { [native code] }";
                }
                else if (this.name && this.name === "toDataURL") {
                    return "function toDataURL() { [native code] }";
                }
                else if (this.name && this.name === "getImageData") {
                    return "function getImageData() { [native code] }";
                }
                return toStringOrigion.apply(this, arguments);
            }
        });
    })();
    //console.log('Rewrite Canvas test');
};

var canvas_script_1 = document.createElement('script');
canvas_script_1.textContent = "(" + canvas_inject + ")()";
canvas_script_1.onload = function () { this.parentNode.removeChild(this); };
document.documentElement.appendChild(canvas_script_1);

if (document.documentElement.dataset.cbscriptallow !== "true") {
    var canvas_script_2 = document.createElement('script');
    canvas_script_2.textContent = `{
    const iframes = window.top.document.querySelectorAll("iframe[sandbox]");
    for (var i = 0; i < iframes.length; i++) {
      if (iframes[i].contentWindow) {
        if (iframes[i].contentWindow.CanvasRenderingContext2D) {
          iframes[i].contentWindow.CanvasRenderingContext2D.prototype.getImageData = CanvasRenderingContext2D.prototype.getImageData;
        }
        if (iframes[i].contentWindow.HTMLCanvasElement) {
          iframes[i].contentWindow.HTMLCanvasElement.prototype.toBlob = HTMLCanvasElement.prototype.toBlob;
          iframes[i].contentWindow.HTMLCanvasElement.prototype.toDataURL = HTMLCanvasElement.prototype.toDataURL;
        }
      }
    }
  }`;
    //
    window.top.document.documentElement.appendChild(canvas_script_2);
}