async function postData(url = '', data = {}, method='POST') {
    // Default options are marked with *
    const response = await fetch(url, {
        method: method, // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

const delBtns = document.getElementsByClassName("delBtn");
for(let i=0; i< delBtns.length; i++)
{
    delBtns[i].addEventListener('click', function(){
        postData('members', { id: this.getAttribute('data-id'), action: 'delete_member' }, 'DELETE')
        .then(data => {
            console.log(data)
            if(data['result'] == 'fail') {
                alert('Oops! The member has relation with copies, please delete the relation at BorrowRecords first.');
            } else {
                alert('The Member has been deleted.');
            }
            location.reload();
        });
    })
}

function closeEditModal()
{
    editModal.classList.add('fade');
    editModal.setAttribute('aria-hidden',true);
    editModal.style.display = 'none';
}

const editBtns = document.getElementsByClassName("editBtn");
const editModal = document.getElementById("editModal");
const editModalClose1 = document.getElementById('editModalClose1');
const editModalClose2 = document.getElementById('editModalClose2');
const fInput = document.getElementById('firstName');
const lInput = document.getElementById('lastName');
const homeInput = document.getElementById('homeAddress');
const emailInput = document.getElementById('email');
const phoneInput = document.getElementById('phone');
const IdInput = document.getElementById('memId');

editModalClose1.addEventListener('click',closeEditModal);
editModalClose2.addEventListener('click',closeEditModal);

for(let i=0; i< editBtns.length; i++)
{
    editBtns[i].addEventListener('click', function(){
        let Id = this.getAttribute('data-id');
        let firstName = this.getAttribute('data-firstName');
        let lastName = this.getAttribute('data-lastName');
        let homeAdd = this.getAttribute('data-home-add');
        let emailAdd = this.getAttribute('data-email');
        let phoneNum = this.getAttribute('data-phone');

        fInput.value = firstName;
        lInput.value = lastName;
        homeInput.value = homeAdd;
        emailInput.value = emailAdd;
        phoneInput.value = phoneNum;
        IdInput.value = Id;
        editModal.classList.remove('fade');
        editModal.setAttribute('aria-hidden',false);
        editModal.style.display = 'block';
    })
}