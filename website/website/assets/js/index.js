(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){ 'use strict'; Object.defineProperty(exports, "__esModule", { value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

const Navigation = function () {
    function Navigation(element) {
        _classCallCheck(this, Navigation);

        this.root = element;

        this.bindEvents();
    }

    _createClass(Navigation, [{
        key: 'toggleNav',
        value: function toggleNav(e) {
            const icon = e.currentTarget;
            const mobileMenu = e.currentTarget.parentNode.parentNode;

            mobileMenu.classList.contains('active') ? this.closeNav(icon, mobileMenu) : this.openNav(icon, mobileMenu);
        }
    }, {
        key: 'openNav',
        value: function openNav(icon, mobileMenu) {
            mobileMenu.classList.add('active');
            icon.classList.add('active');
            document.querySelector('body').classList.add('menu-active');

            // mobileMenu.querySelector('.navlink:first-child').focus();
        }
    }, {
        key: 'closeNav',
        value: function closeNav(icon, mobileMenu) {
            mobileMenu.classList.remove('active');
            icon.classList.remove('active');
            document.querySelector('body').classList.remove('menu-active');
        }
    }, {
        key: 'bindEvents',
        value: function bindEvents() {
            this.root.addEventListener('click', this.toggleNav.bind(this));
        }
    }]);

    return Navigation;
}();

exports.default = Navigation;

},{}],2:[function(require,module,exports){
'use strict';

const _navigation = require('./components/navigation.js');

const _navigation2 = _interopRequireDefault(_navigation);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

const html = document.querySelector('html');
let isMobile = html.classList.contains('mobile');
let resizeId = undefined;
// let menu = new Navigation(document.querySelector('.navigation'));

if (html.querySelector('#year')) {
    const theDate = new Date();
    html.querySelector('#year').innerHTML = theDate.getFullYear();
}

if (html.querySelector('.burger-menu')) {
    new _navigation2.default(html.querySelector('.burger-menu'));
}

// Basic classes to add relevant classes to html tag
function classRemove(element, classes) {
    classes.forEach(function (class_) {
        element.classList.remove(class_);
    });
}

function viewport() {
    const width = document.body.clientWidth;
    let viewportClass = 'default';

    if (width >= 1344) {
        viewportClass = 'desktop-wide';
    }
    if (width < 1344) {
        viewportClass = 'desktop-compact';
    }
    if (width < 1024) {
        viewportClass = 'tablet-portrait';
    }
    if (width < 768) {
        viewportClass = 'mobile-landscape';
    }
    if (width < 481) {
        viewportClass = 'mobile-portrait';
    }

    classRemove(html, ['default', 'desktop-compact', 'tablet-portrait', 'mobile-landscape', 'mobile-portrait']);
    html.classList.add(viewportClass);

    return viewportClass;
}

function touchEnabled() {
    if ('ontouchstart' in window || 'onmsgesturechange' in window) {
        html.classList.add('touchenabled');
        return true;
    }
    html.classList.remove('touchenabled');
    return false;
}

function device() {
    let deviceClass;
    switch (viewport()) {
        case 'desktop-compact':
            deviceClass = 'desktop';
            if (touchEnabled()) {
                deviceClass = 'tablet';
            }
            break;
        case 'tablet-portrait':
            deviceClass = 'tablet';
            break;
        case 'mobile-landscape':
        case 'mobile-portrait':
            deviceClass = 'mobile';
            break;
    }
    classRemove(html, ['mobile', 'tablet', 'tablet-portrait', 'desktop']);
    html.classList.add(deviceClass);

    return deviceClass;
}

function doneResizing() {
    device();
    viewport();

    const wasMobile = isMobile;

    isMobile = html.classList.contains('mobile');

    if (wasMobile !== isMobile) {
        // isMobile ? menu.closeDesktopSearch() : menu.closeMobileMenu();
    }
}

// Basic functions to add relevant classes to html tag
viewport();
device();
touchEnabled();

window.addEventListener('resize', function () {
    clearTimeout(resizeId);
    resizeId = setTimeout(doneResizing, 500);
});

},{"./components/navigation.js":1}]},{},[2])

//# sourceMappingURL=index.js.map
