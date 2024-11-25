const descriptionItem = document.querySelectorAll('.about__product-weight-list-item')


descriptionItem.forEach(item => {
    item.addEventListener('click', () => {
        descriptionItem.forEach(el => {
            if(el.classList.contains('about__product-weight-list-item-active')) {
                el.classList.remove('about__product-weight-list-item-active')
            }
            item.classList.add('about__product-weight-list-item-active')
        })    
    })
})