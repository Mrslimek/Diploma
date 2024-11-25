const callback = document.querySelector('.header__up-button')
const modal = document.querySelector('.modal__wrap')
const callbackForm = document.querySelector('.callback')
const callbackBtn = document.querySelector('.callback > button');
const accessCallback = document.querySelector('.access__callback')
const accessCallbackButton = document.querySelector('.access__callback > button')
const cross = document.querySelectorAll('.cross')
const buyOneClick = document.querySelector('.buy__one-click')
const sliderButton = document.querySelectorAll('.slider__item-btn')
const buyOneClickImg = document.querySelector('.buy__one-click-list-item-img > img');
const buyOneClickTitle = document.querySelector('.buy__one-click-list-item-title');
const buyOneClickWeightList = document.querySelector('.buy__one-click-list-item-weight-list')
const buyOneClickPrice = document.querySelector('.buy__one-click-list-item-quantity > p')
const weightButton = document.querySelector('.buy__one-click-list-item-wrap-weight-title')
const youWeight = document.querySelector('.buy__one-click-list-item-wrap-weight')


modal.addEventListener('click', (e) => {
    if(e.target !== e.currentTarget) return
    else {
        e.target.children[0].classList.remove('modal__active')
        e.target.classList.remove('modal__active')
        document.body.style.overflow = 'auto'
    }
})

callback.addEventListener('click', () => {
    document.body.style.overflow = 'hidden'
    modal.classList.add('modal__active')
    callbackForm.classList.add('modal__active')
})

cross.forEach(item => {
    item.addEventListener('click', () => {
        item.parentElement.classList.remove('modal__active')
        item.parentElement.parentElement.classList.remove('modal__active')
        document.body.style.overflow = 'auto'
    })
})

sliderButton.forEach(item => {
    item.addEventListener('click', (e) => {
        document.body.style.overflow = 'hidden'
        modal.classList.add('modal__active')
        buyOneClick.classList.add('modal__active')
        buyOneClickWeightList.innerHTML = ''
        buyOneClickImg.setAttribute('src', e.currentTarget.parentElement.children[0].children[0].getAttribute('src'))
        buyOneClickTitle.textContent = e.currentTarget.parentElement.children[1].textContent.trim()
        for(let i of e.currentTarget.parentElement.children[2].children) {
            buyOneClickWeightList.innerHTML += `<li class="buy__one-click-list-item-weight-list-item">${i.textContent}</li>`
        }
        buyOneClickPrice.textContent = e.currentTarget.parentElement.children[3].children[0].textContent.trim()
        if(e.currentTarget.parentElement.children[2].children[0].children[0].textContent === 'шт' ) {
            weightButton.style.display = 'none'
        }else{
            weightButton.style.display = 'flex'
        }
    })
})

weightButton.addEventListener('click', () => {
    if(youWeight.style.display !== 'flex') {
        youWeight.style.display = 'flex'
    }else{
        youWeight.style.display = 'none'
    }
})

callbackBtn.addEventListener('click', () => {
    callbackForm.classList.remove('modal__active');
    accessCallback.classList.add('modal__active');
})

accessCallbackButton.addEventListener('click', () => {
    document.body.style.overflow = 'auto'
    modal.classList.remove('modal__active')
    accessCallback.classList.remove('modal__active')

})