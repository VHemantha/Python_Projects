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

//i have get some inspiration to solve some part (not a copypaste to undestan) from youtube videos on this assignment

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}
function mark_read(id){
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}

function mark_archive(id){
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  })
  location.reload();
}

function mark_unarchive(id){
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  })
  location.reload();
}

function reply(emails){
  console.log(emails)
  let sender = emails.sender;
  let subject = emails.subject;
  let body = emails.body

  if ( (subject.startsWith('Re :')) === true ){
    subject = subject;
  }else{
    subject = 'Re :'+ subject;
  }

  body = 'On '+emails.timestamp +' '+ sender + '  wrote :' + body

  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email').style.display = 'none';

  //updating form fields

  document.querySelector('#compose-recipients').value = sender;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;

}

function view_mail(id){
  document.querySelector('#email').style.display = 'none';
  document.querySelector('#email').localStorage = '';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // ... do something else with email ....
  
  console.log(id)
  fetch(`/emails/${id}`)
  
  .then(response => response.json())
  .then(emails => {
  //create a new div
  console.log(emails)
  let btn
  if (emails["archived"] === true){
    btn = "Unarchived";
  }else {
    btn = "Archive";
  };
  document.querySelector('#email').innerHTML = `<div id="mal"><h6>Sender : ${emails.sender}</h6><br>
                                                <h5>Subject : ${emails.subject}</h5><br>
                                                <h6>time : ${emails.timestamp}</h6><br>
                                                <button class="btn btn-primary" type="button" id="reply" value="Reply">Reply</button>
                                                <button class="btn btn-primary" type="button" id="archive">${btn}</button></div>
                                                <div id="mal"><h6>${emails.body}</h6><br></div>`
                                      
                                                
  document.querySelector('#email')
  mark_read(id)
  document.querySelector('#email').style.display = 'block';
  
  if (emails["archived"] === true){
    document.querySelector('#archive').addEventListener('click', () => mark_unarchive(id));
  }else {
    document.querySelector('#archive').addEventListener('click', () => mark_archive(id));
  };
  document.querySelector('#reply').addEventListener('click', () => reply(emails));
  });
}

function load_mailbox(mailbox) {

 // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email').style.display = 'none';
    
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
                          <span class = "time">${element['timestamp']}<span/>`;
        if (element['read'] === true){
          div.style.background = 'grey'
        };
        
          div.addEventListener("click", function() {
           view_mail(element.id)
        });
        document.querySelector('#emails-view').append(div)
      });
      }

  )};



function send_email(){
    // get the parameters to send mail from the form
      const res = document.querySelector('#compose-recipients').value;
      const sub = document.querySelector('#compose-subject').value;
      const body = document.querySelector("#compose-body").value;
      console.log(body);
        fetch('/emails', {
          method: 'POST',
          body: JSON.stringify({
              recipients: res,
              subject: sub,
              body: body
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




