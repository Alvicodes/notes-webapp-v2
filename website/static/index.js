function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

var popup;
function genPassword() {
  popup = window.open("/popup", "Popup", "width=800,height=600");
  popup.focus();
}

//! // Copy to clipboard
//  const clipboard = document.querySelector('.clipboard');
//  clipboard.addEventListener('click', () =>{
//      console.log("object copied to clipboard");
//  });


const usePassword = document.getElementById('use_password');
if (usePassword) {
  usePassword.addEventListener('click', () => {
    setPassword();
  });
}

//! Set Password
function setPassword() {
  const passwordField = window.opener.document.getElementById("password1");
  const passwordField2 = window.opener.document.getElementById("password2");
  const generatedPassword = document.getElementById('generatedPassword');

  if (window.opener && !window.opener.closed) {
    const passwordText = generatedPassword.textContent;
    passwordField.value = passwordText;
    passwordField2.value = passwordText;

  }else {
    console.error("Unable to set password: opener window is null or closed");
  }
  window.close();
};

const clrSelect = document.querySelectorAll(".note-clr");
const note_Background = document.querySelector(".note-pad");
const selectedColorInput = document.getElementById("selected-color");

// clrSelect.forEach((item) => {
//   item.addEventListener("click", () => {
//     var colorClass = item.classList[1];
//     var parentNote = item.closest('.note-pad');
//     if (parentNote && colorClass) {
//       if (parentNote.classList.contains(colorClass)) {
//         parentNote.classList.remove(colorClass);
//       }
//       else {
//         var existingColorClass = parentNote.classList.value.match(/clr-\w+/);// Regular expression to match "clr-" followed by any word characters
//         if (existingColorClass) {
//           parentNote.classList.remove(existingColorClass);
//         }
//         parentNote.classList.add(colorClass);
//       }
//     }
//     });
// });

// Function to update the color of a note
function updateNoteColor(noteId, color) {
  fetch('/update-note-color/' + noteId + '/' + color, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token
    },
    body: JSON.stringify({}) 
  })
  .then(response => {
    if (response.ok) {
      // Optionally, you can handle the success response here
      console.log('Note color updated successfully!');
    } else {
      // Optionally, you can handle the error response here
      console.error('Failed to update note color!');
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

// Event listener to update note color when a color is clicked
clrSelect.forEach((item) => {
  item.addEventListener("click", () => {
    var colorClass = item.classList[1];
    var parentNote = item.closest('.note-pad');
    const noteId = parentNote.dataset.unique;
    if (parentNote && colorClass) {
      if (parentNote.classList.contains(colorClass)) {
        parentNote.classList.remove(colorClass);
      } 
      else 
      {
        const existingColorClass = parentNote.classList.value.match(/clr-\w+/);
        if (existingColorClass) {
          parentNote.classList.remove(existingColorClass);
        }
        parentNote.classList.add(colorClass);
      }
      selectedColorInput.value = colorClass;
      
      // Extract note ID from the data attribute or any other way
      // var noteId = parentNote.getAttribute('data-note-id');
      
      // Call function to update note color
      updateNoteColor(noteId, colorClass);
    }
  });
});

