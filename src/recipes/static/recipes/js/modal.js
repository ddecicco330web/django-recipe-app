// handleClose: closes the modal
const handleClose = () => {
  const modal = document.getElementsByClassName('add-recipe-modal')[0];
  const errors = document.getElementsByClassName('errorlist')[0];
  if (errors) {
    errors.remove();
  }
  modal.classList.remove('active');
};

// handleOpen: opens the modal
const handleOpen = () => {
  const modal = document.getElementsByClassName('add-recipe-modal')[0];
  modal.classList.add('active');
};

// Add event listeners to the modal
// Close the modal when user clicks outside the modal
document.addEventListener('click', (event) => {
  const modal = document.getElementsByClassName('add-recipe-modal')[0];
  const form = document.querySelector('form');

  // Check if the clicked element is outside the modal content
  if (event.target === modal && !form.contains(event.target)) {
    handleClose();
  }
});
