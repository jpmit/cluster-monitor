// This code passed through JSLint (www.jslint.com), and survived to
// tell the tale!
var MONITOR = {};

// 'Init-time branching'
MONITOR.req = false;
try {
    // Firefox, Opera 8.0+, Safari
    MONITOR.req = new window.XMLHttpRequest();
} catch (e1) {
    // Internet Explorer
    try {
        MONITOR.req = new window.ActiveXObject("Microsoft.XMLHTTP");
    } catch (e2) {
        window.alert("Your browser does not support AJAX!");
    }
}

// General method for implementing GET with AJAX
MONITOR.ajaxGet = function (url, callback) {
    var req = MONITOR.req;
    if (req) { // false if AJAX not enabled
        req.open("GET", url, true);
        req.onreadystatechange = function () {
            if (req.readyState === 4) {
                callback(req);
            }
        };
        req.send();
    }
};

MONITOR.refreshJobs = function () {
    var mon = MONITOR;
    mon.ajaxGet('/monitor', mon.writeJobinfo);
};

MONITOR.writeJobinfo = function (req) {
    var resp, alljobs, dirs, njobs, ndirs,
        jstr = "", dirstr = " ",  i, jlistEl,
        nrunEl, dirEl;

    resp = JSON.parse(req.responseText);
    alljobs = resp.alljobs;
    dirs = resp.dirs;

    // build string that contains detailed job info
    njobs = alljobs.length;
    for (i = 0; i !== njobs; i += 1) {
        jstr += '<div>' + alljobs[i] + '</div>\n';
    }

    // build string that contains working dir info
    ndirs = dirs.length;
    for (i = 0; i !== ndirs; i += 1) {
        dirstr += '<div>' + dirs[i] + '</div>\n';
    }

    // get DOM elements and set their html
    jlistEl = document.getElementById('joblist');
    nrunEl = document.getElementById('nrunning');
    dirEl = document.getElementById('dirs');

    jlistEl.innerHTML = jstr;
    nrunEl.innerHTML = njobs;
    dirEl.innerHTML = dirstr;
};
