/*****
 * Carousel control
 */
var Carousel = function (elId, mode) {
  var wrapper = document.getElementById(elId);
  var innerEl = wrapper.getElementsByClassName('carousel-inner')[0];
  var leftButton = wrapper.getElementsByClassName('carousel-left')[0];
  var rightButton = wrapper.getElementsByClassName('carousel-right')[0];
  var items = wrapper.getElementsByClassName('item');

  this.carouselSize = items.length;
  this.itemWidth = null;
  this.itemOuterWidth = null;
  this.currentStep = 0;
  this.itemsAtOnce = 3;
  this.minItemWidth = 200;
  this.position = innerEl.style;
  this.mode = mode;

  this.init = function (mode) {
    this.itemsAtOnce = mode;
    this.calcWidth(wrapper, innerEl, items);
    cb_addEventListener(leftButton, 'click', this.goLeft.bind(this));
    cb_addEventListener(rightButton, 'click', this.goRight.bind(this));
    cb_addEventListener(window, 'resize', this.calcWidth.bind(this, wrapper, innerEl, items));
  };
  return this.init(mode);
};

Carousel.prototype = {
  goLeft: function(e) {
    e.preventDefault();
    if (this.currentStep) {
      --this.currentStep;
    } else {
      this.currentStep = this.carouselSize - this.itemsAtOnce;
    }
    this.makeStep(this.currentStep);
    return false;
  },
  goRight: function(e) {
    e.preventDefault();
    if (this.currentStep < (this.carouselSize - this.itemsAtOnce)) {
      ++this.currentStep;
    } else {
      this.currentStep = 0;
    }
    this.makeStep(this.currentStep);
    return false;
  },
  makeStep: function(step) {
    this.position.left = -(this.itemOuterWidth * step) + 'px';
  },
  calcWidth: function(wrapper, innerEl, items) {
    this.beResponsive();

    var itemStyle = window.getComputedStyle(items[0]);  
    var innerElStyle = innerEl.style;
    var carouselLength = this.carouselSize;
    var wrapWidth = wrapper.offsetWidth - parseInt(itemStyle.marginRight, 10) * (this.itemsAtOnce + 1);

    innerElStyle.display = 'none';
    this.itemWidth = wrapWidth / this.itemsAtOnce;
    this.itemOuterWidth = this.itemWidth + parseInt(itemStyle.marginRight, 10);
    for (i = 0; i < carouselLength; i++) {
        items[i].style.width = this.itemWidth + 'px';
    }
    innerElStyle.width = this.itemOuterWidth * this.carouselSize + 'px';
    innerElStyle.display = 'block';
  },

  beResponsive: function() {
    var winWidth = window.innerWidth;
    if (winWidth >= 650 && winWidth < 950 && this.itemsAtOnce >= 2) {
      this.itemsAtOnce = 2;
    }
    else if (winWidth < 650) {
      this.itemsAtOnce = 1;
    }
    else {
      this.itemsAtOnce = this.mode;
    }
  }
}
/**
* Cross-browser Event Listener
**/
function cb_addEventListener(obj, evt, fnc) {
  if (obj && obj.addEventListener) {
      obj.addEventListener(evt, fnc, false);
      return true;
  } else if (obj && obj.attachEvent) {
      return obj.attachEvent('on' + evt, fnc);
  }
  return false;
}

//Initializing carousel
if (document.getElementById('products')) {
  var productsCarousel = new Carousel('products', 3);
}
if (document.getElementById('products2')) {
  var productsCarousel = new Carousel('products2', 2);
}
if (document.getElementById('products3')) {
  var productsCarousel = new Carousel('products3', 1);
}
