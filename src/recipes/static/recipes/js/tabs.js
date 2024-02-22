// showTab: Show the selected tab and hide the others
//    event: The event that triggered the function
//    tab_id: The id of the tab to show
const showTab = (event, tab_id) => {
  // Remove active class from all tabs
  const tabs = document.querySelectorAll('.tab');
  const tab_labels = document.querySelectorAll('.tab-label');

  tabs.forEach((tab) => {
    tab.classList.remove('active');
  });

  tab_labels.forEach((tab_label) => {
    tab_label.classList.remove('active');
  });

  // Add active class to the selected tab
  document.getElementById(tab_id).classList.add('active');
  event.target.classList.add('active');
};
