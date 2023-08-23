function hover2(page, element) {
  // if page reference is nav access the nav folder 
    img_ID2.setAttribute('src', "/static/img/"+ page +"/nav" + element + ".png");
  }
  
  function unhover2(page) {
    // if the page reference is nav accesss the nav folder
    img_ID2.setAttribute('src', "/static/img/"+ page);
  }

  function sub(mood = "ignore", updat="ignore") {
    if (mood != "ignore")
    {document.getElementById('moodInput').value = mood;
    document.getElementById("moodsub").click();}
    else if (updat!= "ignore") 
    {document.getElementById('updateViewHid').value = updat;
      document.getElementById("updateView").click();}
    
  }

window.addEventListener('beforeunload', pageClosed);

function pageClosed()
{
  document.getElementById('updateViewHid').value = "close";
  document.getElementById("updateView").click();
  window.onbeforeunload = null;
}