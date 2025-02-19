document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

 // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';


    
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      emails.forEach(element => {
        let div = document.createElement('div');
        div.setAttribute("id","mal")
        div.innerHTML = `<span class = "col-3">${element['sender']}<span/>
                          <span class = "col-8">${element['subject']}<span/>
                          <span class = "col-10">${element['timestamp']}<span/>`;
        document.querySelector('.container').append(div);

      });
      }

  )};



function send_email(){
    // get the parameters to send mail from the form
      const res = document.querySelector('#compose-recipients').value;
      const sub = document.querySelector('#compose-subject').value;
      var bod = document.querySelector('#compose-body').values;
        fetch('/emails', {
          method: 'POST',
          body: JSON.stringify({
              recipients: res,
              subject: sub,
              body: bod
          })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
          console.log(result);
        });
        localStorage.clear();
        load_mailbox('sent');
        return false;
      }


