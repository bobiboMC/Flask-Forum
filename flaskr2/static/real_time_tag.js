
//when hover on tag,mark yellow all corresponding post's tag
$(function() {
	  $('.tags').hover(function() {
		let textHovered = this.textContent;
		let postTagsClass=document.getElementsByClassName('postTag');
		//alert(postTagsClass[0]);
		for (let i = 0; i < postTagsClass.length; i++) {
			//alert(postTagsClass[i].textContent);
			if(postTagsClass[i].textContent==textHovered){
				//alert(postTagsClass[i].textContent+','+textHovered);
				$(postTagsClass[i]).css('background-color', 'yellow');
			}
		} 
	  }, function() {
		// on mouseout, reset the background colour
		$('.postTag').css('background-color', '');
	  });
	});