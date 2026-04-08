const stack = document.getElementById('imageStack');
const items = document.querySelectorAll('.stack-item');

stack.addEventListener('mouseenter', () => {
  items[0].style.transform = 'translate(40px, 15px) rotate(8deg)';
  items[1].style.transform = 'translate(0px, -15px) rotate(0deg)';
  items[2].style.transform = 'translate(-40px, 15px) rotate(-8deg)';
});

stack.addEventListener('mouseleave', () => {
  items.forEach(item => {
    item.style.transform = 'translate(0px, 0px) rotate(0deg)';
  });
});