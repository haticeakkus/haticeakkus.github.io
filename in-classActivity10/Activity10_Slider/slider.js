$(document).ready(function() {
	$("#slider").bxSlider({
		randomStart: true,
		moveSlides: 1,
		slideWidth: 250,
		auto: true,
		pause: 3000,
		pagerCustom: '#pager',
		pagerType: "short",
		captions:true
	});
});