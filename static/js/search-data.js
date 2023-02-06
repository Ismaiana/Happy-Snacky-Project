fetch('/restrictions')
.then(response => response.json())
.then(data => {
    
    listIngred = document.querySelectorAll('#info-product')
    for (let i = 0; i < listIngred.length; i++){
        if (data.includes(listIngred[i].innerHTML)){
            listIngred[i].style.backgroundColor = 'red'
            
        }
        
    }

    

});
        
    

//  listIngred.addEventListener('mousemove', function(evt) {

//     if (listIngred[i] === 'red'){
//         text();
//     }
//     else {
//         hideText();
//     }

//  });

//     function text() {
//         document.querySelector('#tooltiptext').style.visibility = 'visible';
//     }

//     function hideText() {
//         document.querySelector('#tooltiptext').style.visibility = 'hidden';
//       }


