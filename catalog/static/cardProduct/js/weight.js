const weight = document.querySelector('.about__product-your-weight > p')
const weightWrap = document.querySelector('.about__product-your-weight-wrap')

weight.addEventListener('click', () => {
    weightWrap.classList.toggle('about__product-your-weight-hide-active')
})