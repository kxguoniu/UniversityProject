!function(e, t, a) {
    //event, document,
    function n() {
        c(".heart{width: 10px;height: 10px;position: fixed;background: #f00;transform: rotate(45deg);-webkit-transform: rotate(45deg);-moz-transform: rotate(45deg);}.heart:after,.heart:before{content: '';width: inherit;height: inherit;background: inherit;border-radius: 50%;-webkit-border-radius: 50%;-moz-border-radius: 50%;position: fixed;}.heart:after{top: -5px;}.heart:before{left: -5px;}"),
        c(".heart1{width: 0px;height: 0px;position: fixed;}"),
        o(),
        r()
    }
    function r() {
        for (var e = 0; e < d.length; e++) {
            if (d[e].alpha <= 0) {
                t.body.removeChild(d[e].el),
                t.body.removeChild(d[e].el1),
                d.splice(e, 1)
            } else {
                d[e].y--,
                d[e].y1--,
                d[e].scale += .004,
                d[e].alpha -= .013,
                d[e].el.style.cssText = "left:" + d[e].x + "px;top:" + d[e].y + "px;opacity:" + d[e].alpha + ";transform:scale(" + d[e].scale + "," + d[e].scale + ") rotate(45deg);background:" + d[e].color + ";z-index:99998",
                d[e].el1.style.cssText = "left:" + d[e].x1 + "px;top:" + d[e].y1 + "px;opacity:" + d[e].alpha + ";z-index:99999"
            }
        }
        requestAnimationFrame(r)
    }
    function o() {
        var t = "function" == typeof e.onclick && e.onclick;
        e.onclick = function(e) {
            t && t(),
            i(e)
        }
    }
    function i(e) {
        var a = t.createElement("div");
        var a1 = t.createElement("div");
        var g = "+" + sum + "s";
        var h = t.createTextNode(g);
        if (sum<10){
            var xx = 16
        } else if (sum<100){
            var xx = 21
        } else {
            var xx = 24
        }
        sum++,
        a.className = "heart",
        a1.className = "heart1",
        a1.appendChild(h),
        d.push({
            el1: a1,
            el: a,
            x: e.clientX - 5,
            y: e.clientY - 5,
            x1: e.clientX - xx,
            y1: e.clientY + 5,
            scale: 1.3,
            alpha: 1,
            color: s()
        }),
        t.body.appendChild(a),
        t.body.appendChild(a1)
    }
    function c(e) {
        var a = t.createElement("style");
        a.type = "text/css";
        try {
            a.appendChild(t.createTextNode(e))
        } catch(t) {
            a.styleSheet.cssText = e
        }
        t.getElementsByTagName("head")[0].appendChild(a)
    }
    function s() {
        return "rgb(" + ~~ (255 * Math.random()) + "," + ~~ (255 * Math.random()) + "," + ~~ (255 * Math.random()) + ")"
    }
    var d = [];
    var sum = 0;
    e.requestAnimationFrame = function() {
        return e.requestAnimationFrame || e.webkitRequestAnimationFrame || e.mozRequestAnimationFrame || e.oRequestAnimationFrame || e.msRequestAnimationFrame ||
        function(e) {
            setTimeout(e, 1e3 / 60)
        }
    } (),
    n()
} (window, document);