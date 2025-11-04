// Grab DOM elements
const createButton = document.querySelector('.create-button');
const popupContainer = document.querySelector('.pop-up-container');
const cancelButton = document.querySelector('#cancel-button');

// Open the form when 'create' is clicked
createButton.addEventListener('click', () => {
  popupContainer.classList.add('active');
});

// Close the form when 'cancel' is clicked
cancelButton.addEventListener('click', () => {
  popupContainer.classList.remove('active');
});

// Optional: close popup when clicking outside the box
popupContainer.addEventListener('click', (e) => {
  // if clicked outside the box
  if (e.target === popupContainer) {
    popupContainer.classList.remove('active');
  }
});