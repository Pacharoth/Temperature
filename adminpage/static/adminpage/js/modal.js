// Get the modal
var   modal=[];
var span=[];
var btn=[];
var modal2=[];
modal[0]= document.getElementById("myModal");
// Get the button that opens the modal
btn[0] = document.getElementById("room");

// Get the <span> element that closes the modal
span[0] = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
modal[1] = document.getElementById("myMain");

// Get the button that opens the modal
// btn[1] = document.getElementById("myRoom");

// // Get the <span> element that closes the modal
// span[1] = document.getElementsByClassName("close2")[0];

// // When the user clicks the button, open the modal 

// btn[1].onclick = ()=> {
//   modal[1].style.display = "block";
// }

// // When the user clicks on <span> (x), close the modal
// span[1].onclick = ()=> {
//   modal[1].style.display = "none";
// }

// When the user clicks anywhere outside of the modal, close it
window.onclick = (event)=> {
  if (event.target == modal[1]) {
    modal[1].style.display = "none";
  }
}
btn[0].onclick = ()=> {
  modal[0].style.display = "block";
  
}

// When the user clicks on <span> (x), close the modal
span[0].onclick = ()=> {
  modal[0].style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = (event)=> {
  if (event.target == modal[0]) {
    modal[0].style.display = "none";
    
  }
}
// Get the modal