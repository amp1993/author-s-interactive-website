// JavaScript to populate the dropdown menu
document.addEventListener('DOMContentLoaded', function () {
  const hiddenBookData = document.getElementById('hidden-book-data');
  const dropdownMenu = document.querySelector('.dropdown-menu');

  // Retrieve book data from hidden elements
  const books = Array.from(hiddenBookData.children).map(bookElement => ({
      title: bookElement.dataset.title,
      link: bookElement.dataset.link
  }));

  // Populate the dropdown menu
  books.forEach(book => {
      const dropdownItem = document.createElement('a');
      dropdownItem.classList.add('dropdown-item');
      dropdownItem.href = book.link;
      dropdownItem.textContent = book.title;
      dropdownMenu.appendChild(dropdownItem);
  });
});
