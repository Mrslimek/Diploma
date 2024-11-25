const burger = document.querySelector('.header__bottom-burger');
const burgerBlock = document.querySelector('.header__up')
const catalogFilter = document.querySelector('.catalog__filter')
const filter = document.querySelector('.catalog__filter-mob')


burger.addEventListener('click', () => {
    if (!filter.classList.contains('catalog__filter-active')) {
        burger.classList.toggle('header__bottom-burger-active')
        burgerBlock.classList.toggle('header__up-active')
        burger.classList.contains('header__bottom-burger-active') ? document.body.style.overflow = 'hidden' : document.body.style.overflow = 'auto'
    } else {
        filter.classList.remove('catalog__filter-active')
        burger.classList.remove('header__bottom-burger-active')
        document.body.style.overflow = 'auto';
    }
})

catalogFilter.addEventListener('click', () => {
    filter.classList.add('catalog__filter-active')
    burger.classList.add('header__bottom-burger-active')
    document.body.style.overflow = 'hidden';
})