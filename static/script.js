// Set localStorage for username
if (!localStorage.getItem('username'))
  localStorage.setItem('username', 'guest');

document.addEventListener('DOMContentLoaded', function() {

  // Get localStorage for username
  document.querySelector('#username').innerHTML = localStorage.getItem('username');

  // By default, submit button is disabled
  document.querySelector('#username-submit').disabled = true;

  // Enable button only uf there is text in the input field
  document.querySelector('#username-input').onkeyup = () => {
    if (document.querySelector('#username-input').value.length > 0)
      document.querySelector('#username-submit').disabled = false;
    else
      document.querySelector('#username-submit').disabled = true;
  };

  document.querySelector('#username-form').onsubmit = function() {
    // Create new item for list
    const p = document.createElement('p');
    p.innerHTML = "Your user name is: " + document.querySelector('#username-input').value;

    // Set innerHTML of username element
    let username = document.querySelector('#username-input').value;
    document.querySelector('#username').innerHTML = username;

    // Set localStorage for username
    localStorage.setItem('username', username);

    // Clear input field
    document.querySelector('#username-input').value = '';

    // Stop form from submitting to other page or website
    return false;
  };
});
