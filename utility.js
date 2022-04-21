/**
 * 
 * @param {string} str 
 * @param {Object} obj
 */
 function createElement(str="div",obj= {}) {
    var elm = document.createElement(str);
    if (obj.addEventListeners) {
        for (let key in obj.addEventListeners) {
            elm.addEventListener(key,obj.addEventListeners[key]);
        }
    }
    if (obj.children) {
        for (let el of obj.children) {
            elm.appendChild(el);
        }
    }
    if (obj.style) {
        for (let key in obj.style) {
            elm.style[key] = obj.style[key];
        }
    }
    for (let key in obj) {
        if(key != "children" && 
        key != "addEventListeners" &&
        key != "setAttributes" &&
        key != "style") {
            elm[key] = obj[key];
        }
    }
    if (obj.setAttributes) {
        for (let key in obj.setAttributes) {
            elm.setAttribute(key,obj.setAttributes[key]);
        }
    }
    return elm;
}

HTMLElement.prototype.removeChildren = function(...elms) {
    for (let elm of elms) {
        this.removeChild(elm);
    }
}

HTMLElement.prototype.removeChildrenByClassName = function(classStr) {
    for (let elm of this.getElementsByClassName(classStr)) {
        this.removeChild(elm);
    }
}