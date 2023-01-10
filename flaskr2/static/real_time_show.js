//set color of like or dislike
function setColor(val){
			let opinion = document.getElementById(val);
			let cssObj = window.getComputedStyle(opinion, null);
			let bgColor = cssObj.getPropertyValue("background-color");
			let bgColorTwo="";
			let text="";
			if (val=='Like'){
				text=document.getElementById('textLike');
				let opinionTwo = document.getElementById('Dislike');
				let cssObjTwo = window.getComputedStyle(opinionTwo, null);
				bgColorTwo = cssObjTwo.getPropertyValue("background-color");
			}
			else{
				text=document.getElementById('textDislike');
				let opinionTwo = document.getElementById('Like');
				let cssObjTwo = window.getComputedStyle(opinionTwo, null);
				bgColorTwo = cssObjTwo.getPropertyValue("background-color");
			}
			if (bgColor=='rgb(128, 128, 128)'){
				if (val=='Like' && bgColorTwo=='rgb(128, 128, 128)'){
				bgColor="linear-gradient(144deg,#AF40FF, #5B42F3 50%,#00DDEB)";
				text.innerHTML = (parseInt(text.textContent)+1).toString();
				}
				else if (val=='Dislike' && bgColorTwo=='rgb(128, 128, 128)'){
				bgColor="linear-gradient(135deg, #f34079 40%, #fc894d)";
				text.innerHTML = (parseInt(text.textContent)+1).toString();
				}
			}
			else{
			bgColor="gray";
			text.innerHTML = (parseInt(text.textContent)-1).toString();
			}
			opinion.style.background=bgColor;
		}
		
//press button 'like' or 'dislike' and show it's color live
$(function() {
	  $('.opinion').on('click',function(e)
                   {
      //alert('why');
	  let val = $(this).val();
	  //alert(val);
      e.preventDefault();
      $.ajax({
        type:'POST',
        url:'/post/'+id,
        data:{
          opinion:val
        },
        success:function()
        {
			setColor(val);
        }
      })
    })
	});
	
//add comment and show it live
$(function() {
	   $('#toComment').on('click',function(e)
                   {
      let comment_text=document.getElementById('commentArea');
	  let comments=document.getElementById('containerComment');
      e.preventDefault();
      $.ajax({
        type:'POST',
        url:'/post/'+id,
        data:{
          comment:comment_text.value
        },
        success:function()
        {

			
			let new_comment=document.createElement('p');
			new_comment.innerHTML=comment_text.value;
			let author_date=document.createElement('p');
			let simple_br=document.createElement('br');
			let date = new Date();
			//alert(new_comment.innerHTML);
			
			const day = date.toLocaleString('default', { day: '2-digit' });
			const month = date.toLocaleString('default', { month: '2-digit' });
			const year = date.toLocaleString('default', { year: 'numeric' });
			const time=date.toLocaleTimeString()
			let strDate=year+ '-' + month + '-' + day+' '+time;
			
			author_date.innerHTML="by " +username +" on " +strDate; //need to solve
			
			let show_comment_div=document.createElement('div');
			let appended_comment=show_comment_div.appendChild(new_comment);
			appended_comment=appended_comment.appendChild(author_date);
			appended_comment=appended_comment.appendChild(simple_br);
			
			//let date = new Date().toLocaleDateString("iw-IL");
			//alert(date);
			//alert(comments.innerHTML);
			//alert(new_comment.innerHTML);
			show_comment_div.classList.add("show_comment");
			//show_comment_div.style.display='block'; //test
			author_date.classList.add("about");
			appended_comment=comments.appendChild(show_comment_div);
			comment_text.value='';//works
        }
      })
    });
	});	