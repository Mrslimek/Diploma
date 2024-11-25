const aboutImg = document.querySelector('.about__product-img > img')
const aboutListImg = document.querySelectorAll('.about__product-img-list-item > img')

aboutListImg.forEach(item => {
    item.addEventListener('click', () => {
        console.log();
        for(let i of item.parentNode.parentNode.children){
            if(i.classList.contains('about__product-img-list-item-active')){
                i.classList.remove('about__product-img-list-item-active')
            }
        }
        item.parentElement.classList.add('about__product-img-list-item-active')
        aboutImg.setAttribute('src', item.getAttribute('src'))
    })
})