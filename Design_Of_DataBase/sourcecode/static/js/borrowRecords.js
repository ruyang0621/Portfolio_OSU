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
        postData('borrowRecords', { id: this.getAttribute('data-id'), action: 'delete_borrowRecords' }, 'DELETE')
        .then(data => {
            console.log(data)
            if(data['result'] == 'fail') {
                alert('Oops! Delete Falied');
            } else {
                alert('The Borrow Record has been deleted.');
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
const memId = document.getElementById('memId');
const copyId = document.getElementById('copyId');
const borrowDate = document.getElementById('borrowDate');
const dueDate = document.getElementById('dueDate');
const passDueYes = document.getElementById('passDueYes');
const passDueNo = document.getElementById('passDueNo');
const borrowId = document.getElementById('borrowId');

editModalClose1.addEventListener('click',closeEditModal);
editModalClose2.addEventListener('click',closeEditModal);

for(let i=0; i< editBtns.length; i++)
{
    editBtns[i].addEventListener('click', function(){
        let Id = this.getAttribute('data-id');
        let oldMemId = this.getAttribute('data-memid');
        let oldCopyId = this.getAttribute('data-copyid');
        let oldBDate = this.getAttribute('data-borrowDate');
        let oldDDate = this.getAttribute('data-dueDate');
        let oldPassDue = this.getAttribute('data-passDue');

        memId.value = oldMemId;
        copyId.value = oldCopyId;
        borrowDate.value = oldBDate;
        dueDate.value = oldDDate;
        if(oldPassDue == '0'){
            passDueNo.checked = true;
        }else{
            passDueYes.checked = true
        }
        //passDue.value = oldPassDue;
        borrowId.value = Id;
        editModal.classList.remove('fade');
        editModal.setAttribute('aria-hidden',false);
        editModal.style.display = 'block';
    })
}