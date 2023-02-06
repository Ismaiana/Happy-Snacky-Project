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
        

const ingRed = document.querySelector('data-bs-toggle');

ingRed.getAttribute('data-bs-toggle'); 

ingRed.setAttribute('data-bs-toggle', 'tooltip');



