const track = document.getElementById('track');
const btnPrev = document.getElementById('btn-prev');
const btnNext = document.getElementById('btn-next');

const getScrollAmount = () => {
  const card = document.querySelector('.showcase-card');
  const cardWidth = card.offsetWidth;
  const gap = parseInt(window.getComputedStyle(track).gap) || 32; 
  return cardWidth + gap;
};

btnNext.addEventListener('click', () => {
  track.scrollBy({ left: getScrollAmount(), behavior: 'smooth' });
});

btnPrev.addEventListener('click', () => {
  track.scrollBy({ left: -getScrollAmount(), behavior: 'smooth' });
});