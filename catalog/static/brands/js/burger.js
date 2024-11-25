const burger = document.querySelector('.header__bottom-burger');
const burgerBlock = document.querySelector('.header__up')


burger.addEventListener('click', () => {
    burger.classList.toggle('header__bottom-burger-active')
    burgerBlock.classList.toggle('header__up-active')
    burger.classList.contains('header__bottom-burger-active') ? document.body.style.overflow = 'hidden' : document.body.style.overflow = 'auto'
})