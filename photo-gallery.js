/* This addition is isolated from the original page's animation code. */
(function(){
  'use strict';
  var photos=Array.from(document.querySelectorAll('[data-live-photo]'));
  var modal=document.getElementById('live-viewer');
  if(!photos.length||!modal||typeof modal.showModal!=='function')return;
  var current=0,trigger=null,previousOverflow='';
  var image=document.getElementById('live-image');
  var caption=document.getElementById('live-caption');
  function show(index){
    current=(index+photos.length)%photos.length;
    image.src=photos[current].href;
    image.alt=photos[current].querySelector('img').alt;
    caption.textContent=(current+1)+' / '+photos.length+' — '+image.alt;
  }
  photos.forEach(function(link,index){
    link.addEventListener('click',function(e){
      if(e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;
      e.preventDefault();trigger=link;show(index);
      previousOverflow=document.body.style.overflow;
      document.body.style.overflow='hidden';
      modal.showModal();modal.querySelector('.live-close').focus();
    });
  });
  modal.querySelector('.live-close').addEventListener('click',function(){modal.close()});
  document.getElementById('live-prev').addEventListener('click',function(){show(current-1)});
  document.getElementById('live-next').addEventListener('click',function(){show(current+1)});
  modal.addEventListener('keydown',function(e){
    if(e.key==='ArrowLeft'){e.preventDefault();show(current+1)}
    if(e.key==='ArrowRight'){e.preventDefault();show(current-1)}
  });
  modal.addEventListener('click',function(e){
    var r=modal.getBoundingClientRect();
    if(e.target===modal&&(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom))modal.close();
  });
  modal.addEventListener('close',function(){document.body.style.overflow=previousOverflow;if(trigger)trigger.focus()});
})();
